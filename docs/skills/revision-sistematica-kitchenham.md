# Revisión Sistemática Kitchenham

Planifica, ejecuta, documenta, respalda, analiza y redacta revisiones sistemáticas de literatura siguiendo exclusivamente Kitchenham y Charters para ingeniería de software. Usar cuando Codex necesite desarrollar una revisión desde la pregunta hasta el informe; validar el protocolo; seleccionar fuentes por cobertura disciplinar y complementariedad; ejecutar búsquedas reproducibles y búsquedas por referencias hacia atrás y hacia delante; probar artículos semilla; medir el aporte marginal y la saturación; descargar, preservar y revisar manualmente todas las fuentes utilizadas; excluir recursos sin texto completo descargable; deduplicar y cribar; evaluar calidad, actualidad, impacto y novedad; extraer y sintetizar evidencia; mantener huellas digitales e instantáneas de respaldo; actualizar búsquedas; o auditar la suficiencia metodológica sin imponer cuotas universales de estudios.

## Ejemplo de uso

```text
Usa $revision-sistematica-kitchenham para planificar, ejecutar, respaldar y redactar una revisión sistemática exclusivamente Kitchenham, descargando y revisando manualmente toda fuente utilizada.
```

## Guía operativa

### Ejecución multiplataforma

Las escrituras usan `editor-en-jefe/scripts/archivos_seguros.py`: JSON, CSV e informes reemplazan atómicamente cada archivo; plantillas, copias de fuentes, manifiestos y ZIP se publican sin sustituir destinos existentes. Las copias preservan contenido, no permisos ni fechas del archivo fuente. Al reclasificar una fuente se verifica la copia antes de eliminar la ubicación anterior. Los comandos conservan su permiso funcional para actualizar matrices y estados; no requieren `--overwrite`. Se rechazan enlaces simbólicos internos y junctions cuando el intérprete permite detectarlos. No es una transacción entre varios archivos ni un bloqueo de concurrencia: usar un solo proceso escritor y rutas estables. Si falla un ZIP puede quedar su manifiesto, pero no un ZIP parcial; una interrupción tras copiar una fuente puede dejar una copia aún no registrada. Revisar estos casos antes de reintentar.

Consultar [la guía común de ejecución](../../editor-en-jefe/references/portabilidad.md) para elegir intérprete y preparar dependencias.

### Autoridad Metodológica

Usar Kitchenham y Charters (2007) como autoridad central. Usar Kitchenham (2004) como antecedente, Brereton et al. (2007) para lecciones de aplicación y Wohlin (2014) solo para operacionalizar snowballing compatible con el protocolo.

No presentar el trabajo como PRISMA, PRISMA-ScR ni metodología combinada. No activar `$revision-sistematica-prisma` por defecto dentro de un proyecto Kitchenham. Si una skill auxiliar contradice Kitchenham o el protocolo congelado, aplicar Kitchenham y registrar cualquier enmienda.

Leer:

- [references/metodologia-kitchenham.md](../../revision-sistematica-kitchenham/references/metodologia-kitchenham.md) antes de planificar las fases.
- [references/artefactos-respaldos.md](../../revision-sistematica-kitchenham/references/artefactos-respaldos.md) antes de crear, descargar o respaldar archivos.
- [references/descarga-revision-manual.md](../../revision-sistematica-kitchenham/references/descarga-revision-manual.md) antes de admitir, analizar o citar cualquier fuente.
- [references/cobertura-impacto-novedad.md](../../revision-sistematica-kitchenham/references/cobertura-impacto-novedad.md) antes de diseñar o auditar búsquedas, actualidad, impacto, novedad o excepciones.
- [references/evaluacion-calidad-sintesis.md](../../revision-sistematica-kitchenham/references/evaluacion-calidad-sintesis.md) antes de calidad, extracción o síntesis.
- [references/coordinacion-skills.md](../../revision-sistematica-kitchenham/references/coordinacion-skills.md) antes de activar apoyos.
- [references/fuentes-base.md](../../revision-sistematica-kitchenham/references/fuentes-base.md) para distinguir la función de los documentos metodológicos adjuntos.

