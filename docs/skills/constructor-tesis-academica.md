# Constructor Tesis Academica

Construye, diagnostica, organiza y revisa tesis, tesinas, trabajos de grado, proyectos de titulación y disertaciones desde el tema inicial hasta la preentrega. Usarlo para planteamiento del problema, objetivos, preguntas o hipótesis, justificación, marco teórico, metodología, resultados, discusión, conclusiones, recomendaciones, matriz de consistencia, operacionalización, coherencia entre secciones, normas universitarias o respuesta a tutor y jurado.

## Uso

Invócala directamente con `$constructor-tesis-academica` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $constructor-tesis-academica para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Objetivo
- Regla central
- Flujo
- Coordinación
- Referencias

## Recursos incluidos

### Referencias

- [`references/diagnostico-tesis.md`](../../constructor-tesis-academica/references/diagnostico-tesis.md)
- [`references/estructura-capitulos.md`](../../constructor-tesis-academica/references/estructura-capitulos.md)
- [`references/matriz-consistencia.md`](../../constructor-tesis-academica/references/matriz-consistencia.md)

### Configuración de interfaz

- [`agents/openai.yaml`](../../constructor-tesis-academica/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `workflow-maestro-academico-editorial` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`constructor-tesis-academica/SKILL.md`](../../constructor-tesis-academica/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
