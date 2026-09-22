# APA 7: documento y revisión de entrega

Complementa [citas y referencias](../../gestor-referencias-academicas/references/apa7-practico.md). Clasificar controles como verificados, pendientes, no aplicables o excepciones institucionales documentadas. Ningún script de esta colección certifica todo el manual.

## Perfil

- Estudiantil: portada con título, autoría, afiliación, curso, docente y fecha de entrega; número de página desde la portada, arriba a la derecha. No exigir encabezado abreviado ni nota de autor salvo encargo. Resumen y palabras clave solo si se solicitan.
- Profesional: portada, autoría/afiliaciones, nota de autor cuando corresponda; encabezado abreviado en mayúsculas (hasta 50 caracteres, incluidos espacios/puntuación) a la izquierda y número a la derecha. Sin etiqueta «Running head:». Resumen y palabras clave según revista/tipo de artículo.
- Libro/tesis con citación APA: identificar qué sigue APA y qué sigue a editorial/universidad. No imponer una portada de artículo ni una extensión universal.

## Página y texto

- Papel carta (21,59 × 27,94 cm) en formato estándar de manuscrito; A4 u otro como elección institucional/editorial documentada. Márgenes de 2,54 cm.
- Numeración arábiga consecutiva, incluida portada; revisar secciones y encabezados de primera página o pares/impares.
- Fuente legible y consistente. Ejemplos: Times New Roman 12, Calibri 11, Arial 11, Georgia 11, Lucida Sans Unicode 10 y Computer Modern 10. No convertir ejemplos en veto automático a otra fuente accesible. Figuras, código y notas pueden tener ajustes.
- Doble espacio en cuerpo, citas en bloque y referencias; sin espacio adicional entre párrafos. Excepciones: cuerpo de tablas y texto dentro de figuras admiten sencillo/1,5/doble; notas al pie, portada y ecuaciones tienen particularidades. Notas al pie no equivalen a notas de tabla.
- Izquierda, margen derecho irregular; sangría inicial de 1,27 cm en párrafos ordinarios. Resumen sin sangría; referencias con sangría francesa; bloques textuales con sangría izquierda. Rótulos/títulos de recursos sin sangría del cuerpo.

## Cinco niveles

| Nivel | Formato | Texto |
|---|---|---|
| 1 | Centrado, negrita | Párrafo nuevo |
| 2 | Izquierda, negrita | Párrafo nuevo |
| 3 | Izquierda, negrita y cursiva | Párrafo nuevo |
| 4 | Sangría inicial 1,27 cm, negrita y punto final | Misma línea, sin heredar negrita |
| 5 | Sangría inicial 1,27 cm, negrita/cursiva y punto final | Misma línea, sin heredar énfasis |

No saltar niveles ni numerarlos por defecto. Capitalización según idioma: no trasladar title case inglés al español automáticamente. La introducción normalmente empieza bajo el título del trabajo, sin rótulo «Introducción». Resumen, Referencias y Apéndices son rótulos de sección.

## Revisión humana de secciones y estilo

- Portada: datos reales, afiliaciones, disposición y espacios. No inventar datos ausentes.
- Resumen: página propia si corresponde; rótulo centrado/negrita, párrafo sin sangría, límite según encargo/revista. Palabras clave debajo, etiqueta en cursiva y sangría de párrafo.
- Cuerpo: atribución, continuidad, lenguaje sin sesgos y categorías respetuosas/precisas. Aplicar JARS pertinentes a artículos de investigación, sin sustituir el protocolo.
- Números/estadística: revisar excepciones a números en palabras/cifras (medidas, edades, fechas, escalas, estadísticas), símbolos, unidades, decimales, valores p, intervalos y tamaños de efecto. No transformar datos para adaptar apariencia. Consultar capítulos 5–6 y estándares de reporte.
- Puntuación/abreviaturas: definir siglas no comunes; revisar listas, cursivas, comillas y símbolos según idioma y función.
- Referencias: página nueva, orden, sangría, cursivas y correspondencia; verificar autoría, año, DOI y apoyo real a afirmaciones.
- Apéndices: página nueva por apéndice, etiqueta/título centrados en negrita; «Apéndice» si es uno, letras si son varios. Mención en cuerpo. Tablas/figuras con identificación propia, p. ej., Tabla A1.
- Notas al pie: numeración y ubicación coherentes; no esconder referencias faltantes.

## Tablas y figuras

- Numerar por orden de mención, series independientes; número negrita y título cursiva arriba/izquierda. Referir y explicar lo relevante sin repetir todos los datos.
- Notas debajo **solo cuando sean necesarias**. Orden si coexisten: general, específicas con superíndices y probabilidad. Etiqueta «Nota.» en cursiva en la nota general.
- Atribuir reproducciones/adaptaciones y comprobar permisos. Una figura original no necesita automáticamente «elaboración propia». Acceso abierto y anexo de prompts son políticas posibles del proyecto, no requisitos APA universales.
- Tablas editables, unidades y encabezados claros; evitar líneas verticales/cuadrícula. Separaciones horizontales según necesidad, sin prohibir toda línea interna.
- Figuras legibles, leyendas/símbolos claros, color accesible y texto alternativo. Número/título editoriales fuera de la imagen. Revisar resolución y atribución.
- No existe cuota APA de 60 palabras inmediatamente después de cada recurso. Evitar rótulos huérfanos y revisar continuaciones visualmente.
- No hay prohibición APA universal de glosarios en tablas: decidir según función, accesibilidad y encargo.

