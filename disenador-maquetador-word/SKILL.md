---
name: disenador-maquetador-word
description: Diseña y maqueta libros profesionales en Microsoft Word mediante estilos, secciones, campos y objetos nativos editables. Usar cuando el usuario necesite transformar un manuscrito en un DOCX con identidad visual, jerarquía tipográfica, páginas preliminares, aperturas de capítulo, tablas, figuras, encabezados, folios y composición resistente a futuras adiciones o eliminaciones. No sustituye la corrección del contenido ni la validación académica final.
---

# Diseñador y maquetador de libros en Word

## Resultado

Entregar un libro diseñado como `.docx` editable y estable. La composición debe conservar su jerarquía y reorganizarse correctamente cuando se agreguen, eliminen o desplacen párrafos, tablas, figuras o capítulos.

El archivo de publicación sigue siendo Word. Se puede generar una representación temporal en PDF o imágenes únicamente para inspeccionar las páginas; no incluirla como entregable salvo petición expresa.

## Frontera

Esta skill gobierna la dirección visual y la composición del libro en Word:

- formato de página, caja de texto, márgenes y secciones;
- sistema tipográfico y estilos jerárquicos;
- preliminares, aperturas de capítulo, encabezados y folios;
- ritmo de página, blancos, cortes y relación entre texto y recursos;
- navegación, campos, referencias cruzadas y editabilidad;
- inspección visual y corrección de la maqueta.

No reescribir contenido, cambiar datos, alterar citas ni inventar recursos para equilibrar páginas. Derivar la preparación especializada a `$gestor-imagenes-academicas-libros`, `$gestor-tablas-figuras-pies`, `$gestor-ecuaciones-academicas` o `$gestor-codigo-tecnico-editorial` cuando corresponda. Tras el diseño, `$maquetacion-academica-preentrega` comprueba requisitos académicos, institucionales y de entrega; no debe reemplazar la dirección visual ya aprobada.

## Principios no negociables

- Construir la apariencia con estilos de Word y propiedades de sección, no con formato manual repetido.
- Mantener texto, tablas, ecuaciones, títulos, pies y referencias como objetos editables.
- No simular alineación con espacios, tabulaciones repetidas, párrafos vacíos o saltos de línea acumulados.
- Usar saltos de página y de sección solo cuando tengan una función editorial estable.
- Evitar cuadros de texto, objetos flotantes y anclajes frágiles cuando el mismo resultado sea posible dentro del flujo del documento.
- Usar campos automáticos para índice, numeración, encabezados, folios y referencias cruzadas cuando Word los admita.
- Conservar originales y trabajar sobre una copia o una salida nueva. No sobrescribir el único manuscrito editable sin autorización expresa.
- No afirmar que la maqueta está terminada sin renderizarla e inspeccionar páginas representativas y zonas afectadas.

## Entradas y decisiones

Localizar antes de diseñar:

- manuscrito y formato de origen;
- plantilla editorial o identidad visual existente;
- tamaño de página, destino de lectura o impresión y márgenes exigidos;
- lector, género, tono y densidad esperada;
- preliminares, capítulos, anexos y otros tipos de sección;
- familias tipográficas disponibles y autorizadas;
- reglas institucionales o de la editorial;
- tablas, figuras, ecuaciones y código que deban permanecer editables.

Si falta una decisión que impida avanzar, solicitar solo esa información. Si no existe una identidad visual prescrita, proponer un sistema sobrio basado en el género y registrar tipografías, tamaños, color, espaciados y supuestos. Leer [dirección visual y perfiles](references/direccion-visual-y-perfiles.md) cuando deba crearse o reconstruirse ese sistema.

## Flujo de trabajo

### 1. Diagnóstico

Inspeccionar estructura, estilos, secciones, campos, tablas, imágenes, notas, ecuaciones, encabezados y pies del documento. Distinguir contenido real de residuos de edición. Si el origen no es DOCX, coordinar su conversión sin perder jerarquía ni objetos editables.

### 2. Propuesta visual

Definir una sola dirección coherente: formato, caja tipográfica, familias y funciones, escala de títulos, paleta, tratamiento de aperturas, encabezados, tablas, figuras, citas y elementos destacados. No mezclar perfiles decorativos por capítulo.

En libros extensos o cuando la dirección visual sea nueva, preparar primero una muestra representativa que incluya apertura de capítulo, página de texto, una página con recurso visual y una página final o bibliográfica. Aplicar al conjunto después de revisar esa muestra, salvo que el usuario pida ejecución directa.

### 3. Arquitectura editable

Construir o depurar el sistema de estilos antes de ajustar páginas individuales. Usar nombres funcionales y una jerarquía inequívoca. Configurar secciones, encabezados, pies, numeración, tabla de contenido, leyendas y referencias según [arquitectura DOCX editable](references/arquitectura-docx-editable.md).

### 4. Composición

Aplicar el sistema a todo el libro. Resolver aperturas, blancos, viudas, huérfanas, títulos aislados, tablas partidas, figuras separadas de sus leyendas y cambios de sección. Preferir reglas de estilo como `mantener con el siguiente`, control de viudas y huérfanas y saltos anteriores a correcciones locales frágiles.

No forzar una página visualmente llena. El blanco puede cumplir una función jerárquica; debe ser intencional y consistente, no el resultado de párrafos vacíos.

### 5. Inspección visual

Renderizar una copia temporal del DOCX y revisar el libro como páginas. El renderizado es un instrumento de control, no un cambio de formato del entregable. Seguir [control de calidad visual](references/control-calidad-visual.md), corregir la fuente DOCX y volver a renderizar las páginas afectadas.

### 6. Prueba de mantenimiento

Antes del cierre, comprobar en una copia que el documento resiste al menos estas operaciones:

1. agregar y quitar un párrafo de cuerpo;
2. insertar un subtítulo dentro de un capítulo;
3. desplazar una figura o tabla;
4. actualizar índice, numeración, leyendas y referencias cruzadas;
5. añadir o retirar páginas sin romper encabezados, folios ni aperturas.

Revertir los cambios de prueba o ejecutarlos sobre una copia desechable. Corregir la arquitectura si el ajuste exige reparaciones manuales página por página.

## Entrega

Entregar como mínimo:

- el `.docx` diseñado, editable y sin marcas de trabajo;
- una nota breve con el sistema visual aplicado, fuentes necesarias y campos que deben actualizarse en Word;
- pendientes reales, si existen, separados del contenido del libro.

No entregar obligatoriamente PDF, TXT ni imágenes de páginas. No bloquear el documento, convertir texto en curvas, rasterizar tablas o ecuaciones ni acoplar objetos editables para preservar una apariencia fija.

## Criterios de cierre

- La jerarquía se reconoce sin depender únicamente del color.
- Todos los elementos repetidos usan estilos o campos, no formato manual disperso.
- El índice, los folios, las leyendas y las referencias pueden actualizarse.
- Encabezados y pies respetan cambios de parte, capítulo y preliminares.
- Tablas, figuras, ecuaciones y código conservan editabilidad y llamadas correctas.
- No hay títulos, leyendas o primeras líneas aisladas por cortes evitables.
- La tipografía utilizada está disponible o incluye sustituciones documentadas.
- El documento puede crecer o reducirse sin perder su sistema visual.
- La inspección renderizada no muestra desbordes, recortes, solapamientos ni páginas accidentales.
- El entregable principal es un DOCX limpio y preparado para futuras revisiones.
