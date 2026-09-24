# Maquetación Académica y Preentrega

Usalo cuando el usuario necesite una revision final de presentacion academica o editorial antes de entrega, incluyendo titulos, subtitulos, numeracion, secciones preliminares, bibliografia, anexos, consistencia visual, exportacion a Word con tablas nativas editables, limpieza general para Word/PDF, o generacion complementaria de TXT limpio sin marcas Markdown para libros y manuscritos.

## Ejemplo de uso

```text
Usa $maquetacion-academica-preentrega para revisar este documento antes de entrega.
```

## Guía operativa

### Ejecución multiplataforma

Consultar [la guía común de ejecución](../../editor-en-jefe/references/portabilidad.md) para elegir intérprete y preparar dependencias.

### Automatizacion Previa

Si el documento esta convertido a Markdown/TXT, ejecutar primero `$auditor-documental-academico`, especialmente `scripts/check_preentrega.py` e `inventariar_documento.py`, para detectar secciones, citas, referencias, tablas y faltantes mecanicos antes de la revision final.

Cuando exista un índice autorizado, pasar su ruta con `--estructura`. Resolver sus alertas de encabezados ajenos al índice, rótulos operativos, casillas, cercas de código, marcadores de trabajo, niveles saltados y títulos duplicados antes de convertir a Word. Si no hay índice, ejecutar el control sin esa opción: sigue detectando residuos y problemas de jerarquía, pero no puede decidir qué encabezados pertenecen al libro.

### Objetivo

Realizar la auditoria final de forma y presentacion. No se centra en la escritura de fondo, sino en que el manuscrito llegue limpio, consistente y listo para entrega academica o editorial.

Cuando un libro requiera identidad visual, composición tipográfica y una arquitectura de Word capaz de resistir futuras adiciones o eliminaciones, activar primero `$disenador-maquetador-word`. Esta skill conserva esa dirección aprobada y comprueba requisitos, limpieza y entrega; no la sustituye por el formato genérico del conversor.

### Regla De Productos Finales

Para libros completos, aplicar el cierre de [producción editorial integrada](../../editor-en-jefe/references/produccion-editorial-eficiente.md). Recibir capítulos con controles editoriales registrados y revisar la obra integrada y renderizada. No confundir exportación exitosa con libro publicable ni omitir inspección visual por ahorro de tokens. Resolver defectos dentro del encargo; si persisten pendientes sustantivos, declarar borrador y sus límites.

Para libros destinados a edición en Microsoft Word, generar como salida principal un `.docx` con tablas nativas editables. Generar además un `.txt` limpio como respaldo de contenido y preservación. Markdown puede usarse como formato intermedio, pero no debe ser la única entrega final.

En proyectos con estructura canónica completa, usar estas rutas; en proyectos compactos, usar `entregables/` y registrar la equivalencia:

```text
09_entregables/v03_final_docx/libro_completo.docx
09_entregables/v03_final_txt/libro_completo.txt
```

Evitar entregar `libro_completo.md` como producto final salvo que el usuario lo pida explícitamente. No convertir tablas a texto antes de generar el DOCX.

### Perfil formal del proyecto

Si la norma activa es IEEE, leer [references/ieee-presentacion.md](../../maquetacion-academica-preentrega/references/ieee-presentacion.md): usar la plantilla del destino y sus convenciones de tablas/figuras, no `--apa7-strict` ni el auditor APA. El conversor genérico es un intermedio, no un maquetador IEEE completo.

Consultar [el perfil editorial común](../../editor-en-jefe/references/perfiles-editoriales.md). Aplicar la plantilla, norma, lengua, formato y extensión seleccionados para esta obra; no imponer el perfil de libro extenso a cualquier manuscrito.

El conversor conserva valores operativos para una maqueta de libro cuando no recibe opciones. Distinguirlos de requisitos del proyecto y de APA estricto; documentar los argumentos utilizados. Aplicar explícitamente tipografía y color para evitar cambios heredados del tema de Word, respetando la jerarquía de la norma activa.

### Flujo De Trabajo

El contexto maestro no es un requisito de preentrega. Si falta, determinar la estructura y el formato desde el encargo, el manuscrito, la plantilla y el perfil editorial disponible. Comprobar igualmente títulos, numeración, marcas visibles, tablas, figuras y paginación; no exigir una matriz previa ni asumir cuotas o convenciones de otra obra.

