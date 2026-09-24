# Gestor de Imágenes Académicas para Libros

Genera, localiza, evalúa, descarga y documenta imágenes para libros académicos, tesis, artículos y materiales educativos. Usar cuando Codex deba crear ilustraciones originales, diagramas o imágenes conceptuales; buscar figuras, mapas, fotografías o gráficos en fuentes académicas e institucionales confiables; comprobar licencia y atribución; preparar pies de figura; o integrar recursos visuales con trazabilidad editorial sin confundir ilustración con evidencia científica.

## Ejemplo de uso

```text
Usa $gestor-imagenes-academicas-libros para crear o localizar imágenes confiables y listas para integrar en este libro.
```

## Guía operativa

El registrador exige capítulo, número de figura, ubicación, fecha real de creación y un archivo verificable; conserva original, archivo de trabajo y derivados con sus hashes SHA-256. Rechaza identificadores duplicados y añade datos mediante publicación atómica por archivo; manifiesto y anexo deben ser distintos y no pueden coincidir con ningún recurso. Para recursos asistidos publica primero el anexo y el manifiesto al final; si falla el manifiesto, restaura el anexo a sus bytes anteriores. Esta compensación requiere un solo proceso escritor y no constituye una transacción frente a concurrencia o fallos durante la reversión. Consultar [protección y límites de escritura](../../editor-en-jefe/references/portabilidad.md#protección-de-informes).

### Principio rector

Seleccionar cada imagen por su función intelectual, no como decoración. Distinguir siempre entre:

- **Evidencia**: figura o dato procedente de una fuente verificable. No generarla con IA.
- **Reproducción o adaptación**: material ajeno con licencia compatible y atribución completa.
- **Ilustración original**: recurso explicativo generado o diseñado para el libro. Rotularlo como ilustración; no atribuirle valor probatorio.

No inventar procedencia, autoría, licencia, resultados, escalas, mapas, anatomía, instrumental ni datos. No descargar ni reutilizar una imagen solo porque sea visible en Internet.

### Regla de necesidad y orden de preferencia

No establecer cuotas como una imagen por tema, capítulo o página. Incluir una imagen solo cuando explique una relación, proceso, objeto, comparación, evidencia o concepto que el texto comunique peor. Si no puede formularse qué comprende mejor el lector gracias a ella, omitirla.

Aplicar este orden cuando la modalidad no venga decidida por el usuario: confirmar una necesidad concreta; buscar primero en artículos, libros, repositorios y organismos confiables; integrar únicamente recursos de acceso abierto con licencia compatible verificable; generar cuando no exista una alternativa adecuada o cuando la obra necesite una explicación original específica. No generar para decorar, llenar espacio ni uniformar capítulos.

### Puerta de procedencia antes de generar

No cambiar la modalidad solicitada sin una razón académica concreta. Si el usuario pide localizar una imagen existente, no entregar una generación como sustituto. Si pide editar un recurso, conservarlo como objetivo de edición y no reemplazarlo por una composición nueva. Si pide expresamente una ilustración original conceptual que no representa evidencia, respetar esa elección.

Antes de generar, documentar una decisión de procedencia. Cuando pueda existir un recurso documental o ajeno adecuado, registrar fecha, consultas, repositorios revisados, candidatos, autoría, licencia, adecuación funcional y razón de descarte; abrir la ficha original, porque una miniatura o consulta genérica no basta. Cuando el usuario pida expresamente una creación original y la función no sea probatoria, registrar `No aplica búsqueda de imagen externa`, junto con la solicitud y la justificación editorial. No inventar una búsqueda para satisfacer el formulario. Una política institucional que exija búsqueda previa prevalece sobre esta excepción.

Usar o adaptar con atribución un recurso ajeno cuando comunique la relación necesaria, tenga calidad suficiente y pueda reutilizarse legalmente. Generar solo cuando ningún candidato abierto cumpla la función intelectual, cuando adaptarlo resulte engañoso o cuando la obra requiera una síntesis inédita. Guardar el registro en `06_recursos_visuales/metadata/registro_busqueda_imagenes.md`.

Clasificar como `generada` toda imagen, diagrama o SVG producido íntegramente por IA o mediante código redactado con asistencia de IA. Clasificar como `adaptada` todo recurso que conserve una estructura intelectual o visual reconocible de otro autor, aunque se redibuje por completo. No ocultar ninguno de estos casos bajo `elaboracion_propia`.

### Flujo operativo

1. Definir capítulo, concepto, audiencia, función de la imagen, formato final y requisitos editoriales.
2. Decidir la ruta:
   - Buscar una fuente externa cuando la imagen documente hechos, resultados, patrimonio, territorio, especímenes o datos.
   - Generar una imagen original cuando la función sea conceptual, pedagógica, narrativa o diagramática y no requiera reproducir evidencia.
   - Recomendar una tabla, gráfico basado en datos o diagrama vectorial cuando comunique mejor que una imagen rasterizada.
3. Antes de buscar o generar, redactar una ficha breve: propósito, contenido indispensable, contenido prohibido, ubicación prevista y pie provisional.
4. Ejecutar la ruta correspondiente.
5. Verificar legibilidad, rigor, accesibilidad, coherencia visual y aptitud para impresión.
6. Guardar el original y sus derivados con nombres estables y registrar el manifiesto mediante `scripts/registrar_imagen.py`; proporcionar la fecha efectiva de creación o adaptación, no la fecha actual por conveniencia.
7. Entregar imagen, pie, texto alternativo, fuente, licencia, enlace permanente, fecha de consulta y observaciones editoriales.
8. Para toda imagen generada, registrar modelo, fecha, prompt completo y razón editorial; incorporar prompt y razón en `09_entregables/v02_revision/anexos/anexo_prompts_recursos_generados.md`.
9. En diagramas, organigramas, mapas conceptuales y gráficos sin datos, conservar SVG como maestro editable. Usar PNG solo como derivado de compatibilidad; no sustituir el SVG cuando Word admita el vector.
10. Para imágenes rasterizadas, ejecutar `scripts/inspeccionar_imagen.py` con el ancho final de impresión antes de inspeccionar el recurso en el DOCX. Rechazar texto cortado, flechas incompletas, rótulos desbordados, fuentes sustituidas, baja resolución o cambios de renderizado.
11. En SVG destinados a Word/PDF, preferir puntas de flecha dibujadas como polígonos o trazos explícitos. Evitar `marker-end` y otros marcadores dependientes del motor cuando la prueba cruzada muestre deformaciones. Escribir `fill="none"`, `stroke` y `stroke-width` directamente en las trayectorias conectoras, porque algunos rasterizadores ignoran esas propiedades cuando solo están en CSS. Comprobar el SVG nativo y su PNG de respaldo.

En proyectos de libro con estructura canónica, guardar originales descargados en `06_recursos_visuales/originales/`, archivos finales en `06_recursos_visuales/imagenes/` y el manifiesto en `06_recursos_visuales/metadata/manifiesto_imagenes.jsonl`. No crear carpetas visuales paralelas en la raíz.

### Registro de trazabilidad

`registrar_imagen.py` requiere `--numero-figura`, `--capitulo`, `--ubicacion`, `--fecha-creacion AAAA-MM-DD` y `--archivo`. La fecha debe corresponder a la creación o adaptación real del recurso y no puede estar en el futuro; `fecha_registro` se incorpora por separado. Si no se proporciona `--archivo-original`, el archivo de trabajo se considera también original. Repetir `--derivado` para cada versión adicional; todos los archivos deben existir, ser distintos de las salidas y quedan registrados con ruta absoluta y SHA-256.

Usar `--estado-revision` con `pendiente_revision_editorial`, `requiere_cambios`, `aprobada` o `rechazada`; el valor predeterminado es pendiente. El esquema conserva además `archivo` y `sha256` como campos compatibles, junto con los objetos `archivo_trabajo`, `archivo_original` y la lista `derivados`. Los registros anteriores no se migran ni reescriben automáticamente.

### Selección de ruta y coordinación con imagegen

- **Buscar**: usar la ruta A cuando se necesite evidencia, una obra existente, patrimonio, territorio, especímenes, resultados o una fuente concreta. La licencia se comprueba en la ficha original.
- **Generar raster**: usar `$imagegen` cuando el usuario solicite una ilustración, fotografía conceptual o recurso bitmap original. La herramienta integrada es la vía predeterminada; no pasar al CLI/API ni solicitar credenciales salvo que el usuario elija expresamente esa modalidad.
- **Editar raster**: tratar la imagen existente como objetivo de edición, inspeccionarla primero si está en el sistema de archivos y declarar qué debe cambiar y qué debe permanecer intacto. Guardar una versión nueva salvo autorización explícita para sustituir el original.
- **Crear o editar vector**: para diagramas, organigramas, mapas conceptuales, iconos o SVG con relaciones y rótulos exactos, usar un formato vectorial determinista y editable. No usar `$imagegen` como sustituto raster de un activo que debe seguir siendo SVG o código.
- **Representar datos**: usar una tabla o gráfico reproducible construido desde datos suministrados y verificables; no pedir a un generador que invente valores o escalas.

En generación o edición raster, conservar la intención y especificidad del usuario; no añadir personajes, marcas, textos, estilos o elementos narrativos no solicitados. Para un archivo local que vaya a editarse con la herramienta integrada, visualizarlo antes. Los rótulos científicos o textos que deban ser exactos se añaden después con una herramienta determinista si la generación no los reproduce fielmente.

#### Anatomía, veterinaria y ciencias morfológicas

Cuando una obra de anatomía humana, anatomía comparada, veterinaria, medicina, biología, zoología, cirugía u otra ciencia morfológica requiera generar ilustraciones raster, usar por defecto un acabado **hiperrealista y tan próximo a la realidad observable como permita la finalidad pedagógica**. No convertir estas imágenes en dibujos estilizados, caricaturas, fantasía, estética publicitaria ni anatomía genérica.

Antes de generar, fijar en la ficha y trasladar al prompt, según corresponda: especie o población; región y estructura; vista, plano y lateralidad; postura u orientación; edad, sexo o etapa biológica cuando alteren la morfología; escala relativa; tejidos, coloración, textura y relaciones espaciales; estado normal o patológico; estructuras que deben verse y elementos que deben excluirse. Sustentar estos rasgos en atlas, literatura o fuentes científicas verificables y no completar vacíos con invenciones plausibles.

La apariencia hiperrealista no demuestra exactitud. Revisar el resultado estructura por estructura contra las referencias antes de aprobarlo; comprobar número, posición, inserciones, continuidad, simetría o asimetría, proporciones y diferencias interespecíficas. Solicitar revisión de una persona experta cuando la imagen vaya a enseñar diagnóstico, cirugía, disección o identificación anatómica. Si no puede verificarse una estructura esencial, regenerar o corregir la imagen y mantenerla como `requiere_cambios`.

No presentar una generación hiperrealista como fotografía clínica, disección real, espécimen, micrografía, radiografía ni evidencia experimental. Mantener su rótulo de ilustración generada y preferir una fotografía o registro real verificable cuando la función documental lo exija.

Un recurso destinado al proyecto debe copiarse desde la ubicación de salida de `$imagegen` a `06_recursos_visuales/imagenes/` o al destino pedido, con nombre versionado y sin sobrescribir implícitamente. Después, ejecutar la inspección técnica raster y registrar original, derivados, modelo, prompt, fecha, decisión de procedencia y estado de revisión.

### Ruta A: localizar y descargar

Buscar en Internet cuando el usuario solicite una imagen existente o cuando la exactitud documental lo exija. Preferir fuentes primarias y repositorios institucionales. Leer `references/fuentes-y-licencias.md` antes de seleccionar o descargar.

Verificar en la página del recurso, no en el buscador:

- autor o institución responsable;
- título o descripción del recurso;
- fecha y versión, si existen;
- URL de la ficha original o DOI;
- licencia específica del archivo;
- restricciones de edición, uso comercial y atribución;
- resolución y formato disponibles.

Descargar solo si la licencia permite el uso previsto o si el usuario acredita permiso. Conservar el archivo original sin alteraciones y trabajar sobre una copia. Si la licencia es ambigua, entregar el enlace y solicitar permiso en lugar de descargar o integrar.

No usar Google Images, Pinterest, blogs, agregadores ni redes sociales como fuente final. Pueden servir para descubrir el repositorio original. Una imagen visible sin licencia explícita no se considera abierta.

### Ruta B: generar una imagen original

Usar `$imagegen` para la creación o edición raster cuando corresponda. Formular el prompt con propósito editorial, composición, estilo, relación de aspecto, espacio para rotulación y restricciones científicas. Para gráficos o diagramas vectoriales deterministas, conservar la ruta SVG indicada arriba.

En anatomía, veterinaria y ciencias morfológicas, incluir explícitamente en el prompt el acabado hiperrealista, la fidelidad a la realidad observable y las especificaciones anatómicas definidas en la ficha. No confiar en términos vagos como `anatomía correcta`: enumerar las estructuras y relaciones que deben comprobarse y las deformaciones que deben evitarse.

No generar como sustituto de:

- una micrografía, radiografía, fotografía clínica o registro experimental;
- un mapa que pretenda precisión cartográfica;
- un gráfico con valores no suministrados;
- una reconstrucción histórica presentada como documento;
- una figura que imite deliberadamente el estilo identificable de un artista vivo.

Rotular el resultado como `Ilustración original generada con asistencia de IA` cuando la política editorial o institucional lo requiera. Revisar manualmente texto incrustado, anatomía, escalas, símbolos, relaciones espaciales y posibles estereotipos. No conservar rótulos generados defectuosos: añadirlos después con una herramienta apropiada.

El pie o nota debe identificar el modelo generador y la fecha. El anexo separado debe conservar el prompt literal, la razón de generación, la necesidad que satisface y, cuando corresponda, las búsquedas previas que no ofrecieron una alternativa abierta adecuada.

No incrustar en el lienzo el número de figura, título editorial, nota ni referencia. En APA 7 pertenecen al documento: número en negrita y título en cursiva sobre la figura; nota y atribución debajo. Conservar `<title>` en SVG únicamente como metadato de accesibilidad no visible.

Para una creación íntegra asistida por IA, declarar `Ilustración original generada con asistencia de [modelo], [fecha]`. Para una adaptación asistida, declarar `Adaptación vectorial realizada con asistencia de [modelo], [fecha], a partir de...`. Incorporar las fuentes conceptuales mediante cita APA normal y aclarar cuando el recurso no represente datos empíricos.

### Pies, atribución y archivo

Seguir las plantillas de `references/pies-y-trazabilidad.md`. En APA 7, integrar procedencia y aclaraciones dentro de una nota única; usar fórmulas separadas como `Fuente:` solo cuando otra norma editorial las exija.

Usar nombres como `fig-03-02-ciclo-agua-v01.png`; evitar `imagen_final2.png`. Para impresión, preferir SVG/PDF en diagramas y gráficos, y TIFF/PNG/JPEG de resolución suficiente en imágenes rasterizadas. No prometer una resolución efectiva sin comprobar dimensiones y tamaño de impresión.

#### Inspección técnica raster

El inspector decodifica el archivo completo con Pillow, informa formato, modo, dimensiones, fotogramas, canal alfa, presencia real de píxeles transparentes y PPI efectivo calculado desde el ancho final indicado. Ejemplo desde la raíz de la colección:

```text
python editor-en-jefe/scripts/ejecutar.py gestor-imagenes-academicas-libros/scripts/inspeccionar_imagen.py "ruta/figura.png" --ancho-cm 15 --ppi-minimo 300 --out "ruta/informe-figura.json"
```

El perfil está fijado en `scripts/requirements-lock.txt`. Instalarlo en un entorno aislado con `python -m pip install --only-binary=:all: -r gestor-imagenes-academicas-libros/scripts/requirements-lock.txt`. Salida 0 significa imagen íntegra que alcanza el PPI mínimo; 1 indica baja resolución o archivo rechazado por daño; 2 corresponde a argumentos, rutas, dependencias o destinos inválidos. `--overwrite` debe ser explícito para reemplazar un informe existente.

La transparencia se informa, no se considera por sí sola un defecto. El PPI se calcula con el ancho proporcionado y no con el metadato DPI incrustado. La inspección automatizada cubre formatos raster compatibles con Pillow; no prueba exactitud científica, legibilidad, color de impresión ni el renderizado final. Para SVG/PDF y para toda integración editorial, conservar la inspección visual en el DOCX/PDF final.

### Integración con otras skills

- Coordinar con `$imagegen` únicamente para generar o editar recursos raster; esta skill mantiene la decisión académica, procedencia, licencia, inspección y trazabilidad.
- Coordinar con `$editor-en-jefe` para ubicación, secuencia y control de preentrega.
- Coordinar con `$constructor-tesis-academica` o `$redaccion-articulo-cientifico-imryd` cuando una figura represente método, resultados o discusión.
- No modificar citas ni bibliografía al preparar pies de figura.

### Criterios de cierre

No declarar terminada una imagen hasta comprobar:

- función clara y referencia desde el texto;
- fidelidad científica o señalización explícita como ilustración;
- en anatomía, veterinaria y ciencias morfológicas: acabado hiperrealista, comparación estructura por estructura con referencias verificables y estado `requiere_cambios` mientras exista una discrepancia esencial;
- archivo accesible y formato adecuado;
- pie y texto alternativo;
- fuente y licencia verificadas;
- registro de cambios si hubo adaptación;
- manifiesto de trazabilidad creado.
- ausencia de recursos decorativos o incluidos por cuota;
- anexo de prompts generado cuando existan imágenes asistidas por IA.
- decisión de procedencia documentada antes de cada generación: búsqueda verificable o justificación explícita de que no aplica;
- SVG maestro editable en recursos diagramáticos;
- número, título, nota y cita fuera del lienzo;
- inspección del SVG y de su representación en el DOCX sin recortes ni desbordes.

## Recursos incluidos

### Herramientas automatizadas

| Recurso | Función |
| --- | --- |
| [`scripts/inspeccionar_imagen.py`](../../gestor-imagenes-academicas-libros/scripts/inspeccionar_imagen.py) | Inspeccionar integridad, dimensiones, transparencia y PPI efectivo de una imagen raster. |
| [`scripts/registrar_imagen.py`](../../gestor-imagenes-academicas-libros/scripts/registrar_imagen.py) | Crear o actualizar un manifiesto JSONL de imágenes editoriales. |
| [`scripts/requirements-lock.txt`](../../gestor-imagenes-academicas-libros/scripts/requirements-lock.txt) | Dependencias Python fijadas para esta herramienta. |

### Referencias

| Recurso | Función |
| --- | --- |
| [`references/fuentes-y-licencias.md`](../../gestor-imagenes-academicas-libros/references/fuentes-y-licencias.md) | Fuentes y licencias |
| [`references/pies-y-trazabilidad.md`](../../gestor-imagenes-academicas-libros/references/pies-y-trazabilidad.md) | Pies y trazabilidad |

### Pruebas

| Recurso | Función |
| --- | --- |
| [`tests/test_inspeccionar_imagen.py`](../../gestor-imagenes-academicas-libros/tests/test_inspeccionar_imagen.py) | Pruebas del inspector técnico de imágenes rasterizadas. |
| [`tests/test_registrar_imagen.py`](../../gestor-imagenes-academicas-libros/tests/test_registrar_imagen.py) | Pruebas de coherencia académica del manifiesto de imágenes. |

### Configuración de interfaz

| Recurso | Función |
| --- | --- |
| [`agents/openai.yaml`](../../gestor-imagenes-academicas-libros/agents/openai.yaml) | Metadatos de interfaz e invocación de la skill. |

## Fuente normativa

Esta ficha se genera desde [`gestor-imagenes-academicas-libros/SKILL.md`](../../gestor-imagenes-academicas-libros/SKILL.md), que permanece como contrato normativo. Regenera la ficha después de modificar ese archivo.
