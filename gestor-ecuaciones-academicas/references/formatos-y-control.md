# Formatos, notación y control editorial

## Fuente y entrega

Mantener una representación maestra editable y registrar el formato de destino:

| Destino | Representación preferida | Comprobación mínima |
| --- | --- | --- |
| LaTeX/PDF | LaTeX estructurado | Compilar, revisar advertencias y comparar el PDF. |
| Word | OMML nativo | Abrir/renderizar el DOCX y comprobar edición, saltos y alineación. |
| HTML/EPUB | MathML o motor admitido por el destino | Probar accesibilidad y renderizado en el lector objetivo. |
| Canal sin soporte matemático | Derivado SVG/raster más fuente editable | Documentar la pérdida de editabilidad y verificar resolución. |

No asumir que una conversión visualmente aceptable conserva semántica. Comparar antes/después: fracciones, raíces, límites, superíndices, subíndices, acentos, matrices, casos, operadores y caracteres griegos.

## Control matemático y científico

- Definir símbolos cerca de la primera ecuación o mediante una lista inequívoca.
- Mantener distinción entre escalar, vector, matriz, tensor, conjunto y operador.
- Revisar dominios, condiciones iniciales o de frontera y restricciones cuando formen parte del modelo.
- Comprobar unidades término por término; una igualdad con dimensiones incompatibles requiere corrección o justificación.
- Verificar que redondeo, precisión y unidades coincidan con tablas, resultados, código y narrativa.
- Para una transformación algebraica, conservar los pasos necesarios para auditar equivalencia; usar cálculo simbólico solo como apoyo y registrar supuestos.
- En fórmulas tomadas o adaptadas de una fuente, conservar cita y localizador; la ecuación no reemplaza la explicación de su pertinencia.

## Presentación

Seguir primero la plantilla de la revista, universidad o editorial. APA 7 o IEEE no sustituyen instrucciones específicas del destino. Mantener un solo sistema de numeración y referencias automáticas; evitar numerar expresiones que nunca se citan salvo exigencia de la plantilla.

### Numeración de ecuaciones en bloque

Cuando el destino no indique otra convención, aplicar este criterio editorial predeterminado:

- Centrar o componer la ecuación según la plantilla y colocar su número al margen derecho, en la misma línea visual, con números arábigos entre paréntesis: `(1)`, `(2)`, `(3)`.
- Numerar consecutivamente en todo el artículo. En libros, tesis o documentos extensos puede usarse numeración por capítulo o sección —por ejemplo, `(2.1)`— si mejora la localización y se mantiene uniforme. Para apéndices y grupos relacionados, admitir formas como `(A1)` y `(3a)` solo cuando el perfil editorial las contemple.
- En ecuaciones de varias líneas, asignar un único número y alinearlo con la última línea, salvo instrucción distinta de la plantilla.
- Citar cada ecuación numerada en el texto y respetar la forma verbal del destino: `en (1)`, `Ec. (1)` o `ecuación (1)`. No mezclar estas variantes dentro del mismo manuscrito.
- No numerar por defecto fórmulas breves en línea ni ecuaciones en bloque que no se citarán. No reutilizar números ni dejar saltos involuntarios.
- En LaTeX, usar `equation`, `align` u otros entornos con `\label` y `\eqref`; evitar `\tag` manual salvo exigencia justificada. En Word, conservar OMML y referencias cruzadas editables. No alinear el número mediante espacios o tabulaciones manuales.

Esta convención coincide con la práctica de IEEE, Taylor & Francis y Springer Nature, pero no es universal. IEEE usa numeración consecutiva al margen derecho y referencia ordinaria mediante `(1)`; Taylor & Francis recomienda numerar serialmente a la derecha las ecuaciones citadas; Springer Nature suele numerar por capítulo a la derecha en libros. La plantilla específica siempre tiene precedencia.

Usar tipografía matemática coherente: distinguir variables, constantes, operadores, unidades y texto descriptivo conforme a la convención disciplinar y al motor de composición. No insertar espacios manuales para simular alineación. Dividir ecuaciones extensas en puntos matemáticamente válidos, preservando operadores y legibilidad.

Para accesibilidad, acompañar expresiones complejas con una explicación textual de su función y variables. El texto alternativo no debe ser una lectura ambigua de símbolos; usar MathML semántico o la capacidad accesible del formato cuando exista.

## Lista de revisión

- Signos, operadores, paréntesis y delimitadores completos.
- Índices y exponentes unidos al símbolo correcto.
- Fracciones, radicales, sumas, productos, integrales y límites completos.
- Filas, columnas, separadores y casos de matrices o sistemas conservados.
- Variables definidas y usadas con un único significado.
- Unidades, dimensiones, precisión y convenciones consistentes.
- Etiquetas únicas, numeración estable y referencias resueltas.
- Ecuaciones editables y representación final inspeccionada.