Para libros con contexto maestro, leer [interpretación integral del contexto](../../editor-en-jefe/references/interpretacion-contexto-editorial.md) y recibir su matriz de requisitos y jerarquía acordada. Comparar los encabezados reales antes de exportar; no maquetar como contenido instrucciones, roles, checklist ni pendientes de producción. Aplicar las convenciones de todo el contexto y documentar conflictos, no únicamente su checklist final.

Tras exportar, renderizar el DOCX a páginas o PDF y revisar jerarquía, numeración, separación de capítulos, tablas, figuras y pies. Buscar marcas Markdown literales, cercas, casillas, separadores heredados, títulos duplicados y rótulos de trabajo, distinguiéndolos de notación legítima. Corregir en la fuente o estilos y volver a inspeccionar las páginas afectadas. Sin renderizado, informar revisión visual pendiente y no afirmar que la maquetación está validada.

1. Revisar estructura general y preliminares.
2. Verificar titulos, numeracion y jerarquia.
3. Comprobar uniformidad de tablas, figuras, citas, bibliografia y anexos.
   - Confirmar numeración consecutiva del cuerpo y series independientes de figuras; en APA, tratar aparte tablas/figuras de apéndices (A1, A2, etc.).
   - Verificar que cada tabla o imagen tenga una función declarada y una llamada pertinente desde el texto.
   - Verificar explicación pertinente de cada recurso; exigir ubicación inmediata o extensión del análisis solo si lo establece el perfil editorial, no por APA.
   - Rechazar recursos decorativos, insertados por cuota o sin valor explicativo.
   - Confirmar derechos/licencia de recursos externos y declaración de generación según el proyecto. Acceso abierto y anexo de prompts son políticas editoriales, no requisitos universales APA.
   - Confirmar que pies, notas, citas y referencias cumplen la skill normativa seleccionada.
4. Detectar residuos de edicion, marcas y formatos inconsistentes.
5. Si hay un Markdown de trabajo, convertirlo primero a DOCX y comprobar que cada tabla sea una tabla real de Word.
6. Generar después el TXT final limpio como respaldo complementario.
7. Entregar el `.docx` para edición y el `.txt` para preservación.

### Herramienta para Word

Los exportadores DOCX y TXT requieren `editor-en-jefe/scripts/archivos_seguros.py`, también al ejecutarlos directamente. Rechazan salidas existentes salvo `--overwrite`; nunca autorizan sustituir el manuscrito, la plantilla o las imágenes de entrada. Con el lanzador, añadir además `--permitir-sobrescritura` antes de la ruta del script. El DOCX se ensambla completo (incluidos los SVG) antes de publicarse atómicamente; un fallo de conversión conserva la salida anterior. Esto protege el archivo, no certifica su presentación visual. Consultar los límites de escritura y sistemas de archivos en [portabilidad](../../editor-en-jefe/references/portabilidad.md).

Usar el Python del entorno del preprocesador, que incluye `python-docx`:

```text
python skills/editor-en-jefe/scripts/ejecutar.py maquetacion-academica-preentrega/scripts/markdown_a_docx.py "ruta/09_entregables/v02_revision/libro_completo.md" --out "ruta/09_entregables/v03_final_docx/libro_completo.docx"
```

El script convierte encabezados, párrafos, listas, imágenes locales y tablas Markdown. Las tablas se crean como objetos nativos de Word con estilo de cuadrícula y encabezado repetible.

Guardar entregables separados del trabajo cotidiano. En estructura completa, la fuente integrada va en `09_entregables/v02_revision/` y el Word en `09_entregables/v03_final_docx/`; en estructura compacta, usar los destinos equivalentes registrados.

### Formato editorial e imágenes

La opción preferida para una colección o editorial es proporcionar una plantilla `.docx` en `plantillas/`. Puede contener tamaño de página, márgenes, estilos de títulos, tipografía, encabezados, pies y numeración. Ejemplo:

```text
python skills/editor-en-jefe/scripts/ejecutar.py maquetacion-academica-preentrega/scripts/markdown_a_docx.py "ruta/09_entregables/v02_revision/libro_completo.md" --out "ruta/09_entregables/v03_final_docx/libro_completo.docx" --template "ruta/plantillas/plantilla_editorial.docx" --assets-root "ruta/06_recursos_visuales/imagenes"
```

