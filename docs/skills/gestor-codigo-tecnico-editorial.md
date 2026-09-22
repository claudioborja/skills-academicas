# Gestor Codigo Tecnico Editorial

Presenta y revisa listados de código, salidas de consola y fragmentos técnicos para libros, manuales y documentación de software. Úsalo cuando el código sea parte legible de la obra; no para desarrollar ni validar el software.

## Uso

Invócala directamente con `$gestor-codigo-tecnico-editorial` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $gestor-codigo-tecnico-editorial para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Objetivo
- Decisiones editoriales
- Presentación
- Ejecución Python obligatoria
- DOCX para fragmentos breves
- Flujo y controles

## Recursos incluidos

### Scripts

- [`scripts/archivos_seguros.py`](../../gestor-codigo-tecnico-editorial/scripts/archivos_seguros.py)
- [`scripts/auditar_listados_codigo.py`](../../gestor-codigo-tecnico-editorial/scripts/auditar_listados_codigo.py)
- [`scripts/generar_listado_docx.py`](../../gestor-codigo-tecnico-editorial/scripts/generar_listado_docx.py)
- [`scripts/requirements-lock.txt`](../../gestor-codigo-tecnico-editorial/scripts/requirements-lock.txt)

### Referencias

- [`references/criterios-listados.md`](../../gestor-codigo-tecnico-editorial/references/criterios-listados.md)

### Pruebas

- [`tests/test_auditar_listados_codigo.py`](../../gestor-codigo-tecnico-editorial/tests/test_auditar_listados_codigo.py)

### Configuración de interfaz

- [`agents/openai.yaml`](../../gestor-codigo-tecnico-editorial/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `editor-en-jefe` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`gestor-codigo-tecnico-editorial/SKILL.md`](../../gestor-codigo-tecnico-editorial/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
