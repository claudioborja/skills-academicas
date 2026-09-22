# Producción editorial integrada

Aplicar al producir libros completos. En intervenciones parciales, conservar el alcance solicitado. Objetivo: entregar una obra completa que haya pasado los controles editoriales pertinentes, reduciendo tiempo y tokens mediante reutilización, sin reducir rigor, profundidad, cobertura ni revisión visual.

## Contrato de entrega

Registrar en el estado existente lector, índice, alcance, profundidad, norma, formato y requisitos del destino editorial cuando se conozcan. Sin destino identificado, usar el perfil acordado y declarar ese límite; no detener decisiones reversibles. La entrega incluye manuscrito completo, DOCX editable cuando se solicite Word, recursos integrados, bibliografía y controles resueltos. Mantener decisiones, pendientes e informes fuera del cuerpo publicable. No garantizar aceptación por una editorial o por pares.

## Unidad de producción

Trabajar por capítulos o secciones con argumento completo. Antes de redactar, reunir función del bloque, evidencia pertinente con localizadores, términos acordados y relación con capítulos vecinos. Redactar con profundidad y revisar respaldo, coherencia y estilo en la misma intervención. Activar una especialidad adicional solo ante una necesidad concreta; no encadenar reescrituras integrales por rutina. Marcar un capítulo como revisado únicamente después de comprobar esos aspectos, con referencia a su versión.

Mantener un registro breve único de decisiones, estado de capítulos y controles. Los informes especializados se producen cuando hacen falta, sin duplicar el mismo estado en matrices y resúmenes. Reutilizar comprobaciones vigentes; un cambio de fuente, afirmación, contexto, estructura o formato invalida los controles afectados. Revisar también las dependencias: conclusiones, glosario, citas, referencias cruzadas y capítulos relacionados.

## Evidencia y contexto

Consultar primero fuentes y extracciones existentes. Reutilizar una extracción solo si coinciden el hash del original y las opciones/versión del extractor; comprobar legibilidad y conservar páginas y secciones. Leer el pasaje con contexto suficiente, ampliando al método, resultados, limitaciones, tablas o figuras cuando la interpretación lo requiera. No sustituir el original por resúmenes, similitud o fragmentos aislados.

Registrar fuente, archivo/hash, afirmación, pasaje/localizador, alcance, límites, decisión y usos. Una fuente admitida no valida cualquier afirmación. Reutilizar una evidencia revisada para el mismo alcance, sin exigir aprobación del usuario por cada cita salvo que el encargo o protocolo la requiera. Kitchenham conserva sus controles de selección y revisión manual.

Usar registros existentes en Markdown/JSON o SQLite si hay una herramienta disponible y verificada. La búsqueda textual, filtros y sinónimos pueden recuperar candidatos; los embeddings son opcionales. No instalar una base vectorial ni introducir llamadas adicionales a modelos por defecto. La colección no incorpora por esta instrucción un motor SQLite/RAG ni una caché automática: no afirmar que existen sin implementación y ejecución comprobadas.

## Tiempo y tokens

Ejecutar controles mecánicos con scripts; leer resúmenes de incidencias y abrir los pasajes afectados en vez de volcar archivos completos repetidamente. Cargar solo las referencias de skills pertinentes. No reducir el manuscrito, omitir fuentes contradictorias ni saltar controles para ajustar consumo.

Evaluar cambios de flujo con tareas comparables, mismo alcance, materiales, profundidad y criterios de calidad. Contabilizar tiempo total y tokens de entrada/salida de todas las llamadas, incluidas recuperación asistida, revisiones, reintentos y preparación amortizada. Si no hay telemetría, declarar consumo no medido: menos archivos o menos llamadas no demuestran ahorro. Admitir una optimización como verificada solo con tiempo menor, tokens totales no superiores y calidad sin deterioro en respaldo, localizadores, cobertura, coherencia y presentación. Si no se cumplen las tres condiciones, corregir o retirar esa optimización; no rebajar el estándar.

## Cierre de la obra

Conservar una revisión global del libro integrado: progresión, contradicciones, repeticiones, profundidad, conclusiones, terminología y correspondencia de citas. Verificar recursos, permisos y requisitos editoriales. Exportar, renderizar y revisar la presentación completa; tras correcciones, inspeccionar páginas afectadas y efectos de repaginación. Los controles mecánicos complementan el juicio editorial.

Si faltan evidencias, permisos o revisiones sustantivas, entregar el estado real como borrador con pendientes; no etiquetar como listo para publicación. Si los controles se completaron, informar qué se verificó y para qué perfil, sin trasladar al usuario tareas editoriales ya incluidas en el encargo ni prometer aprobación externa.
