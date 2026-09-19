# Conexiones Con Otras Skills

## Regla

Esta skill gobierna la forma científica del artículo. Las demás skills complementan tareas específicas sin desplazar la lógica IMRyD.

## Workflow Maestro

Usar `$workflow-maestro-academico-editorial` cuando:
- el usuario no tenga clara la etapa del manuscrito;
- el material venga de tesis, libro o informe y haya que decidir qué conservar;
- el proyecto requiera ruta por fases;
- haya que coordinar marco teórico, referencias, revisión y cierre.

Después del diagnóstico, volver a esta skill para convertir la ruta en arquitectura de artículo.

## Referencias Y Citas

Usar `$gestor-referencias-academicas` cuando:
- el usuario pida IEEE;
- la revista pertenezca a ingeniería, computación, tecnología o áreas que exijan citación numérica;
- el manuscrito use citas como `[1]`, `[4], [13]`.

Usar `$gestor-referencias-academicas` cuando:
- la revista pida autor-fecha;
- el área sea educación, ciencias sociales, psicología, gestión o humanidades aplicadas.

Usar `$revisor-citas-consistencia-bibliografica` antes de entrega para verificar que toda cita tenga referencia, toda referencia esté citada y DOI/URLs no se alteren.

Usar `$filtro-editoriales-depredadoras` si se va a elegir revista, buscar fuentes o evaluar reputación editorial.

## Resumen Y Abstract

Usar `$revisor-resumen-abstract-palabras-clave` cuando:
- el artículo ya tenga resultados claros;
- se necesite resumen estructurado o no estructurado;
- haya que adaptar palabras clave a tesauros o vocabulario de la revista.

## Tablas Y Figuras

Usar `$gestor-tablas-figuras-pies` cuando:
- existan tablas/figuras;
- haya duplicación entre texto y tabla;
- falten títulos, notas, fuentes o unidades;
- se necesite numeración y llamada en texto.

## Humanización Y Estilo

Usar `$humanizar-redaccion-academica` cuando el manuscrito esté científicamente armado pero suene mecánico, repetitivo o demasiado genérico. Proteger siempre citas, DOI, datos, tablas, nombres de instrumentos y resultados numéricos.

## Respuesta A Revisores

Usar `$respondedor-observaciones-academicas` cuando existan dictámenes, comentarios de pares, editor o comité. Mantener una matriz: comentario, decisión, cambio realizado, ubicación en manuscrito y respuesta redactada.
