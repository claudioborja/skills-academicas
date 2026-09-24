# Revisión Sistemática PRISMA

Planifica, documenta, audita y redacta revisiones sistemáticas y metaanálisis con PRISMA 2020, PRISMA-P y PRISMA-S, seleccionando extensiones oficiales cuando corresponda. Usar para protocolos, búsquedas reproducibles, cribado, diagramas de flujo, matrices de cumplimiento, síntesis y reporte transparente; no usar como sustituto de un método de conducción disciplinar ni para revisiones Kitchenham.

## Ejemplo de uso

```text
Usa $revision-sistematica-prisma para planificar, documentar y auditar una revisión sistemática con PRISMA 2020 y las extensiones que correspondan.
```

## Guía operativa

### Autoridad y límite metodológico

Tratar PRISMA como guía de **reporte transparente y completo**, no como certificado de calidad ni método autosuficiente para conducir una revisión. Antes de actuar, distinguir:

- guía de reporte: PRISMA 2020 y extensiones aplicables;
- protocolo: PRISMA-P para documentarlo, más el método de conducción elegido;
- búsqueda: PRISMA-S para reportarla, más técnicas de recuperación de información;
- conducción: manual o estándar disciplinar declarado por el proyecto;
- evaluación: herramientas de riesgo de sesgo y certeza adecuadas a los diseños;
- síntesis: método narrativo, cualitativo o cuantitativo compatible con los datos.

No afirmar “se realizó la revisión según PRISMA” si PRISMA es la única base metodológica. Preferir “se reportó conforme a PRISMA 2020” y nombrar por separado el método de conducción.

Leer [fuentes oficiales](../../revision-sistematica-prisma/references/fuentes-oficiales.md) antes de citar PRISMA o elegir documentos. No copiar una lista obsoleta de PRISMA 2009 cuando corresponde PRISMA 2020.

### Enrutamiento

1. Confirmar el tipo de producto: protocolo, revisión sistemática, revisión actualizada, revisión viva, metaanálisis o revisión de alcance.
2. Consultar [selección de guía y extensiones](../../revision-sistematica-prisma/references/seleccion-guia-extension.md).
3. Si es una revisión de alcance, usar PRISMA-ScR y un método de conducción para scoping reviews; no presentarla como revisión sistemática de efectos.
4. Si es una revisión de ingeniería de software regida por Kitchenham, usar `$revision-sistematica-kitchenham`. No combinar autoridades salvo exigencia explícita y documentada del usuario, revista o institución.
5. Si el usuario solo pide auditar un manuscrito existente, no rehacer la revisión ni cambiar criterios sin autorización.

### Resultado esperado

Mantener trazabilidad entre pregunta, protocolo, búsqueda, registros, informes, estudios, decisiones, extracción, análisis y reporte. Entregar, según alcance:

- justificación y pregunta estructurada;
- protocolo versionado y registro o razón de no registro;
- estrategias completas por fuente y bitácora de búsquedas;
- conjunto bruto, deduplicado y seleccionado;
- razones de exclusión a texto completo;
- relación correcta entre registros, informes y estudios;
- evaluación de riesgo de sesgo y, cuando proceda, certeza;
- extracción y síntesis trazables;
- conteos coherentes y diagrama PRISMA adecuado;
- matriz PRISMA 2020 con ubicación y evidencia;
- limitaciones, financiación, conflictos y disponibilidad de materiales.

### Flujo de trabajo

#### 1. Definir necesidad, pregunta y alcance

- Localizar revisiones previas y explicar por qué se requiere una nueva, actualización o revisión viva.
- Formular objetivos y preguntas con PICO u otro marco pertinente; no forzar PICO fuera de preguntas de intervención.
- Definir población o contexto, fenómeno/intervención, comparadores, resultados, diseños, idiomas, periodo y fuentes.
- Separar criterios de elegibilidad de filtros técnicos de búsqueda.
- Identificar usuarios, decisiones que informará la revisión y productos requeridos.

Puerta: la pregunta es respondible, la necesidad está justificada y los datos requeridos pueden observarse.

#### 2. Seleccionar documentos PRISMA aplicables

- Base: PRISMA 2020 para el informe final.
- Protocolo: PRISMA-P 2015.
- Búsqueda: PRISMA-S.
- Resumen: PRISMA 2020 for Abstracts.
- Extensión temática o de diseño: añadir solo la oficial que corresponda.

Registrar versión, referencia, URL oficial, fecha de consulta y justificación. No mezclar listas como si todos sus ítems fueran obligatorios para toda revisión.

#### 3. Construir y congelar el protocolo

Aplicar [protocolo y búsqueda](../../revision-sistematica-prisma/references/protocolo-busqueda.md). Especificar antes de revisar resultados:

- pregunta, objetivos y elegibilidad;
- fuentes, cadenas, límites y búsqueda complementaria;
- deduplicación y unidad de selección;
- revisores, pilotaje y resolución de desacuerdos;
- datos, resultados y supuestos;
- riesgo de sesgo, síntesis, heterogeneidad y sensibilidad;
- sesgo de publicación y certeza cuando correspondan;
- subgrupos, metarregresión u otros análisis planificados;
- enmiendas, actualización de búsqueda, datos y código compartibles.

