---
name: convertidor-tesis-a-libro
description: Úsalo cuando el usuario necesite transformar una tesis, tesina, trabajo de grado, disertación, informe de investigación o manuscrito universitario en un libro académico, divulgativo o profesional. Aplica para diagnosticar marcas de tesis, rediseñar índice, convertir objetivos e hipótesis en promesa editorial, adaptar marco teórico y metodología, reubicar resultados, crear capítulos legibles, eliminar lenguaje de tribunal/universidad, preparar prólogo, introducción, conclusiones, glosario, bibliografía, tablas, figuras y plan de publicación sin perder rigor ni alterar citas textuales, datos, fuentes o evidencias.
---

# Convertidor Tesis A Libro

## Objetivo

Convertir una tesis escrita en un manuscrito de libro académico publicable. La transformación no es cosmética: cambia lector, propósito, arquitectura, voz, ritmo y aparato paratextual, conservando el rigor académico y la trazabilidad de fuentes. El libro debe desarrollar una sola propuesta central derivada de la tesis; no debe ser una compilación de temas cercanos ni reproducir la secuencia de capítulos universitarios.

## Regla Central

No borrar evidencia ni cambiar resultados para que el texto "parezca libro". Reubicar, resumir o explicar los componentes académicos según su función editorial.

No parafrasear citas textuales, transcripciones, datos, tablas de resultados, instrumentos, referencias, DOI ni fragmentos normativos. Si un pasaje es evidencia o cita literal, se conserva o se marca para decisión del usuario.

No convertir, resumir ni suprimir una tabla, figura, anexo, cita extensa o dato identificable sin registrar su procedencia, su destino editorial y la aprobación necesaria. Una síntesis narrativa nunca reemplaza el original: conserva la tabla o figura fuente, o una referencia verificable a ella.

No crear capítulos solo porque sean afines al tema. Todo capítulo debe declarar qué parte de la pregunta, tesis argumental, hallazgo, caso o evidencia de la investigación desarrolla. Si la tesis no lo respalda y el usuario no autoriza una ampliación con fuentes nuevas, no incorporarlo.

## Diagnóstico Inicial

Antes de reescribir, identificar:

- tipo de tesis: grado, maestría, doctorado, informe técnico, estudio de caso, investigación aplicada;
- público del futuro libro: estudiantes, docentes, profesionales, público general, especialistas;
- tipo de libro: manual, monografía, libro de texto, ensayo académico, guía aplicada, divulgación técnica;
- partes aprovechables: marco teórico, resultados, discusión, instrumentos, tablas, casos, conclusiones;
- partes que deben transformarse: planteamiento del problema, objetivos, hipótesis, justificación, metodología, defensa institucional;
- restricciones: norma de citas, confidencialidad, permisos de reproducción, datos personales, derechos de autor.
- núcleo del libro: pregunta editorial, tesis argumental y aportación basada en los hallazgos;
- mapa de evidencia: qué datos, resultados, casos y fuentes de la tesis sostienen cada capítulo;
- alcance material: extensión solicitada, formato de publicación y contenido disponible para sostenerla.

Para DOCX, PDF, HTML o manuscritos extensos, usar primero `$preprocesador-documentos` para obtener Markdown, inventario y bloques protegidos; conservar el original. Ejecutar `scripts/diagnosticar_tesis.py` sobre el Markdown o TXT resultante. El script no interpreta el diseño ni el contenido interno de DOCX/PDF: sus conteos son señales, no decisiones editoriales.

## Flujo De Transformación

1. Inventariar la estructura original, incluidos anexos, tablas, figuras y bloques protegidos.
2. Detectar marcas universitarias y registrar sus ubicaciones; no decidir solo por frecuencia.
3. Definir lector, tipo de libro y promesa editorial.
4. Formular la tesis argumental del libro y comprobar que procede de la evidencia disponible.
5. Diseñar el mapa capítulo -> pregunta -> evidencia antes de reescribir.
6. Elaborar y validar la matriz de conversión y el presupuesto de extensión antes de reescribir.
7. Convertir el índice de tesis en índice de libro, con progresión acumulativa.
8. Reubicar metodología, resultados y anexos según su utilidad, sin aislar los datos en un único capítulo cuando sostienen argumentos posteriores.
9. Resolver antes de publicar los permisos, confidencialidad, datos personales y atribuciones pendientes.
10. Reescribir introducciones y transiciones para lector de libro.
11. Aplicar continuidad, humanización académica y corrección final.
12. Preparar preliminares y cierre editorial.

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

Usar `references/arquitectura-libro-derivado.md` al proponer un índice, distribuir resultados entre capítulos o planificar un libro de más de 100 páginas.

La matriz de conversión debe incluir, como mínimo: ubicación o sección de origen, función en la tesis, tratamiento, destino en el libro, evidencia que debe preservarse, estado de permisos/confidencialidad y la decisión o aprobación pendiente. No reescribir elementos con riesgo pendiente como si estuvieran autorizados.

El mapa de evidencia por capítulo debe indicar: propósito del capítulo, vínculo con la tesis argumental, material de origen, datos/hallazgos/casos que lo sostienen y su transición al siguiente capítulo. Un capítulo de contexto puede no repetir cifras, pero debe explicar qué problema o interpretación de la evidencia habilita; no puede quedar desconectado del núcleo investigado.

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
- arquitectura argumental y mapa de evidencia por capítulo;
- tabla "tesis -> libro";
- matriz de conversión trazable, con decisiones pendientes claramente separadas;
- presupuesto de extensión por capítulo cuando se solicite una longitud objetivo;
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
- cada transformación de evidencia, tabla, figura o anexo conserva origen y decisión editorial;
- no quedan permisos, atribuciones, datos personales o confidencialidad sin resolver en el material destinado a publicación.
- todos los capítulos desarrollan la misma tesis argumental y tienen una relación explícita con evidencia, hallazgos o casos de la investigación;
- los datos no quedan relegados a un único capítulo si fundamentan interpretaciones o aplicaciones posteriores;
- la extensión solicitada se sostiene con contenido planificado y verificable, sin relleno ni temas externos no autorizados.
