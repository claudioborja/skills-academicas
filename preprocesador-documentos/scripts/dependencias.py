"""Comprobar versiones fijadas e importaciones sin instalar ni modificar paquetes."""
import argparse
import importlib
from importlib import metadata
import json
from pathlib import Path
import re
import sys


def check_dependencies(lock=None):
    lock = Path(lock) if lock is not None else Path(__file__).with_name('requirements-lock.txt')
    requirements = []
    names = set()
    for line in lock.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        match = re.fullmatch(r'([A-Za-z0-9_.-]+)==([A-Za-z0-9_.+!-]+)', line)
        if not match or match[1].lower().replace('_', '-') in names:
            raise ValueError(f'El lock requiere entradas únicas con versión exacta: {line}')
        names.add(match[1].lower().replace('_', '-'))
        requirements.append(match.groups())
    if not requirements:
        raise ValueError('El lock está vacío')
    result = {'python': sys.version, 'ok': sys.version_info >= (3, 10), 'packages': []}
    modules = {'python-docx': 'docx', 'typing-extensions': 'typing_extensions',
               'python-dateutil': 'dateutil', 'fonttools': 'fontTools', 'pillow': 'PIL', 'pyyaml': 'yaml'}
    for name, expected in requirements:
        package = dict(name=name, expected=expected, installed=None, status='missing')
        try:
            package['installed'] = metadata.version(name)
        except metadata.PackageNotFoundError:
            pass
        else:
            package['status'] = 'version_mismatch' if package['installed'] != expected else 'ok'
            if package['status'] == 'ok':
                try:
                    importlib.import_module(modules.get(name.lower().replace('_', '-'), name.replace('-', '_')))
                except Exception as error:
                    package.update(status='import_error', detail=str(error))
        result['packages'].append(package)
        result['ok'] &= package['status'] == 'ok'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lock', type=Path)
    args = parser.parse_args()
    try:
        result = check_dependencies(args.lock)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