### Regla De Ejecución

Generar un plan persistente y ejecutarlo. Mantener sincronizados el plan operativo y `00_gestion/02_planificacion/00-02_plan.md`. Actualizar `00_gestion/03_seguimiento/00-03_estado.json` y `00_gestion/03_seguimiento/00-03_bitacora.csv` al iniciar o cerrar fases. Crear snapshots al cerrar protocolo, búsqueda, selección, calidad, extracción, síntesis e informe.

No usar el tamaño del corpus como sustituto de rigor. Hacer que la cantidad de estudios sea consecuencia de pertinencia, evidencia disponible y criterios protocolizados.

### Convención Obligatoria De Numeración

Organizar todo archivo producido, descargado, derivado, auditado, respaldado o entregado por etapa y paso:

- Numerar cada componente de directorio con dos dígitos y guion bajo: `EE_etapa/PP_paso/SS_subpaso/`.
- Anteponer al archivo el código completo de su destino, con segmentos separados por guiones: `EE-PP_nombre.ext` o `EE-PP-SS_nombre.ext`.
- Usar números correlativos para carpetas dinámicas dentro de un mismo paso, por ejemplo `01_scopus/`, `02_ieee-xplore/`.
- Añadir fecha, identificador o versión después del código cuando sea necesario, sin eliminar el prefijo de etapa.
- No producir archivos nuevos fuera de la estructura descrita en `references/artefactos-respaldos.md`.

Ejemplos:

- `02_busquedas/04_resultados/01_brutos/01_scopus/02-04-01_20260727-153000_scopus.csv`
- `04_fuentes/01_originales/01_incluidos/04-01-01_20260727-153500_estudio.pdf`
- `07_sintesis/10_trazabilidad/07-10_mapa-evidencia.csv`

Ejecutar `audit` antes de cerrar cada fase. Una carpeta o archivo producido que incumpla esta convención constituye una pérdida de organización y trazabilidad; la auditoría debe devolver `BLOCKED` hasta reubicarlo o renombrarlo y actualizar su inventario.

### Regla Absoluta De Descarga Y Uso

Usar como evidencia o cita únicamente fuentes cuyo texto completo:

1. se haya descargado legítimamente dentro de `04_fuentes/01_originales/`;
2. esté inventariado mediante `register-source` con identificador, ruta y SHA-256;
3. pueda abrirse y leerse;
4. tenga revisión manual de contenido y citas registrada;
5. esté vinculado al registro maestro y a `04_fuentes/04_metadatos/04-04_fuentes-usadas.csv`.

Aplicar esta regla a estudios primarios, revisiones anteriores, antecedentes, documentos metodológicos y cualquier otra referencia usada en el manuscrito. Un resumen, metadato, DOI, URL, página de resultados, fragmento o referencia secundaria no sustituye al texto completo.

Si el archivo completo no puede descargarse legalmente o no puede abrirse, marcar `FT-NO-DESCARGADO`, registrar los intentos y excluir el recurso. No usarlo en calidad, extracción, síntesis, discusión, conclusiones ni como apoyo de una afirmación. Esta regla no admite excepción metodológica.

### Suficiencia Y Umbrales

Evaluar suficiencia por:

1. cobertura de todas las disciplinas implicadas;
2. fuente multidisciplinaria;
3. fuente especializada en el dominio;
4. fuente independiente complementaria o ausencia justificada;
5. búsqueda retrospectiva y prospectiva o equivalente justificado;
6. cadenas adaptadas y probadas;
7. recuperación de artículos semilla cuando estén disponibles;
8. aporte marginal por fuente;
9. saturación razonable;
10. exportaciones, cadenas, filtros, fechas, conteos, archivos y hashes trazables;
11. aplicación consistente de criterios;
12. limitaciones de acceso y cobertura documentadas.

Recomendar cuatro a cinco fuentes principales bien seleccionadas. No considerar suficiente o insuficiente una estrategia únicamente por el número ejecutado.

