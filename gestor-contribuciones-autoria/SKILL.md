---
name: gestor-contribuciones-autoria
description: Selecciona, aplica y audita taxonomías de contribución, criterios de autoría y formatos de metadatos según la obra y su destino. Usar para declaraciones de contribuciones, orden y elegibilidad de autoría, reconocimientos, datasets, software, libros, traducciones, JATS, Crossref, DataCite, ORCID o grafos de procedencia; no usar CRediT como criterio automático de autoría ni para resolver disputas sin la política aplicable.
---

# Gestor de contribuciones y autoría

## Responsabilidad

Determinar quién hizo qué, qué personas cumplen los criterios de autoría aplicables y cómo representar esa información en el producto y sus metadatos. Mantener separadas tres capas:

1. **Contribución:** tareas realmente realizadas, normalmente descritas con CRediT u otro vocabulario especializado.
2. **Autoría y responsabilidad:** criterios que determinan firma, aprobación y rendición de cuentas.
3. **Representación técnica:** formato usado para intercambiar nombres, identificadores, roles y procedencia.

CRediT no decide autoría, orden de firma ni importancia. ORCID identifica personas. JATS, Crossref, DataCite, CodeMeta, CFF, MARC y PROV-O transportan o estructuran información; no sustituyen la política de autoría.

## Información mínima

Antes de seleccionar un perfil, identificar:

- tipo de obra o recurso;
- si constituye una salida de investigación;
- disciplina y política de la revista, editorial, repositorio o institución;
- personas y organizaciones participantes;
- tareas efectivamente realizadas y evidencia disponible;
- necesidad de decidir autoría, reconocimientos u orden de firma;
- destinos de metadatos y formatos exigidos;
- identificadores autenticados disponibles, especialmente ORCID.

No exigir todos los datos para una orientación preliminar. Marcar lo desconocido y no convertir supuestos en asignaciones definitivas.

## Selección del perfil

Usar [selección de perfiles](references/seleccion-perfiles.md) y aplicar solo las capas necesarias:

- **Artículo, tesis, revisión o informe de investigación:** CRediT como núcleo.
- **Biomedicina:** ICMJE para elegibilidad, CRediT para contribuciones y COPE para integridad o disputas.
- **Dataset:** CRediT más DataCite Contributor Types; añadir el esquema real del repositorio.
- **Software de investigación:** CRediT más CodeMeta o CFF según el artefacto de entrega.
- **Libro, capítulo, traducción o catálogo:** MARC Relator Terms para relaciones bibliográficas; añadir CRediT únicamente si se documentan contribuciones a una salida de investigación.
- **JATS o depósito Crossref:** conservar los roles canónicos y mapearlos según la versión del esquema del destino.
- **Grafo de conocimiento o procedencia:** CRO para granularidad ontológica y PROV-O para agentes, actividades y entidades.

La política explícita del destino prevalece sobre el perfil general. No combinar vocabularios por acumulación: cada uno debe responder a una necesidad concreta.

Puede obtenerse una recomendación mecánica inicial con:

```text
python gestor-contribuciones-autoria/scripts/seleccionar_perfil.py \
  --input gestor-contribuciones-autoria/assets/contexto-ejemplo.json
```

El selector no evalúa contribuciones personales ni adjudica autoría. Su salida debe revisarse contra las instrucciones actuales del destino.

## Flujo de trabajo

### 1. Congelar la autoridad aplicable

Registrar la política de la revista, editorial, universidad, repositorio o financiador, con versión o fecha de consulta. Si varias reglas compiten, aplicar esta precedencia:

1. encargo y requisitos legales o institucionales obligatorios;
2. política vigente del destino;
3. criterio disciplinar reconocido;
4. taxonomía general;
5. convención local documentada.

No aplicar retrospectivamente una norma distinta solo para justificar una lista de autores ya acordada.

### 2. Inventariar contribuciones reales

Entrevistar o solicitar confirmación a los participantes. Registrar tareas observables, artefactos y periodo; después mapearlas al término canónico. Una persona puede tener varios roles y un rol puede corresponder a varias personas.

Usar [roles CRediT](references/roles-credit.md) para evitar asignaciones basadas únicamente en el cargo, antigüedad, financiación, supervisión nominal o posición jerárquica. No asignar contribuciones a herramientas de IA ni tratarlas como autoras responsables.

### 3. Evaluar autoría por separado

Leer [autoría y responsabilidad](references/autoria-responsabilidad.md). Aplicar todos los criterios acumulativos cuando la política lo exija. Clasificar cada participación como:

- autoría confirmada;
- colaboración no autoral o reconocimiento;
- contribución organizacional;
- pendiente de confirmación;
- conflicto que requiere mediación institucional.

No inferir el orden de autoría desde la cantidad de roles CRediT. Registrar el criterio de orden por separado y obtener aprobación de todos los autores.

### 4. Mapear al formato de destino

Leer [representación técnica](references/representacion-tecnica.md) solo para los destinos solicitados. Mantener el término canónico junto con su vocabulario y, cuando exista, URI o código. Conservar nombres de visualización separados de identificadores y afiliaciones.

No prometer interoperabilidad sin validar la versión exacta del esquema, los campos admitidos y el resultado exportado.

### 5. Confirmar y cerrar

Entregar una matriz editable basada en `assets/matriz-contribuciones.csv` con:

- persona u organización;
- ORCID u otro identificador autenticado, si existe;
- condición de autor, colaborador o reconocimiento;
- roles CRediT y roles especializados;
- evidencia o artefacto asociado;
- confirmación del participante;
- norma aplicada y destino técnico;
- conflictos, vacíos y fecha de revisión.

Solicitar confirmación explícita de las personas antes de publicar la declaración. Preservar el historial si cambia la lista de autores o sus roles.

## Controles

Bloquear una declaración definitiva cuando:

- falta la política requerida para decidir autoría;
- se asignan roles solo por cargo, prestigio o financiación;
- una persona no confirmó sus contribuciones;
- se confunde corrección de estilo, traducción o apoyo administrativo con autoría automática;
- se intenta registrar una herramienta de IA como autora;
- el orden de firma se deduce de CRediT sin acuerdo documentado;
- el esquema de destino no admite el término o la versión propuesta;
- existe una disputa no resuelta que debe tratar la institución.

Clasificar el resultado como `PERFIL_RECOMENDADO`, `MATRIZ_PENDIENTE_DE_CONFIRMACION`, `LISTO_PARA_DECLARACION`, `REQUIERE_POLITICA_AUTORIA`, `REQUIERE_MAPEO_TECNICO` o `CONFLICTO_DE_AUTORIA`.

## Coordinación

- `$editor-en-jefe`: sitúa la obra, el destino y la etapa.
- `$redaccion-articulo-cientifico-imryd`: integra la declaración en el manuscrito sin alterar el diseño del estudio.
- `$gestor-referencias-academicas`: verifica y cita normas o políticas cuando deban documentarse.
- `$gestor-codigo-tecnico-editorial`: presenta fragmentos CodeMeta, CFF, XML o JSON como contenido editorial.
- `$maquetacion-academica-preentrega`: comprueba que la declaración final permanezca legible y editable.
- `$respondedor-observaciones-academicas`: gestiona solicitudes de cambio de autoría o contribución de revisores y editores.

Consultar [fuentes oficiales](references/fuentes-oficiales.md) antes de afirmar vigencia, obligatoriedad o compatibilidad técnica.
