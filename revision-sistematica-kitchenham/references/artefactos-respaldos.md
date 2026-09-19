# Artefactos, Directorios Y Respaldos

## Convención Obligatoria

Todo directorio y archivo del proyecto debe revelar la etapa y el paso al que pertenece.

- Directorios: `EE_etapa/PP_paso/SS_subpaso/`.
- Archivos: `EE-PP_nombre.ext` o `EE-PP-SS_nombre.ext`.
- Carpetas creadas dinámicamente: número correlativo de dos dígitos y nombre normalizado, por ejemplo `01_scopus/`.
- Versiones, fechas e identificadores se añaden después del prefijo: `02-04-01_20260727-153000_scopus.csv`.
- No se permiten archivos producidos, descargados o derivados en la raíz ni en carpetas sin numerar.

El inicializador debe crear toda la estructura aunque algunas carpetas permanezcan vacías al comienzo. Los temporales deben eliminarse o registrarse y trasladarse a su destino numerado. La auditoría considera grave cualquier incumplimiento de esta convención porque rompe la trazabilidad por etapas.

## Estructura Obligatoria

```text
proyecto/
├── 00_gestion/
│   ├── 01_configuracion/
│   ├── 02_planificacion/
│   ├── 03_seguimiento/
│   ├── 04_inventario/
│   ├── 05_decisiones/
│   ├── 06_riesgos/
│   ├── 07_cronograma/
│   └── 08_excepciones/
├── 01_protocolo/
│   ├── 01_vigente/
│   ├── 02_versiones/
│   ├── 03_pilotos/
│   │   ├── 01_busqueda/
│   │   ├── 02_seleccion/
│   │   ├── 03_calidad/
│   │   └── 04_extraccion/
│   └── 04_aprobaciones/
├── 02_busquedas/
│   ├── 01_fuentes/
│   ├── 02_cadenas/
│   │   ├── 01_borradores/
│   │   └── 02_definitivas/
│   ├── 03_registro/
│   ├── 04_resultados/
│   │   ├── 01_brutos/
│   │   └── 02_normalizados/
│   ├── 05_articulos-semilla/
│   ├── 06_busqueda-manual/
│   ├── 07_literatura-gris/
│   ├── 08_actualizaciones/
│   ├── 09_aporte-marginal/
│   ├── 10_saturacion/
│   └── 11_logs/
├── 03_seleccion/
│   ├── 01_registro-maestro/
│   ├── 02_deduplicacion/
│   ├── 03_cribado-titulo-resumen/
│   ├── 04_cribado-texto-completo/
│   ├── 05_desacuerdos/
│   ├── 06_snowballing/
│   └── 07_impacto-novedad/
├── 04_fuentes/
│   ├── 01_originales/
│   │   ├── 01_incluidos/
│   │   ├── 02_excluidos/
│   │   └── 03_pendientes/
│   ├── 02_suplementos/
│   │   ├── 01_incluidos/
│   │   ├── 02_excluidos/
│   │   └── 03_pendientes/
│   ├── 03_procesados/
│   │   ├── 01_markdown/
│   │   ├── 02_texto/
│   │   └── 03_segmentos/
│   ├── 04_metadatos/
│   ├── 05_inaccesibles/
│   └── 06_cuarentena/
├── 05_calidad/
│   ├── 01_instrumentos/
│   ├── 02_piloto/
│   ├── 03_evaluaciones/
│   │   ├── 01_revisor-1/
│   │   └── 02_revisor-2/
│   ├── 04_resoluciones/
│   └── 05_sensibilidad/
├── 06_extraccion/
│   ├── 01_formularios/
│   ├── 02_piloto/
│   ├── 03_individual/
│   ├── 04_verificacion/
│   └── 05_consolidado/
├── 07_sintesis/
│   ├── 01_descriptiva/
│   ├── 02_narrativa/
│   ├── 03_tematica/
│   ├── 04_cuantitativa/
│   ├── 05_heterogeneidad/
│   ├── 06_sensibilidad/
│   ├── 07_brechas-novedad/
│   ├── 08_tablas/
│   ├── 09_graficos/
│   └── 10_trazabilidad/
├── 08_informe/
│   ├── 01_borradores/
│   ├── 02_final/
│   ├── 03_referencias/
│   ├── 04_anexos/
│   ├── 05_material-suplementario/
│   └── 06_envio/
├── 09_auditorias/
│   ├── 01_integridad/
│   ├── 02_cobertura/
│   ├── 03_metodologia/
│   ├── 04_citas/
│   └── 05_entrega/
├── 10_respaldo/
│   ├── 01_manifiestos/
│   ├── 02_snapshots/
│   ├── 03_logs/
│   ├── 04_recuperacion/
│   └── 05_otros/
└── 11_entrega/
    ├── 01_manuscrito/
    ├── 02_matrices/
    ├── 03_fuentes/
    └── 04_paquete-reproducible/
```

## Destino De Cada Tipo De Archivo

