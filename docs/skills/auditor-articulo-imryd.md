# Auditor Artículo IMRyD

Extrae secciones, fragmentos y señales mecánicas de artículos IMRyD para orientar una revisión científica. Usar para elaborar un inventario estructural y una lista de comprobación previa al envío; sus herramientas automatizadas no prueban la coherencia entre objetivo, método y resultados ni la suficiencia de la evidencia.

## Uso

Invócala directamente con `$auditor-articulo-imryd` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $auditor-articulo-imryd para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Ejecución multiplataforma
- Objetivo
- Herramientas automatizadas
- Uso

## Recursos incluidos

### Herramientas automatizadas

- [`scripts/auditar_imryd.py`](../../auditor-articulo-imryd/scripts/auditar_imryd.py)
- [`scripts/check_envio_revista.py`](../../auditor-articulo-imryd/scripts/check_envio_revista.py)
- [`scripts/matriz_objetivo_metodo_resultados.py`](../../auditor-articulo-imryd/scripts/matriz_objetivo_metodo_resultados.py)

### Referencias

- [`references/criterios.md`](../../auditor-articulo-imryd/references/criterios.md)

### Configuración de interfaz

- [`agents/openai.yaml`](../../auditor-articulo-imryd/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `editor-en-jefe` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`auditor-articulo-imryd/SKILL.md`](../../auditor-articulo-imryd/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
