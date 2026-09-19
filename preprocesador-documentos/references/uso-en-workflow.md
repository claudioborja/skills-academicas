# Uso En Workflow

## Regla De Enrutamiento

Si el usuario entrega un archivo largo, PDF, DOCX, HTML, TXT o Markdown extenso, ejecutar primero:

1. `documento_a_markdown.py`
2. `segmentar_manuscrito.py`
3. `proteger_bloques.py`

Después activar la skill especializada según el resultado:
- tesis o marcas universitarias: `$convertidor-tesis-a-libro`;
- artículo IMRyD/IMRAD: `$redaccion-articulo-cientifico-imryd`;
- citas y referencias: `$gestor-referencias-academicas`;
- prosa mecánica o genérica: `$humanizar-redaccion-academica`;
- tablas/figuras: `$gestor-tablas-figuras-pies`;
- cierre formal: `$maquetacion-academica-preentrega`.

En proyectos de libro inicializados por `$planificador-obra-academica`, guardar originales en `00_contexto_y_diagnostico/originales` y todas las salidas de conversión, segmentación y protección en `00_contexto_y_diagnostico/preprocesado`.

## Principio De Ahorro De Tokens

El agente debe leer primero:
- índice de secciones;
- segmentos relevantes;
- inventario de bloques protegidos;
- advertencias y próximos pasos.

Solo debe leer el documento completo si la tarea lo exige.
