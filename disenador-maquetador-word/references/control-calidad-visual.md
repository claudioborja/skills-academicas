# Control de calidad visual en Word

Leer este documento después de generar o modificar la maqueta y antes de declarar el DOCX listo.

## Renderizado de control

Validar primero estilos, secciones, campos y objetos mediante OOXML. Abrir después una copia temporal en Microsoft Word para inspeccionar páginas representativas cuando esté disponible. LibreOffice no forma parte de este flujo. Cualquier PDF o imagen de control es un instrumento interno: el entregable continúa siendo el DOCX.

Si no es posible renderizar, informar que la validación visual está pendiente. La estructura interna del archivo no demuestra que Word lo presentará correctamente.

Usar un directorio temporal o una carpeta de control separada. No mezclar representaciones de revisión con los entregables ni sustituir el DOCX por ellas.

## Muestra mínima de páginas

Inspeccionar, cuando existan:

- portada, portadilla y página legal;
- índice con entradas cortas y largas;
- primera página de parte o capítulo;
- página de texto denso y página con poco texto;
- cambio entre dos niveles de subtítulo;
- cita extensa, lista, nota o recuadro;
- tabla estrecha y tabla ancha;
- figura horizontal y vertical con sus leyendas;
- ecuación, código o contenido técnico;
- bibliografía y anexos;
- páginas anteriores y posteriores a cada salto de sección.

Revisar también la primera y última página del documento y cualquier página modificada después de la inspección anterior.

## Inspección

### Página y navegación

- tamaño, orientación y márgenes correctos;
- folios continuos y ausentes donde corresponda;
- encabezados adecuados a capítulo, sección y lado de página;
- aperturas coherentes y páginas en blanco intencionales;
- índice actualizado, legible y alineado.

### Tipografía y ritmo

- cuerpo cómodo de leer y líneas de longitud razonable;
- jerarquía clara entre niveles;
- interlineado, sangrías y espaciados consistentes;
- ausencia de títulos aislados, viudas y huérfanas evidentes;
- blancos equilibrados sin relleno artificial.

### Objetos

- tablas dentro de la caja de texto y con encabezados repetidos;
- imágenes sin recorte, deformación o pixelación visible;
- leyendas unidas a su recurso;
- ecuaciones completas y alineadas;
- notas, pies y llamadas sin solapamientos.

### Limpieza

- sin marcas Markdown, instrucciones internas, comentarios no destinados al usuario ni texto oculto accidental;
- sin estilos improvisados visibles;
- sin páginas casi vacías causadas por reglas de paginación incompatibles;
- sin enlaces, campos o referencias con mensajes de error.

## Prueba de reflujo

Trabajar sobre una copia y ejecutar cambios pequeños que representen la edición futura:

1. insertar un párrafo de varias líneas;
2. eliminar un párrafo cercano a un salto de página;
3. añadir un subtítulo con una línea larga;
4. mover una tabla o figura a otra sección;
5. actualizar todos los campos.

El documento debe reorganizarse sin perder numeración, encabezados, índice, leyendas ni asociación entre títulos y contenido. Si aparecen correcciones manuales en cadena, reparar estilos, secciones o anclajes en vez de ajustar las páginas resultantes una por una.

## Cierre

Repetir el renderizado después de corregir. Una inspección anterior no valida cambios posteriores. Entregar únicamente cuando la versión inspeccionada coincida con el DOCX final y no queden problemas conocidos sin declarar.
