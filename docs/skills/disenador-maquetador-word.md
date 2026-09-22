# Diseñador y maquetador de libros en Word

Diseña y maqueta libros profesionales en Microsoft Word mediante estilos, secciones, campos y objetos nativos editables. Usar cuando el usuario necesite transformar un manuscrito en un DOCX con identidad visual, jerarquía tipográfica, páginas preliminares, aperturas de capítulo, tablas, figuras, encabezados, folios y composición resistente a futuras adiciones o eliminaciones. No sustituye la corrección del contenido ni la validación académica final.

## Uso

Invócala directamente con `$disenador-maquetador-word` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $disenador-maquetador-word para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Resultado
- Frontera
- Principios no negociables
- Entradas y decisiones
- Flujo de trabajo
- Entrega
- Criterios de cierre

## Recursos incluidos

### Referencias

- [`references/arquitectura-docx-editable.md`](../../disenador-maquetador-word/references/arquitectura-docx-editable.md)
- [`references/control-calidad-visual.md`](../../disenador-maquetador-word/references/control-calidad-visual.md)
- [`references/direccion-visual-y-perfiles.md`](../../disenador-maquetador-word/references/direccion-visual-y-perfiles.md)

### Configuración de interfaz

- [`agents/openai.yaml`](../../disenador-maquetador-word/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `editor-en-jefe` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`disenador-maquetador-word/SKILL.md`](../../disenador-maquetador-word/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
