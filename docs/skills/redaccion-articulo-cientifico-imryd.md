# Redaccion Articulo Cientifico Imryd

Redacta, estructura, diagnostica y revisa artículos científicos de alto nivel con lógica IMRyD/IMRAD: título, resumen, palabras clave, introducción, métodos, resultados, discusión, conclusiones, limitaciones, tablas, figuras, citas, respuesta a revisores y adecuación a normas de revista. Use when Codex needs to convert tesis, informes, resultados de investigación, capítulos o borradores en artículos publicables; planificar un paper desde cero; auditar coherencia científica; preparar manuscritos para envío; o coordinar esta tarea con editor-en-jefe, gestores de referencias APA7/IEEE, revisor de resumen/abstract, tablas/figuras, humanización académica y respuesta a observaciones.

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
