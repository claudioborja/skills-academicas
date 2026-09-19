"""Intérprete y dependencias locales sin comandos específicos del sistema."""
from __future__ import annotations

import os
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys

SCRIPTS = Path(__file__).resolve().parent


def utf8_environment() -> dict[str, str]:
    return dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8')


def configure_console() -> None:
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')


def runtime_directory() -> Path:
    override = os.environ.get('SKILLS_RUNTIME_DIR')
    if override:
        return Path(override).expanduser().resolve()
    tag = f'{sys.platform}-{platform.machine().lower()}-py{sys.version_info.major}{sys.version_info.minor}'
    return SCRIPTS.parent / '.runtime' / tag


def runtime_python(directory: Path) -> Path:
    return directory / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')


def usable(python: Path) -> bool:
    if not python.is_file():
        return False
    try:
        return subprocess.run([str(python), '-c', 'import sys; sys.exit(sys.version_info < (3, 10))'],
                              capture_output=True, timeout=15).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def select_python(prepare: bool = False) -> str:
    if sys.version_info < (3, 10):
        raise RuntimeError('Se requiere Python 3.10 o posterior.')
    directory = runtime_directory()
    python = runtime_python(directory)
    valid = usable(python)
    if not prepare:
        return str(python) if valid else sys.executable
    if not valid:
        if directory.exists():
            raise RuntimeError(f'Entorno no válido: {directory}. Usa SKILLS_RUNTIME_DIR con una carpeta nueva.')
        if importlib.util.find_spec('venv') is None or importlib.util.find_spec('ensurepip') is None:
            raise RuntimeError('Faltan venv/ensurepip en este Python. Instala el paquete venv correspondiente '
                               'a su versión o usa un entorno Python completo.')
        subprocess.run([sys.executable, '-m', 'venv', str(directory)], check=True,
                       env=utf8_environment())
    probe_command = [str(python), str(SCRIPTS / 'dependencias.py')]
    probe = subprocess.run(probe_command, capture_output=True, text=True, encoding='utf-8',
                           env=utf8_environment(), timeout=30)
    if probe.returncode:
        try:
            state = json.loads(probe.stdout)
        except (ValueError, TypeError) as error:
            raise RuntimeError('No se pudo comprobar el entorno de dependencias: ' + probe.stderr) from error
        if any(p['status'] == 'version_mismatch' for p in state.get('packages', [])):
            raise RuntimeError('El entorno tiene versiones distintas de la base fijada. '
                               'Usa SKILLS_RUNTIME_DIR con una carpeta nueva; no se reemplazan paquetes existentes.')
        subprocess.run([str(python), '-m', 'pip', 'install', '--disable-pip-version-check',
                        '--only-binary=:all:', '-r', str(SCRIPTS / 'requirements-lock.txt')], check=True,
                       env=utf8_environment())
        subprocess.run(probe_command, check=True, capture_output=True, env=utf8_environment(), timeout=30)
    subprocess.run([str(python), '-m', 'pip', 'check'], check=True,
                   capture_output=True, env=utf8_environment(), timeout=30)
    return str(python)


def run_script(python: str, script: Path, arguments: list[str]) -> int:
    return subprocess.run([python, '-X', 'utf8', str(script), *arguments],
                          env=utf8_environment()).returncode