Mantener 300 registros únicos, 100 textos completos, 50 estudios incluidos, 60 % reciente y 90 días desde la búsqueda como referencias operativas configurables con aplicación `advisory`. No bloquear una revisión solo por no alcanzarlas. Usar `external_requirement` únicamente cuando el usuario identifique una obligación institucional, editorial o contractual y registrar su autoridad.

Nunca incluir estudios irrelevantes, duplicar publicaciones, mezclar fenómenos, relajar criterios ni ampliar artificialmente periodo o alcance para alcanzar cifras.

### Inicio Obligatorio

Crear el espacio de revisión:

```text
python skills/editor-en-jefe/scripts/ejecutar.py revision-sistematica-kitchenham/scripts/kitchenham_workspace.py init --project-dir "revisiones/mi-revision" --title "Título provisional" --topic "Tema delimitado" --question "Pregunta principal" --disciplines "informática;ingeniería" --citation-style apa7 --threshold-enforcement advisory --search-update-enforcement advisory
```

Si `python` no está disponible, usar el intérprete creado por `$preprocesador-documentos`.

No guardar resultados nuevos fuera de la estructura creada, salvo temporales. Registrar toda exportación, texto o suplemento con `register-source`.

### Fases Y Puertas

#### 0. Diagnosticar Necesidad Y Alcance

1. Confirmar la necesidad de una revisión sistemática.
2. Localizar revisiones anteriores y decidir si replicar, actualizar, contrastar o cubrir una brecha.
3. Delimitar preguntas, población o dominio, intervención, comparación, resultados y contexto cuando correspondan.
4. Definir disciplinas, periodo, idiomas, tipos documentales, audiencia, recursos y restricciones.
5. Distinguir expectativas operativas de requisitos externos.
6. Generar plan, riesgos, cronograma y entregables.

Puerta: necesidad justificada, alcance coherente y plan ejecutable.

#### 1. Formular Preguntas

1. Formular pregunta principal y preguntas secundarias no solapadas.
2. Usar PICOC cuando ayude; no forzar componentes.
3. Relacionar cada pregunta con variables de extracción y síntesis.

Puerta: preguntas respondibles y datos observables.

#### 2. Construir Y Validar Protocolo

Completar `01_protocolo/01_vigente/01-01_protocolo.md` antes de la búsqueda definitiva. Especificar:

- preguntas, alcance y disciplinas;
- tipología, función, complementariedad y justificación de fuentes;
- fuentes relevantes no consultables;
- regla de exclusión `FT-NO-DESCARGADO` y procedimiento de descarga, inventario y revisión manual;
- conceptos, sinónimos, cadenas y campos por fuente;
- artículos semilla y objetivo de recuperación;
- búsqueda por referencias o citaciones;
- criterios de selección, deduplicación y desacuerdos;
- calidad, extracción, síntesis, heterogeneidad y sensibilidad;
- aporte marginal y criterio de saturación;
- señales operativas, aplicación `advisory` o `external_requirement`;
- actualización, riesgos, respaldos y reporte.

Pilotear búsqueda, selección, calidad y extracción. Evaluar el protocolo y congelarlo en snapshot. Registrar todo cambio posterior en `01_protocolo/02_versiones/01-02_desviaciones.csv`.

Puerta: protocolo completo, pilotado, evaluado y versionado.

#### 3. Diseñar Y Ejecutar Búsquedas Reproducibles

1. Clasificar cada fuente como base bibliográfica, índice de citación, biblioteca digital especializada, plataforma editorial, motor académico, repositorio o complemento.
2. Registrar su función, cobertura disciplinar, grupo de independencia, justificación y acceso.
3. Incluir una fuente multidisciplinaria, una especializada y una independiente complementaria, o justificar la ausencia de esta última.
4. No contar plataformas editoriales como equivalentes a índices sin justificar el aporte directo.
5. Adaptar cadena, campos y sintaxis a cada fuente.
6. Registrar fecha, filtros, responsable, conteo y archivo de cadena.
7. Exportar y registrar resultados brutos inmutables con SHA-256.
8. Probar entre cinco y diez artículos semilla cuando existan; buscar 90 % de recuperación como referencia configurable.
9. Registrar fuentes previstas no consultadas y su efecto.

