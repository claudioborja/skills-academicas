#!/usr/bin/env python3
"""Inspeccionar integridad, dimensiones, transparencia y PPI efectivo de una imagen raster."""
import argparse
import json
from pathlib import Path
import sys
import warnings

try:
    from PIL import Image, UnidentifiedImageError
except ImportError:  # pragma: no cover - depende del entorno de ejecución
    Image = None
    UnidentifiedImageError = OSError

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'editor-en-jefe/scripts'))
from archivos_seguros import atomic_write, validate_outputs


def inspect_raster(path: Path, width_cm: float, minimum_ppi: float) -> dict:
    base = {
        'archivo': str(path.resolve()),
        'bytes': path.stat().st_size,
        'ancho_impresion_cm': width_cm,
        'ppi_minimo': minimum_ppi,
    }
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            with Image.open(path) as candidate:
                candidate.verify()
            with Image.open(path) as candidate:
                candidate.load()
                width, height = candidate.size
                image_format = candidate.format
                mode = candidate.mode
                frames = getattr(candidate, 'n_frames', 1)
                alpha_channel = 'A' in candidate.getbands()
                transparency_metadata = 'transparency' in candidate.info
                transparent = False
                if alpha_channel or transparency_metadata:
                    transparent = candidate.convert('RGBA').getchannel('A').getextrema()[0] < 255
    except (Image.DecompressionBombError, Image.DecompressionBombWarning,
            UnidentifiedImageError, OSError, SyntaxError, ValueError) as error:
        return dict(base, integridad=False, estado='rechazada', error=str(error))

    effective_ppi = round(width * 2.54 / width_cm, 2)
    meets_ppi = effective_ppi >= minimum_ppi
    observations = []
    if not meets_ppi:
        observations.append(
            f'Resolución efectiva {effective_ppi:g} PPI inferior al mínimo {minimum_ppi:g} PPI.'
        )
    return dict(
        base,
        integridad=True,
        formato=image_format,
        modo=mode,
        fotogramas=frames,
        ancho_px=width,
        alto_px=height,
        proporcion=round(width / height, 4),
        canal_alpha=alpha_channel,
        tiene_transparencia=transparent,
        alto_impresion_cm=round(width_cm * height / width, 2),
        ppi_efectivo=effective_ppi,
        cumple_ppi=meets_ppi,
        estado='aprobada' if meets_ppi else 'advertencia',
        observaciones=observations,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('imagen', type=Path)
    parser.add_argument('--ancho-cm', required=True, type=float,
                        help='Ancho final de reproducción en centímetros')
    parser.add_argument('--ppi-minimo', type=float, default=300.0)
    parser.add_argument('--out', type=Path, help='Informe JSON opcional')
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    try:
        if Image is None:
            raise ValueError('Falta Pillow; instalar scripts/requirements-lock.txt en un entorno aislado')
        if not args.imagen.is_file():
            raise ValueError(f'No existe la imagen: {args.imagen}')
        if args.ancho_cm <= 0 or args.ppi_minimo <= 0:
            raise ValueError('El ancho y el PPI mínimo deben ser positivos')
        validate_outputs([args.imagen], [args.out], overwrite=args.overwrite)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    report = inspect_raster(args.imagen, args.ancho_cm, args.ppi_minimo)
    serialized = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        atomic_write(args.out, serialized + '\n', overwrite=args.overwrite)
    print(serialized)
    return 0 if report['estado'] == 'aprobada' else 1


if __name__ == '__main__':
    raise SystemExit(main())
