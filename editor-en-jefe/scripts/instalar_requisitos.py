#!/usr/bin/env python3
"""Preparar dependencias en el Python actual; entorno virtual opcional en los tres sistemas."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'preprocesador-documentos/scripts'))
from runtime_portable import configure_console, runtime_python, utf8_environment


def installation_needed(reports):
    """Rechazar incompatibilidades antes de descargar o reemplazar paquetes."""
    packages = [package for report in reports for package in report['packages']]
    invalid = [p for p in packages if p['status'] not in ('ok', 'missing')]
    if invalid:
        names = ', '.join(p['name'] + ': ' + p['status'] for p in invalid)
        raise RuntimeError('Entorno incompatible o importación dañada (' + names + '). '
                           'Selecciona una carpeta nueva con --entorno; no se reemplazan paquetes.')
    return any(p['status'] == 'missing' for p in packages)


def probe(python, locks):
    reports = []
    for lock in locks:
        result = subprocess.run(
            [str(python), str(ROOT / 'preprocesador-documentos/scripts/dependencias.py'), '--lock', str(lock)],
            capture_output=True, text=True, encoding='utf-8', env=utf8_environment(), timeout=60)
        if result.returncode not in (0, 1):
            raise RuntimeError(result.stderr or 'No se pudo comprobar el entorno.')
        try:
            report = json.loads(result.stdout)
        except ValueError as error:
            raise RuntimeError('Diagnóstico inválido: ' + result.stderr) from error
        if not report.get('packages'):
            raise RuntimeError('Diagnóstico sin paquetes.')
        reports.append(report)
    return reports


def main():
    configure_console()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--entorno', type=Path, help='Crear o usar un entorno virtual; por defecto usa el Python actual')
    parser.add_argument('--graficos', action='store_true', help='Compatibilidad: los gráficos ya están incluidos por defecto')
    parser.add_argument('--comprobar', action='store_true', help='Solo diagnóstico; no crea ni instala nada')
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        parser.error('El conjunto completo de dependencias requiere Python >=3.12.')
    directory = args.entorno.expanduser().resolve() if args.entorno else None
    python = runtime_python(directory) if directory else Path(sys.executable)
    # La copia empaquetada permite instalar las skills sin copiar la raíz del repositorio.
    packaged = Path(__file__).with_name('requirements.txt')
    requirements = ROOT / 'requirements.txt'
    if not requirements.is_file():
        requirements = packaged
    locks = [requirements]
    try:
        for lock in locks:
            if not lock.is_file():
                raise RuntimeError(f'Falta {lock}. Instala juntas las skills de la colección.')
        print(f'Python: {python}', flush=True)
        if directory is not None and not directory.exists():
            if args.comprobar:
                print('Pendiente: entorno y dependencias sin preparar.')
                return 1
            if importlib.util.find_spec('venv') is None or importlib.util.find_spec('ensurepip') is None:
                raise RuntimeError('Faltan venv/ensurepip en Python. En Linux instala el paquete venv '
                                   'de tu versión; en Windows/macOS usa una instalación completa de Python.')
            subprocess.run([sys.executable, '-m', 'venv', str(directory)], check=True, env=utf8_environment())
        if directory is not None and (not (directory / 'pyvenv.cfg').is_file() or not python.is_file()):
            raise RuntimeError('El destino no es un entorno virtual válido. Selecciona una carpeta nueva.')
        version = subprocess.run([str(python), '-c', 'import sys; print(sys.version_info.major, sys.version_info.minor)'],
                                 check=True, capture_output=True, text=True, timeout=30)
        if tuple(map(int, version.stdout.split())) < (3, 12):
            raise RuntimeError('Python del entorno no cumple el mínimo. Selecciona una carpeta nueva.')
        reports = probe(python, locks)
        needed = installation_needed(reports)
        for report in reports:
            for p in report['packages']:
                print(f"{p['name']}: {p['status']}")
        if needed and args.comprobar:
            return 1
        if needed:
            command = [str(python), '-m', 'pip', 'install', '--disable-pip-version-check', '--only-binary=:all:',
                       '-r', str(requirements)]
            subprocess.run(command, check=True, env=utf8_environment())
            if installation_needed(probe(python, locks)):
                raise RuntimeError('La instalación terminó con dependencias pendientes.')
        subprocess.run([str(python), '-m', 'pip', 'check'], check=True, env=utf8_environment())
        print(f'Dependencias verificadas. Python: {python}')
        print('Si usaste --entorno, define SKILLS_RUNTIME_DIR con esa ruta para ejecutar las herramientas.')
        print('Renderizado externo (no instalado por pip): ' + ', '.join(
            f'{name}={shutil.which(name) or "no detectado en PATH"}' for name in ('libreoffice', 'pdftoppm')))
        return 0
    except (OSError, RuntimeError, subprocess.SubprocessError) as error:
        print(f'Error: {error}', file=sys.stderr)
        print('Comprueba pip, red, permisos y wheels compatibles. Si Python está gestionado por el sistema '
              '(externally-managed-environment), usa --entorno; no se fuerza --break-system-packages. '
              'venv/ensurepip solo son necesarios para crear un entorno opcional.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