## Automatización y límites

```text
python skills/editor-en-jefe/scripts/ejecutar.py maquetacion-academica-preentrega/scripts/markdown_a_docx.py fuente.md --out salida.docx --apa7-strict
python skills/editor-en-jefe/scripts/ejecutar.py maquetacion-academica-preentrega/scripts/auditar_docx_apa7.py salida.docx
```

`--apa7-strict` conserva su nombre por compatibilidad: aplica **formato base**, no produce ni valida por sí solo un manuscrito completo. Usa carta, 2,54 cm, doble espacio, izquierda, cinco niveles, bloques `>` sin decoración y campo PAGE en encabezados vacíos. Documentar `--page-size A4` o `template` como excepción. Preserva encabezados no vacíos de plantillas: comprobar paginación y encabezado profesional.

Niveles 4–5: título en `####`/`#####` y párrafo ordinario en la siguiente línea no vacía; el conversor los une. Bloques: marcar `>` explícitamente; comprobar longitud, localizador y sangría adicional en citas de varios párrafos. No convierte comillas automáticamente ni verifica literalidad.

La opción `--apa-metadata datos.json`, junto con `--apa7-strict`, genera una portada básica y encabezado estudiantil/profesional. Es incompatible con `--template` para no duplicar portadas ni destruir encabezados. Admite una línea de autoría con una afiliación compartida; autorías con varias afiliaciones, superíndices o requisitos editoriales especiales se resuelven mediante plantilla/edición. No inventa datos ni completa campos faltantes. El cuerpo Markdown debe incluir su propio título cuando corresponda; la portada no lo duplica automáticamente al inicio del cuerpo.

Ejemplo de estructura JSON (sustituir todos los valores por datos reales):

```json
{
  "profile": "student",
  "title": "Título del trabajo",
  "authors": "Nombre de la autora",
  "affiliation": "Departamento, Universidad",
  "course": "Código y nombre del curso",
  "instructor": "Nombre del docente",
  "due_date": "Fecha de entrega"
}
```

Para `professional`, conservar `title`, `authors` y `affiliation`, quitar `course`, `instructor` y `due_date`, y proporcionar `running_head` (hasta 50 caracteres después de convertir a mayúsculas). `author_note` es una lista opcional de párrafos reales; `author_note_label` permite indicar su rótulo en el idioma del manuscrito. Revisar cuándo corresponde la nota, su contenido y ubicación. Campos desconocidos, datos incompletos y mezcla de perfiles se rechazan. El JSON también se protege frente a sobrescritura accidental.

El auditor reconoce los estilos `APA Cover Title`, `APA Cover Data` y `APA Cover Note`: comprueba su interlineado, pero deja alineación, espacios y contenido de portada a revisión manual. No reutilizar esos estilos en el cuerpo. Renderizar siempre: títulos extensos y notas largas pueden necesitar ajuste de página; los tests estructurales no comprueban esa disposición.

En `--apa7-strict`, un apartado Markdown `# Resumen` o `# Abstract` recibe párrafos sin sangría hasta el siguiente encabezado. Ese encabezado comienza una página nueva, sin exigir un salto manual; los encabezados posteriores del cuerpo no reciben este salto adicional. Marcar el título inicial del cuerpo con `#`: el conversor no puede deducir dónde termina un resumen si solo hay párrafos consecutivos. Revisar palabras clave y estructura real. El idioma operativo `es-EC` es local, no APA; elegir `--language es-PE`, `en-US` u otra etiqueta apropiada cuando difiera.

La portada automática anula los bordes decorativos heredados de `Title` y elimina el tabulador central del encabezado profesional para colocar el campo de página en el margen derecho. Estos ajustes se limitan a la portada automática; no reparan portadas existentes ni encabezados no vacíos de plantillas.

El auditor verifica márgenes, formato heredado de párrafos del cuerpo, niveles usados, sangría de referencias y secuencia básica de recursos. Fuente/bordes pueden requerir juicio. No garantiza semántica, correspondencia de citas, orden alfabético, todas las corridas, cuadros de texto, portada, notas complejas/al pie, paginación renderizada ni todas las excepciones de espaciado. Revisar estas áreas manualmente; documentar falsos positivos válidos, sin alterar contenido correcto para silenciarlos.

`--language` y `--min-analysis-words` son controles editoriales opcionales, desactivados por defecto. Márgenes/interlineados alternativos representan excepciones. Salida 0 significa únicamente «sin errores detectados en controles ejecutados»; siempre se informa el alcance parcial.

## Puerta de entrega

