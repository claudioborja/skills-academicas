# Preprocesador Documentos

Convierte, limpia, segmenta e inventaria documentos largos en Linux, Windows y macOS antes de que otras skills los lean o reescriban. Usar para PDF, DOCX, HTML, TXT y Markdown cuando se necesite extraer texto, reducir contexto, segmentar manuscritos o proteger citas, DOI, tablas, código y referencias.

## Uso

Invócala directamente con `$preprocesador-documentos` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $preprocesador-documentos para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Objetivo
- Ejecución multiplataforma
- Dependencias y entorno
- Herramientas individuales
- Enrutamiento y salida

## Recursos incluidos

### Scripts

- [`scripts/dependencias.py`](../../preprocesador-documentos/scripts/dependencias.py)
- [`scripts/documento_a_markdown.py`](../../preprocesador-documentos/scripts/documento_a_markdown.py)
- [`scripts/preprocesar_documento.ps1`](../../preprocesador-documentos/scripts/preprocesar_documento.ps1)
- [`scripts/preprocesar_documento.py`](../../preprocesador-documentos/scripts/preprocesar_documento.py)
- [`scripts/preprocesar_documento.sh`](../../preprocesador-documentos/scripts/preprocesar_documento.sh)
- [`scripts/proteger_bloques.py`](../../preprocesador-documentos/scripts/proteger_bloques.py)
- [`scripts/requirements-lock.txt`](../../preprocesador-documentos/scripts/requirements-lock.txt)
- [`scripts/requirements.txt`](../../preprocesador-documentos/scripts/requirements.txt)
- [`scripts/runtime_portable.py`](../../preprocesador-documentos/scripts/runtime_portable.py)
- [`scripts/segmentar_manuscrito.py`](../../preprocesador-documentos/scripts/segmentar_manuscrito.py)

### Referencias

- [`references/uso-en-workflow.md`](../../preprocesador-documentos/references/uso-en-workflow.md)

### Pruebas

- [`tests/test_dependencias.py`](../../preprocesador-documentos/tests/test_dependencias.py)
- [`tests/test_runtime.py`](../../preprocesador-documentos/tests/test_runtime.py)

### Configuración de interfaz

- [`agents/openai.yaml`](../../preprocesador-documentos/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `workflow-maestro-academico-editorial` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`preprocesador-documentos/SKILL.md`](../../preprocesador-documentos/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
