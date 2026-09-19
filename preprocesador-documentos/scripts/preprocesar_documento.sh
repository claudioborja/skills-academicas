#!/bin/sh
# Lanzador POSIX para Linux/macOS. Toda la lógica reside en Python.
set -eu
script_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1 &&
       "$candidate" -c 'import sys; sys.exit(sys.version_info < (3, 10))' 2>/dev/null; then
        exec "$candidate" -X utf8 "$script_directory/preprocesar_documento.py" "$@"
    fi
done
echo 'Se requiere Python 3.10 o posterior disponible como python3 o python.' >&2
exit 1
