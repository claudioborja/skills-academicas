# Automatizador Referencias

Automatiza tareas mecánicas de citas, DOI, bibliografía y fuentes descargadas para reducir consumo de tokens. Use when Codex needs to auditar citas APA/IEEE frente a bibliografía, detectar DOI faltantes o repetidos, consultar metadatos DOI en Crossref, inventariar PDFs/HTML/Markdown de referencias, normalizar entradas bibliográficas preliminares, o preparar insumos para gestor-referencias-academicas, revisor-citas-consistencia-bibliografica, filtro-editoriales-depredadoras y workflow-maestro-academico-editorial.

## Uso

Invócala directamente con `$automatizador-referencias` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $automatizador-referencias para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Ejecución multiplataforma
- Objetivo
- Regla Central
- Scripts
- Salida Esperada

## Recursos incluidos

### Scripts

- [`scripts/auditar_citas_bibliografia.py`](../../automatizador-referencias/scripts/auditar_citas_bibliografia.py)
- [`scripts/doi_a_referencia.py`](../../automatizador-referencias/scripts/doi_a_referencia.py)
- [`scripts/inventario_fuentes.py`](../../automatizador-referencias/scripts/inventario_fuentes.py)
- [`scripts/normalizar_referencias.py`](../../automatizador-referencias/scripts/normalizar_referencias.py)

### Referencias

- [`references/criterios.md`](../../automatizador-referencias/references/criterios.md)

### Pruebas

- [`tests/test_duplicados.py`](../../automatizador-referencias/tests/test_duplicados.py)
- [`tests/test_ieee.py`](../../automatizador-referencias/tests/test_ieee.py)

### Configuración de interfaz

- [`agents/openai.yaml`](../../automatizador-referencias/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `workflow-maestro-academico-editorial` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`automatizador-referencias/SKILL.md`](../../automatizador-referencias/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