Registrar exportaciones:

```text
python skills/editor-en-jefe/scripts/ejecutar.py revision-sistematica-kitchenham/scripts/kitchenham_workspace.py register-source --project-dir "revisiones/mi-revision" --file "descargas/scopus.csv" --kind search-export --database "Scopus" --query-id "Q-SCOPUS-001" --origin "Exportación directa"
```

Puerta: cobertura funcional y disciplinar razonable, cadenas reproducibles, evidencia bruta preservada y limitaciones explícitas. No afirmar exhaustividad absoluta.

#### 4. Ejecutar Búsqueda Complementaria

1. Formar un conjunto semilla diverso.
2. Ejecutar backward y forward snowballing.
3. Revisar contexto de citación.
4. Iterar hasta una ronda sin nuevas inclusiones o documentar la limitación.
5. Registrar ronda, semilla, dirección, candidato, decisión y motivo.

Puerta: búsqueda complementaria ejecutada y saturación evaluada.

#### 5. Deduplicar Y Seleccionar

1. Conservar el conjunto bruto.
2. Deduplicar por DOI, título normalizado, autores y año.
3. Pilotear criterios.
4. Cribar título/resumen y texto completo.
5. Descargar y registrar el texto completo antes de decidir inclusión.
6. Excluir con `FT-NO-DESCARGADO` todo recurso cuyo archivo completo no se obtenga o no pueda abrirse.
7. Registrar razón específica para cada exclusión final.
8. Resolver desacuerdos según el protocolo.
9. Calcular aporte marginal por fuente.
10. Completar la matriz de impacto y novedad.

Si participa un solo revisor, hacer una segunda pasada separada y declarar la limitación.

Puerta: cada registro tiene estado, exclusiones trazables y el corpus refleja pertinencia, no una cuota.

#### 6. Descargar, Preservar Y Leer Textos

Registrar textos y suplementos con hash. Separar incluidos, excluidos y pendientes. Verificar apertura y legibilidad. Revisar manualmente contenido, referencias y uso previsto; registrar responsable, fecha y localizadores. Usar `$preprocesador-documentos` para convertir y segmentar y `$automatizador-referencias` para inventario y metadatos cuando estén disponibles.

Registrar primero el texto pendiente:

```text
python skills/editor-en-jefe/scripts/ejecutar.py revision-sistematica-kitchenham/scripts/kitchenham_workspace.py register-source --project-dir "revisiones/mi-revision" --file "descargas/estudio.pdf" --kind fulltext --decision pending --source-id "SRC-001" --study-id "S001" --source-role primary-study --title "Título del estudio" --doi "10.xxxx/xxxxx" --origin "Repositorio institucional"
```

Después de abrirlo y revisar manualmente contenido y citas, clasificarlo usando el `record_id` devuelto:

```text
python skills/editor-en-jefe/scripts/ejecutar.py revision-sistematica-kitchenham/scripts/kitchenham_workspace.py review-source --project-dir "revisiones/mi-revision" --record-id "SRC-..." --decision included --content-reviewed --citations-reviewed --reviewed-by "Investigador"
```

Puerta: cada fuente utilizada tiene texto completo local, hash válido, vínculo de inventario y revisión manual de contenido y citas. Una indisponibilidad nunca justifica inclusión.

#### 7. Evaluar Calidad

Aplicar y pilotear un instrumento coherente con los diseños. Conservar respuesta, evidencia, localizador, revisor y resolución. Usar la calidad como establezca el protocolo; no cambiar umbrales después de ver resultados sin desviación.

Puerta: evaluación completa y uso analítico definido.

#### 8. Extraer Datos

Pilotear el formulario. Extraer identificación, contexto, diseño, muestra, intervención, comparación, resultados, métricas y limitaciones. Conservar localizadores y verificar datos. Marcar ausencias; no inferirlas.

Puerta: cada hallazgo conserva estudio, localizador y pregunta.

#### 9. Sintetizar Y Analizar

