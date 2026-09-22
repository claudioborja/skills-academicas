# Redacción Artículo Científico IMRyD

Redacta, estructura, diagnostica y revisa artículos científicos de alto nivel con lógica IMRyD o IMRAD: título, resumen, palabras clave, introducción, métodos, resultados, discusión, conclusiones, limitaciones, tablas, figuras, citas, respuesta a revisores y adecuación a las normas de la revista. Usar cuando Codex necesite convertir tesis, informes, resultados de investigación, capítulos o borradores en artículos publicables; planificar un artículo desde cero; auditar la coherencia científica; preparar manuscritos para envío; o coordinar esta tarea con editor-en-jefe, los gestores de referencias APA 7 o IEEE, el revisor de resúmenes y palabras clave, el gestor de tablas y figuras, la humanización académica y la respuesta a observaciones.

## Uso

Invócala directamente con `$redaccion-articulo-cientifico-imryd` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $redaccion-articulo-cientifico-imryd para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Objetivo
- Regla Central
- Activación Operativa
- Flujo De Trabajo
- Criterios De Calidad
- Coordinación Con Otras Skills
- Antes de redactar: guia metodologica
- Salida Esperada

## Recursos incluidos

### Referencias

- [`references/checklist-envio.md`](../../redaccion-articulo-cientifico-imryd/references/checklist-envio.md)
- [`references/conexiones-skills.md`](../../redaccion-articulo-cientifico-imryd/references/conexiones-skills.md)
- [`references/estructura-imryd.md`](../../redaccion-articulo-cientifico-imryd/references/estructura-imryd.md)

### Configuración de interfaz

- [`agents/openai.yaml`](../../redaccion-articulo-cientifico-imryd/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `editor-en-jefe` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`redaccion-articulo-cientifico-imryd/SKILL.md`](../../redaccion-articulo-cientifico-imryd/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
