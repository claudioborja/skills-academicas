# Maquetación Académica y Preentrega

Usalo cuando el usuario necesite una revision final de presentacion academica o editorial antes de entrega, incluyendo titulos, subtitulos, numeracion, secciones preliminares, bibliografia, anexos, consistencia visual, exportacion a Word con tablas nativas editables, limpieza general para Word/PDF, o generacion complementaria de TXT limpio sin marcas Markdown para libros y manuscritos.

## Uso

Invócala directamente con `$maquetacion-academica-preentrega` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $maquetacion-academica-preentrega para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Ejecución multiplataforma
- Automatizacion Previa
- Objetivo
- Regla De Productos Finales
- Perfil formal del proyecto
- Flujo De Trabajo
- Herramienta para Word
- Formato editorial e imágenes
- Herramienta para el TXT final
- Validacion Final

## Recursos incluidos

### Herramientas automatizadas

- [`scripts/auditar_docx_apa7.py`](../../maquetacion-academica-preentrega/scripts/auditar_docx_apa7.py)
- [`scripts/markdown_a_docx.py`](../../maquetacion-academica-preentrega/scripts/markdown_a_docx.py)
- [`scripts/markdown_a_txt_final.py`](../../maquetacion-academica-preentrega/scripts/markdown_a_txt_final.py)
- [`scripts/portada_apa.py`](../../maquetacion-academica-preentrega/scripts/portada_apa.py)
- [`scripts/regresion_visual_apa.py`](../../maquetacion-academica-preentrega/scripts/regresion_visual_apa.py)

### Referencias

- [`references/apa7-docx.md`](../../maquetacion-academica-preentrega/references/apa7-docx.md)
- [`references/ieee-presentacion.md`](../../maquetacion-academica-preentrega/references/ieee-presentacion.md)

### Pruebas

- [`tests/test_apa7.py`](../../maquetacion-academica-preentrega/tests/test_apa7.py)
- [`tests/test_exportacion_segura.py`](../../maquetacion-academica-preentrega/tests/test_exportacion_segura.py)
- [`tests/test_portada_apa.py`](../../maquetacion-academica-preentrega/tests/test_portada_apa.py)
- [`tests/test_regresion_visual_apa.py`](../../maquetacion-academica-preentrega/tests/test_regresion_visual_apa.py)

### Configuración de interfaz

- [`agents/openai.yaml`](../../maquetacion-academica-preentrega/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `editor-en-jefe` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`maquetacion-academica-preentrega/SKILL.md`](../../maquetacion-academica-preentrega/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
