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

