"""Validar estructura, pruebas, dependencias y copias sin instalar ni sincronizar."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from archivos_seguros import atomic_write, validate_outputs

IGNORED = {'.runtime', '__pycache__', '.git'}


def discover_skills(root):
    root = Path(root)
    skills = sorted(p.name for p in root.iterdir() if not p.name.startswith('.') and (p / 'SKILL.md').is_file())
    if not skills:
        raise ValueError(f'No se encontraron skills en {root}')
    return skills


def inventory(root, names):
    files = {}
    for name in names:
        directory = root / name
        if directory.is_symlink():
            raise ValueError(f'Skill enlazada: {directory}')
        for base, dirs, entries in os.walk(directory, followlinks=False):
            dirs[:] = sorted(d for d in dirs if d not in IGNORED)
            for entry in [*dirs, *entries]:
                path = Path(base) / entry
                if path.is_symlink() or (hasattr(path, 'is_junction') and path.is_junction()):
                    raise ValueError(f'Enlace no admitido en la comparación: {path}')
            for entry in entries:
                path = Path(base) / entry
                files[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return files


def compare_collections(root, other, names):
    root, other = Path(root).resolve(), Path(other).resolve()
    if root == other or root in other.parents or other in root.parents:
        raise ValueError('Las colecciones deben ser distintas y no estar anidadas')
    if not other.is_dir():
        raise ValueError(f'No existe la otra colección: {other}')
    left, right = inventory(root, names), inventory(other, names)
    differences = []
    for name in sorted(left.keys() | right.keys()):
        if left.get(name) != right.get(name):
            differences.append(dict(path=name, kind='extra' if name not in left else 'missing' if name not in right else 'changed'))
    return dict(files=len(left), differences=differences)


def process(command, timeout):
    try:
        with tempfile.TemporaryDirectory(prefix='skills-validation-') as temporary:
            run = subprocess.run([str(x) for x in command], capture_output=True, text=True,
                                 encoding='utf-8', errors='replace', timeout=timeout,
                                 env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1',
                                          PYTHONIOENCODING='utf-8', PIP_DISABLE_PIP_VERSION_CHECK='1',
                                          MPLCONFIGDIR=temporary, MPLBACKEND='Agg'))
        return dict(code=run.returncode, output=run.stdout + run.stderr)
    except (OSError, subprocess.TimeoutExpired) as error:
        return dict(code=None, output=str(error))


def run_tests(python, suite, timeout):
    # Los subprocesos PDF/DOCX deben reutilizar el entorno de las pruebas.
    # sys.prefix existe incluso sin venv: nunca se crea otra carpeta aquí.
    bootstrap = ('import os, runpy, sys; '
                 'os.environ["SKILLS_RUNTIME_DIR"] = sys.prefix; '
                 'sys.argv[0] = "unittest"; '
                 'runpy.run_module("unittest", run_name="__main__")')
    result = process([python, '-c', bootstrap, 'discover', '-s', Path(suite).resolve(), '-q'], timeout)
    counts = re.findall(r'Ran (\d+) tests? in ', result['output'])
    skipped = re.findall(r'skipped=(\d+)', result['output'])
    result.update(count=int(counts[-1]) if counts else 0, skipped=int(skipped[-1]) if skipped else 0)
    result['status'] = ('error' if result['code'] is None else
                        'failed' if result['code'] != 0 or not result['count'] else
                        'partial' if result['skipped'] else 'passed')
    return result


def validate_collection(root, other, validator, test_python, validator_python, timeout):
    root, other = Path(root).resolve(), Path(other).resolve()
    names = discover_skills(root)
    comparison = compare_collections(root, other, names)
    report = dict(scope='Skills presentes en la colección de origen; excluye runtime, cachés y skills ajenas.',
                  roots=[str(root), str(other)], skills=names, comparison=comparison,
                  validation=[], tests=[], dependencies=[], status='passed',
                  visual='No ejecutada: usar la regresión visual APA con su renderizador explícito.')
    for directory in (root, other):
        for name in names:
            skill = directory / name
            print(f'Validando {skill}', file=sys.stderr, flush=True)
            result = process([validator_python, validator, skill], timeout)
            report['validation'].append(dict(root=str(directory), skill=name, **result))
            suite = skill / 'tests'
            if suite.is_dir():
                report['tests'].append(dict(root=str(directory), skill=name, **run_tests(test_python, suite, timeout)))
        probe = directory / 'preprocesador-documentos/scripts/dependencias.py'
        dependencies = process([test_python, probe], timeout)
        report['dependencies'].append(dict(root=str(directory), profile='base', **dependencies))
        for profile, python, lock in (
            ('graphics', test_python, directory / 'explorador-temas-articulos/scripts/requirements-graficos-lock.txt'),
            ('images', test_python, directory / 'gestor-imagenes-academicas-libros/scripts/requirements-lock.txt'),
            ('maintenance', validator_python, directory / 'workflow-maestro-academico-editorial/scripts/requirements-mantenimiento.txt'),
        ):
            dependencies = process([python, probe, '--lock', lock], timeout)
            report['dependencies'].append(dict(root=str(directory), profile=profile, **dependencies))
    report['pip_check'] = process([test_python, '-m', 'pip', 'check'], timeout)
    failed = (comparison['differences'] or any(x['code'] != 0 for x in report['validation'])
              or any(x['status'] != 'passed' for x in report['tests']) or not report['tests']
              or any(x['code'] != 0 for x in report['dependencies']) or report['pip_check']['code'] != 0)
    report['status'] = 'failed' if failed else 'passed'
    report['test_count'] = sum(x['count'] for x in report['tests'])
    report['skipped'] = sum(x['skipped'] for x in report['tests'])
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--compare', type=Path, required=True)
    parser.add_argument('--validator', type=Path, required=True, help='quick_validate.py de skill-creator, de confianza')
    parser.add_argument('--test-python', default=sys.executable)
    parser.add_argument('--validator-python', default=sys.executable, help='Python con PyYAML para el validador oficial')
    parser.add_argument('--timeout', type=int, default=180, help='Segundos por subproceso')
    parser.add_argument('--out', type=Path, help='JSON opcional, fuera de ambas colecciones')
    args = parser.parse_args()
    try:
        if not args.validator.is_file() or args.timeout <= 0:
            raise ValueError('Validador inexistente o timeout no positivo')
        if args.out:
            if any(args.out.resolve().is_relative_to(p.resolve()) for p in (args.root, args.compare)):
                raise ValueError('Guardar el informe fuera de ambas colecciones')
            validate_outputs([args.validator], [args.out])
        report = validate_collection(args.root, args.compare, args.validator.resolve(),
                                     args.test_python, args.validator_python, args.timeout)
        serialized = json.dumps(report, ensure_ascii=False, indent=2)
        if args.out:
            atomic_write(args.out, serialized)
            print(json.dumps(dict(status=report['status'], tests=report['test_count'],
                                  skipped=report['skipped'], report=str(args.out)), ensure_ascii=False))
        else:
            print(serialized)
        return 0 if report['status'] == 'passed' else 1
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    raise SystemExit(main())
