# Auditoria de automatizacion de skills

Registro de mantenimiento de las automatizaciones existentes. Consultarlo al revisar cobertura o evolución de herramientas; no es un paso obligatorio del flujo editorial ni un certificado de validación vigente.

## Objetivo

Reducir consumo de tokens delegando tareas mecanicas a scripts locales: conversion documental, segmentacion, proteccion de bloques, auditoria bibliografica, inventario documental, exploracion de temas, propuesta de articulos, visualizacion y revision IMRyD.

## Automatizaciones implementadas

| Skill | Scripts | Funcion |
| --- | --- | --- |
| `preprocesador-documentos` | `documento_a_markdown.py`, `segmentar_manuscrito.py`, `proteger_bloques.py` | Convierte PDF/DOCX/HTML/TXT/MD, segmenta manuscritos y detecta bloques protegidos. |
| `automatizador-referencias` | `doi_a_referencia.py`, `auditar_citas_bibliografia.py`, `inventario_fuentes.py`, `normalizar_referencias.py` | Audita citas, DOI, bibliografia y fuentes descargadas. |
| `auditor-documental-academico` | `inventariar_documento.py`, `inventariar_tablas_figuras.py`, `auditar_terminologia.py`, `check_preentrega.py`, `analizar_repeticiones.py` | Inventaria estructura, tablas, figuras, terminos, preentrega y repeticiones. |
| `auditor-articulo-imryd` | `auditar_imryd.py`, `matriz_objetivo_metodo_resultados.py`, `check_envio_revista.py` | Audita estructura IMRyD, alineacion y checklist de envio a revista. |
| `maquetacion-academica-preentrega` | `markdown_a_txt_final.py` | Convierte entregas finales Markdown a TXT limpio sin marcas de estilo; para libros produce `libro_completo.txt`. |
| `humanizar-redaccion-academica` | `analizar_marcas_ia.py`, `analizar_reporte_compilatio.py`, `documento_a_perfil_estilo.py`, `comparar_con_perfil_estilo.py`, `perfilar_y_comparar_estilo.py` | Detecta marcas mecanicas, interpreta reportes de similitud/IA, extrae perfil de estilo desde PDF/DOCX/MD/TXT/HTML, guarda cada estilo en `styles/<nombre>` dentro del skill y compara borradores contra la voz objetivo sin alterar citas o fuentes. |
| `explorador-temas-articulos` | `generar_protocolo_revision.py`, `cribar_fuentes_revision.py`, `clasificar_literatura.py`, `matriz_estado_arte.py`, `proponer_temas.py`, `seleccionar_metodologia.py`, `tabular_visualizar.py` | Genera protocolo y cadenas de busqueda, deduplica y criba fuentes con conteos tipo PRISMA, clasifica literatura, separa originales/revisiones, agrupa similares, detecta vacios, vincula PRISMA/STROBE/CONSORT/COREQ/SRQR y otras guias, propone temas y genera tablas/graficos. |
| `respondedor-observaciones-academicas` | `observaciones_a_matriz.py` | Convierte observaciones dispersas en matriz de respuesta. |
| `filtro-editoriales-depredadoras` | `check_editorial_risk.py --file` | Revisa riesgo editorial por nombre individual o lote. |
| `gestor-referencias-academicas` | `pdf_a_contexto.py --profile fuente|imryd|tesis` | Extrae contexto compacto de PDFs con perfiles de lectura. |

## Flujo recomendado

1. Si llega PDF/DOCX/HTML/TXT/MD largo: usar `$preprocesador-documentos`.
2. Si se busca tema de articulo, similares, vacios, lineas posibles, revision con trazabilidad PRISMA o metodologia estandarizada: usar `$explorador-temas-articulos`.
3. Si ya hay literatura o fuentes: usar `$automatizador-referencias` y `$filtro-editoriales-depredadoras`.
4. Si ya hay manuscrito convertido: usar `$auditor-documental-academico`.
5. Si el producto sera articulo cientifico: usar `$auditor-articulo-imryd` y luego `$redaccion-articulo-cientifico-imryd`.
6. Si hay que reducir prosa mecanica o alinear una voz con documentos modelo: usar `$humanizar-redaccion-academica`.
7. Si hay libro o manuscrito final en Markdown: usar `$maquetacion-academica-preentrega` para generar `.txt` limpio.
8. Si hay observaciones: usar `$respondedor-observaciones-academicas`.

## Estado

Actualización de portabilidad: usar `editor-en-jefe/scripts/ejecutar.py` y las instrucciones de [portabilidad](portabilidad.md) para Linux, Windows y macOS. El preprocesador comparte una implementación Python y ofrece lanzadores POSIX y PowerShell. Los entornos virtuales se separan por plataforma, arquitectura y versión de Python; no forman parte del código portable. Las comprobaciones locales no equivalen a ejecución nativa en los tres sistemas.

- Implementado y probado con archivos de muestra.
- Todas las skills principales validan con `quick_validate.py`.
- Los scripts Python compilan.
- Las rutas son portables dentro de `skills/`.

## Nota sobre visualizacion

`explorador-temas-articulos/scripts/tabular_visualizar.py` genera siempre CSV, JSON y Markdown. Genera PNG si `matplotlib` esta instalado; si no, deja advertencia y conserva las tablas.
