# Gestor De Continuidad De Libro

Úsalo cuando el usuario necesite mantener continuidad temática, estilística, terminológica y estructural entre capítulos de un libro, tesis extensa o manuscrito largo, evitando repeticiones, cambios de voz y quiebres de enfoque.

## Uso

Invócala directamente con `$gestor-continuidad-libro` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $gestor-continuidad-libro para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Objetivo
- Cuándo usarlo
- Flujo de trabajo
- Validación final
- Referencias de apoyo

## Recursos incluidos

### Referencias

- [`references/continuidad-de-manuscrito.md`](../../gestor-continuidad-libro/references/continuidad-de-manuscrito.md)

### Configuración de interfaz

- [`agents/openai.yaml`](../../gestor-continuidad-libro/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `editor-en-jefe` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`gestor-continuidad-libro/SKILL.md`](../../gestor-continuidad-libro/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
