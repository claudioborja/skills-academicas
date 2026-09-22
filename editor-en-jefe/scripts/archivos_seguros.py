"""Validación y publicación de archivos sin sobrescritura implícita."""
from pathlib import Path
from contextlib import contextmanager
import os
import tempfile
import shutil


def same_path(a: Path, b: Path) -> bool:
    return a.resolve() == b.resolve() or (a.exists() and b.exists() and a.samefile(b))


def validate_outputs(inputs, outputs, overwrite=False):
    inputs = [Path(p) for p in inputs if p is not None]
    outputs = [Path(p) for p in outputs if p is not None]
    for index, target in enumerate(outputs):
        for parent in target.parents:
            if parent.exists() and not parent.is_dir():
                raise ValueError(f'Un padre de la salida no es un directorio: {parent}')
        if any(target.resolve() in other.resolve().parents or other.resolve() in target.resolve().parents
               for other in outputs[:index]):
            raise ValueError(f'Una salida ocupa el directorio de otra salida: {target}')
        if any(same_path(target, source) for source in inputs):
            raise ValueError(f'La salida coincide con una entrada: {target}')
        if any(same_path(target, other) for other in outputs[:index]):
            raise ValueError(f'Dos salidas coinciden: {target}')
        if target.is_symlink():
            raise ValueError(f'No se escribe sobre enlaces simbólicos: {target}')
        if target.exists() and (not overwrite or not target.is_file()):
            raise ValueError(f'La salida ya existe: {target}; elegir otro nombre o autorizar sobrescritura.')


@contextmanager
def atomic_output(path, overwrite=False):
    """Producir bytes en un temporal y publicar únicamente al terminar sin error."""
    path = Path(path)
    validate_outputs([], [path], overwrite)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    temporary = Path(temporary)
    try:
        with os.fdopen(descriptor, 'w+b') as stream:
            yield stream
            stream.flush()
            os.fsync(stream.fileno())
        if overwrite:
            os.replace(temporary, path)
        else:
            # Publicación exclusiva: nunca sustituye un destino creado concurrentemente.
            os.link(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def atomic_write(path, data, overwrite=False):
    with atomic_output(path, overwrite) as stream:
        stream.write(data.encode('utf-8') if isinstance(data, str) else data)


def atomic_append(path, data):
    """Añadir conservando bytes previos; requiere un solo proceso escritor."""
    path = Path(path)
    validate_outputs([], [path], overwrite=True)
    exists = path.exists()
    with atomic_output(path, overwrite=exists) as stream:
        if exists:
            with path.open('rb') as source:
                shutil.copyfileobj(source, stream)
        stream.write(data.encode('utf-8') if isinstance(data, str) else data)


def validate_cli(arguments, overwrite=False):
    """Preflight conservador para opciones comunes; no sustituye validación del script."""
    output_flags = {'--out', '--json-out', '--report', '--csv-out', '--backup'}
    outputs, inputs = [], []
    index = 0
    while index < len(arguments):
        token = arguments[index]
        flag, separator, value = token.partition('=')
        if flag in output_flags:
            if not separator:
                index += 1
                if index >= len(arguments):
                    raise ValueError(f'Falta ruta para {flag}')
                value = arguments[index]
            outputs.append(Path(value))
        else:
            value = value if separator else token
            if not value.startswith('-') and '://' not in value and Path(value).is_file():
                inputs.append(Path(value))
        index += 1
    validate_outputs(inputs, outputs, overwrite)
