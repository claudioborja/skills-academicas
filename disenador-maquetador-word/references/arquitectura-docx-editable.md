# Arquitectura de un DOCX editable

Leer este documento al crear o reconstruir estilos, secciones, navegación y objetos de Word.

## Estilos como fuente de verdad

Usar estilos con nombres funcionales. Adaptar la lista al contenido real:

- `Título del libro`, `Subtítulo del libro` y datos de portada;
- `Título 1` a `Título 4` para la jerarquía navegable;
- `Cuerpo`, `Primer párrafo` y `Cuerpo sin sangría` cuando la convención los distinga;
- `Cita en bloque`, `Epígrafe`, `Nota`, `Pie de figura` y `Título de tabla`;
- `Lista`, `Código`, `Bibliografía` y estilos de anexos cuando existan.

Configurar en cada estilo solo lo que le corresponde: fuente, tamaño, color, alineación, sangrías, espaciado, interlineado, tabulaciones y reglas de paginación. Reducir al mínimo las excepciones directas. El énfasis local en cursiva o negrita es válido; reconstruir manualmente un título completo no lo es.

Basar estilos derivados en un estilo padre cuando una modificación global deba propagarse. No crear variantes casi idénticas sin una función editorial distinguible.

## Secciones, páginas y folios

- Usar saltos de sección para cambios reales de formato, numeración, orientación, columnas o encabezados.
- Usar saltos de página para aperturas estables; no insertar párrafos vacíos hasta alcanzar la página siguiente.
- Distinguir preliminares, cuerpo y anexos cuando cambien numeración o encabezados.
- Controlar correctamente `Vincular al anterior`; una sección nueva no debe heredar o perder encabezados por accidente.
- Aplicar primera página diferente y páginas pares/impares solo cuando el diseño las utilice.
- Mantener la numeración mediante campos. No escribir folios manualmente.

## Encabezados y pies

Los encabezados deben ayudar a navegar y no competir con el texto. Pueden mostrar parte, capítulo o título abreviado mediante campos vinculados a estilos. Verificar páginas de apertura, páginas en blanco intencionales y cambios de sección.

No colocar información esencial únicamente en encabezados o pies. Mantener distancia suficiente del borde y de la caja de texto. Evitar adornos construidos con caracteres repetidos.

## Índice, leyendas y referencias

- Construir la tabla de contenido desde los niveles de título aprobados.
- Usar leyendas automáticas para tablas y figuras cuando el proyecto lo permita.
- Insertar referencias cruzadas a títulos, tablas, figuras y ecuaciones mediante campos.
- Actualizar todos los campos antes de revisar y antes de entregar. Advertir que Word puede requerir `Ctrl+A` y `F9` para una actualización completa.
- No reemplazar campos por texto fijo para corregir una visualización temporal.

## Paginación resistente

Aplicar las propiedades en estilos o párrafos pertinentes:

- `mantener con el siguiente` para títulos, números, leyendas y otros pares inseparables;
- `mantener líneas juntas` solo donde la fragmentación sea realmente inaceptable;
- control de viudas y huérfanas en el cuerpo;
- salto de página anterior para aperturas que siempre deban comenzar en página nueva.

Evitar el uso indiscriminado de `mantener líneas juntas`: puede crear grandes blancos o páginas inesperadas cuando crezca el texto.

## Tablas

- Mantenerlas como tablas nativas, con filas de encabezado repetibles.
- Definir anchos y alineaciones razonables sin depender de espacios.
- Permitir o impedir división de filas según legibilidad y longitud real.
- No usar tablas invisibles para maquetar todo el documento.
- Si una tabla no cabe, evaluar orientación de sección, división semántica o rediseño; no reducir el texto hasta volverlo ilegible.

## Figuras

- Preferir inserción en línea cuando el documento deba refluir con estabilidad.
- Usar objetos flotantes solo si la composición lo exige y se verifican anclaje, ajuste y posición.
- Conservar proporción y resolución; no estirar la imagen.
- Mantener número, título, figura y nota como una unidad editorial mediante reglas de párrafo.
- Incluir texto alternativo cuando corresponda y evitar incorporar el pie dentro de la imagen.

## Ecuaciones y código

- Mantener ecuaciones como OMML editable y revisar que no pierdan signos, límites ni agrupaciones.
- No convertirlas en capturas para fijar su apariencia.
- Aplicar al código un estilo monoespaciado con espaciado y saltos controlados; evitar cuadros de texto si el bloque puede crecer.
- Tratar líneas demasiado largas de forma editorial, sin alterar código significativo.

## Accesibilidad y metadatos

- Definir el idioma del documento y de pasajes en otra lengua cuando sea viable.
- Conservar el orden lógico de títulos.
- Añadir texto alternativo útil a imágenes informativas.
- No usar solo color para distinguir tipos de contenido.
- Completar título, autor y otras propiedades documentales confirmadas; no inventar metadatos.

## Construcciones frágiles que deben evitarse

- sangrías hechas con espacios o tabulaciones repetidas;
- páginas creadas con retornos vacíos;
- números de capítulos, figuras o páginas escritos manualmente;
- encabezados simulados dentro del cuerpo;
- tablas y ecuaciones rasterizadas;
- capas de cuadros de texto superpuestos;
- objetos flotantes sin anclaje revisado;
- estilos duplicados por copiar contenido de otros documentos;
- cambios de fuente o tamaño aplicados párrafo por párrafo.
