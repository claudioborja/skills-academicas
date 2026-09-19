# Auditor Coherencia Argumentativa

Úsalo cuando el usuario necesite revisar si un texto tiene continuidad lógica, tesis clara, transiciones válidas, conclusiones derivadas del desarrollo y ausencia de contradicciones, repeticiones conceptuales o saltos argumentativos.

## Uso

Invócala directamente con `$auditor-coherencia-argumentativa` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $auditor-coherencia-argumentativa para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Objetivo
- Cuándo usarlo
- Flujo de trabajo
- Salida esperada
- Validación final

## Recursos incluidos

### Configuración de interfaz

- [`agents/openai.yaml`](../../auditor-coherencia-argumentativa/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `workflow-maestro-academico-editorial` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`auditor-coherencia-argumentativa/SKILL.md`](../../auditor-coherencia-argumentativa/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
