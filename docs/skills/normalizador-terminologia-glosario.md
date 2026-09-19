# Normalizador Terminologia Glosario

Úsalo cuando el usuario necesite uniformar términos técnicos, conceptos, nombres de variables, siglas, traducciones, categorías o etiquetas a lo largo de un manuscrito, y construir un glosario o banco terminológico consistente.

## Uso

Invócala directamente con `$normalizador-terminologia-glosario` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $normalizador-terminologia-glosario para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Automatización Previa
- Objetivo
- Cuándo usarlo
- Flujo de trabajo
- Validación final

## Recursos incluidos

### Configuración de interfaz

- [`agents/openai.yaml`](../../normalizador-terminologia-glosario/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `workflow-maestro-academico-editorial` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`normalizador-terminologia-glosario/SKILL.md`](../../normalizador-terminologia-glosario/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
