# Gestor De Tablas Figuras Y Pies

Úsalo cuando el usuario necesite decidir, crear, revisar, uniformar o exportar tablas, figuras, gráficos, títulos, numeración, fuentes, notas al pie, llamadas en el texto y criterios de presentación visual dentro de un documento académico o editorial, especialmente cuando las tablas Markdown deban conservarse como tablas editables en Word o publicarse en HTML para facilitar su revisión y copia.

## Ejemplo de uso

```text
Usa $gestor-tablas-figuras-pies para revisar las tablas, figuras y notas de este documento.
```

## Guía operativa

El exportador HTML exige `--overwrite` para reemplazar informes. El registrador añade datos mediante publicación atómica y exige manifiesto y anexo distintos. Requieren el helper del orquestador y un solo proceso escritor. Consultar [protección y límites de escritura](../../editor-en-jefe/references/portabilidad.md#protección-de-informes).

### Ejecución multiplataforma

Consultar [la guía común de ejecución](../../editor-en-jefe/references/portabilidad.md) para elegir intérprete y preparar dependencias.

### Automatización Previa

Si el documento está en Markdown/TXT o fue convertido por `$preprocesador-documentos`, ejecutar primero `$auditor-documental-academico`, especialmente `scripts/inventariar_tablas_figuras.py`, para obtener títulos, numeración, tablas Markdown y llamadas en texto antes de intervenir editorialmente.

### Objetivo

Este skill organiza el aparato visual y paratextual del documento. Su función es asegurar que tablas, figuras y notas estén justificadas, bien nombradas, bien llamadas desde el texto y uniformemente presentadas.

### Regla de necesidad y procedencia

No incluir tablas ni figuras por decoración, simetría, cuota por capítulo o automatismo. Cada recurso debe responder a una pregunta, condensar una comparación, organizar evidencia, mostrar una relación o facilitar una decisión. Si el contenido se entiende igual o mejor en una frase breve, omitir la tabla.

Copiar únicamente tablas de fuentes verificadas de acceso abierto con licencia compatible. Conservar fuente, DOI o URL, licencia y ubicación original. Se permite traducirlas, pero la nota debe indicar `Traducida de...`; si cambia estructura o contenido, indicar `Traducida y adaptada de...` y describir los cambios.

Generar una tabla solo cuando sea una elaboración analítica necesaria para la obra y no exista una tabla abierta adecuada. Si interviene un modelo generativo, indicar modelo y fecha en la nota y registrar prompt literal y razón en `09_entregables/v02_revision/anexos/anexo_prompts_recursos_generados.md`. Nunca presentar como evidencia valores inventados por un modelo.

### Cuándo usarlo

- cuando el documento usa tablas o figuras
- cuando la numeración o las leyendas están desordenadas
- cuando hay llamadas en el texto inconsistentes
- cuando la obra necesita limpieza visual y editorial

### Flujo de trabajo

1. Revisa inventario de tablas, figuras y notas.
2. Verifica si cada elemento tiene función real.
3. Uniforma títulos, fuentes, notas y numeración.
   - Numerar tablas en una única secuencia continua para toda la obra: `Tabla 1`, `Tabla 2`, `Tabla 3`. No reiniciar la numeración por capítulo ni usar formas como `Tabla 5.1`, salvo exigencia editorial expresa.
   - Mantener una secuencia independiente y también continua para las figuras: `Figura 1`, `Figura 2`, `Figura 3`.
4. Revisa llamadas en el texto y ubicación.
   - Introducir cada recurso mediante una llamada previa que explique su función en el argumento.
   - Después de la nota, incorporar un párrafo de análisis sustantivo y una transición antes de preguntas, otro recurso o un nuevo apartado.
   - No considerar la tabla o figura como evidencia autoexplicativa ni usar las preguntas de reflexión como cierre analítico.
5. Sugiere simplificaciones o reubicaciones.
6. Mantén las tablas estructuradas en Markdown durante la redacción; no las conviertas manualmente en texto alineado.
7. Antes de entrega, coordina con `$maquetacion-academica-preentrega` para generar un DOCX con tablas nativas.
8. Aplicar a título, numeración, nota, fuente, cita y referencia las reglas de `$gestor-referencias-academicas` u otra skill normativa seleccionada.
9. Registrar procedencia, traducción, generación y justificación con `scripts/registrar_tabla.py`.

### Presentación APA 7

Si el destino es IEEE, no aplicar este apartado: leer [presentación IEEE](../../maquetacion-academica-preentrega/references/ieee-presentacion.md). La plantilla IEEE usa convenciones propias (tablas en romanos y pies de figuras debajo), que prevalecen sobre las preferencias genéricas anteriores.

Cuando la norma activa sea APA 7:

Consultar [la guía APA de maquetación](../../maquetacion-academica-preentrega/references/apa7-docx.md). Las políticas anteriores de acceso abierto, registro de prompts y análisis inmediatamente posterior pertenecen al perfil editorial, no a APA; no imponerlas al corregir solo la norma. Las tablas/figuras de apéndices usan identificación propia (p. ej., A1), no la serie principal.

- colocar el número de tabla o figura en negrita y alineado a la izquierda;
- colocar el título en cursiva, en la línea siguiente y antes del recurso;
- situar la imagen después del número y del título, nunca antes;
- colocar notas debajo cuando sean necesarias; en la general, etiqueta `Nota.` en cursiva; distinguir notas específicas y de probabilidad;
- integrar atribución, adaptación, traducción, licencia y aclaraciones dentro de una única nota cuando sea posible;
- evitar títulos al pie, pies duplicados y secuencias separadas de `Fuente:` y `Nota:`;
- usar en tablas bordes horizontales mínimos: borde superior, separación bajo el encabezado y borde inferior; omitir cuadrículas completas y bordes verticales;
- mantener llamadas explícitas en el texto antes de cada recurso.

### Salidas para tablas

Priorizar, en este orden:

1. **DOCX con tablas nativas:** salida principal cuando el usuario trabajará en Microsoft Word.
2. **HTML con índice y anclas:** salida auxiliar para revisar o copiar tablas desde el navegador.
3. **TXT:** salida de preservación y lectura; no usarla como fuente para reconstruir tablas en Word.

Para crear el HTML auxiliar:

```text
python skills/editor-en-jefe/scripts/ejecutar.py gestor-tablas-figuras-pies/scripts/exportar_tablas_html.py "ruta/02_manuscrito/libro_completo.md" --out "ruta/06_recursos_visuales/tablas_html/tablas_del_libro.html"
```

El script detecta tablas Markdown, reutiliza como título la línea inmediatamente anterior cuando comienza con `Tabla`, y genera enlaces internos para cada elemento.

### Validación final

- cada tabla o figura cumple una función
- la numeración es consistente
- las tablas siguen una secuencia global continua y no una numeración por sección, salvo excepción editorial documentada
- las llamadas en el texto existen y son correctas
- las fuentes y notas son uniformes
- el DOCX conserva filas y columnas como celdas editables
- el HTML auxiliar incluye título, número y enlace interno para cada tabla
- cada recurso tiene una justificación editorial explícita y no decorativa
- cada recurso tiene análisis posterior; no existen secuencias directas entre su nota y preguntas, otro recurso o un encabezado
- el párrafo posterior interpreta relaciones, implicaciones o límites en vez de repetir el título, las celdas o la descripción visual
- las tablas copiadas o traducidas tienen acceso abierto y licencia verificados
- los recursos generados conservan modelo, fecha, prompt y razón en anexo separado
- títulos, notas, citas y referencias cumplen la norma bibliográfica seleccionada

## Recursos incluidos

### Herramientas automatizadas

| Recurso | Función |
| --- | --- |
| [`scripts/exportar_tablas_html.py`](../../gestor-tablas-figuras-pies/scripts/exportar_tablas_html.py) | Exportar tablas Markdown a una página HTML con índice y anclas. |
| [`scripts/registrar_tabla.py`](../../gestor-tablas-figuras-pies/scripts/registrar_tabla.py) | Registrar procedencia y necesidad de una tabla editorial. |

### Configuración de interfaz

| Recurso | Función |
| --- | --- |
| [`agents/openai.yaml`](../../gestor-tablas-figuras-pies/agents/openai.yaml) | Metadatos de interfaz e invocación de la skill. |

## Fuente normativa

Esta ficha se genera desde [`gestor-tablas-figuras-pies/SKILL.md`](../../gestor-tablas-figuras-pies/SKILL.md), que permanece como contrato normativo. Regenera la ficha después de modificar ese archivo.
