# Gestor De Redacción Latinoamérica

Úsalo cuando el usuario necesite redactar, reescribir, estructurar o pulir textos académicos, técnicos, institucionales o editoriales en español neutro latinoamericano, especialmente tesis, artículos, ensayos, informes, capítulos y libros. También aplica cuando se requiera elevar claridad, rigor, cohesión, consistencia terminológica y tono profesional sin introducir patrones típicos de texto generado por IA.

## Uso

Invócala directamente con `$gestor-redaccion-latinoamerica` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $gestor-redaccion-latinoamerica para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Objetivo
- Rol
- Cuándo usarlo
- Alcance
- Flujo de trabajo
- Reglas de redacción
- Ritmo de párrafo y puntuación
- Antipatrones IA
- Prohibiciones explícitas
- Sustitución recomendada
- Comportamiento por tarea
- Validación final
- Referencias de apoyo

## Recursos incluidos

### Referencias

- [`references/estilo-latinoamericano.md`](../../gestor-redaccion-latinoamerica/references/estilo-latinoamericano.md)
- [`references/estructuras-redaccion.md`](../../gestor-redaccion-latinoamerica/references/estructuras-redaccion.md)

### Configuración de interfaz

- [`agents/openai.yaml`](../../gestor-redaccion-latinoamerica/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `editor-en-jefe` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`gestor-redaccion-latinoamerica/SKILL.md`](../../gestor-redaccion-latinoamerica/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
