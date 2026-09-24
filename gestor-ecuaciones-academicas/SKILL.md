---
name: gestor-ecuaciones-academicas
description: Crea, revisa, normaliza, convierte e integra ecuaciones académicas y científicas en LaTeX, Markdown, MathML, OMML/Word y formatos editoriales. Usar cuando Codex deba comprobar notación, variables, unidades, dimensiones, numeración, referencias cruzadas, editabilidad o presentación de fórmulas; no sustituye la validación disciplinar de una demostración o modelo.
---

# Gestor de Ecuaciones Académicas

## Responsabilidad

Preservar significado matemático, trazabilidad y editabilidad desde el manuscrito hasta la entrega. Tratar una ecuación como contenido científico, no como decoración ni como una imagen. No cambiar operadores, signos, índices, exponentes, límites, agrupaciones, unidades o condiciones para mejorar solamente la apariencia.

Separar tres revisiones y declarar cuál se realizó:

- **Mecánica**: delimitadores, etiquetas, numeración, referencias y sintaxis visible.
- **Editorial**: notación uniforme, definición de símbolos, legibilidad, ubicación y cumplimiento de la plantilla.
- **Sustantiva**: equivalencia algebraica, dimensiones, supuestos y validez respecto del modelo o disciplina. Una comprobación mecánica no certifica esta capa.

## Flujo

1. Identificar disciplina, audiencia, formato fuente, formato final, plantilla y convención ya usada en la obra.
2. Inventariar ecuaciones en bloque y en línea; conservar una copia del origen y localizar llamadas, definiciones de variables y unidades.
3. Establecer una notación canónica antes de convertir: símbolos, índices, vectores, matrices, operadores, conjuntos, unidades y condiciones.
4. Revisar cada ecuación contra el texto y, cuando corresponda, contra la fuente, derivación, datos o implementación que la sustenta. No completar términos ausentes por intuición.
5. Comprobar consistencia dimensional y algebraica solo cuando los supuestos y unidades estén disponibles; marcar lo no verificable.
6. Numerar únicamente las ecuaciones que deban citarse o que la plantilla exija. Si el destino no prescribe otro sistema, usar números arábigos entre paréntesis al margen derecho —por ejemplo, `(1)`— y una secuencia estable adecuada al producto. Mantener etiquetas y referencias cruzadas automáticas, nunca números escritos manualmente como fuente de verdad.
7. Convertir al formato de entrega sin rasterizar. En Word, normalizar los espacios OMML accidentales y componer las ecuaciones numeradas en dos columnas —ecuación amplia y número estrecho— antes de validar el OOXML y realizar la inspección autorizada en Microsoft Word. Conservar el formato maestro editable.
8. Entregar inventario de cambios, incidencias resueltas, incidencias pendientes y límites de la revisión.

## Formatos

- Preferir LaTeX como fuente canónica en manuscritos matemáticos o flujos TeX.
- En Word, usar ecuaciones OMML editables; no pegarlas como capturas. Coordinar con `$maquetacion-academica-preentrega` y la skill de documentos para crear y revisar el DOCX. En este flujo no usar LibreOffice: realizar controles OOXML reproducibles y reservar la comprobación visual final para Microsoft Word u otro motor autorizado expresamente por el usuario.
- No insertar ejecuciones OMML vacías ni espacios literales entre símbolos para simular separación. El motor matemático debe resolver el espaciado de operadores; conservar los espacios internos del texto descriptivo incluido en una ecuación.
- Para ecuaciones numeradas en Word, usar una tabla sin bordes de dos columnas: la primera ocupa el ancho restante y centra la ecuación; la segunda tiene ancho fijo suficiente para el número, alineación derecha, centrado vertical y sin ajuste de línea. No reservar una tercera columna vacía para compensar el centrado.
- Una ecuación extensa puede dividirse dentro del objeto OMML en puntos matemáticamente válidos. No estrecharla, reducirla de forma ilegible ni hacerla saltar de línea solo para conservar una tabla simétrica.
- En HTML o EPUB, preferir MathML accesible o la tecnología matemática admitida por el destino. Conservar LaTeX equivalente cuando facilite mantenimiento.
- Usar SVG o raster solo si el canal final no admite matemáticas editables y el usuario acepta esa limitación; conservar siempre el original editable y documentar la conversión.
- No sustituir una ecuación por texto Unicode cuando se pierdan estructura, agrupación o accesibilidad.

Leer [formatos, notación y control editorial](references/formatos-y-control.md) cuando haya conversión, exigencias APA/IEEE, unidades, matrices, sistemas o accesibilidad.

## Auditoría mecánica reproducible

Desde la raíz de la colección:

