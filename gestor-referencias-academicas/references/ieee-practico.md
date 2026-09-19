# IEEE: citas y referencias

Guía operativa para el perfil IEEE, no sustituto de la guía oficial ni certificación de cumplimiento. Si el encargo incluye un artículo completo, leer [presentación IEEE](../../maquetacion-academica-preentrega/references/ieee-presentacion.md). Registrar revista/conferencia, plantilla, idioma y excepciones institucionales; no confundir citas IEEE en una tesis con maquetación para una publicación IEEE.

## Citas numéricas

- Numerar por primera aparición y reutilizar el identificador de la misma obra, aunque cambie la página citada. Una entrada por número, sin agrupar varias obras distintas.
- Corchetes en la línea del texto, antes de la puntuación: `… como se demuestra [1].`
- Varias fuentes: `[1], [3], [7]`. La guía oficial consultada indica enumerar también las consecutivas: `[4], [5], [6]`, no `[4]–[6]`. Conservar un rango solo si el destino exige explícitamente otra convención y documentarlo.
- Mención narrativa opcional: `Smith [1]`, `Smith and Jones [2]`; con tres o más nombres, `Smith et al. [3]`. En prosa española adaptar el conector narrativo; no sustituir por autor-fecha.
- Localizadores: `[4, p. 27]`, `[4, pp. 27–29]`, `[4, Sec. IV]`, `[4, eq. (2)]`, `[4, Fig. 1]`, `[4, Ch. 2, pp. 5–10]`. No crear entradas distintas para páginas distintas. No inventar paginación.
- Evitar `ibid.` y `op. cit.`: reutilizar el número con el localizador pertinente.
- Renumerar solo dentro de una intervención autorizada y coordinando citas, lista, tablas, figuras y apéndices. No corregir aisladamente un fragmento como si fuera la obra completa.
- Verificar correspondencia texto/lista. Las entradas no citadas son señales para revisar según destino, no permiso para borrarlas automáticamente.
- Cita literal: verificar texto y localizador, distinguir de paráfrasis y cumplir límites de reproducción. No importar el umbral APA de 40 palabras como regla universal IEEE; consultar la publicación para bloques textuales.

## Autoría y datos

- Iniciales antes del apellido y orden publicado. Conservar apellidos compuestos, sufijos y autores corporativos.
- Hasta seis autores: todos; con más de seis: primer autor y `et al.`. En salida para IEEE en inglés, usar `and` antes del último cuando se enumeran varios. No confundir esta regla con la abreviación de nombres mencionados en el cuerpo.
- No inventar autores ausentes ni asumir que un sitio es autor. Revisar el modelo sin autor o institucional aplicable.
- Año/mes: fecha de publicación pertinente; una fecha de creación o depósito de DOI no es evidencia de publicación. Artículos early access y versión asignada a volumen pueden requerir fechas distintas.
- Títulos de artículos/capítulos entre comillas; revista, libro y actas según el modelo en cursiva. Usar abreviatura oficial de la revista o conferencia; no fabricar abreviaturas.
- Distinguir `p.`, `pp.` y `Art. no.`. No convertir un identificador de artículo en páginas.
- DOI en la forma `doi: 10.…` conforme al modelo. Las referencias terminan en punto, incluidas las que terminan en DOI; las terminadas en URL no llevan punto final.
- Recursos web: aplicar el modelo con autor/entidad, título, sitio, fecha y fecha real de acceso cuando corresponda, `[Online]. Available:` y URL. No inventar fechas.
- DOI, acceso abierto, antigüedad y reputación son controles distintos del formato. La ausencia de DOI no invalida por sí sola una referencia IEEE.
- Lista ordenada numéricamente, no alfabéticamente. Los números entre corchetes quedan en columna propia; alinear el texto de las entradas con sangría colgante según plantilla.

## Modelos y variantes

