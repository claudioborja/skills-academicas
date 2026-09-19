# Gestor Ecuaciones Academicas

Crea, revisa, normaliza, convierte e integra ecuaciones académicas y científicas en LaTeX, Markdown, MathML, OMML/Word y formatos editoriales. Usar cuando Codex deba comprobar notación, variables, unidades, dimensiones, numeración, referencias cruzadas, editabilidad o presentación de fórmulas; no sustituye la validación disciplinar de una demostración o modelo.

## Uso

Invócala directamente con `$gestor-ecuaciones-academicas` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $gestor-ecuaciones-academicas para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Responsabilidad
- Flujo
- Formatos
- Auditoría mecánica reproducible
- Límites de intervención
- Coordinación
- Cierre

## Recursos incluidos

### Scripts

- [`scripts/auditar_ecuaciones.py`](../../gestor-ecuaciones-academicas/scripts/auditar_ecuaciones.py)

### Referencias

- [`references/formatos-y-control.md`](../../gestor-ecuaciones-academicas/references/formatos-y-control.md)

### Pruebas

- [`tests/test_auditar_ecuaciones.py`](../../gestor-ecuaciones-academicas/tests/test_auditar_ecuaciones.py)

### Configuración de interfaz

- [`agents/openai.yaml`](../../gestor-ecuaciones-academicas/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `workflow-maestro-academico-editorial` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`gestor-ecuaciones-academicas/SKILL.md`](../../gestor-ecuaciones-academicas/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