Sin plantilla, el script aplica automáticamente A4, márgenes de 2,5 cm, Times New Roman 12 e interlineado 1,5. Se admiten `--font`, `--font-size`, `--margin-cm`, `--line-spacing`, `--page-size` y `--image-width` para excepciones expresas. Las imágenes Markdown `![pie](archivo.png)` se insertan como imágenes reales en el DOCX: primero se resuelven respecto al manuscrito y luego respecto a `--assets-root`.

En la salida predeterminada, justificar los párrafos del cuerpo, aplicar sangría de primera línea de 1,27 cm y mantener 0 puntos antes y después: no insertar espacio adicional ni párrafos vacíos para separar párrafos consecutivos. Mantener títulos, listas, notas, rótulos de tablas y figuras, y referencias alineados a la izquierda y sin sangría inicial. Aplicar sangría francesa de 1,27 cm a las referencias APA. El texto entre corchetes de una imagen Markdown se trata como texto alternativo de accesibilidad y no debe aparecer como pie visible.

APA 7 usa normalmente interlineado doble. Si una convocatoria establece expresamente otro interlineado, como 1,5, esa regla de presentación prevalece y debe registrarse como excepción editorial; no convertirla en espacio posterior entre párrafos.

Cuando el usuario exija APA 7, leer [references/apa7-docx.md](../../maquetacion-academica-preentrega/references/apa7-docx.md) y seleccionar el perfil estudiantil, profesional o institucional. El conversor con `--apa7-strict` aplica formato base: carta, márgenes de 2,54 cm, doble espacio, izquierda, cinco niveles y paginación en encabezados vacíos. El nombre de la opción se conserva por compatibilidad; no certifica un manuscrito completo. Completar portada, resumen y encabezado profesional cuando correspondan. A4 se selecciona explícitamente como excepción mediante `--page-size A4`.

Ejecutar `scripts/auditar_docx_apa7.py` y completar su revisión manual antes de entregar un archivo APA. Sus controles son parciales; `--language` y `--min-analysis-words` son preferencias editoriales opcionales, desactivadas por defecto. No rechaza por defecto fuentes admitidas distintas de Times New Roman ni exige notas innecesarias.

Para generar portada básica y encabezado, usar `--apa7-strict --apa-metadata datos.json` con el esquema de [references/apa7-docx.md](../../maquetacion-academica-preentrega/references/apa7-docx.md). Exige datos explícitos y una afiliación compartida; no combinar con plantilla. La portada generada y las notas de autor requieren revisión visual y editorial antes de entrega.

