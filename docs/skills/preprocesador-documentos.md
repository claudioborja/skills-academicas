# Preprocesador Documentos

Convierte, limpia, segmenta e inventaria documentos largos en Linux, Windows y macOS antes de que otras skills los lean o reescriban. Usar para PDF, DOCX, HTML, TXT y Markdown cuando se necesite extraer texto, reducir contexto, segmentar manuscritos o proteger citas, DOI, tablas, código y referencias.

## Ejemplo de uso

```text
Usa $preprocesador-documentos para instalar automáticamente las dependencias necesarias, convertir y segmentar este PDF, DOCX, HTML o TXT antes de procesarlo.
```

## Guía operativa

Los generadores de informes y perfiles exigen `--overwrite` para reemplazar salidas existentes, nunca entradas. Requieren `editor-en-jefe/scripts/archivos_seguros.py`, también en ejecución directa. Consultar [protección y límites de escritura](../../editor-en-jefe/references/portabilidad.md#protección-de-informes).

### Objetivo

Preparar documentos largos para que las demás skills trabajen con menos contexto y menos riesgo. Convertir a Markdown, segmentar e inventariar bloques protegidos antes de leer o reescribir un manuscrito extenso.

### Ejecución multiplataforma

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

### Dependencias y entorno

Si el Python actual ya cumple el perfil base y no se ha definido `SKILLS_RUNTIME_DIR`, reutilizarlo sin crear un entorno. Para preparar el equipo, Editor en jefe ofrece `scripts/instalar_requisitos.py`: instala en el Python actual por defecto y admite aislamiento opcional mediante `--entorno`. El mecanismo de preparación descrito a continuación es el respaldo cuando no hay una base compatible disponible.

TXT, Markdown y HTML se procesan sin dependencias externas ni descargas. Para PDF/DOCX el lanzador crea un entorno aislado e instala la base de `scripts/requirements-lock.txt` cuando faltan paquetes; `requirements.txt` remite al mismo lock. Comprueba versiones exactas, importaciones y `pip check`. Si un entorno existente tiene versiones distintas, pide seleccionar una carpeta nueva con `SKILLS_RUNTIME_DIR`; no fuerza actualizaciones o degradaciones. La instalación requiere acceso a paquetes binarios compatibles.

`scripts/dependencias.py` diagnostica versiones e importaciones sin instalar nada. Consultar [perfiles y límites](../../editor-en-jefe/references/portabilidad.md#dependencias-fijadas).

El entorno se separa por sistema operativo, arquitectura y versión de Python dentro de `.runtime/<plataforma-arquitectura-python>/`. No copiar entornos virtuales entre equipos. El antiguo `.runtime/Scripts/python.exe` no se reutiliza. Para una instalación de skills de solo lectura, definir `SKILLS_RUNTIME_DIR` con una carpeta nueva y escribible fuera de la instalación.

Si falta el módulo `venv`, instalar el soporte de entornos virtuales de la distribución de Python. Si una instalación falla, corregir la causa y volver a ejecutar; no borrar entornos existentes de forma automática.

### Herramientas individuales

El lanzador común `skills/editor-en-jefe/scripts/ejecutar.py` selecciona el entorno local cuando está disponible y configura UTF-8. En estos ejemplos, sustituir `python` por `python3` en Linux/macOS o por `py -3` en Windows:

```text
python skills/editor-en-jefe/scripts/ejecutar.py --preparar
python skills/editor-en-jefe/scripts/ejecutar.py preprocesador-documentos/scripts/documento_a_markdown.py "ruta/archivo.pdf" --out "ruta/salida.md" --json-out "ruta/salida.json"
python skills/editor-en-jefe/scripts/ejecutar.py preprocesador-documentos/scripts/segmentar_manuscrito.py "ruta/salida.md" --out "ruta/segmentos.md" --json-out "ruta/segmentos.json"
python skills/editor-en-jefe/scripts/ejecutar.py preprocesador-documentos/scripts/proteger_bloques.py "ruta/salida.md" --out "ruta/protegidos.md" --json-out "ruta/protegidos.json"
```

En proyectos de libro, guardar la salida en `RUTA_LIBRO/00_contexto_y_diagnostico/preprocesado`. Conservar el original y evitar que las rutas de salida lo sobrescriban.

### Enrutamiento y salida

Usar primero para tesis-libro, artículos IMRyD, humanización, referencias APA7/IEEE y preentrega cuando la entrada sea un documento largo. Entregar Markdown y JSON de conversión, segmentación y bloques protegidos; usar estos mapas para decidir qué fragmentos leer y qué skill activar después.

Detectar citas, transcripciones, DOI, URLs, referencias, tablas, código, Mermaid y fórmulas que no deben alterarse. Leer `references/uso-en-workflow.md` para conectar el resultado con las skills especializadas.

## Recursos incluidos

### Herramientas automatizadas

| Recurso | Función |
| --- | --- |
| [`scripts/dependencias.py`](../../preprocesador-documentos/scripts/dependencias.py) | Comprobar versiones fijadas e importaciones sin instalar ni modificar paquetes. |
| [`scripts/documento_a_markdown.py`](../../preprocesador-documentos/scripts/documento_a_markdown.py) | Recurso auxiliar: Documento a markdown. |
| [`scripts/preprocesar_documento.ps1`](../../preprocesador-documentos/scripts/preprocesar_documento.ps1) | Recurso auxiliar: Preprocesar documento. |
| [`scripts/preprocesar_documento.py`](../../preprocesador-documentos/scripts/preprocesar_documento.py) | Conversión, segmentación y protección en Linux, Windows y macOS. |
| [`scripts/preprocesar_documento.sh`](../../preprocesador-documentos/scripts/preprocesar_documento.sh) | Recurso auxiliar: Preprocesar documento. |
| [`scripts/proteger_bloques.py`](../../preprocesador-documentos/scripts/proteger_bloques.py) | Recurso auxiliar: Proteger bloques. |
| [`scripts/requirements-lock.txt`](../../preprocesador-documentos/scripts/requirements-lock.txt) | Dependencias Python fijadas para esta herramienta. |
| [`scripts/requirements.txt`](../../preprocesador-documentos/scripts/requirements.txt) | Dependencias Python fijadas para esta herramienta. |
| [`scripts/runtime_portable.py`](../../preprocesador-documentos/scripts/runtime_portable.py) | Intérprete y dependencias locales sin comandos específicos del sistema. |
| [`scripts/segmentar_manuscrito.py`](../../preprocesador-documentos/scripts/segmentar_manuscrito.py) | Recurso auxiliar: Segmentar manuscrito. |

### Referencias

| Recurso | Función |
| --- | --- |
| [`references/uso-en-workflow.md`](../../preprocesador-documentos/references/uso-en-workflow.md) | Uso En Workflow |

### Pruebas

| Recurso | Función |
| --- | --- |
| [`tests/test_dependencias.py`](../../preprocesador-documentos/tests/test_dependencias.py) | Recurso auxiliar: Test dependencias. |
| [`tests/test_runtime.py`](../../preprocesador-documentos/tests/test_runtime.py) | Evitar entornos incompletos cuando falta el soporte de instalación. |

### Configuración de interfaz

| Recurso | Función |
| --- | --- |
| [`agents/openai.yaml`](../../preprocesador-documentos/agents/openai.yaml) | Metadatos de interfaz e invocación de la skill. |

## Fuente normativa

Esta ficha se genera desde [`preprocesador-documentos/SKILL.md`](../../preprocesador-documentos/SKILL.md), que permanece como contrato normativo. Regenera la ficha después de modificar ese archivo.
