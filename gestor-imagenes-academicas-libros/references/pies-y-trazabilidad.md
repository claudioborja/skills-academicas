# Pies y trazabilidad

## Plantillas

En APA 7, colocar en líneas separadas: `Figura N` en negrita; título en cursiva; recurso; y debajo una nota que comienza con `Nota.` en cursiva. No unir número y título con punto ni incrustarlos dentro del gráfico.

**Reproducción**

`Nota. Tomado de *Título del recurso* [Figura], por A. A. Autor o Institución, año, Fuente (DOI o URL). Copyright/licencia.`

**Adaptación**

`Nota. Adaptado de *Título del recurso* [Figura], por A. A. Autor o Institución, año, Fuente (DOI o URL). Copyright/licencia. Cambios: [describir].`

**Elaboración propia basada en datos**

`Nota. Elaboración propia con datos de [fuente].` Añadir cita autor-fecha y referencia completa.

**Ilustración original asistida por IA**

`Nota. Ilustración original generada con asistencia de [modelo], [fecha], a partir de las fuentes conceptuales citadas ([Autor, año; Autor, año]). Dirección y revisión editorial de [autor/equipo]. El prompt literal y la justificación constan en el anexo de recursos generados. No representa datos empíricos.`

**Adaptación vectorial asistida por IA**

`Nota. Adaptación vectorial realizada con asistencia de [modelo], [fecha], a partir de *Título* [Figura], por Autor o institución, año (DOI o URL). Licencia/permiso. Cambios: [describir]. El prompt literal consta en el anexo de recursos generados.`

En notas con varias fuentes, usar una cita parentética consolidada y ordenada. En español, usar `y` en citas narrativas y `&` dentro de paréntesis. Conservar completos los apellidos compuestos o unidos por guion.

Adaptar estas fórmulas a la norma editorial y a las condiciones específicas de la licencia.

## Texto alternativo

Describir la información relevante y su relación, no cada detalle ornamental. Evitar comenzar con “imagen de”. Para gráficos, resumir tendencia, variables y conclusión principal; no depender únicamente del color.

## Campos mínimos del manifiesto

- identificador y número de figura;
- capítulo y ubicación prevista;
- función: evidencia, reproducción, adaptación o ilustración;
- archivo original y archivo de trabajo;
- autor o institución;
- título, año, DOI o URL permanente;
- licencia y URL de la licencia;
- fecha de consulta;
- necesidad editorial y aporte concreto al lector;
- origen: descargada, adaptada, generada o elaboración propia;
- método: manual, software convencional, IA generativa o código asistido por IA;
- modelo y fecha de generación cuando corresponda;
- prompt literal y razón de generación en anexo separado;
- transformaciones realizadas;
- pie y texto alternativo;
- estado de revisión editorial;
- hash SHA-256, cuando exista un archivo local.

En los registros creados por `registrar_imagen.py`, `fecha_creacion` es la fecha efectiva suministrada por el responsable y `fecha_registro` es la fecha automática de incorporación al manifiesto. `archivo_trabajo` y `archivo_original` son objetos con `ruta` y `sha256`; `derivados` es una lista de objetos con esos mismos campos. Si el recurso no posee un original separado, ambos objetos pueden identificar el mismo archivo. El estado de revisión debe ser uno de: `pendiente_revision_editorial`, `requiere_cambios`, `aprobada` o `rechazada`.
