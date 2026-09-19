---
name: preprocesador-documentos
description: Convierte, limpia, segmenta e inventaria documentos largos en Linux, Windows y macOS antes de que otras skills los lean o reescriban. Usar para PDF, DOCX, HTML, TXT y Markdown cuando se necesite extraer texto, reducir contexto, segmentar manuscritos o proteger citas, DOI, tablas, código y referencias.
---

# Preprocesador Documentos

Los generadores de informes y perfiles exigen `--overwrite` para reemplazar salidas existentes, nunca entradas. Requieren `workflow-maestro-academico-editorial/scripts/archivos_seguros.py`, también en ejecución directa. Consultar [protección y límites de escritura](../workflow-maestro-academico-editorial/references/portabilidad.md#protección-de-informes).

## Objetivo

Preparar documentos largos para que las demás skills trabajen con menos contexto y menos riesgo. Convertir a Markdown, segmentar e inventariar bloques protegidos antes de leer o reescribir un manuscrito extenso.

## Ejecución multiplataforma

Requiere Python 3.10 o posterior. La entrada principal es `scripts/preprocesar_documento.py`, compartida por Linux, Windows y macOS.

Los ejemplos parten del directorio que contiene `skills/`. Usar rutas absolutas si se trabaja desde otra carpeta. En Linux/macOS usar `python3`; en Windows, `py -3` o `python`.

Linux/macOS:

```sh
python3 skills/preprocesador-documentos/scripts/preprocesar_documento.py "ruta/archivo.pdf" "ruta/salida"
```

Windows:

```powershell
py -3 skills/preprocesador-documentos/scripts/preprocesar_documento.py "ruta/archivo.pdf" "ruta/salida"
```

El segundo argumento es opcional: por defecto crea `<nombre>-preprocesado` junto al documento. `--max-words 900` controla la segmentación, entre 100 y 10000 palabras.

También están disponibles los lanzadores del sistema:

```sh
sh skills/preprocesador-documentos/scripts/preprocesar_documento.sh "ruta/archivo.pdf" "ruta/salida"
```

```powershell
powershell -ExecutionPolicy Bypass -File skills/preprocesador-documentos/scripts/preprocesar_documento.ps1 "ruta/archivo.pdf" "ruta/salida" -MaxWords 900
```

La entrada Python y el lanzador POSIX requieren Python instalado. En Windows, el lanzador PowerShell busca Python 3.10 o posterior; si falta, instala Python 3.12 mediante `winget` para el usuario actual y vuelve a localizarlo. Si falta `winget` o falla la instalación, informa del problema y se detiene. Valida primero que el archivo de entrada exista.

## Dependencias y entorno

TXT, Markdown y HTML se procesan sin dependencias externas ni descargas. Para PDF/DOCX el lanzador crea un entorno aislado e instala la base de `scripts/requirements-lock.txt` cuando faltan paquetes; `requirements.txt` remite al mismo lock. Comprueba versiones exactas, importaciones y `pip check`. Si un entorno existente tiene versiones distintas, pide seleccionar una carpeta nueva con `SKILLS_RUNTIME_DIR`; no fuerza actualizaciones o degradaciones. La instalación requiere acceso a paquetes binarios compatibles.

`scripts/dependencias.py` diagnostica versiones e importaciones sin instalar nada. Consultar [perfiles y límites](../workflow-maestro-academico-editorial/references/portabilidad.md#dependencias-fijadas).

El entorno se separa por sistema operativo, arquitectura y versión de Python dentro de `.runtime/<plataforma-arquitectura-python>/`. No copiar entornos virtuales entre equipos. El antiguo `.runtime/Scripts/python.exe` no se reutiliza. Para una instalación de skills de solo lectura, definir `SKILLS_RUNTIME_DIR` con una carpeta nueva y escribible fuera de la instalación.

Si falta el módulo `venv`, instalar el soporte de entornos virtuales de la distribución de Python. Si una instalación falla, corregir la causa y volver a ejecutar; no borrar entornos existentes de forma automática.

## Herramientas individuales

El lanzador común `skills/workflow-maestro-academico-editorial/scripts/ejecutar.py` selecciona el entorno local cuando está disponible y configura UTF-8. En estos ejemplos, sustituir `python` por `python3` en Linux/macOS o por `py -3` en Windows:

```text
python skills/workflow-maestro-academico-editorial/scripts/ejecutar.py --preparar
python skills/workflow-maestro-academico-editorial/scripts/ejecutar.py preprocesador-documentos/scripts/documento_a_markdown.py "ruta/archivo.pdf" --out "ruta/salida.md" --json-out "ruta/salida.json"
python skills/workflow-maestro-academico-editorial/scripts/ejecutar.py preprocesador-documentos/scripts/segmentar_manuscrito.py "ruta/salida.md" --out "ruta/segmentos.md" --json-out "ruta/segmentos.json"
python skills/workflow-maestro-academico-editorial/scripts/ejecutar.py preprocesador-documentos/scripts/proteger_bloques.py "ruta/salida.md" --out "ruta/protegidos.md" --json-out "ruta/protegidos.json"
```

En proyectos de libro, guardar la salida en `RUTA_LIBRO/00_contexto_y_diagnostico/preprocesado`. Conservar el original y evitar que las rutas de salida lo sobrescriban.

## Enrutamiento y salida

Usar primero para tesis-libro, artículos IMRyD, humanización, referencias APA7/IEEE y preentrega cuando la entrada sea un documento largo. Entregar Markdown y JSON de conversión, segmentación y bloques protegidos; usar estos mapas para decidir qué fragmentos leer y qué skill activar después.

Detectar citas, transcripciones, DOI, URLs, referencias, tablas, código, Mermaid y fórmulas que no deben alterarse. Leer `references/uso-en-workflow.md` para conectar el resultado con las skills especializadas.