1. Registrar perfil y excepciones; recorrer esta lista y la guía bibliográfica.
2. Ejecutar auditoría y resolver errores o documentar excepciones válidas.
3. Revisar contenido y fuentes; no inferir corrección semántica de un script.
4. Renderizar DOCX en Word/LibreOffice o PDF y revisar portada, encabezados, páginas, citas, tablas, figuras, referencias y apéndices. Sin renderizador, declarar revisión visual pendiente.
5. Entregar cobertura real y pendientes; no afirmar «todos los parámetros» sin revisión completa del alcance aplicable.

## Regresión del renderizado

`scripts/regresion_visual_apa.py` genera cuatro casos ficticios (estudiantil, título largo, profesional y nota larga), ejecuta el conversor y el renderizador, y examina la geometría y el texto del PDF resultante. Está destinado al mantenimiento del generador, no a manuscritos arbitrarios. No compara capturas píxel a píxel ni garantiza ausencia de toda superposición, recorte, sustitución de fuente o defecto editorial.

Requisitos: Python 3.10+ con `pymupdf` para el verificador; un entorno de renderizado con `python-docx`, `pdf2image`, LibreOffice y Poppler. Proporcionar explícitamente el Python y el `render_docx.py` de confianza de ese entorno. En Codex, seleccionar las dependencias empaquetadas según la skill de documentos, sin recurrir silenciosamente al LibreOffice de escritorio. No descarga ni instala dependencias. No copiar el entorno Python entre sistemas.

Desde la raíz de la colección, reemplazar las rutas de ejemplo por las del equipo:

```text
python editor-en-jefe/scripts/ejecutar.py maquetacion-academica-preentrega/scripts/regresion_visual_apa.py --out "ruta/nueva/revision-apa" --renderer-python "ruta/al/python-del-renderizador" --renderer-script "ruta/a/render_docx.py"
```

El Python que ejecute el verificador debe disponer de PyMuPDF; el conversor usa el Python explícito del renderizador. En Windows puede iniciarse el lanzador con `py -3`; en Linux/macOS, con `python3`. Se invocan procesos sin shell y se admiten rutas con espacios. La compatibilidad del código no sustituye pruebas nativas en cada plataforma.

Controles de estos casos: tres páginas carta (portada, resumen y cuerpo); numeración consecutiva en la zona superior y a 6 puntos como máximo del margen derecho esperado; encabezado profesional a la izquierda; ausencia de líneas vectoriales horizontales decorativas de al menos 80 puntos en la portada; título completo en portada y cuerpo; resumen, cuerpo y nota en las páginas previstas; PNG decodificables para cada página con tamaño y proporción suficientes. Son tolerancias operativas de regresión, no requisitos adicionales de APA.

La carpeta `--out` debe ser nueva: no se admite sobrescritura ni se reutilizan renders anteriores. Cada caso conserva Markdown, metadatos, DOCX, PDF y PNG. `informe.json` registra resultados, plataforma y ruta/huella del renderizador. Código de salida: **0**, controles ejecutados sin hallazgos; **1**, regresión detectada; **2**, error de preparación o ejecución. Si un proceso falla o supera `--timeout` (120 segundos por proceso por defecto), la ejecución no se presenta como aprobada. Pueden quedar artefactos parciales para diagnóstico; no se borran archivos del usuario. Una carpeta existente o dependencia ausente se rechaza antes de crear salidas.

Las pruebas unitarias incluyen PDF controlados con bordes, números desplazados/ausentes y saltos incorrectos, además de fallos del renderizador. Ejecutar `python -m unittest discover -s maquetacion-academica-preentrega/tests -p test_regresion_visual_apa.py -v`. El recorrido real de renderizado se ejecuta por separado con el comando anterior. Abrir los PNG para la revisión humana final cuando se modifique la maquetación.

## Consulta normativa

- [Manual oficial: alcance](https://www.apa.org/pubs/books/publication-manual-7th-edition-spiral)
- [Formato](https://apastyle.apa.org/style-grammar-guidelines/paper-format)
- [Portada](https://apastyle.apa.org/style-grammar-guidelines/paper-format/title-page)
- [Encabezado de página](https://apastyle.apa.org/style-grammar-guidelines/paper-format/page-header)
- [Fuentes](https://apastyle.apa.org/style-grammar-guidelines/paper-format/font)
- [Interlineado](https://apastyle.apa.org/style-grammar-guidelines/paper-format/line-spacing)
- [Encabezados](https://apastyle.apa.org/style-grammar-guidelines/paper-format/headings)
- [Tablas/figuras](https://apastyle.apa.org/style-grammar-guidelines/tables-figures)
- [Lenguaje sin sesgos](https://apastyle.apa.org/style-grammar-guidelines/bias-free-language)
- [Números](https://apastyle.apa.org/style-grammar-guidelines/numbers)
- [JARS](https://apastyle.apa.org/jars)
- [Guía estudiantil APA](https://www.apa.org/ed/precollege/psn/2020/09/apa-style-student-papers)
