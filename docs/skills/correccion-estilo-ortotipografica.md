# Correccion Estilo Ortotipografica

Úsalo cuando el usuario necesite revisar, corregir o pulir un texto en español, especialmente para mejorar ortografía, puntuación, acentuación, mayúsculas, cursivas, comillas, rayas, abreviaturas, numeración, uniformidad editorial, claridad sintáctica, fluidez, concisión y consistencia de estilo sin alterar innecesariamente la voz del autor. También aplica a capítulos, artículos, tesis, informes, libros, prólogos, introducciones, conclusiones y textos institucionales.

## Uso

Invócala directamente con `$correccion-estilo-ortotipografica` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $correccion-estilo-ortotipografica para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Objetivo
- Rol
- Cuándo usarlo
- Alcance de corrección
- Flujo de trabajo
- Reglas de intervención
- Problemas frecuentes a detectar
- Preferencias editoriales para libros
- Salidas posibles
- Validación final
- Referencias de apoyo

## Recursos incluidos

### Referencias

- [`references/criterios-estilo.md`](../../correccion-estilo-ortotipografica/references/criterios-estilo.md)
- [`references/criterios-ortotipografia.md`](../../correccion-estilo-ortotipografica/references/criterios-ortotipografia.md)

### Configuración de interfaz

- [`agents/openai.yaml`](../../correccion-estilo-ortotipografica/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `editor-en-jefe` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`correccion-estilo-ortotipografica/SKILL.md`](../../correccion-estilo-ortotipografica/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
