# Explorador de Temas para Artículos

Explora, clasifica y propone temas de artículos científicos a partir de literatura, resultados bibliográficos, PDFs convertidos, matrices de fuentes o notas de estado del arte. Usar para mapear estudios similares, distinguir originales de revisiones, detectar vacíos, agrupar temas, orientar el tipo de estudio o guía de reporte, preparar insumos preliminares de búsqueda y cribado, construir matrices y generar tablas o visualizaciones antes de transferir el trabajo a la skill metodológica o de redacción responsable. No gobierna una revisión PRISMA ni Kitchenham.

## Ejemplo de uso

```text
Usa $explorador-temas-articulos para clasificar literatura, mapear similares, detectar vacíos y proponer temas de artículos.
```

## Guía operativa

Los generadores de informes y perfiles exigen `--overwrite` para reemplazar salidas existentes, nunca entradas. Requieren `editor-en-jefe/scripts/archivos_seguros.py`, también en ejecución directa. Consultar [protección y límites de escritura](../../editor-en-jefe/references/portabilidad.md#protección-de-informes).

### Ejecución multiplataforma

Consultar [la guía común de ejecución](../../editor-en-jefe/references/portabilidad.md) para elegir intérprete y preparar dependencias.

### Objetivo

Si ya existe un protocolo Kitchenham, usar esta skill únicamente para clasificar literatura, explorar vocabulario y tabular. No ejecutar su selector metodológico, generador de protocolo ni cribado sobre ese proyecto. El protocolo aprobado gobierna las decisiones de selección.

Si el proyecto se reportará con PRISMA, usar esta skill solo para exploración preliminar y transferir protocolo, búsqueda, cribado, conteos y checklist a `$revision-sistematica-prisma`. Sus scripts no certifican cumplimiento PRISMA.

Apoyar la fase previa a la redaccion de articulos: convertir una coleccion de fuentes o notas en un mapa de temas, tipos de estudio, similitudes, vacios, propuestas investigables y metodologias estandarizadas aplicables.

### Regla Central

No presentar las propuestas como conclusiones definitivas. Los scripts producen hipotesis de organizacion, priorizacion y seleccion metodologica; el agente debe verificar fuentes, DOI, pertinencia, lectura completa e instrucciones de la revista antes de recomendar un tema final.

### Flujo

1. Preparar insumos con `$preprocesador-documentos`, `$automatizador-referencias` o busquedas bibliograficas.
2. Orientar la metodología o guía de reporte candidata: PRISMA 2020, PRISMA-ScR, STROBE, CONSORT 2025, COREQ/SRQR, STARD, TRIPOD, CARE, SPIRIT o PRISMA-P.
3. Si será una revisión PRISMA, transferir la decisión y los insumos a `$revision-sistematica-prisma`; para Kitchenham, transferir a su skill exclusiva.
4. Generar borradores de protocolo, cadenas, deduplicación o cribado solo como insumos preliminares, con criterios explícitos y sin declarar cumplimiento metodológico.
5. Clasificar literatura en original, revision, metodologico, caso, teorico u otro.
6. Construir matriz de estado del arte: tema, enfoque, metodo, poblacion/contexto, resultados, vacio.
7. Proponer temas y preguntas investigables segun frecuencia, novedad, vacios, factibilidad y compatibilidad metodologica.
8. Generar tablas y visualizaciones para comparar lineas, anos, tipos de estudio y grupos tematicos.
9. Pasar el corpus incluido a `$redaccion-articulo-cientifico-imryd` o `$gestor-marco-teorico-estado-del-arte`.

### Herramientas automatizadas

#### Clasificar Literatura

```text
python skills/editor-en-jefe/scripts/ejecutar.py explorador-temas-articulos/scripts/clasificar_literatura.py fuentes.csv --out clasificacion.md --json-out clasificacion.json --csv-out clasificacion.csv
```

Clasifica documentos por tipo y tema probable usando titulo, resumen, palabras clave y fuente.

#### Matriz Estado Del Arte

```text
python skills/editor-en-jefe/scripts/ejecutar.py explorador-temas-articulos/scripts/matriz_estado_arte.py clasificacion.csv --out matriz.md --json-out matriz.json --csv-out matriz.csv
```

Agrupa literatura por tema y tipo de estudio, y produce vacios probables.

#### Seleccionar Metodologia

```text
python skills/editor-en-jefe/scripts/ejecutar.py explorador-temas-articulos/scripts/seleccionar_metodologia.py clasificacion.csv --out metodologia.md --json-out metodologia.json
```

Orienta una metodología o guía de reporte según el corpus o el objetivo. La recomendación debe ser confirmada por la skill especializada. Acepta `--goal revision`, `--goal scoping`, `--goal metaanalisis`, `--goal observacional`, `--goal ensayo`, `--goal cualitativo`, `--goal diagnostico`, `--goal predictivo`, `--goal caso` o `--goal protocolo`.

#### Generar Protocolo De Revision

```text
python skills/editor-en-jefe/scripts/ejecutar.py explorador-temas-articulos/scripts/generar_protocolo_revision.py --topic "tema" --question "pregunta" --methodology revision_sistematica --concepts "termino 1; termino 2" --contexts "contexto" --years 2020-2026 --out protocolo.md --json-out protocolo.json
```

Genera un borrador de protocolo, criterios y cadenas por base de datos. Para PRISMA o PRISMA-ScR, someter ese borrador a `$revision-sistematica-prisma` antes de ejecutar o declarar conformidad.

#### Cribar Fuentes De Revision

```text
python skills/editor-en-jefe/scripts/ejecutar.py explorador-temas-articulos/scripts/cribar_fuentes_revision.py registros.csv --include-terms "concepto; contexto" --year-min 2020 --require-doi --require-full-text --exclude-red --out cribado.md --json-out cribado.json --csv-out cribado.csv
```

Deduplica por DOI/título, aplica filtros mecánicos, registra razones y produce conteos preliminares. No sustituye el cribado humano protocolizado ni el diagrama oficial; `$revision-sistematica-prisma` valida el flujo cuando esa guía está activa.

#### Proponer Temas

```text
python skills/editor-en-jefe/scripts/ejecutar.py explorador-temas-articulos/scripts/proponer_temas.py matriz.csv --out propuestas.md --json-out propuestas.json
```

Sugiere temas, preguntas, tipo de articulo recomendado y siguientes pasos.

#### Tabular Y Visualizar

```text
python skills/editor-en-jefe/scripts/ejecutar.py explorador-temas-articulos/scripts/tabular_visualizar.py clasificacion.csv --out-dir graficos --prefix exploracion
```

Genera tablas CSV y graficos PNG. Usa `matplotlib` si esta instalado; si no, conserva tablas CSV y reporta la dependencia.

Para reconstruir el perfil gráfico validado, usar `scripts/requirements-graficos-lock.txt` en un entorno aislado Python 3.12+; incluye dependencias transitivas. No se instala al preparar la base PDF/Word. Consultar [perfiles y límites](../../editor-en-jefe/references/portabilidad.md#dependencias-fijadas).

### Insumos Recomendados

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

### Metodologias Estandarizadas

Leer `references/metodologias-estandarizadas.md` para orientar el tipo de producto. Si la decisión es PRISMA, continuar con `$revision-sistematica-prisma` y sus fuentes oficiales.

### Busqueda Sistematica

Leer `references/busqueda-sistematica.md` para preparar vocabulario, cadenas o matrices preliminares. La conducción y documentación PRISMA pertenecen a `$revision-sistematica-prisma`.

### Conexiones

Leer `references/criterios-propuesta.md` antes de recomendar temas finales. Usar `$filtro-editoriales-depredadoras` y `$automatizador-referencias` para verificar fuentes antes de citar o tomar decisiones. Si el resultado sera manuscrito, entregar junto al tema una recomendacion metodologica para `$redaccion-articulo-cientifico-imryd`.

## Recursos incluidos

### Herramientas automatizadas

| Recurso | Función |
| --- | --- |
| [`scripts/clasificar_literatura.py`](../../explorador-temas-articulos/scripts/clasificar_literatura.py) | Recurso auxiliar: Clasificar literatura. |
| [`scripts/common.py`](../../explorador-temas-articulos/scripts/common.py) | Recurso auxiliar: Common. |
| [`scripts/cribar_fuentes_revision.py`](../../explorador-temas-articulos/scripts/cribar_fuentes_revision.py) | Recurso auxiliar: Cribar fuentes revision. |
| [`scripts/generar_protocolo_revision.py`](../../explorador-temas-articulos/scripts/generar_protocolo_revision.py) | Recurso auxiliar: Generar protocolo revision. |
| [`scripts/matriz_estado_arte.py`](../../explorador-temas-articulos/scripts/matriz_estado_arte.py) | Recurso auxiliar: Matriz estado arte. |
| [`scripts/proponer_temas.py`](../../explorador-temas-articulos/scripts/proponer_temas.py) | Recurso auxiliar: Proponer temas. |
| [`scripts/requirements-graficos-lock.txt`](../../explorador-temas-articulos/scripts/requirements-graficos-lock.txt) | Dependencias Python fijadas para esta herramienta. |
| [`scripts/seleccionar_metodologia.py`](../../explorador-temas-articulos/scripts/seleccionar_metodologia.py) | Recurso auxiliar: Seleccionar metodologia. |
| [`scripts/tabular_visualizar.py`](../../explorador-temas-articulos/scripts/tabular_visualizar.py) | Recurso auxiliar: Tabular visualizar. |

### Referencias

| Recurso | Función |
| --- | --- |
| [`references/busqueda-sistematica.md`](../../explorador-temas-articulos/references/busqueda-sistematica.md) | Busqueda Sistematica Y Trazabilidad |
| [`references/criterios-propuesta.md`](../../explorador-temas-articulos/references/criterios-propuesta.md) | Criterios Para Proponer Temas |
| [`references/metodologias-estandarizadas.md`](../../explorador-temas-articulos/references/metodologias-estandarizadas.md) | Metodologias Estandarizadas Para Elegir Diseno Y Guia De Reporte |

### Configuración de interfaz

| Recurso | Función |
| --- | --- |
| [`agents/openai.yaml`](../../explorador-temas-articulos/agents/openai.yaml) | Metadatos de interfaz e invocación de la skill. |

## Fuente normativa

Esta ficha se genera desde [`explorador-temas-articulos/SKILL.md`](../../explorador-temas-articulos/SKILL.md), que permanece como contrato normativo. Regenera la ficha después de modificar ese archivo.
