"""Publicar el DOCX sin sobrescrituras implícitas ni salidas peligrosas."""
from contextlib import contextmanager
import os
from pathlib import Path
import tempfile


def same_path(a: Path, b: Path) -> bool:
    return a.resolve() == b.resolve() or (a.exists() and b.exists() and a.samefile(b))


def validate_outputs(inputs, outputs, overwrite=False):
    inputs = [Path(path) for path in inputs if path is not None]
    outputs = [Path(path) for path in outputs if path is not None]
    for index, target in enumerate(outputs):
        for parent in target.parents:
            if parent.exists() and not parent.is_dir():
                raise ValueError(f"Un padre de la salida no es un directorio: {parent}")
        if any(target.resolve() in other.resolve().parents or other.resolve() in target.resolve().parents
               for other in outputs[:index]):
            raise ValueError(f"Una salida ocupa el directorio de otra salida: {target}")
        if any(same_path(target, source) for source in inputs):
            raise ValueError(f"La salida coincide con una entrada: {target}")
        if any(same_path(target, other) for other in outputs[:index]):
            raise ValueError(f"Dos salidas coinciden: {target}")
        if target.is_symlink():
            raise ValueError(f"No se escribe sobre enlaces simbólicos: {target}")
        if target.exists() and (not overwrite or not target.is_file()):
            raise ValueError(f"La salida ya existe: {target}; elegir otro nombre o autorizar sobrescritura.")


@contextmanager
def atomic_output(path, overwrite=False):
    path = Path(path)
    validate_outputs([], [path], overwrite)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix="." + path.name + ".", dir=path.parent)
    temporary = Path(temporary)
    try:
        with os.fdopen(descriptor, "w+b") as stream:
            yield stream
            stream.flush()
            os.fsync(stream.fileno())
        if overwrite:
            os.replace(temporary, path)
        else:
            os.link(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