Versionar el protocolo. Registrar toda desviación con fecha, motivo, impacto y etapa en que se decidió. No reescribir el protocolo retrospectivamente para que coincida con los resultados.

#### 4. Diseñar y ejecutar búsquedas reproducibles

- Seleccionar bases, registros y otras fuentes por cobertura y complementariedad, no por cuota.
- Conservar la estrategia completa tal como se ejecutó para cada fuente: plataforma, campos, sintaxis, límites y fecha.
- Registrar deduplicación, automatización, búsqueda de citas, referencias, literatura gris y contacto con autores cuando se usen.
- Identificar quién diseñó, revisó y ejecutó la búsqueda.
- Exportar resultados brutos sin sobrescribirlos y conservar fecha, formato y procedencia.
- Actualizar la búsqueda cerca del cierre si el protocolo, la revista o la velocidad del campo lo requieren.

No afirmar exhaustividad absoluta. Describir fuentes no accesibles y su impacto.

#### 5. Deduplicar y seleccionar

- Distinguir **registro**, **informe** y **estudio**; varios informes pueden corresponder a un estudio.
- Preservar el conjunto bruto y documentar reglas/herramienta de deduplicación.
- Pilotear criterios con una muestra antes del cribado definitivo.
- Registrar decisiones por fase y revisor; resolver desacuerdos como indique el protocolo.
- Conservar una razón primaria, específica y mutuamente interpretable por informe excluido a texto completo.
- No inventar conteos ausentes a partir del diagrama o del manuscrito.

Si trabaja un solo revisor, declararlo y explicar las salvaguardas adoptadas; no simular doble revisión.

#### 6. Extraer, evaluar y sintetizar

Aplicar [evaluación y síntesis](../../revision-sistematica-prisma/references/evaluacion-sintesis.md).

- Pilotear el formulario y conservar localizadores para cada dato.
- Usar una herramienta de riesgo de sesgo apropiada al diseño; no confundir calidad de reporte con riesgo de sesgo.
- Definir medidas de efecto y transformaciones antes de combinar resultados.
- Sintetizar solo grupos defendibles; documentar exclusiones de cada síntesis.
- Explicar heterogeneidad, datos faltantes, sensibilidad, sesgo de reporte y certeza cuando sean aplicables.
- Separar ausencia de evidencia de evidencia de ausencia.
- Mantener conclusiones proporcionales al corpus, riesgo de sesgo y certeza.

Un metaanálisis no es obligatorio. No combinar estudios incompatibles para producir una estimación global.

#### 7. Construir el flujo PRISMA

Leer [flujo y trazabilidad](../../revision-sistematica-prisma/references/flujo-trazabilidad.md). Elegir la plantilla oficial para revisión nueva o actualizada y según use solo bases/registros o también otras fuentes.

Partir de registros reales y decisiones persistidas. Comprobar la aritmética con:

```text
python revision-sistematica-prisma/scripts/auditar_prisma.py flow-check \
  --input revision-sistematica-prisma/assets/conteos-flujo-ejemplo.json
```

El script detecta incoherencias mecánicas; no genera evidencia ni valida la corrección de las decisiones.

#### 8. Redactar y auditar el informe

Usar la lista de PRISMA 2020 durante la redacción, no solo al final. Para cada subítem registrar estado, sección/página y evidencia concreta en una copia de `assets/matriz-prisma-2020.csv`.

```text
python revision-sistematica-prisma/scripts/auditar_prisma.py checklist-audit \
  --input ruta/matriz-prisma-2020.csv --out ruta/auditoria-prisma.json
```

Estados permitidos:

- `complete`: ubicación y evidencia verificables;
- `partial`: existe información insuficiente;
- `missing`: no se reportó;
- `not_applicable`: no corresponde y se justifica en notas;
- `unverifiable`: el manuscrito afirma algo sin artefacto comprobable.

No marcar un ítem como completo por la presencia de una palabra clave. Revisar el contenido y, para usuarios nuevos, consultar la explicación y elaboración oficial.

#### 9. Preparar el paquete reproducible

Incluir, según permisos y licencias:

- protocolo y enmiendas;
- estrategias y bitácora de búsquedas;
- reglas de deduplicación y selección;
- lista de excluidos a texto completo con razón;
- formularios, matrices y diccionario de datos;
- scripts de análisis y versiones de software;
- lista PRISMA cumplimentada y diagrama;
- datos derivados compartibles y condiciones de acceso.

No publicar textos completos de terceros sin autorización.

### Auditoría y bloqueos

Detener la afirmación de cumplimiento y reportar el problema cuando haya:

- conteos inventados, negativos o incompatibles entre fases;
- estrategias de búsqueda no conservadas;
- criterios cambiados sin enmienda;
- exclusiones a texto completo sin razones;
- mezcla de registros, informes y estudios;
- síntesis sin vínculo a estudios o datos extraídos;
- herramienta de riesgo de sesgo inadecuada o aplicación no documentada;
- metaanálisis incompatible o sin medida de efecto definida;
- matriz marcada como completa sin ubicación/evidencia;
- extensión PRISMA equivocada para el producto;
- afirmación de que PRISMA demuestra calidad metodológica.

