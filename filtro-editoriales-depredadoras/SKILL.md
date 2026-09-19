---
name: filtro-editoriales-depredadoras
description: Úsalo como filtro auxiliar antes de buscar, descargar, citar o validar fuentes académicas, cuando sea necesario evitar revistas, editoriales, congresos, plataformas o sitios clonados potencialmente depredadores, espurios o de reputación dudosa. Aplica especialmente en búsquedas bibliográficas APA 7, IEEE, revisión de bibliografía, selección de revistas, verificación de DOI, acceso abierto, indexación real, Scopus/WoS/DOAJ/SciELO/Redalyc/Latindex y evaluación de fuentes de América Latina, el Caribe e Iberoamérica.
---

# Filtro De Editoriales Depredadoras

Los generadores de informes y perfiles exigen `--overwrite` para reemplazar salidas existentes, nunca entradas. Requieren `workflow-maestro-academico-editorial/scripts/archivos_seguros.py`, también en ejecución directa. Consultar [protección y límites de escritura](../workflow-maestro-academico-editorial/references/portabilidad.md#protección-de-informes).

## Objetivo

Este skill actúa como una barrera de calidad antes de descargar, citar o aceptar una fuente. Su función es detectar señales de revista, editorial, congreso, plataforma o sitio clonado potencialmente depredador, sin convertir una lista de alerta en una acusación automática.

## Regla central

Antes de usar una fuente bibliográfica, verifica tres capas:

1. DOI verificable y texto completo accesible.
2. Reputación editorial de la revista, editorial o plataforma.
3. Coherencia entre sitio oficial, ISSN, indexación, política editorial, revisión por pares, APC, preservación y comité editorial.

Si una fuente falla en DOI/acceso o cae en nivel rojo por reputación editorial, no la descargues ni la cites salvo instrucción explícita del usuario.

## Cuándo activarlo

Actívalo dentro de:

- `$gestor-referencias-academicas`
- `$gestor-referencias-academicas`
- `$revisor-citas-consistencia-bibliografica`
- `$ajustes-editoriales-bibliograficos`
- `$workflow-maestro-academico-editorial`

También úsalo cuando el usuario pregunte si una revista, editorial, congreso o fuente es confiable.

## Flujo de verificación

1. Identifica el nombre exacto de la revista, editorial, congreso o plataforma.
2. Extrae ISSN, eISSN, DOI, URL oficial, editorial, país y base donde aparece.
3. Ejecuta si conviene el script local:
   `python skills/filtro-editoriales-depredadoras/scripts/check_editorial_risk.py "<nombre>"`
4. Revisa coincidencias en la lista local de alerta.
5. Verifica directamente, cuando sea posible, en fuentes externas confiables:
   DOAJ, SciELO, Redalyc, Latindex Catálogo 2.0, Scopus Sources, Web of Science Master Journal List, COPE/OASPA y sitio oficial de la revista.
6. Evalúa señales de riesgo mediante `references/criterios-verificacion.md`.
7. Clasifica la fuente como verde, amarillo o rojo.
8. Usa fuentes verdes. Usa fuentes amarillas solo si son imprescindibles y con nota de cautela. Descarta fuentes rojas.

## Clasificación

### Verde

Puede usarse si además cumple DOI y acceso completo.

- Indexación verificable en bases reconocidas.
- DOI resuelve correctamente y coincide con título, revista y editorial.
- Sitio oficial claro, HTTPS, ISSN verificable y políticas editoriales completas.
- Revisión por pares descrita, comité editorial trazable, APC transparente.

### Amarillo

No usar como primera opción. Requiere verificación adicional.

- Revista descontinuada en Scopus o con historial editorial irregular.
- Indexación declarada pero no confirmada directamente.
- APC, revisión por pares, comité editorial o preservación poco claros.
- Sitio regional legítimo pero con información incompleta.
- Nombre parecido a una revista legítima o riesgo de sitio clonado.

### Rojo

Descartar antes de descargar o citar.

- Aparece en una lista de alerta reconocida o en la lista local del proyecto con estado rojo.
- Tiene caso legal, sanción, sentencia o historial documentado de prácticas engañosas.
- Usa métricas falsas, indexación falsa, revisión por pares garantizada o aceptación acelerada.
- El sitio suplanta una revista legítima o no corresponde al ISSN oficial.
- La fuente no tiene DOI verificable o no permite acceso completo.

## Salida esperada

Cuando audites una fuente, entrega:

- clasificación: verde, amarillo o rojo
- evidencia consultada
- decisión: usar, usar con cautela, reemplazar o descartar
- motivo breve
- alternativa de búsqueda si se descarta

## Validación final

Antes de cerrar:

- no se citó ninguna fuente roja
- las fuentes amarillas quedaron justificadas o reemplazadas
- toda fuente usada tiene DOI verificable y texto completo accesible
- no se confundió revista regional de acceso abierto legítimo con publicación depredadora
- no se acusó una editorial o revista sin evidencia documental

## Referencias de apoyo

- Para criterios y fuentes de verificación: lee [references/criterios-verificacion.md](references/criterios-verificacion.md).
- Para la lista local resumida del proyecto: lee [references/lista-alerta-local.md](references/lista-alerta-local.md).
- Para coincidencias rápidas por nombre: usa [scripts/check_editorial_risk.py](scripts/check_editorial_risk.py).
- Para revisar lotes de revistas/editoriales/congresos: usa `scripts/check_editorial_risk.py --file fuentes.txt --out riesgo.md --json-out riesgo.json`.