1. Describir corpus, distribución temporal, contextos, diseños y calidad.
2. Agrupar por pregunta y comparabilidad.
3. Elegir síntesis narrativa, temática, tabular o cuantitativa según los datos.
4. Analizar heterogeneidad, contradicciones, sensibilidad y sesgos.
5. Contextualizar la proporción reciente según velocidad del campo y estudios fundacionales.
6. Completar mapa de evidencia y matriz de brechas.
7. Separar datos, interpretación y recomendaciones.

Puerta: conclusiones proporcionales y trazables.

#### 10. Redactar Y Auditar

Reportar fuentes y función, cadenas, fechas, filtros, registros brutos y únicos, semillas, aporte marginal, snowballing, saturación, distribución temporal, selección, calidad, síntesis, excepciones, fuentes no consultadas, exclusiones `FT-NO-DESCARGADO`, auditoría manual de citas, limitaciones y estado final.

Recomendar actualizar la búsqueda antes del envío. Tratar 90 días como referencia configurable según ritmo del campo, fecha de envío, revista y nueva evidencia esperable.

Puerta: informe, matrices, auditorías, paquete reproducible y snapshot final completos.

### Auditoría Metodológica

Ejecutar:

```text
python skills/editor-en-jefe/scripts/ejecutar.py revision-sistematica-kitchenham/scripts/kitchenham_workspace.py audit --project-dir "revisiones/mi-revision"
```

Interpretar:

- `PASS`: continuar.
- `PASS_WITH_WARNINGS`: continuar y reportar limitaciones.
- `REQUIRES_SEARCH_AUDIT`: revisar preguntas, sinónimos, sintaxis, campos, fuentes, semillas, idiomas, periodo, criterios y disponibilidad real.
- `REQUIRES_PROTOCOL_AMENDMENT`: detener la parte afectada y registrar enmienda.
- `BLOCKED`: corregir fuentes utilizadas sin texto completo local y revisado, pérdida de trazabilidad, archivos alterados, búsquedas irreproducibles u otro error grave.

Registrar una auditoría de búsqueda:

```text
python skills/editor-en-jefe/scripts/ejecutar.py revision-sistematica-kitchenham/scripts/kitchenham_workspace.py search-audit --project-dir "revisiones/mi-revision" --decision keep-protocol --reviewed-by "Investigador" --review-notes "Se revisaron en orden preguntas, sinónimos, sintaxis, campos, fuentes, semillas, idiomas, periodo, criterios y evidencia disponible."
```

### Excepciones Y Requisitos Externos

Generar borradores de excepción cuando un valor esperado no se alcance. Completar cada excepción con responsable, revisiones, cambios, justificación, riesgo, impacto, decisión y aprobación:

```text
python skills/editor-en-jefe/scripts/ejecutar.py revision-sistematica-kitchenham/scripts/kitchenham_workspace.py methodological-exception --project-dir "revisiones/mi-revision" --exception-id "EXC-CORPUS-001" --threshold included_studies --expected 50 --obtained 28 --responsible "Investigador" --reviews-performed "Auditoría completa de búsqueda" --changes-applied "Ninguno; mantener alcance" --justification "El campo especializado contiene evidencia primaria limitada." --risk "Baja precisión y generalización restringida" --impact "Interpretar como evidencia emergente" --decision "Continuar sin ampliar artificialmente" --approved-by "Responsable metodológico"
```

No llamar “excepción” al simple incumplimiento de una recomendación antes de auditarlo. Si el valor era un requisito externo, identificarlo como tal y no atribuirlo a Kitchenham.

### Respaldo Y Bloqueos

Crear snapshots con `snapshot`. No sobrescribir exportaciones ni originales. Conservar hashes, origen, consulta, decisión y versiones.

Bloquear ante fuentes incluidas, analizadas o citadas sin texto completo descargado, legible, inventariado y revisado manualmente; datos inventados; búsquedas no reproducibles; archivos faltantes o alterados; criterios indefinidos; cambios no registrados; o inclusión deliberada de estudios irrelevantes. No bloquear únicamente por 300/100/50, 60 %, 90 días o una cantidad de fuentes.

