# Gestor De Control Editorial De Libros

Gestiona la admisibilidad, el front matter, la preparación opcional para BKCI y el control técnico prepublicación de libros académicos. Usar para monografías, libros derivados de tesis, obras colectivas y volúmenes editados cuando se necesite seleccionar una plantilla, comprobar evidencia editorial o documentar autorización y pendientes; no sustituye la transformación de una tesis, la revisión por pares ni la decisión de aceptación.

## Ejemplo de uso

```text
Usa $gestor-control-editorial-libros para seleccionar y documentar el control editorial aplicable a esta obra.
```

## Guía operativa

### Responsabilidad

Convertir requisitos editoriales dispersos en un control trazable del libro como producto. Separar siempre la admisibilidad previa a revisión por pares del control técnico posterior a la aceptación. No presentar una comprobación documental como evaluación científica ni como garantía de indexación.

Si el encargo es transformar el contenido de una tesis, usar primero `$convertidor-tesis-a-libro`. Esta skill recibe el libro ya diagnosticado o transformado y controla su preparación editorial. Si el usuario pide solo diagnóstico, no modificar el manuscrito ni los DOCX.

### Selección Del Modo

1. Identificar tipo de obra, etapa editorial, forma de autoría de los capítulos y destino declarado.
2. Para una recomendación reproducible, ejecutar `scripts/seleccionar_control.py` con un JSON que contenga `tipo_obra`, `autoria_capitulos`, `etapa` y `objetivo_bkci`.
3. Aplicar únicamente los modos resultantes:
   - `control-admisibilidad`: recepción y preparación para revisión por pares;
   - selección de front matter: obra completa o libro por capítulos;
   - `preevaluacion-bkci`: solo si BKCI es un objetivo explícito;
   - `control-tecnico-prepublicacion`: después de la aceptación científica.
4. Registrar cada criterio como `CUMPLE`, `NO_CUMPLE`, `N_A`, `NO_VERIFICABLE` o `PENDIENTE_CONFIRMACION`.
5. Vincular cada estado con evidencia, explicación, acción requerida, responsable y fecha de comprobación. No completar datos institucionales ni personales por inferencia.

Ejemplo:

```bash
python editor-en-jefe/scripts/ejecutar.py gestor-control-editorial-libros/scripts/seleccionar_control.py --input contexto-libro.json --out perfil-control.json
```

Valores admitidos:

- `tipo_obra`: `tesis-convertida`, `monografia`, `obra-colectiva`, `volumen-editado` u `otro`;
- `autoria_capitulos`: `integral`, `independiente` o `por-determinar`;
- `etapa`: `recepcion`, `pre-revision`, `aceptada` o `prepublicacion`;
- `objetivo_bkci`: booleano.

### Guías Bajo Demanda

- Leer [admisibilidad y control prepublicación](../../gestor-control-editorial-libros/references/admisibilidad-y-control.md) para aplicar la ficha, separar etapas y documentar decisiones.
- Leer [selección y contenido del front matter](../../gestor-control-editorial-libros/references/front-matter.md) para elegir entre obra completa y libro por capítulos.
- Leer [perfil BKCI](../../gestor-control-editorial-libros/references/perfil-bkci.md) únicamente cuando el destino declarado sea Book Citation Index; verificar primero la fuente oficial vigente.
- Leer [trazabilidad e informe](../../gestor-control-editorial-libros/references/trazabilidad.md) para registrar hallazgos, pendientes y cierre sin correcciones silenciosas.

Los seis DOCX originales se conservan en `assets/` como formularios, instructivos y plantillas editables. Copiar el recurso pertinente a un destino nuevo; no sobrescribir el original.

### Coordinación

- `$convertidor-tesis-a-libro` cambia el género, la arquitectura y la voz de una tesis; esta skill controla después el expediente, front matter y cierre editorial.
- `$gestor-contribuciones-autoria` decide cómo documentar contribuciones y qué política de autoría corresponde; esta skill comprueba que la decisión confirmada sea consistente en el libro y sus metadatos.
- `$gestor-referencias-academicas` y `$revisor-citas-consistencia-bibliografica` verifican fuentes y correspondencia bibliográfica; esta skill registra su estado dentro del expediente.
- `$disenador-maquetador-word` gobierna el diseño editable y `$maquetacion-academica-preentrega` la comprobación final del artefacto. Esta skill no deshace la dirección visual ni reemplaza esos controles.
- `$verificador-resultados-investigacion` comprueba resultados reutilizados; esta skill no recalcula ni valida datos científicos.

### Límites

