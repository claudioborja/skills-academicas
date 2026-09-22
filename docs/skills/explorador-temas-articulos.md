# Explorador de Temas para Artículos

Explora, clasifica y propone temas de artículos científicos a partir de literatura, resultados bibliográficos, PDFs convertidos, matrices de fuentes o notas de estado del arte. Usar para mapear estudios similares, distinguir originales de revisiones, detectar vacíos, agrupar temas, orientar el tipo de estudio o guía de reporte, preparar insumos preliminares de búsqueda y cribado, construir matrices y generar tablas o visualizaciones antes de transferir el trabajo a la skill metodológica o de redacción responsable. No gobierna una revisión PRISMA ni Kitchenham.

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
- Herramientas automatizadas
- Insumos Recomendados
- Metodologias Estandarizadas
- Busqueda Sistematica
- Conexiones

## Recursos incluidos

### Herramientas automatizadas

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
