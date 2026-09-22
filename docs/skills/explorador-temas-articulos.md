# Explorador Temas Articulos

Explora, clasifica y propone temas de articulos cientificos a partir de literatura, resultados bibliograficos, PDFs convertidos, matrices de fuentes o notas de estado del arte. Use when Codex needs to investigar lineas posibles, mapear articulos similares, distinguir estudios originales de revisiones, detectar vacios, agrupar temas, seleccionar metodologias estandarizadas como PRISMA/STROBE/CONSORT/COREQ/SRQR, generar protocolo de busqueda sistematica, crear cadenas reproducibles, deduplicar y cribar fuentes con conteos tipo PRISMA, combinar resultados preliminares, construir matrices de estado del arte, priorizar preguntas investigables, o generar tablas y visualizaciones Python antes de pasar a redaccion-articulo-cientifico-imryd, gestor-marco-teorico-estado-del-arte, automatizador-referencias o editor-en-jefe.

## Uso

Invócala directamente con `$explorador-temas-articulos` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $explorador-temas-articulos para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Ejecución multiplataforma
- Objetivo
- Regla Central
- Flujo
- Scripts
- Insumos Recomendados
- Metodologias Estandarizadas
- Busqueda Sistematica
- Conexiones

## Recursos incluidos

### Scripts

- [`scripts/clasificar_literatura.py`](../../explorador-temas-articulos/scripts/clasificar_literatura.py)
- [`scripts/common.py`](../../explorador-temas-articulos/scripts/common.py)
- [`scripts/cribar_fuentes_revision.py`](../../explorador-temas-articulos/scripts/cribar_fuentes_revision.py)
- [`scripts/generar_protocolo_revision.py`](../../explorador-temas-articulos/scripts/generar_protocolo_revision.py)
- [`scripts/matriz_estado_arte.py`](../../explorador-temas-articulos/scripts/matriz_estado_arte.py)
- [`scripts/proponer_temas.py`](../../explorador-temas-articulos/scripts/proponer_temas.py)
- [`scripts/requirements-graficos-lock.txt`](../../explorador-temas-articulos/scripts/requirements-graficos-lock.txt)
- [`scripts/seleccionar_metodologia.py`](../../explorador-temas-articulos/scripts/seleccionar_metodologia.py)
- [`scripts/tabular_visualizar.py`](../../explorador-temas-articulos/scripts/tabular_visualizar.py)

### Referencias

- [`references/busqueda-sistematica.md`](../../explorador-temas-articulos/references/busqueda-sistematica.md)
- [`references/criterios-propuesta.md`](../../explorador-temas-articulos/references/criterios-propuesta.md)
- [`references/metodologias-estandarizadas.md`](../../explorador-temas-articulos/references/metodologias-estandarizadas.md)

### Configuración de interfaz

- [`agents/openai.yaml`](../../explorador-temas-articulos/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `editor-en-jefe` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`explorador-temas-articulos/SKILL.md`](../../explorador-temas-articulos/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
