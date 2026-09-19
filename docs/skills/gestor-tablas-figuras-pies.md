# Gestor Tablas Figuras Pies

Úsalo cuando el usuario necesite decidir, crear, revisar, uniformar o exportar tablas, figuras, gráficos, títulos, numeración, fuentes, notas al pie, llamadas en el texto y criterios de presentación visual dentro de un documento académico o editorial, especialmente cuando las tablas Markdown deban conservarse como tablas editables en Word o publicarse en HTML para facilitar su revisión y copia.

## Uso

Invócala directamente con `$gestor-tablas-figuras-pies` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $gestor-tablas-figuras-pies para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Ejecución multiplataforma
- Automatización Previa
- Objetivo
- Regla de necesidad y procedencia
- Cuándo usarlo
- Flujo de trabajo
- Presentación APA 7
- Salidas para tablas
- Validación final

## Recursos incluidos

### Scripts

- [`scripts/exportar_tablas_html.py`](../../gestor-tablas-figuras-pies/scripts/exportar_tablas_html.py)
- [`scripts/registrar_tabla.py`](../../gestor-tablas-figuras-pies/scripts/registrar_tabla.py)

### Configuración de interfaz

- [`agents/openai.yaml`](../../gestor-tablas-figuras-pies/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `workflow-maestro-academico-editorial` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`gestor-tablas-figuras-pies/SKILL.md`](../../gestor-tablas-figuras-pies/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
