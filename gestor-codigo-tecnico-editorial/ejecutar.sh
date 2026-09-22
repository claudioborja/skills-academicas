#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
case "$(uname -s):$(uname -m)" in
  Linux:x86_64) TAG=linux-x86_64-py314 ;;
  Darwin:x86_64) TAG=macos-x86_64-py314 ;;
  Darwin:arm64|Darwin:aarch64) TAG=macos-arm64-py314 ;;
  *) echo "Plataforma no empaquetada: $(uname -s) $(uname -m)" >&2; exit 2 ;;
esac

case "${1:-}" in
  generar-listado) SCRIPT="$ROOT/scripts/generar_listado_docx.py"; NEEDS_DOCX=1 ;;
  auditar-listados) SCRIPT="$ROOT/scripts/auditar_listados_codigo.py" ;;
  *) echo "Uso: $0 {generar-listado|auditar-listados} argumentos" >&2; exit 2 ;;
esac
shift
RUNTIME="$ROOT/../editor-en-jefe/runtime/python"
PYTHON="$RUNTIME/$TAG/bin/python"
if [ "${NEEDS_DOCX:-0}" = 1 ]; then
  "$PYTHON" -m pip install --disable-pip-version-check --no-index \
    --find-links "$RUNTIME/wheels/$TAG" \
    -r "$ROOT/../requirements.txt" >/dev/null
fi
exec "$PYTHON" -X utf8 "$SCRIPT" "$@"
