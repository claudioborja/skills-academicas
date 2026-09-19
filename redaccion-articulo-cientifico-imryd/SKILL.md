---
name: redaccion-articulo-cientifico-imryd
description: "Redacta, estructura, diagnostica y revisa artículos científicos de alto nivel con lógica IMRyD/IMRAD: título, resumen, palabras clave, introducción, métodos, resultados, discusión, conclusiones, limitaciones, tablas, figuras, citas, respuesta a revisores y adecuación a normas de revista. Use when Codex needs to convert tesis, informes, resultados de investigación, capítulos o borradores en artículos publicables; planificar un paper desde cero; auditar coherencia científica; preparar manuscritos para envío; o coordinar esta tarea con workflow-maestro-academico-editorial, gestores de referencias APA7/IEEE, revisor de resumen/abstract, tablas/figuras, humanización académica y respuesta a observaciones."
---

# Redacción Artículo Científico IMRyD

## Objetivo

Guiar la construcción de artículos científicos publicables con estructura IMRyD/IMRAD y criterios editoriales de revista. Coordinarse con las otras skills académicas cuando el trabajo necesite planificación general, citas, tablas, resumen, revisión de estilo, respuesta a pares o control bibliográfico.

## Regla Central

No inventar datos, resultados, fuentes, tamaño muestral, instrumentos, análisis estadísticos, aprobación ética ni hallazgos. Si falta información empírica, señalar el vacío y proponer una forma precisa de obtenerla o redactar con alcance limitado.

## Activación Operativa

Usar esta skill como skill principal cuando el producto final sea un artículo científico, aunque el material de origen sea una tesis, informe, base de datos, capítulo o borrador narrativo.

Si el usuario aún está definiendo el tema o comparando artículos similares, activar antes `$explorador-temas-articulos` para clasificar literatura, separar originales/revisiones, detectar vacíos y proponer preguntas investigables.

Si el usuario pide una ruta completa, activar primero `$workflow-maestro-academico-editorial` para diagnosticar etapa y luego volver a esta skill para la arquitectura de artículo.

Si el usuario entrega un artículo ya escrito, activar primero `$auditor-articulo-imryd` para detectar secciones faltantes, señales de objetivo, método, resultados, discusión, limitaciones y checklist de envío.

Si el usuario pide citas, bibliografía o normas de revista:
- usar `$automatizador-referencias` para auditoría mecánica de citas, DOI y referencias antes de aplicar estilo;
- usar `$gestor-referencias-academicas` cuando la revista, área o usuario pida IEEE;
- usar `$gestor-referencias-academicas` cuando la revista, área o usuario pida APA 7;
- usar `$revisor-citas-consistencia-bibliografica` antes de entrega;
- usar `$ajustes-editoriales-bibliograficos` si la revista impone reglas propias.

## Flujo De Trabajo

1. Diagnosticar el tipo de artículo: original empírico, revisión, estudio de caso, comunicación breve, ensayo científico, artículo metodológico o artículo derivado de tesis.
2. Identificar revista, audiencia, idioma, norma bibliográfica, límite de palabras y estructura requerida. Si falta revista, trabajar con IMRyD estándar y dejar advertencia.
3. Construir la pregunta, brecha, objetivo y contribución. No redactar resultados sin datos verificables.
4. Diseñar el mapa IMRyD:
   - Introducción: problema, literatura crítica, brecha, objetivo e hipótesis/pregunta.
   - Métodos: diseño, muestra/corpus, instrumentos, procedimiento, análisis, ética y reproducibilidad.
   - Resultados: hallazgos ordenados por pregunta/objetivo, tablas/figuras y datos sin interpretación excesiva.
   - Discusión: interpretación, comparación con literatura, contribución, implicaciones, limitaciones y futuras líneas.
5. Revisar resumen, título y palabras clave al final, no al inicio, salvo que el usuario pida un esquema preliminar.
6. Coordinar citas, tablas, figuras, estilo y respuesta a revisores con las skills correspondientes.
7. Cerrar con checklist de envío y riesgos pendientes.

## Criterios De Calidad

Exigir alineación entre pregunta, objetivo, método, resultados y discusión. Si una sección promete algo que otra no cumple, marcarlo como inconsistencia.

Separar con claridad:
- resultado observado;
- interpretación del resultado;
- comparación con estudios previos;
- implicación práctica o teórica;
- limitación real del estudio.

Evitar afirmaciones infladas como "se demuestra", "se comprueba definitivamente" o "impacto significativo" si el diseño y los datos no lo sostienen.

## Coordinación Con Otras Skills

Leer `references/conexiones-skills.md` cuando la tarea requiera citas IEEE/APA, conversión desde tesis, revisión de abstract, tablas/figuras, respuesta a pares o humanización del manuscrito.

Leer `references/estructura-imryd.md` cuando se vaya a planificar, redactar o revisar secciones IMRyD.

Leer `references/checklist-envio.md` antes de entregar un manuscrito final, una carta al editor o una respuesta a revisores.

## Antes de redactar: guia metodologica

Identificar primero el método activo. Si el proyecto usa `$revision-sistematica-kitchenham`, conservar su protocolo, criterios y trazabilidad; esta skill organiza el informe sin generar protocolo, cribado ni conteos PRISMA. La ruta general siguiente se aplica solo cuando es compatible con el método elegido.

Si el usuario aun define tema, tipo de articulo o guia internacional, usar `$explorador-temas-articulos` antes de escribir el manuscrito. Ejecutar `seleccionar_metodologia.py` cuando haya corpus o clasificacion previa, y alinear la estructura IMRyD con la guia que corresponda: PRISMA/PRISMA-ScR para revisiones, STROBE para observacionales, CONSORT 2025 para ensayos, COREQ/SRQR para cualitativos, STARD para diagnosticos, TRIPOD para modelos predictivos, CARE para casos, SPIRIT o PRISMA-P para protocolos.

Para articulos de revision, no redactar como PRISMA/PRISMA-ScR sin protocolo y cribado trazable. Pedir o generar con `$explorador-temas-articulos` el protocolo de busqueda, las cadenas por base, la matriz de cribado, las razones de exclusion y los conteos tipo PRISMA antes de escribir metodos y resultados.

## Salida Esperada

Según el pedido, entregar uno de estos productos:
- diagnóstico del manuscrito y ruta de trabajo;
- esquema IMRyD comentado;
- redacción o reescritura de secciones;
- resumen/abstract y palabras clave;
- tabla de correspondencia objetivo-método-resultados-discusión;
- checklist de envío;
- respuesta técnica a observaciones de revisores.

Al finalizar, indicar brevemente qué quedó listo, qué información falta y qué skill complementaria conviene activar si aplica.
