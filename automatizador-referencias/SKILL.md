---
name: automatizador-referencias
description: "Automatiza tareas mecánicas de citas, DOI, bibliografía y fuentes descargadas para reducir consumo de tokens. Use when Codex needs to auditar citas APA/IEEE frente a bibliografía, detectar DOI faltantes o repetidos, consultar metadatos DOI en Crossref, inventariar PDFs/HTML/Markdown de referencias, normalizar entradas bibliográficas preliminares, o preparar insumos para gestor-referencias-academicas, revisor-citas-consistencia-bibliografica, filtro-editoriales-depredadoras y editor-en-jefe."
---

# Automatizador Referencias

Los generadores de informes y perfiles exigen `--overwrite` para reemplazar salidas existentes, nunca entradas. Requieren `editor-en-jefe/scripts/archivos_seguros.py`, también en ejecución directa. Consultar [protección y límites de escritura](../editor-en-jefe/references/portabilidad.md#protección-de-informes).

## Ejecución multiplataforma

Consultar [la guía común de ejecución](../editor-en-jefe/references/portabilidad.md) para elegir intérprete y preparar dependencias.

## Objetivo

Delegar en scripts las tareas repetibles de referencias: detectar citas, separar bibliografía, extraer DOI, consultar metadatos, inventariar fuentes y producir reportes compactos.

## Regla Central

No inventar metadatos. Si DOI, año, autores, revista, volumen, número o páginas no son verificables, marcar `pendiente` y dejar que la skill bibliográfica especializada decida.

## Scripts

### DOI A Referencia

```text
python skills/editor-en-jefe/scripts/ejecutar.py automatizador-referencias/scripts/doi_a_referencia.py 10.xxxx/xxxxx --style apa --out refs.md --json-out refs.json
```

Acepta uno o varios DOI. Consulta Crossref si hay red; si falla, conserva el DOI y marca metadatos pendientes.

La salida es preliminar en ambas normas. IEEE genera borradores de artículos de revista; otros tipos y datos esenciales incompletos quedan pendientes sin aplicarles una plantilla errónea. Revisar abreviatura oficial, versión/fecha, mes, autoría y localizadores. `borrador` no equivale a cumplimiento; `pendiente` exige completar o seleccionar el modelo adecuado. El año de depósito del DOI no se usa como año de publicación.

### Auditoría De Citas Y Bibliografía

```text
python skills/editor-en-jefe/scripts/ejecutar.py automatizador-referencias/scripts/auditar_citas_bibliografia.py manuscrito.md --out auditoria.md --json-out auditoria.json
```

Detecta citas numéricas, citas APA probables, referencias finales, DOI, citas sin referencia y referencias no citadas.

Para una obra completa IEEE añadir `--style ieee --strict`: reconoce localizadores, alerta de rangos comprimidos, orden incorrecto y números duplicados; devuelve 1 si hay errores mecánicos. Sin `--strict` conserva salida 0 para generar informes. No renumera ni borra fuentes. Requiere sección explícita Referencias/References/Bibliografía; si falta, avisa y no infiere bibliografía de citas del cuerpo. Fragmentos, expresiones matemáticas y encabezados no estándar requieren revisión. Siempre informa alcance parcial.

### Inventario De Fuentes

```text
python skills/editor-en-jefe/scripts/ejecutar.py automatizador-referencias/scripts/inventario_fuentes.py referencias-descargadas --recursive --out fuentes.md --json-out fuentes.json
```

Lista archivos fuente, tamaño, extensión, DOI probable y decisión inicial.

### Normalizar Referencias

```text
python skills/editor-en-jefe/scripts/ejecutar.py automatizador-referencias/scripts/normalizar_referencias.py bibliografia.md --out normalizadas.md --json-out normalizadas.json
```

Limpia espacios, detecta estilo probable, DOI y duplicados exactos.

La detección de duplicados compara DOI normalizado o texto sin el número inicial. Es una señal para revisión, no deduplicación destructiva ni comprobación semántica de versiones.

## Salida Esperada

Usar los reportes como insumo para `$gestor-referencias-academicas` o `$revisor-citas-consistencia-bibliografica`. El agente debe leer primero advertencias, faltantes y tablas compactas, no la bibliografía completa.