```text
python editor-en-jefe/scripts/ejecutar.py gestor-ecuaciones-academicas/scripts/auditar_ecuaciones.py "ruta/manuscrito.tex" --out "ruta/informe-ecuaciones.json"
```

El auditor usa únicamente la biblioteca estándar de Python y funciona en Linux, Windows y macOS. Procesa UTF-8 en `.md`, `.tex` y `.txt`; inventaría `$$...$$`, `\[...\]` y los entornos `equation`, `align`, `gather` y `multline`, incluidas sus variantes con asterisco. Detecta delimitadores o entornos sin cierre, llaves desbalanceadas, etiquetas duplicadas, referencias `\eqref` inexistentes y etiquetas sin `\eqref`.

La salida 0 indica ausencia de errores mecánicos; 1 indica hallazgos de error y conserva el informe; 2 corresponde a argumentos, rutas, codificación o destino inválidos. Un informe existente solo se reemplaza con `--overwrite`. El auditor no interpreta macros, ecuaciones en DOCX/PDF, referencias creadas con otros comandos ni corrección matemática.

## Normalización de ecuaciones en Word

Para corregir un DOCX existente sin sobrescribirlo:

```text
python editor-en-jefe/scripts/ejecutar.py \
  gestor-ecuaciones-academicas/scripts/normalizar_ecuaciones_word.py \
  --input "ruta/original.docx" \
  --out "ruta/original-ecuaciones-normalizadas.docx"
```

La herramienta:

- elimina ejecuciones matemáticas vacías y espacios ASCII periféricos que producen huecos como `a + [vacío] b`, sin borrar los espacios internos de texto explicativo;
- reconoce únicamente tablas de tres columnas cuyo primer espacio está vacío, la columna central contiene OMML y la última contiene un número de ecuación o campo `SEQ`;
- convierte esas tablas en dos columnas, suma el ancho vacío al área de la ecuación y mantiene el número fijo a la derecha y sin salto de línea;
- conserva las tablas ambiguas o de contenido ordinario y escribe siempre un DOCX nuevo.

El código 0 indica que se produjo el DOCX de salida, incluso cuando no hubo nada que cambiar; el 2 indica entrada, XML o destino inválidos. El resumen JSON informa cuántos separadores y tablas se modificaron. Después, validar la estructura OOXML y abrir las páginas afectadas en Microsoft Word para la inspección visual final; no usar LibreOffice en este flujo. Esta normalización no demuestra equivalencia matemática ni reemplaza la comparación con la ecuación fuente.

## Límites de intervención

- No declarar correcta una ecuación solo porque compila o carece de alertas.
- No transformar una expresión en otra supuestamente equivalente sin mostrar la derivación o verificarla por un método adecuado.
- No inventar valores, unidades, condiciones iniciales, dominios, resultados ni definiciones de variables.
- No imponer notación nueva si la existente es válida y consistente; ante variantes disciplinares, seguir la fuente o el perfil del proyecto.
- No convertir ecuaciones en imágenes para resolver problemas de compatibilidad sin autorización explícita.
- No editar datos empíricos ni código de cálculo cuando el encargo se limite a presentación.

## Coordinación

- `$editor-en-jefe` activa esta skill cuando la obra contiene matemáticas relevantes, cuando se convierten formatos o cuando una revisión afecta símbolos, unidades o referencias.
- `$maquetacion-academica-preentrega` gobierna la integración y comprobación visual en Word/PDF conforme al perfil editorial.
- `$normalizador-terminologia-glosario` coordina nombres, siglas y conceptos; esta skill gobierna símbolos y notación matemática.
- `$auditor-documental-academico` puede inventariar la presencia de fórmulas, pero esta skill realiza su revisión especializada.

## Cierre

No declarar terminada la intervención hasta comprobar que:

- las ecuaciones conservan significado y permanecen editables;
- cada símbolo, abreviatura y unidad se define en su primera aparición o en una lista inequívoca;
- notación, índices, vectores, matrices, operadores y unidades son consistentes;
- etiquetas, numeración, llamadas y referencias cruzadas resuelven correctamente;
- la conversión no perdió términos, límites, alineación ni agrupaciones;
- ninguna ecuación contiene huecos producidos por ejecuciones OMML vacías o espacios periféricos accidentales;
- las ecuaciones numeradas en Word usan dos columnas, conservan el mayor ancho útil posible y mantienen el número alineado a la derecha sin salto de línea;
- el DOCX final superó controles OOXML y fue inspeccionado en Microsoft Word cuando se modificó su presentación; no se usó LibreOffice;
- el PDF, HTML o EPUB final fue renderizado e inspeccionado con una herramienta autorizada cuando se modificó su presentación;
- el informe distingue errores confirmados, advertencias y aspectos no verificables.
