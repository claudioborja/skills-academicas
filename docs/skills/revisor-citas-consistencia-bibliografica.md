# Revisor Citas Consistencia Bibliografica

Úsalo cuando el usuario necesite comprobar que las citas del cuerpo coinciden con la bibliografía final, detectar referencias huérfanas, entradas faltantes, datos inconsistentes, fuentes sin DOI/acceso completo, revistas o editoriales depredadoras y mezclas de estilo bibliográfico dentro de un mismo documento.

## Uso

Invócala directamente con `$revisor-citas-consistencia-bibliografica` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $revisor-citas-consistencia-bibliografica para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Automatización Previa
- Objetivo
- Cuándo usarlo
- Flujo de trabajo
- Validación final

## Recursos incluidos

### Configuración de interfaz

- [`agents/openai.yaml`](../../revisor-citas-consistencia-bibliografica/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `workflow-maestro-academico-editorial` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`revisor-citas-consistencia-bibliografica/SKILL.md`](../../revisor-citas-consistencia-bibliografica/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
