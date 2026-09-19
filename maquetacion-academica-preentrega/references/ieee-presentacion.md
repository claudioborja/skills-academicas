# IEEE: presentación según publicación

Usar junto con [citas y referencias IEEE](../../gestor-referencias-academicas/references/ieee-practico.md). Distinguir una obra que solo usa citas IEEE de un manuscrito destinado a una revista/conferencia IEEE.

## Elegir plantilla y alcance

1. Identificar destino, tipo de artículo y fase (revisión o versión final). Obtener plantilla Word/LaTeX e instrucciones desde la publicación o IEEE Author Center; no imponer universalmente dos columnas, un tamaño o un límite de palabras.
2. Registrar fecha/versión de plantilla y requisitos. Si una universidad adapta IEEE, documentar diferencias sin llamarlas norma IEEE general.
3. Conservar las instrucciones de anonimización, autoría, ORCID, afiliaciones, financiación y declaraciones que correspondan. No inventar datos faltantes.

## Revisión de contenido y presentación

- Título, autoría, afiliaciones y primeras notas según plantilla. Resumen y términos de índice según destino; comprobar restricciones a citas, abreviaturas y ecuaciones en el resumen.
- Jerarquía de secciones IEEE, a menudo I., A., 1), a), según nivel y plantilla. No heredar los cinco niveles APA ni numerar todos los rótulos especiales como secciones del cuerpo.
- Ecuaciones, símbolos, unidades y números: formato y numeración consistentes, variables definidas y referencias cruzadas verificadas; no modificar datos para obtener apariencia uniforme.
- Tablas: rótulo TABLE y número romano, con título encima, conforme a plantilla. Figuras: Fig. y número arábigo, pie debajo. Mantener series independientes y orden de primera mención.
- No trasladar automáticamente la secuencia APA «número y título encima de figura». Revisar leyendas, tamaños, resolución, color accesible y derechos de reutilización. Notas/créditos se integran según el destino, no como una nota APA obligatoria.
- Referencias: números en columna propia, entradas alineadas; verificar estilo tipográfico, abreviaturas y puntuación con la guía bibliográfica.
- Apéndices, agradecimientos, material suplementario y biografías solo según tipo de publicación; no exigir biografías a toda ponencia.
- Revisar lenguaje inclusivo, integridad, permisos y declaraciones de uso de IA según políticas vigentes del destino.

## Límites del conversor local

`markdown_a_docx.py` no tiene un modo IEEE completo. **No ejecutar `--apa7-strict` para IEEE.** Su perfil predeterminado de libro tampoco equivale a la plantilla de un artículo IEEE.

Aunque acepta `--template`, el conversor normaliza estilos y formato, por lo que una plantilla no garantiza conservación íntegra de IEEE. Usar el conversor solo como intermedio de contenido/tablas y terminar en la plantilla oficial, o trabajar directamente en Word/LaTeX. No entregar su salida como IEEE final sin revisión.

No usar `auditar_docx_apa7.py` para aprobar/rechazar IEEE. Ejecutar el auditor bibliográfico en modo IEEE, revisar la plantilla y renderizar el documento; comprobar columnas, encabezados, pies, saltos, ecuaciones, tablas y referencias. Si no se puede renderizar, declarar revisión visual pendiente.

## Entrega

Informar controles ejecutados, versión de plantilla, excepciones y pendientes. Cero alertas de citas no demuestra cumplimiento editorial integral. No renumerar ni eliminar fuentes automáticamente por una advertencia heurística.

Fuentes: [manual editorial IEEE](https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/IEEE-Editorial-Style-Manual-for-Authors.pdf) y [IEEE Author Center](https://ieeeauthorcenter.ieee.org/). Para exigencias específicas y cambios recientes prevalecen las instrucciones verificadas del destino.
