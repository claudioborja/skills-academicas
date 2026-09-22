# Respondedor De Observaciones Académicas

Úsalo cuando el usuario necesite responder observaciones de tutor, jurado, editor, evaluador o par revisor, convirtiendo comentarios dispersos en una matriz de cambios, plan de respuesta y ajustes concretos al manuscrito.

## Uso

Invócala directamente con `$respondedor-observaciones-academicas` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $respondedor-observaciones-academicas para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Automatización Previa
- Objetivo
- Cuándo usarlo
- Flujo de trabajo
- Salida esperada
- Validación final

## Recursos incluidos

### Herramientas automatizadas

- [`scripts/observaciones_a_matriz.py`](../../respondedor-observaciones-academicas/scripts/observaciones_a_matriz.py)

### Configuración de interfaz

- [`agents/openai.yaml`](../../respondedor-observaciones-academicas/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `editor-en-jefe` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`respondedor-observaciones-academicas/SKILL.md`](../../respondedor-observaciones-academicas/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
