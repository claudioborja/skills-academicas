# Auditor Documental Academico

Inventaria y audita mecánicamente documentos académicos o editoriales para reducir lectura manual: estructura, encabezados, extensión por sección, tablas, figuras, citas, bibliografía, terminología, anexos y checklist de preentrega. Use when Codex needs to prepare compact reports for editor-en-jefe, convertidor-tesis-a-libro, redaccion-articulo-cientifico-imryd, gestor-tablas-figuras-pies, normalizador-terminologia-glosario or maquetacion-academica-preentrega.

## Uso

Invócala directamente con `$auditor-documental-academico` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $auditor-documental-academico para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Ejecución multiplataforma
- Objetivo
- Scripts
- Uso

## Recursos incluidos

### Scripts

- [`scripts/analizar_repeticiones.py`](../../auditor-documental-academico/scripts/analizar_repeticiones.py)
- [`scripts/auditar_terminologia.py`](../../auditor-documental-academico/scripts/auditar_terminologia.py)
- [`scripts/check_preentrega.py`](../../auditor-documental-academico/scripts/check_preentrega.py)
- [`scripts/inventariar_documento.py`](../../auditor-documental-academico/scripts/inventariar_documento.py)
- [`scripts/inventariar_tablas_figuras.py`](../../auditor-documental-academico/scripts/inventariar_tablas_figuras.py)

### Referencias

- [`references/criterios.md`](../../auditor-documental-academico/references/criterios.md)

### Pruebas

- [`tests/test_preentrega.py`](../../auditor-documental-academico/tests/test_preentrega.py)

### Configuración de interfaz

- [`agents/openai.yaml`](../../auditor-documental-academico/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `editor-en-jefe` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`auditor-documental-academico/SKILL.md`](../../auditor-documental-academico/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
