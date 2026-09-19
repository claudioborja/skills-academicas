# Ajustes Editoriales Bibliograficos

Úsalo cuando el usuario necesite aplicar reglas editoriales o institucionales adicionales sobre citas y bibliografía, más estrictas o diferentes de la norma base, por ejemplo prohibir referencias sin fecha, exigir tipos de fuente concretos, vetar ciertas clases de documentos o adaptar el manuscrito a criterios de un editor, revista o universidad.

## Uso

Invócala directamente con `$ajustes-editoriales-bibliograficos` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $ajustes-editoriales-bibliograficos para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Objetivo
- Cuándo usarlo
- Regla central
- Tipos de ajustes editoriales frecuentes
- Flujo de trabajo
- Salida esperada
- Validación final
- Referencias de apoyo

## Recursos incluidos

### Referencias

- [`references/norma-vs-politica-editorial.md`](../../ajustes-editoriales-bibliograficos/references/norma-vs-politica-editorial.md)

### Configuración de interfaz

- [`agents/openai.yaml`](../../ajustes-editoriales-bibliograficos/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `workflow-maestro-academico-editorial` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`ajustes-editoriales-bibliograficos/SKILL.md`](../../ajustes-editoriales-bibliograficos/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
