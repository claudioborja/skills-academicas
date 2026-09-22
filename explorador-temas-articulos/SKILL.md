---
name: explorador-temas-articulos
description: "Explora, clasifica y propone temas de articulos cientificos a partir de literatura, resultados bibliograficos, PDFs convertidos, matrices de fuentes o notas de estado del arte. Use when Codex needs to investigar lineas posibles, mapear articulos similares, distinguir estudios originales de revisiones, detectar vacios, agrupar temas, seleccionar metodologias estandarizadas como PRISMA/STROBE/CONSORT/COREQ/SRQR, generar protocolo de busqueda sistematica, crear cadenas reproducibles, deduplicar y cribar fuentes con conteos tipo PRISMA, combinar resultados preliminares, construir matrices de estado del arte, priorizar preguntas investigables, o generar tablas y visualizaciones Python antes de pasar a redaccion-articulo-cientifico-imryd, gestor-marco-teorico-estado-del-arte, automatizador-referencias o editor-en-jefe."
---

# Explorador Temas Articulos

Los generadores de informes y perfiles exigen `--overwrite` para reemplazar salidas existentes, nunca entradas. Requieren `editor-en-jefe/scripts/archivos_seguros.py`, también en ejecución directa. Consultar [protección y límites de escritura](../editor-en-jefe/references/portabilidad.md#protección-de-informes).

## Ejecución multiplataforma

Consultar [la guía común de ejecución](../editor-en-jefe/references/portabilidad.md) para elegir intérprete y preparar dependencias.

## Objetivo

Si ya existe un protocolo Kitchenham, usar esta skill únicamente para clasificar literatura, explorar vocabulario y tabular. No ejecutar su selector metodológico, generador de protocolo ni cribado PRISMA sobre ese proyecto. El protocolo aprobado gobierna las decisiones de selección.

Apoyar la fase previa a la redaccion de articulos: convertir una coleccion de fuentes o notas en un mapa de temas, tipos de estudio, similitudes, vacios, propuestas investigables y metodologias estandarizadas aplicables.

## Regla Central

No presentar las propuestas como conclusiones definitivas. Los scripts producen hipotesis de organizacion, priorizacion y seleccion metodologica; el agente debe verificar fuentes, DOI, pertinencia, lectura completa e instrucciones de la revista antes de recomendar un tema final.

## Flujo

1. Preparar insumos con `$preprocesador-documentos`, `$automatizador-referencias` o busquedas bibliograficas.
2. Seleccionar metodologia o guia de reporte estandarizada cuando corresponda: PRISMA 2020, PRISMA-ScR, STROBE, CONSORT 2025, COREQ/SRQR, STARD, TRIPOD, CARE, SPIRIT o PRISMA-P.
3. Si sera revision sistematica/scoping/integrativa, generar protocolo y cadenas de busqueda reproducibles.
4. Cribar y deduplicar registros con criterios explicitos, registrando razones de exclusion y conteos tipo PRISMA.
5. Clasificar literatura en original, revision, metodologico, caso, teorico u otro.
6. Construir matriz de estado del arte: tema, enfoque, metodo, poblacion/contexto, resultados, vacio.
7. Proponer temas y preguntas investigables segun frecuencia, novedad, vacios, factibilidad y compatibilidad metodologica.
8. Generar tablas y visualizaciones para comparar lineas, anos, tipos de estudio y grupos tematicos.
9. Pasar el corpus incluido a `$redaccion-articulo-cientifico-imryd` o `$gestor-marco-teorico-estado-del-arte`.

## Scripts

### Clasificar Literatura

```text
python skills/editor-en-jefe/scripts/ejecutar.py explorador-temas-articulos/scripts/clasificar_literatura.py fuentes.csv --out clasificacion.md --json-out clasificacion.json --csv-out clasificacion.csv
```

Clasifica documentos por tipo y tema probable usando titulo, resumen, palabras clave y fuente.

### Matriz Estado Del Arte

```text
python skills/editor-en-jefe/scripts/ejecutar.py explorador-temas-articulos/scripts/matriz_estado_arte.py clasificacion.csv --out matriz.md --json-out matriz.json --csv-out matriz.csv
```

Agrupa literatura por tema y tipo de estudio, y produce vacios probables.

### Seleccionar Metodologia

```text
python skills/editor-en-jefe/scripts/ejecutar.py explorador-temas-articulos/scripts/seleccionar_metodologia.py clasificacion.csv --out metodologia.md --json-out metodologia.json
```

Recomienda una metodologia o guia de reporte estandarizada segun el corpus o el objetivo. Acepta `--goal revision`, `--goal scoping`, `--goal metaanalisis`, `--goal observacional`, `--goal ensayo`, `--goal cualitativo`, `--goal diagnostico`, `--goal predictivo`, `--goal caso` o `--goal protocolo`.

### Generar Protocolo De Revision

```text
python skills/editor-en-jefe/scripts/ejecutar.py explorador-temas-articulos/scripts/generar_protocolo_revision.py --topic "tema" --question "pregunta" --methodology revision_sistematica --concepts "termino 1; termino 2" --contexts "contexto" --years 2020-2026 --out protocolo.md --json-out protocolo.json
```

Genera protocolo, criterios de inclusion/exclusion y cadenas reproducibles por base de datos. Usar antes de declarar PRISMA, PRISMA-ScR o cualquier revision trazable.

### Cribar Fuentes De Revision

```text
python skills/editor-en-jefe/scripts/ejecutar.py explorador-temas-articulos/scripts/cribar_fuentes_revision.py registros.csv --include-terms "concepto; contexto" --year-min 2020 --require-doi --require-full-text --exclude-red --out cribado.md --json-out cribado.json --csv-out cribado.csv
```

Deduplica por DOI/titulo, aplica criterios mecanicos de inclusion/exclusion, registra razones y produce conteos tipo PRISMA para identificacion, duplicados, cribado, exclusion y elegibilidad.

### Proponer Temas

```text
python skills/editor-en-jefe/scripts/ejecutar.py explorador-temas-articulos/scripts/proponer_temas.py matriz.csv --out propuestas.md --json-out propuestas.json
```

Sugiere temas, preguntas, tipo de articulo recomendado y siguientes pasos.

### Tabular Y Visualizar

```text
python skills/editor-en-jefe/scripts/ejecutar.py explorador-temas-articulos/scripts/tabular_visualizar.py clasificacion.csv --out-dir graficos --prefix exploracion
```

Genera tablas CSV y graficos PNG. Usa `matplotlib` si esta instalado; si no, conserva tablas CSV y reporta la dependencia.

Para reconstruir el perfil gráfico validado, usar `scripts/requirements-graficos-lock.txt` en un entorno aislado Python 3.12+; incluye dependencias transitivas. No se instala al preparar la base PDF/Word. Consultar [perfiles y límites](../editor-en-jefe/references/portabilidad.md#dependencias-fijadas).

## Insumos Recomendados

Preferir CSV con columnas:
- `title`
- `abstract`
- `year`
- `doi`
- `source`
- `keywords`
- `method`
- `population`
- `findings`

Si solo hay Markdown o TXT, el script extrae registros por encabezados o lineas con DOI/titulo probable.

## Metodologias Estandarizadas

Leer `references/metodologias-estandarizadas.md` cuando el usuario pida vincular el tema con PRISMA, revisiones sistematicas, scoping reviews, estudios originales, ensayos, cualitativos, diagnosticos, predictivos, protocolos o guias internacionales de uso comun.

## Busqueda Sistematica

Leer `references/busqueda-sistematica.md` cuando el usuario pida completar una revision metodologica, dejar trazabilidad PRISMA, construir cadenas de busqueda, deduplicar resultados, cribar fuentes o registrar razones de exclusion.

## Conexiones

Leer `references/criterios-propuesta.md` antes de recomendar temas finales. Usar `$filtro-editoriales-depredadoras` y `$automatizador-referencias` para verificar fuentes antes de citar o tomar decisiones. Si el resultado sera manuscrito, entregar junto al tema una recomendacion metodologica para `$redaccion-articulo-cientifico-imryd`.
