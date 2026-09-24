# Auditor Artículo IMRyD

Extrae secciones, fragmentos y señales mecánicas de artículos IMRyD para orientar una revisión científica. Usar para elaborar un inventario estructural y una lista de comprobación previa al envío; sus herramientas automatizadas no prueban la coherencia entre objetivo, método y resultados ni la suficiencia de la evidencia.

## Ejemplo de uso

```text
Usa $auditor-articulo-imryd para revisar estructura IMRyD, alineación objetivo-método-resultados y checklist de envío.
```

## Guía operativa

### Ejecución multiplataforma

Consultar [la guía común de ejecución](../../editor-en-jefe/references/portabilidad.md) para elegir intérprete y preparar dependencias.

### Objetivo

Producir un diagnóstico rápido de estructura científica antes de redactar, reordenar o enviar un artículo.

### Herramientas automatizadas

```text
python skills/editor-en-jefe/scripts/ejecutar.py auditor-articulo-imryd/scripts/auditar_imryd.py articulo.md --out imryd.md --json-out imryd.json
python skills/editor-en-jefe/scripts/ejecutar.py auditor-articulo-imryd/scripts/matriz_objetivo_metodo_resultados.py articulo.md --out matriz.md --json-out matriz.json
python skills/editor-en-jefe/scripts/ejecutar.py auditor-articulo-imryd/scripts/check_envio_revista.py articulo.md --out envio.md --json-out envio.json
```

### Uso

Las expresiones regulares identifican encabezados y palabras, no relaciones científicas. "No detectado" significa ausencia de una coincidencia, no ausencia demostrada de contenido. Comprobar manualmente los pasajes antes de concluir desalineación, falta de evidencia o aptitud para envío. La matriz es una extracción de candidatos, no una evaluación semántica.

Ejecutar después de `$preprocesador-documentos`. Usar el reporte para orientar `$redaccion-articulo-cientifico-imryd` y evitar que el agente lea todo el artículo si solo necesita saber qué sección falla.

## Recursos incluidos

### Herramientas automatizadas

| Recurso | Función |
| --- | --- |
| [`scripts/auditar_imryd.py`](../../auditor-articulo-imryd/scripts/auditar_imryd.py) | Recurso auxiliar: Auditar imryd. |
| [`scripts/check_envio_revista.py`](../../auditor-articulo-imryd/scripts/check_envio_revista.py) | Recurso auxiliar: Check envio revista. |
| [`scripts/matriz_objetivo_metodo_resultados.py`](../../auditor-articulo-imryd/scripts/matriz_objetivo_metodo_resultados.py) | Recurso auxiliar: Matriz objetivo metodo resultados. |

### Referencias

| Recurso | Función |
| --- | --- |
| [`references/criterios.md`](../../auditor-articulo-imryd/references/criterios.md) | Criterios IMRyD |

### Configuración de interfaz

| Recurso | Función |
| --- | --- |
| [`agents/openai.yaml`](../../auditor-articulo-imryd/agents/openai.yaml) | Metadatos de interfaz e invocación de la skill. |

## Fuente normativa

Esta ficha se genera desde [`auditor-articulo-imryd/SKILL.md`](../../auditor-articulo-imryd/SKILL.md), que permanece como contrato normativo. Regenera la ficha después de modificar ese archivo.
