# Busqueda Sistematica Y Trazabilidad

## Objetivo

Convertir una busqueda bibliografica de calidad en un proceso reproducible para revisiones sistematicas, scoping reviews, revisiones integrativas o estados del arte con criterios explicitos.

## Flujo Minimo

1. Definir pregunta de revision y tipo de revision.
2. Definir marco de pregunta: PICO/PICOS, PECO, PCC, SPIDER u otro.
3. Registrar bases consultadas, fecha de busqueda, idiomas, rango temporal y tipos de documento.
4. Construir cadenas de busqueda con terminos principales, sinonimos y operadores booleanos.
5. Exportar resultados a CSV/JSON/RIS/BibTeX cuando sea posible.
6. Cribar registros por titulo/resumen con criterios de inclusion/exclusion.
7. Deduplicar por DOI y por titulo normalizado.
8. Registrar razones de exclusion.
9. Leer texto completo de los candidatos incluidos.
10. Generar matriz y conteos preliminares; si PRISMA está activo, transferirlos a `$revision-sistematica-prisma` para distinguir rutas, validar el flujo y completar el checklist oficial.

## Criterios De Calidad Base

- DOI verificable cuando el area lo permita.
- Texto completo accesible.
- Revista, editorial, congreso o plataforma sin alerta roja.
- Pertinencia con pregunta, poblacion/contexto, concepto/intervencion y tipo de evidencia.
- Preferencia por articulos revisados por pares, revisiones sistematicas, metaanalisis y estudios primarios pertinentes.

## No Confundir

- Una busqueda de fuentes para respaldar afirmaciones no equivale a una revision sistematica.
- PRISMA guía el reporte, no reemplaza el método de conducción. La skill `$revision-sistematica-prisma` gobierna su aplicación y extensiones.
- Si no hay busqueda exhaustiva ni cribado trazable, usar "revision narrativa", "revision integrativa" o "estado del arte" con transparencia.

## Evidencias Que Debe Dejar El Agente

- Protocolo o plan de busqueda.
- Cadenas por base de datos.
- Archivo de resultados brutos o matriz inicial.
- Matriz cribada con decision y razon.
- Conteos trazables de registros, informes y estudios, sin confundir esas unidades.
- Lista final de fuentes incluidas y fuentes excluidas principales.
