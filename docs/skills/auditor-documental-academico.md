# Auditor Documental Académico

Inventaria y audita mecánicamente documentos académicos o editoriales para reducir la lectura manual: estructura, encabezados, extensión por sección, tablas, figuras, citas, bibliografía, terminología, anexos y lista de comprobación de preentrega. Usar cuando Codex necesite preparar informes compactos para editor-en-jefe, convertidor-tesis-a-libro, redaccion-articulo-cientifico-imryd, gestor-tablas-figuras-pies, normalizador-terminologia-glosario o maquetacion-academica-preentrega.

## Ejemplo de uso

```text
Usa $auditor-documental-academico para inventariar estructura, tablas, figuras, terminología y preentrega.
```

## Guía operativa

### Ejecución multiplataforma

Consultar [la guía común de ejecución](../../editor-en-jefe/references/portabilidad.md) para elegir intérprete y preparar dependencias.

### Objetivo

Generar inventarios compactos para que el agente no tenga que leer un manuscrito completo antes de decidir qué corregir, reordenar o revisar.

### Herramientas automatizadas

```text
python skills/editor-en-jefe/scripts/ejecutar.py auditor-documental-academico/scripts/inventariar_documento.py manuscrito.md --out inventario.md --json-out inventario.json
python skills/editor-en-jefe/scripts/ejecutar.py auditor-documental-academico/scripts/inventariar_tablas_figuras.py manuscrito.md --out visual.md --json-out visual.json
python skills/editor-en-jefe/scripts/ejecutar.py auditor-documental-academico/scripts/auditar_terminologia.py manuscrito.md --terms "aprendizaje automático" "machine learning" --out terminos.md --json-out terminos.json
python skills/editor-en-jefe/scripts/ejecutar.py auditor-documental-academico/scripts/check_preentrega.py manuscrito.md --out preentrega.md --json-out preentrega.json
python skills/editor-en-jefe/scripts/ejecutar.py auditor-documental-academico/scripts/check_preentrega.py manuscrito.md --estructura indice-autorizado.md --out preentrega.md --json-out preentrega.json
python skills/editor-en-jefe/scripts/ejecutar.py auditor-documental-academico/scripts/analizar_repeticiones.py manuscrito.md --out repeticiones.md --json-out repeticiones.json
```

### Uso

Interpretar los reportes como inventarios y alertas heurísticas. No certifican exhaustividad, respaldo bibliográfico ni calidad editorial. Revisar manualmente los hallazgos y las secciones relevantes; la ausencia de una coincidencia no demuestra una omisión.

Ejecutar después de `$preprocesador-documentos` cuando el documento ya esté en Markdown o texto plano. Usar los reportes para decidir si conviene activar tablas/figuras, terminología, preentrega, coherencia o redacción.

En libros, usar `--estructura` con el índice Markdown autorizado cuando exista. El control detecta encabezados no previstos, rótulos operativos filtrados al manuscrito, casillas, cercas de código, marcadores de trabajo, niveles saltados y títulos duplicados. Sus alertas no deciden por sí solas si un subtítulo legítimo debe eliminarse: revisarlas antes de corregir.

## Recursos incluidos

### Herramientas automatizadas

| Recurso | Función |
| --- | --- |
| [`scripts/analizar_repeticiones.py`](../../auditor-documental-academico/scripts/analizar_repeticiones.py) | Recurso auxiliar: Analizar repeticiones. |
| [`scripts/auditar_terminologia.py`](../../auditor-documental-academico/scripts/auditar_terminologia.py) | Recurso auxiliar: Auditar terminologia. |
| [`scripts/check_preentrega.py`](../../auditor-documental-academico/scripts/check_preentrega.py) | Recurso auxiliar: Check preentrega. |
| [`scripts/inventariar_documento.py`](../../auditor-documental-academico/scripts/inventariar_documento.py) | Recurso auxiliar: Inventariar documento. |
| [`scripts/inventariar_tablas_figuras.py`](../../auditor-documental-academico/scripts/inventariar_tablas_figuras.py) | Recurso auxiliar: Inventariar tablas figuras. |

### Referencias

| Recurso | Función |
| --- | --- |
| [`references/criterios.md`](../../auditor-documental-academico/references/criterios.md) | Criterios |

### Pruebas

| Recurso | Función |
| --- | --- |
| [`tests/test_preentrega.py`](../../auditor-documental-academico/tests/test_preentrega.py) | Recurso auxiliar: Test preentrega. |

### Configuración de interfaz

| Recurso | Función |
| --- | --- |
| [`agents/openai.yaml`](../../auditor-documental-academico/agents/openai.yaml) | Metadatos de interfaz e invocación de la skill. |

## Fuente normativa

Esta ficha se genera desde [`auditor-documental-academico/SKILL.md`](../../auditor-documental-academico/SKILL.md), que permanece como contrato normativo. Regenera la ficha después de modificar ese archivo.
