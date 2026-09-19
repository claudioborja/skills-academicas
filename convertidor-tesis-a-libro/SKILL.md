---
name: convertidor-tesis-a-libro
description: Úsalo cuando el usuario necesite transformar una tesis, tesina, trabajo de grado, disertación, informe de investigación o manuscrito universitario en un libro académico, divulgativo o profesional. Aplica para diagnosticar marcas de tesis, rediseñar índice, convertir objetivos e hipótesis en promesa editorial, adaptar marco teórico y metodología, reubicar resultados, crear capítulos legibles, eliminar lenguaje de tribunal/universidad, preparar prólogo, introducción, conclusiones, glosario, bibliografía, tablas, figuras y plan de publicación sin perder rigor ni alterar citas textuales, datos, fuentes o evidencias.
---

# Convertidor Tesis A Libro

## Objetivo

Convertir una tesis escrita en un manuscrito de libro publicable. La transformación no es cosmética: cambia lector, propósito, arquitectura, voz, ritmo y aparato paratextual, conservando el rigor académico y la trazabilidad de fuentes.

## Regla Central

No borrar evidencia ni cambiar resultados para que el texto "parezca libro". Reubicar, resumir o explicar los componentes académicos según su función editorial.

No parafrasear citas textuales, transcripciones, datos, tablas de resultados, instrumentos, referencias, DOI ni fragmentos normativos. Si un pasaje es evidencia o cita literal, se conserva o se marca para decisión del usuario.

## Diagnóstico Inicial

Antes de reescribir, identificar:

- tipo de tesis: grado, maestría, doctorado, informe técnico, estudio de caso, investigación aplicada;
- público del futuro libro: estudiantes, docentes, profesionales, público general, especialistas;
- tipo de libro: manual, monografía, libro de texto, ensayo académico, guía aplicada, divulgación técnica;
- partes aprovechables: marco teórico, resultados, discusión, instrumentos, tablas, casos, conclusiones;
- partes que deben transformarse: planteamiento del problema, objetivos, hipótesis, justificación, metodología, defensa institucional;
- restricciones: norma de citas, confidencialidad, permisos de reproducción, datos personales, derechos de autor.

Para manuscritos largos, ejecutar `scripts/diagnosticar_tesis.py` sobre el archivo fuente.

## Flujo De Transformación

1. Inventariar la estructura original de la tesis.
2. Detectar marcas universitarias que no pertenecen al libro.
3. Definir el lector y la promesa editorial.
4. Convertir el índice de tesis en índice de libro.
5. Reubicar metodología, resultados y anexos según su utilidad.
6. Reescribir introducciones y transiciones para lector de libro.
7. Revisar citas, tablas, figuras, permisos y bibliografía.
8. Aplicar continuidad, humanización académica y corrección final.
9. Preparar preliminares y cierre editorial.

Si el usuario pide solo diagnóstico, no reescribir todavía: entregar mapa de conversión y prioridades.

## Qué Cambiar

### Marcas De Tesis

Transformar o eliminar:

- "La presente investigación...";
- "El objetivo general...";
- "Los objetivos específicos...";
- "La hipótesis planteada...";
- "Se justifica porque...";
- "Capítulo I: Planteamiento del problema";
- "Capítulo II: Marco teórico";
- "Capítulo III: Metodología";
- "Capítulo IV: Resultados";
- "Trabajo presentado para optar...";
- menciones a tutor, tribunal, institución o requisitos de grado, salvo en agradecimientos si el usuario los conserva.

### Arquitectura

Una tesis suele organizarse por exigencia metodológica. Un libro debe organizarse por progresión de lectura.

Convertir:

- problema de investigación -> pregunta editorial o necesidad del lector;
- objetivo general -> propósito del libro;
- objetivos específicos -> promesas de capítulos;
- hipótesis -> tesis argumental o eje interpretativo;
- marco teórico -> capítulo conceptual o hilo distribuido;
- metodología -> nota metodológica, anexo o sección breve;
- resultados -> capítulos analíticos, casos o hallazgos;
- discusión -> interpretación editorial;
- conclusiones -> cierre, recomendaciones o agenda de trabajo.

### Voz

Sustituir el tono de defensa por tono de acompañamiento editorial:

- de "se realizó una investigación" a "este libro examina";
- de "la población objeto de estudio" a "el grupo analizado";
- de "los resultados obtenidos evidencian" a "los hallazgos muestran";
- de "en cumplimiento de los objetivos" a "este recorrido permite observar".

## Qué Conservar

- hallazgos y datos;
- citas y fuentes;
- instrumentos si son útiles;
- tablas o figuras con valor explicativo;
- definiciones técnicas;
- delimitaciones metodológicas necesarias;
- advertencias éticas o legales;
- anexos relevantes para reproducibilidad.

## Criterios De Decisión

Usar `references/mapa-transformacion.md` para decidir qué hacer con cada sección de tesis.

Usar `references/marcas-de-tesis.md` cuando el texto conserva lenguaje universitario o defensivo.

Usar otros skills del workflow después de esta conversión:

- `$gestor-continuidad-libro` para coherencia entre capítulos;
- `$revisor-citas-consistencia-bibliografica` para citas y bibliografía;
- `$gestor-tablas-figuras-pies` para aparato visual;
- `$humanizar-redaccion-academica` para naturalidad;
- `$correccion-estilo-ortotipografica` para cierre editorial;
- `$maquetacion-academica-preentrega` antes de exportar.

## Salida Esperada

Según el pedido, entregar:

- diagnóstico de conversión;
- índice editorial propuesto;
- tabla "tesis -> libro";
- lista de secciones que se conservan, se resumen, se mueven o se eliminan;
- capítulos reescritos;
- preliminares de libro;
- plan de revisión final.

## Validación Final

Comprobar:

- el libro ya no se lee como documento presentado a un tribunal;
- la metodología queda proporcionada al lector;
- los resultados no pierden trazabilidad;
- las citas y datos se conservan;
- el índice tiene progresión editorial;
- el tono es académico, claro y publicable;
- no se inventó contenido para completar el libro.