Tras cambiar la portada o la paginación del conversor, ejecutar `scripts/regresion_visual_apa.py` según [la prueba de renderizado](../../maquetacion-academica-preentrega/references/apa7-docx.md#regresión-del-renderizado). Comprueba cuatro casos controlados sobre PDF y conserva PNG para inspección; no usarlo para certificar manuscritos completos.

Elegir presentación de glosarios por función y perfil editorial: entradas independientes o tablas cuando aporten legibilidad. APA no prohíbe universalmente los glosarios tabulares. Respaldar definiciones cuando corresponda.

Para APA 7, usar `número en negrita -> título en cursiva -> tabla o figura -> notas si hacen falta`. Distinguir notas generales, específicas y de probabilidad. Usar bordes horizontales necesarios y evitar cuadrículas, títulos bajo figuras y atribuciones duplicadas.

Aplicar `mantener con el siguiente` al número y al título de cada tabla o figura; en las figuras, aplicarlo también al párrafo que contiene la imagen. No permitir que el número o el título queden huérfanos al pie de una página mientras el recurso aparece en la siguiente.

### Herramienta para el TXT final

```text
python skills/editor-en-jefe/scripts/ejecutar.py maquetacion-academica-preentrega/scripts/markdown_a_txt_final.py "ruta/09_entregables/v02_revision/libro_completo.md" --out "ruta/09_entregables/v03_final_txt/libro_completo.txt"
```

El script elimina o convierte marcas Markdown: encabezados `#`, enfasis `**`, enlaces, codigo inline, cercas de codigo, listas y tablas Markdown. Las tablas se vuelven texto alineado sin filas separadoras `|---|`.

### Validacion Final

- jerarquia de titulos estable;
- secciones preliminares completas si aplican;
- bibliografia y anexos integrados;
- documento limpio para entrega;
- archivo final en `.txt`;
- archivo final en `.docx` cuando el usuario edite en Word;
- tablas del DOCX verificadas como objetos editables, no como texto, imagen o tabulaciones;
- sin marcas Markdown visibles como `#`, `**`, `|---|`, cercas ``` o enlaces sin limpiar.
- sin imágenes o tablas carentes de justificación editorial;
- permisos/licencia verificados; acceso abierto cuando lo exija el perfil;
- declaración y registro de recursos generados según las reglas del proyecto;
- una sola norma coherente para títulos, citas, notas, pies y referencias.
- modo `--apa7-strict` usado cuando se solicite cumplimiento APA sin excepciones; cualquier desviación queda documentada como decisión editorial;
- párrafos del cuerpo justificados en el perfil editorial predeterminado o alineados a la izquierda en `--apa7-strict`; elementos normativos alineados según el modo activo;
- cuerpo con sangría inicial de 1,27 cm y 0 puntos antes y después, sin líneas vacías usadas como separación;
- números y títulos de tablas y figuras colocados antes del recurso, y notas después;
- números y títulos no quedan separados del recurso por un salto de página;
- cada recurso tiene explicación pertinente; ubicación y extensión según su función, sin cuotas atribuidas a APA;
- tablas del cuerpo en secuencia continua; apéndices APA con series propias;
- referencias APA con sangría francesa;
- tamaño, fuente y espaciado según perfil: distinguir A4/2,5 cm/1,5 editorial del formato base APA carta/2,54 cm/doble y sus fuentes legibles alternativas;
- títulos y subtítulos en la misma familia, tamaño y color negro exigidos por el perfil, sin formato heredado del tema de Word;
- glosarios legibles según encargo y con definiciones respaldadas cuando corresponda;
- extensión ajustada al objetivo o límite registrado en el perfil del proyecto; no rellenar para alcanzar una cantidad de páginas.

## Recursos incluidos

### Herramientas automatizadas

| Recurso | Función |
| --- | --- |
| [`scripts/auditar_docx_apa7.py`](../../maquetacion-academica-preentrega/scripts/auditar_docx_apa7.py) | Comprobaciones parciales APA 7; no certifica cumplimiento integral. |
| [`scripts/markdown_a_docx.py`](../../maquetacion-academica-preentrega/scripts/markdown_a_docx.py) | Convertir Markdown editorial a DOCX con tablas nativas editables. |
| [`scripts/markdown_a_txt_final.py`](../../maquetacion-academica-preentrega/scripts/markdown_a_txt_final.py) | Recurso auxiliar: Markdown a txt final. |
| [`scripts/portada_apa.py`](../../maquetacion-academica-preentrega/scripts/portada_apa.py) | Portada básica APA con una afiliación compartida y datos suministrados. |
| [`scripts/regresion_visual_apa.py`](../../maquetacion-academica-preentrega/scripts/regresion_visual_apa.py) | Regresión geométrica del PDF renderizado de cuatro casos APA controlados. |

### Referencias

| Recurso | Función |
| --- | --- |
| [`references/apa7-docx.md`](../../maquetacion-academica-preentrega/references/apa7-docx.md) | APA 7: documento y revisión de entrega |
| [`references/ieee-presentacion.md`](../../maquetacion-academica-preentrega/references/ieee-presentacion.md) | IEEE: presentación según publicación |

### Pruebas

| Recurso | Función |
| --- | --- |
| [`tests/test_apa7.py`](../../maquetacion-academica-preentrega/tests/test_apa7.py) | Regresiones con DOCX reales; no certifican revisión semántica ni visual. |
| [`tests/test_exportacion_segura.py`](../../maquetacion-academica-preentrega/tests/test_exportacion_segura.py) | Recurso auxiliar: Test exportacion segura. |
| [`tests/test_portada_apa.py`](../../maquetacion-academica-preentrega/tests/test_portada_apa.py) | Recurso auxiliar: Test portada apa. |
| [`tests/test_regresion_visual_apa.py`](../../maquetacion-academica-preentrega/tests/test_regresion_visual_apa.py) | Recurso auxiliar: Test regresion visual apa. |

### Configuración de interfaz

| Recurso | Función |
| --- | --- |
| [`agents/openai.yaml`](../../maquetacion-academica-preentrega/agents/openai.yaml) | Metadatos de interfaz e invocación de la skill. |

## Fuente normativa

Esta ficha se genera desde [`maquetacion-academica-preentrega/SKILL.md`](../../maquetacion-academica-preentrega/SKILL.md), que permanece como contrato normativo. Regenera la ficha después de modificar ese archivo.