### Entrega Obligatoria

Entregar plan y estado; protocolo y desviaciones; tabla de fuentes y funciones; cadenas; exportaciones brutas; registros únicos; semillas; aporte marginal; snowballing; saturación; selección; textos completos locales e inventario según sus licencias; matriz de fuentes usadas; auditoría manual de citas y contenidos; hashes; calidad; extracción; distribución temporal; impacto, novedad y brechas; excepciones; auditorías; manuscrito; snapshot y paquete reproducible.

## Recursos incluidos

### Herramientas automatizadas

| Recurso | Función |
| --- | --- |
| [`scripts/kitchenham_workspace.py`](../../revision-sistematica-kitchenham/scripts/kitchenham_workspace.py) | Recurso auxiliar: Kitchenham workspace. |

### Referencias

| Recurso | Función |
| --- | --- |
| [`references/artefactos-respaldos.md`](../../revision-sistematica-kitchenham/references/artefactos-respaldos.md) | Artefactos, Directorios Y Respaldos |
| [`references/cobertura-impacto-novedad.md`](../../revision-sistematica-kitchenham/references/cobertura-impacto-novedad.md) | Suficiencia, Cobertura, Actualidad, Impacto Y Novedad |
| [`references/coordinacion-skills.md`](../../revision-sistematica-kitchenham/references/coordinacion-skills.md) | Coordinación Con Skills Auxiliares |
| [`references/descarga-revision-manual.md`](../../revision-sistematica-kitchenham/references/descarga-revision-manual.md) | Descarga Y Revisión Manual De Todas Las Fuentes |
| [`references/evaluacion-calidad-sintesis.md`](../../revision-sistematica-kitchenham/references/evaluacion-calidad-sintesis.md) | Evaluación De Calidad Y Síntesis |
| [`references/fuentes-base.md`](../../revision-sistematica-kitchenham/references/fuentes-base.md) | Fuentes Base |
| [`references/metodologia-kitchenham.md`](../../revision-sistematica-kitchenham/references/metodologia-kitchenham.md) | Metodología Kitchenham |

### Plantillas y recursos

