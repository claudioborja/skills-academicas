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
COLLECTION_ROOT = SCRIPTS.parents[2]


def utf8_environment() -> dict[str, str]:
    return dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8')


def configure_console() -> None:
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')


def runtime_directory(owner: Path | None = None) -> Path:
    override = os.environ.get('SKILLS_RUNTIME_DIR')
    if override:
        return Path(override).expanduser().resolve()
    tag = f'{sys.platform}-{platform.machine().lower()}-py{sys.version_info.major}{sys.version_info.minor}'
    base = Path(owner).resolve() if owner is not None else SCRIPTS.parent
    return base / '.runtime' / tag


def runtime_python(directory: Path) -> Path:
    return directory / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')


def bundled_python(directory: Path) -> Path | None:
    """Localizar un intérprete opcional empaquetado para esta plataforma."""
    machine = platform.machine().lower()
    bundle = bundled_label()
    if bundle is None:
        return None
    candidate = COLLECTION_ROOT / 'editor-en-jefe' / 'runtime' / 'python' / bundle / ('python.exe' if os.name == 'nt' else 'bin/python')
    return candidate if candidate.is_file() else None


def bundled_label() -> str | None:
    machine = platform.machine().lower()
    return {
        ('linux', 'x86_64'): 'linux-x86_64-py314',
        ('win32', 'amd64'): 'windows-x86_64-py314',
        ('darwin', 'x86_64'): 'macos-x86_64-py314',
        ('darwin', 'arm64'): 'macos-arm64-py314',
    }.get((sys.platform, machine))


def bundled_wheels(directory: Path) -> Path | None:
    bundle = bundled_label()
    if bundle is None:
        return None
    wheels = COLLECTION_ROOT / 'editor-en-jefe' / 'runtime' / 'python' / 'wheels' / bundle
    return wheels if wheels.is_dir() else None


def usable(python: Path) -> bool:
    if not python.is_file():
        return False
    try:
        return subprocess.run([str(python), '-c', 'import sys; sys.exit(sys.version_info < (3, 10))'],
                              capture_output=True, timeout=15).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def select_python(prepare: bool = False, lock: Path | None = None, directory: Path | None = None) -> str:
    """Seleccionar Python y, al preparar, instalar solo el perfil declarado."""
    if sys.version_info < (3, 10):
        raise RuntimeError('Se requiere Python 3.10 o posterior.')
    lock = Path(lock) if lock is not None else SCRIPTS / 'requirements-lock.txt'
    if not lock.is_file():
        raise RuntimeError(f'No existe el lock de dependencias: {lock}')
    isolated = directory is not None or bool(os.environ.get('SKILLS_RUNTIME_DIR'))
    if not isolated:
        current = subprocess.run([sys.executable, str(SCRIPTS / 'dependencias.py'), '--lock', str(lock)],
                                 capture_output=True, env=utf8_environment(), timeout=30)
        if current.returncode == 0:
            return sys.executable
    directory = Path(directory).resolve() if directory is not None else runtime_directory()
    packaged = bundled_python(directory)
    python = packaged or runtime_python(directory)
    valid = usable(python)
    if not prepare:
        return str(python) if valid else sys.executable
    if not valid:
        if packaged is not None:
            raise RuntimeError(f'El intérprete empaquetado no es ejecutable: {packaged}')
        if directory.exists():
            raise RuntimeError(f'Entorno no válido: {directory}. Usa SKILLS_RUNTIME_DIR con una carpeta nueva.')
        creator = Path(sys.executable)
        if creator == Path(sys.executable) and (importlib.util.find_spec('venv') is None or importlib.util.find_spec('ensurepip') is None):
            raise RuntimeError('Faltan venv/ensurepip en este Python. Instala el paquete venv correspondiente '
                               'a su versión o incluye un intérprete completo en runtime/python.')
        subprocess.run([str(creator), '-m', 'venv', str(directory)], check=True,
                       env=utf8_environment())
    probe_command = [str(python), str(SCRIPTS / 'dependencias.py'), '--lock', str(lock)]
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
        command = [str(python), '-m', 'pip', 'install', '--disable-pip-version-check',
                   '--only-binary=:all:']
        wheels = bundled_wheels(directory)
        if wheels is not None:
            command.extend(['--no-index', '--find-links', str(wheels)])
        command.extend(['-r', str(lock)])
        subprocess.run(command, check=True,
                       env=utf8_environment())
        subprocess.run(probe_command, check=True, capture_output=True, env=utf8_environment(), timeout=30)
    subprocess.run([str(python), '-m', 'pip', 'check'], check=True,
                   capture_output=True, env=utf8_environment(), timeout=30)
    return str(python)


def run_script(python: str, script: Path, arguments: list[str]) -> int:
    return subprocess.run([python, '-X', 'utf8', str(script), *arguments],
                          env=utf8_environment()).returncode