- No decidir aceptación, rechazo, autoría, conflictos, permisos, ética, licencias, ISBN o DOI sin autoridad y evidencia.
- No marcar `N_A` para evitar resolver un incumplimiento aplicable.
- No usar un porcentaje de similitud como decisión automática.
- No activar BKCI por rutina ni prometer selección. Clarivate conserva la decisión y solo el editor puede presentar la obra.
- No confundir una tesis sin revisar con un libro derivado de tesis que ya fue transformado, revisado y publicado como obra académica.
- No usar LibreOffice. Conservar DOCX editables y aplicar controles OOXML; la inspección visual final corresponde a Microsoft Word u otro motor autorizado expresamente.

### Entregables

Según el encargo, producir uno o varios de estos resultados:

- perfil de control y plantilla seleccionada;
- ficha de admisibilidad con evidencia y decisión pendiente o confirmada;
- matriz de front matter y metadatos;
- preevaluación BKCI separada de la decisión de Clarivate;
- ficha técnica prepublicación;
- informe consolidado de hallazgos y pendientes, sin incorporarlo al manuscrito como capítulo.

### Cierre

Confirmar que el modo aplicado corresponde a la etapa, la plantilla coincide con la autoría real, los estados tienen evidencia, los datos sensibles o institucionales fueron confirmados, BKCI se trató como perfil condicional y ningún pendiente bloqueante fue ocultado por la maquetación.

## Recursos incluidos

### Herramientas automatizadas

| Recurso | Función |
| --- | --- |
| [`scripts/seleccionar_control.py`](../../gestor-control-editorial-libros/scripts/seleccionar_control.py) | Selecciona el perfil de control editorial de un libro desde contexto JSON. |

### Referencias

| Recurso | Función |
| --- | --- |
| [`references/admisibilidad-y-control.md`](../../gestor-control-editorial-libros/references/admisibilidad-y-control.md) | Admisibilidad Y Control Prepublicación |
| [`references/front-matter.md`](../../gestor-control-editorial-libros/references/front-matter.md) | Selección Y Contenido Del Front Matter |
| [`references/perfil-bkci.md`](../../gestor-control-editorial-libros/references/perfil-bkci.md) | Perfil BKCI |
| [`references/trazabilidad.md`](../../gestor-control-editorial-libros/references/trazabilidad.md) | Trazabilidad E Informe |

### Plantillas y recursos

| Recurso | Función |
| --- | --- |
| [`assets/01_Ficha_control_editorial_libros_EUC.docx`](../../gestor-control-editorial-libros/assets/01_Ficha_control_editorial_libros_EUC.docx) | Ficha de control editorial de libros |
| [`assets/02_Instructivo_ficha_control_editorial_EUC.docx`](../../gestor-control-editorial-libros/assets/02_Instructivo_ficha_control_editorial_EUC.docx) | Instructivo para completar la ficha de control editorial |
| [`assets/03_Guia_18_criterios_BKCI_EUC.docx`](../../gestor-control-editorial-libros/assets/03_Guia_18_criterios_BKCI_EUC.docx) | Guía interna: 18 criterios de evaluación de libros para BKCI |
| [`assets/04_Plantilla_front_matter_obra_completa_EUC.docx`](../../gestor-control-editorial-libros/assets/04_Plantilla_front_matter_obra_completa_EUC.docx) | Plantilla de front matter - obra completa |
| [`assets/05_Plantilla_front_matter_libro_por_capitulos_EUC.docx`](../../gestor-control-editorial-libros/assets/05_Plantilla_front_matter_libro_por_capitulos_EUC.docx) | Plantilla de front matter - libro por capítulos |
| [`assets/06_Instructivo_front_matter_EUC.docx`](../../gestor-control-editorial-libros/assets/06_Instructivo_front_matter_EUC.docx) | Instructivo de uso de las plantillas de front matter |

### Pruebas

| Recurso | Función |
| --- | --- |
| [`tests/test_seleccionar_control.py`](../../gestor-control-editorial-libros/tests/test_seleccionar_control.py) | Pruebas funcionales del selector de control editorial para libros. |

### Configuración de interfaz

| Recurso | Función |
| --- | --- |
| [`agents/openai.yaml`](../../gestor-control-editorial-libros/agents/openai.yaml) | Metadatos de interfaz e invocación de la skill. |

## Fuente normativa

Esta ficha se genera desde [`gestor-control-editorial-libros/SKILL.md`](../../gestor-control-editorial-libros/SKILL.md), que permanece como contrato normativo. Regenera la ficha después de modificar ese archivo.