| Recurso | Función |
| --- | --- |
| [`assets/aporte-marginal-fuentes.csv`](../../revision-sistematica-kitchenham/assets/aporte-marginal-fuentes.csv) | Plantilla o registro editable: Aporte marginal fuentes. |
| [`assets/articulos-semilla.csv`](../../revision-sistematica-kitchenham/assets/articulos-semilla.csv) | Plantilla o registro editable: Articulos semilla. |
| [`assets/auditoria-busqueda.md`](../../revision-sistematica-kitchenham/assets/auditoria-busqueda.md) | Auditoría Metodológica De Búsqueda |
| [`assets/auditoria-citas.csv`](../../revision-sistematica-kitchenham/assets/auditoria-citas.csv) | Plantilla o registro editable: Auditoria citas. |
| [`assets/cribado.csv`](../../revision-sistematica-kitchenham/assets/cribado.csv) | Plantilla o registro editable: Cribado. |
| [`assets/criterios-cobertura-impacto.md`](../../revision-sistematica-kitchenham/assets/criterios-cobertura-impacto.md) | Criterios De Cobertura, Actualidad, Impacto Y Novedad |
| [`assets/datos-extraidos.csv`](../../revision-sistematica-kitchenham/assets/datos-extraidos.csv) | Plantilla o registro editable: Datos extraidos. |
| [`assets/desviaciones.csv`](../../revision-sistematica-kitchenham/assets/desviaciones.csv) | Plantilla o registro editable: Desviaciones. |
| [`assets/distribucion-temporal.csv`](../../revision-sistematica-kitchenham/assets/distribucion-temporal.csv) | Plantilla o registro editable: Distribucion temporal. |
| [`assets/evaluacion-calidad.csv`](../../revision-sistematica-kitchenham/assets/evaluacion-calidad.csv) | Plantilla o registro editable: Evaluacion calidad. |
| [`assets/evaluacion-protocolo.md`](../../revision-sistematica-kitchenham/assets/evaluacion-protocolo.md) | Evaluación Del Protocolo |
| [`assets/evaluacion-saturacion.csv`](../../revision-sistematica-kitchenham/assets/evaluacion-saturacion.csv) | Plantilla o registro editable: Evaluacion saturacion. |
| [`assets/excepciones-metodologicas.csv`](../../revision-sistematica-kitchenham/assets/excepciones-metodologicas.csv) | Plantilla o registro editable: Excepciones metodologicas. |
| [`assets/exclusiones-texto-completo.csv`](../../revision-sistematica-kitchenham/assets/exclusiones-texto-completo.csv) | Plantilla o registro editable: Exclusiones texto completo. |
| [`assets/formulario-extraccion.md`](../../revision-sistematica-kitchenham/assets/formulario-extraccion.md) | Formulario De Extracción |
| [`assets/fuentes-consultadas.csv`](../../revision-sistematica-kitchenham/assets/fuentes-consultadas.csv) | Plantilla o registro editable: Fuentes consultadas. |
| [`assets/fuentes-inaccesibles.csv`](../../revision-sistematica-kitchenham/assets/fuentes-inaccesibles.csv) | Plantilla o registro editable: Fuentes inaccesibles. |
| [`assets/fuentes-no-consultadas.csv`](../../revision-sistematica-kitchenham/assets/fuentes-no-consultadas.csv) | Plantilla o registro editable: Fuentes no consultadas. |
| [`assets/fuentes-usadas.csv`](../../revision-sistematica-kitchenham/assets/fuentes-usadas.csv) | Plantilla o registro editable: Fuentes usadas. |
| [`assets/instrumento-calidad.md`](../../revision-sistematica-kitchenham/assets/instrumento-calidad.md) | Instrumento De Evaluación De Calidad |
| [`assets/manuscrito.md`](../../revision-sistematica-kitchenham/assets/manuscrito.md) | {{TITLE}} |
| [`assets/mapa-evidencia.csv`](../../revision-sistematica-kitchenham/assets/mapa-evidencia.csv) | Plantilla o registro editable: Mapa evidencia. |
| [`assets/matriz-brechas-novedad.csv`](../../revision-sistematica-kitchenham/assets/matriz-brechas-novedad.csv) | Plantilla o registro editable: Matriz brechas novedad. |
| [`assets/matriz-impacto-novedad.csv`](../../revision-sistematica-kitchenham/assets/matriz-impacto-novedad.csv) | Plantilla o registro editable: Matriz impacto novedad. |
| [`assets/plan.md`](../../revision-sistematica-kitchenham/assets/plan.md) | Plan De Revisión Sistemática |
| [`assets/protocolo.md`](../../revision-sistematica-kitchenham/assets/protocolo.md) | Protocolo De Revisión Sistemática Kitchenham |
| [`assets/registro-busquedas.csv`](../../revision-sistematica-kitchenham/assets/registro-busquedas.csv) | Plantilla o registro editable: Registro busquedas. |
| [`assets/registros-maestros.csv`](../../revision-sistematica-kitchenham/assets/registros-maestros.csv) | Plantilla o registro editable: Registros maestros. |
| [`assets/snowballing.csv`](../../revision-sistematica-kitchenham/assets/snowballing.csv) | Plantilla o registro editable: Snowballing. |

### Pruebas

| Recurso | Función |
| --- | --- |
| [`tests/test_escritura_segura.py`](../../revision-sistematica-kitchenham/tests/test_escritura_segura.py) | Recurso auxiliar: Test escritura segura. |

### Configuración de interfaz

| Recurso | Función |
| --- | --- |
| [`agents/openai.yaml`](../../revision-sistematica-kitchenham/agents/openai.yaml) | Metadatos de interfaz e invocación de la skill. |

## Fuente normativa

Esta ficha se genera desde [`revision-sistematica-kitchenham/SKILL.md`](../../revision-sistematica-kitchenham/SKILL.md), que permanece como contrato normativo. Regenera la ficha después de modificar ese archivo.