| Tipo | Destino principal |
|---|---|
| Configuración | `00_gestion/01_configuracion/` |
| Plan | `00_gestion/02_planificacion/` |
| Estado y bitácora | `00_gestion/03_seguimiento/` |
| Inventario y hashes | `00_gestion/04_inventario/` |
| Decisiones, riesgos, cronograma y excepciones | pasos `05` a `08` de `00_gestion/` |
| Protocolo vigente | `01_protocolo/01_vigente/` |
| Versiones, desviaciones, pilotos y aprobaciones | pasos `02` a `04` de `01_protocolo/` |
| Tipología, función y justificación de fuentes | `02_busquedas/01_fuentes/` |
| Cadenas definitivas | `02_busquedas/02_cadenas/02_definitivas/` |
| Registro reproducible de búsquedas | `02_busquedas/03_registro/` |
| Exportaciones intactas por base | `02_busquedas/04_resultados/01_brutos/<NN_base>/` |
| Registros normalizados | `02_busquedas/04_resultados/02_normalizados/` |
| Semillas, búsqueda manual, literatura gris y actualizaciones | pasos `05` a `08` de `02_busquedas/` |
| Aporte marginal, saturación y logs | pasos `09` a `11` de `02_busquedas/` |
| Registro maestro y deduplicación | pasos `01` y `02` de `03_seleccion/` |
| Cribados, desacuerdos y snowballing | pasos `03` a `06` de `03_seleccion/` |
| Evaluación de impacto y novedad | `03_seleccion/07_impacto-novedad/` |
| Textos completos originales | `04_fuentes/01_originales/<NN_decision>/` |
| Anexos y datos suplementarios | `04_fuentes/02_suplementos/<NN_decision>/` |
| Texto convertido y segmentos | `04_fuentes/03_procesados/` |
| Matriz de todas las fuentes usadas | `04_fuentes/04_metadatos/04-04_fuentes-usadas.csv` |
| Registro de recursos no descargables y excluidos | `04_fuentes/05_inaccesibles/04-05_fuentes-inaccesibles.csv` |
| Metadatos, fuentes no recuperadas o sospechosas | pasos `04` a `06` de `04_fuentes/` |
| Instrumentos y evaluaciones de calidad | `05_calidad/` en su paso numerado |
| Extracción individual, verificada y consolidada | `06_extraccion/` en su paso numerado |
| Análisis, síntesis y trazabilidad | `07_sintesis/` en su paso numerado |
| Borradores, versión final y anexos | `08_informe/` en su paso numerado |
| Auditorías separadas por objeto | `09_auditorias/` en su paso numerado |
| Auditoría manual de citas | `09_auditorias/04_citas/09-04_auditoria-citas.csv` |
| Manifiestos, snapshots y recuperación | `10_respaldo/` en su paso numerado |
| Copia final autocontenida | `11_entrega/` en su paso numerado |

## Reglas De Preservación

- Tratar exportaciones brutas, textos completos y suplementos descargados como inmutables.
- No editar archivos dentro de `02_busquedas/04_resultados/01_brutos/`, `04_fuentes/01_originales/` ni `04_fuentes/02_suplementos/`.
- Trabajar con copias derivadas y registrar su relación con el original.
- No borrar estudios excluidos; separarlos del corpus activo.
- Calcular SHA-256 al registrar cada archivo.
- Conservar URL, base, consulta, fecha, decisión, nombre original y ruta almacenada.
- Conservar `source_id`, `study_id`, vínculo al inventario, estado de descarga, revisión manual de contenido y citas, revisor y fecha.
- No marcar una fuente como incluida o usada si el texto completo no está en `04_fuentes/01_originales/01_incluidos/`.
- Tratar `04_fuentes/05_inaccesibles/` solo como registro de exclusión; nada contenido allí puede alimentar calidad, extracción, síntesis o citas.
- Versionar cadenas, protocolo, matrices e informes; no reemplazar versiones congeladas.
- Crear snapshot después de cada puerta de control.
- Mantener una copia externa cuando el proyecto sea crítico; el ZIP local no sustituye esa copia.

## Registro De Descargas

Usar `register-source` para exportaciones CSV, RIS, BibTeX o JSON; textos PDF, HTML u otro formato completo; suplementos; conjuntos de datos y anexos. Una captura o metadato no puede registrarse como `fulltext`. El comando debe:

1. seleccionar el destino numerado según tipo y decisión;
2. crear una subcarpeta correlativa cuando corresponda;
3. renombrar la copia con el prefijo completo de etapa;
4. calcular su hash;
5. añadirla a `00_gestion/04_inventario/00-04_inventario-archivos.csv`.

Toda fuente usada debe vincularse además en `04_fuentes/04_metadatos/04-04_fuentes-usadas.csv`. Toda cita del manuscrito debe verificarse en `09_auditorias/04_citas/09-04_auditoria-citas.csv`.

## Snapshot

El snapshot crea un manifiesto SHA-256 en `10_respaldo/01_manifiestos/` y un ZIP numerado en `10_respaldo/02_snapshots/`. Excluye snapshots anteriores para evitar crecimiento recursivo y conserva fecha y fase.

## Recuperación

1. Elegir el último snapshot válido.
2. Verificar el hash del ZIP y los hashes del manifiesto.
3. Restaurar en una carpeta nueva.
4. No sobrescribir el proyecto activo sin autorización.
5. Registrar fecha, responsable, causa y resultado en `10_respaldo/04_recuperacion/` con prefijo `10-04_`.

## Paquete De Entrega

Al finalizar, `11_entrega/` debe contener copias de solo lectura en los pasos numerados correspondientes: manuscrito, matrices publicables, inventario de fuentes permitido y paquete reproducible. No duplicar textos completos cuya licencia impida redistribución; incluir en su lugar metadatos, hashes y enlaces legítimos.