Esquemas ficticios en inglés para publicaciones IEEE. Sustituir solo con datos verificados. DOI/URL representan enlaces reales, no texto literal. Para adaptación institucional española, elegir un idioma de etiquetas y registrarlo; no mezclar `en`, `in`, `Disponible` y `Available` arbitrariamente.

| Tipo | Esquema |
|---|---|
| Artículo | [1] A. Author and B. Author, “Article title,” *Abbrev. Journal*, vol. 10, no. 2, pp. 45–60, Feb. 2023, doi: DOI. |
| Número de artículo | [2] A. Author, “Title,” *Abbrev. Journal*, vol. 10, no. 2, Feb. 2023, Art. no. e123, doi: DOI. |
| Actas publicadas | [3] A. Author, “Paper title,” in *Proc. Abbrev. Conf.*, City, Country, 2023, pp. 11–18, doi: DOI. |
| Ponencia sin actas | [4] A. Author, “Title,” presented at the Conf. Name, City, Country, fecha verificable. |
| Libro | [5] A. Author, *Book Title*, 2nd ed. City, Country: Publisher, 2023. |
| Capítulo editado | [6] A. Author, “Chapter title,” in *Book Title*, B. Editor, Ed. City, Country: Publisher, 2023, pp. 20–35. |
| Tesis | [7] A. Author, “Title,” M.S. thesis o Ph.D. dissertation, Dept., Univ., City, Country, 2023. |
| Informe técnico | [8] A. Author, “Title,” Organization, City, Country, Rep. identificador, 2023. |
| Web | [9] Autor/entidad. “Page title.” Site. Accessed: fecha real. [Online]. Available: URL |

Consultar el ejemplo específico para normas técnicas, patentes, datasets, software, preprints, artículos aceptados/no publicados, manuales, comunicaciones privadas y recursos audiovisuales. No tratarlos todos como artículos. No trasladar la exclusión APA de comunicaciones personales automáticamente a IEEE: consultar las reglas del destino, recuperabilidad, consentimiento y modelo pertinente.

## Herramientas y control final

- `auditar_citas_bibliografia.py --style ieee --strict` comprueba localizadores, faltantes, duplicación de números, orden de aparición/lista y rangos comprimidos. No renumera el manuscrito. Usar la obra completa con una sección explícita `Referencias`/`References`/`Bibliografía`, con o sin encabezado Markdown.
- Detecta rangos heredados para inventariarlos y advertirlos; no convierte esa detección en aprobación normativa. Rangos descendentes o expansiones de más de 10 000 elementos se rechazan por seguridad.
- El análisis numérico sigue siendo heurístico: corchetes matemáticos sin marcado de código, encabezados atípicos, notas complejas o documentos convertidos pueden necesitar ajuste manual. No verifica equivalencia semántica de fuentes duplicadas ni atribución real.
- `doi_a_referencia.py --style ieee` produce **borradores de artículos de revista** desde Crossref, no referencias certificadas. Otros tipos o datos esenciales incompletos quedan pendientes; conserva metadatos para resolverlos manualmente.
- Comprobar la abreviatura sugerida por Crossref contra la oficial, fechas/mes, versión, páginas, identificador y tipo de fuente. Estado `borrador` significa metadatos recuperados, no validez normativa. El modo APA del mismo script también es preliminar.
- Revisar manualmente comillas, cursivas, puntuación, autoría, localizadores, títulos, fuentes completas y plantilla final. Un resultado sin errores mecánicos no certifica todo IEEE.

## Fuentes oficiales

Verificación de esta corrección: 19 de septiembre de 2026. El enlace de la guía de referencias puede redirigir a un documento vivo; comprobar la versión disponible antes de nuevos encargos. No afirmar lectura íntegra si falla el acceso.

- [IEEE Reference Guide](https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/IEEE_Reference_Guide.pdf)
- [IEEE Editorial Style Manual for Authors](https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/IEEE-Editorial-Style-Manual-for-Authors.pdf)
- [IEEE Author Center](https://ieeeauthorcenter.ieee.org/)