Clasificar el cierre como:

- `READY_TO_REPORT`: artefactos y reporte verificables;
- `READY_WITH_LIMITATIONS`: faltas no críticas descritas con efecto;
- `REQUIRES_AMENDMENT`: cambio metodológico que exige enmienda;
- `INCOMPLETE_REPORTING`: faltan elementos PRISMA reportables;
- `BLOCKED`: no puede reconstruirse el proceso o hay evidencia/conteos no fiables.

### Coordinación

- `$gestor-referencias-academicas`: localizar, verificar y citar fuentes; el protocolo decide elegibilidad.
- `$automatizador-referencias`: deduplicación y metadatos; no decide inclusión.
- `$filtro-editoriales-depredadoras`: evaluar procedencia dudosa sin usarlo como exclusión automática no protocolizada.
- `$preprocesador-documentos`: convertir y segmentar textos obtenidos legítimamente.
- `$gestor-tablas-figuras-pies`: integrar diagrama, tablas y llamadas en el manuscrito.
- `$redaccion-articulo-cientifico-imryd`: adaptar el informe a revista sin alterar método o resultados.
- `$revisor-citas-consistencia-bibliografica`: cierre de correspondencia entre citas y referencias.

Consultar [fuentes oficiales](../../revision-sistematica-prisma/references/fuentes-oficiales.md), [selector de extensiones](../../revision-sistematica-prisma/references/seleccion-guia-extension.md), [protocolo y búsqueda](../../revision-sistematica-prisma/references/protocolo-busqueda.md), [evaluación y síntesis](../../revision-sistematica-prisma/references/evaluacion-sintesis.md), [flujo y trazabilidad](../../revision-sistematica-prisma/references/flujo-trazabilidad.md) y [matriz de reporte](../../revision-sistematica-prisma/references/matriz-reporte-prisma-2020.md) solo cuando la fase lo requiera.

## Recursos incluidos

### Herramientas automatizadas

| Recurso | Función |
| --- | --- |
| [`scripts/auditar_prisma.py`](../../revision-sistematica-prisma/scripts/auditar_prisma.py) | Audita conteos del flujo y cobertura documental PRISMA 2020. |

### Referencias

| Recurso | Función |
| --- | --- |
| [`references/evaluacion-sintesis.md`](../../revision-sistematica-prisma/references/evaluacion-sintesis.md) | Evaluación, síntesis y certeza |
| [`references/flujo-trazabilidad.md`](../../revision-sistematica-prisma/references/flujo-trazabilidad.md) | Flujo PRISMA 2020 y trazabilidad |
| [`references/fuentes-oficiales.md`](../../revision-sistematica-prisma/references/fuentes-oficiales.md) | Fuentes oficiales PRISMA |
| [`references/matriz-reporte-prisma-2020.md`](../../revision-sistematica-prisma/references/matriz-reporte-prisma-2020.md) | Matriz de reporte PRISMA 2020 |
| [`references/protocolo-busqueda.md`](../../revision-sistematica-prisma/references/protocolo-busqueda.md) | Protocolo PRISMA-P y búsqueda PRISMA-S |
| [`references/seleccion-guia-extension.md`](../../revision-sistematica-prisma/references/seleccion-guia-extension.md) | Selección de guía y extensión |

### Plantillas y recursos

| Recurso | Función |
| --- | --- |
| [`assets/conteos-flujo-ejemplo.json`](../../revision-sistematica-prisma/assets/conteos-flujo-ejemplo.json) | Datos estructurados o ejemplo: Conteos flujo ejemplo. |
| [`assets/exclusiones-texto-completo.csv`](../../revision-sistematica-prisma/assets/exclusiones-texto-completo.csv) | Plantilla o registro editable: Exclusiones texto completo. |
| [`assets/matriz-prisma-2020.csv`](../../revision-sistematica-prisma/assets/matriz-prisma-2020.csv) | Plantilla o registro editable: Matriz prisma 2020. |
| [`assets/registro-busquedas.csv`](../../revision-sistematica-prisma/assets/registro-busquedas.csv) | Plantilla o registro editable: Registro busquedas. |

### Pruebas

| Recurso | Función |
| --- | --- |
| [`tests/test_auditar_prisma.py`](../../revision-sistematica-prisma/tests/test_auditar_prisma.py) | Pruebas funcionales de la auditoría mecánica PRISMA. |

### Configuración de interfaz

| Recurso | Función |
| --- | --- |
| [`agents/openai.yaml`](../../revision-sistematica-prisma/agents/openai.yaml) | Metadatos de interfaz e invocación de la skill. |

## Fuente normativa

Esta ficha se genera desde [`revision-sistematica-prisma/SKILL.md`](../../revision-sistematica-prisma/SKILL.md), que permanece como contrato normativo. Regenera la ficha después de modificar ese archivo.
