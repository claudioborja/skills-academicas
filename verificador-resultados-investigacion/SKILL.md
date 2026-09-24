---
name: verificador-resultados-investigacion
description: Verifica resultados cuantitativos y cualitativos antes de reutilizarlos, publicarlos o convertirlos en capítulos, distingue errores confirmados de aspectos no verificables y documenta cada intervención. Usar para tesis, artículos, informes, libros derivados, tablas, figuras y conclusiones cuando deban comprobarse cálculos, consistencia, trazabilidad, interpretación o correspondencia con método y objetivos; no usar una comprobación mecánica como certificación científica ni corregir datos sin fuente y autorización.
---

# Verificador de resultados de investigación

## Responsabilidad

Comprobar si los resultados presentados pueden sostenerse con los datos, cálculos, métodos y artefactos disponibles; explicar cada problema y preparar una corrección trazable. Separar siempre:

1. **verificación mecánica:** operaciones reproducibles, totales, porcentajes, medias y valores repetidos;
2. **reproducibilidad computacional:** ejecución de código o consultas sobre una copia controlada de los datos;
3. **revisión metodológica:** adecuación del diseño, supuestos, análisis, incertidumbre y alcance;
4. **revisión interpretativa:** relación entre resultado, discusión, conclusión y afirmaciones causales;
5. **decisión editorial:** aprobar, posponer o rechazar la corrección propuesta.

Una salida sin alertas mecánicas no demuestra que el método, los datos o las conclusiones sean válidos.

## Límites y protección de evidencia

- No modificar datos originales, instrumentos, transcripciones, código fuente ni manuscritos durante la auditoría.
- No reemplazar un resultado solo porque parezca improbable. Exigir fuente de autoridad y reproducción del cálculo.
- No fabricar denominadores, tamaños muestrales, valores perdidos, parámetros, unidades, intervalos ni valores `p`.
- No acusar fraude o manipulación a partir de una inconsistencia. Registrar el hallazgo y escalarlo según la política institucional.
- No aplicar una guía de reporte como si evaluara por sí sola la calidad del diseño o la ejecución.
- Preservar original, propuesta, aprobación y versión corregida como estados distintos.

## Activación y alcance

Usar esta skill antes de:

- distribuir resultados de una tesis entre capítulos de un libro;
- redactar discusión, conclusiones, resumen o recomendaciones;
- adaptar tablas y figuras o convertirlas en narrativa;
- enviar un artículo o responder observaciones sobre sus resultados;
- corregir cifras contradictorias entre secciones;
- afirmar reproducibilidad, significación, asociación, efecto o causalidad.

Si el usuario solicita solo diagnóstico, no intervenir el manuscrito. Entregar los informes y las acciones propuestas.

## Flujo de verificación

### 1. Congelar fuentes y unidades de análisis

Inventariar manuscrito, datos, tablas, figuras, anexos, instrumentos, diccionario de variables, código, salidas de software y versiones. Calcular huellas cuando la trazabilidad del proyecto lo requiera. Identificar qué artefacto es autoridad para cada resultado y conservar una copia sin alterar.

Si solo existe el manuscrito, limitar la revisión a consistencia interna y calidad del reporte. Marcar como `NO_VERIFICABLE` todo cálculo que requiera datos ausentes.

### 2. Construir el registro de resultados

Asignar un identificador estable (`RES-001`, `RES-002`, etc.) a cada resultado material. Registrar ubicación, afirmación exacta, valor, unidad, población o corpus, fuente, transformación aplicada y destinos donde se repite.

Usar `assets/registro-resultados-ejemplo.json` como esquema inicial. Para auditoría mecánica ejecutar:

```text
python verificador-resultados-investigacion/scripts/verificar_resultados.py \
  --input ruta/registro-resultados.json \
  --out-dir ruta/informe-resultados-v01
```

El directorio de salida debe ser nuevo. El código `0` significa que los controles declarados coincidieron; `1`, que existen resultados incorrectos, inconsistentes o no verificables; `2`, entrada o destino inválidos. Ningún código certifica validez científica.

### 3. Revisar cuantitativamente

Leer [revisión cuantitativa](references/revision-cuantitativa.md) cuando existan cifras o análisis estadísticos. Aplicar en capas:

- recalcular operaciones simples;
- contrastar tamaños muestrales, denominadores y pérdidas;
- reproducir análisis desde datos y código cuando estén disponibles;
- comprobar supuestos, estimaciones, incertidumbre y multiplicidad con competencia metodológica adecuada;
- revisar que el texto no equipare significación estadística con importancia o causalidad.

Un recálculo manual aislado no reemplaza la reproducción mediante el mismo conjunto de datos cuando esta sea posible.

### 4. Revisar cualitativamente

Leer [revisión cualitativa](references/revision-cualitativa.md) cuando haya categorías, temas, codificación, entrevistas u observaciones. Comprobar trazabilidad entre afirmación, fragmentos o unidades de significado, matriz de análisis y procedimiento declarado.

No convertir frecuencia de códigos en importancia sustantiva sin justificación. No recalcular acuerdos ni saturación si faltan decisiones, corpus o registros de codificación.

### 5. Evaluar coherencia e interpretación

Para cada resultado, comprobar:

- objetivo o pregunta que responde;
- método y población/corpus que lo generan;
- tabla, figura, dato o fragmento que lo sustenta;
- interpretación permitida por el diseño;
- presencia coherente en resumen, discusión y conclusiones;
- limitaciones y fuentes de incertidumbre;
- cambios derivados si el valor se corrige.

Usar la guía de reporte pertinente al diseño solo para comprobar información que debe declararse. EQUATOR distingue reporte de calidad o conducción; mantener esa frontera.

### 6. Clasificar y proponer intervención

Asignar uno de estos estados:

- `VERIFICADO_MECANICAMENTE`: coincide el control reproducido; falta aún cualquier revisión sustantiva aplicable.
- `ERROR_CONFIRMADO`: fuente y cálculo determinan de forma inequívoca que el valor publicado es erróneo.
- `INCONSISTENTE`: dos o más apariciones no coinciden y aún no se estableció la autoridad.
- `NO_VERIFICABLE`: faltan datos, código, denominador, instrumento u otra evidencia necesaria.
- `REQUIERE_REVISION_METODOLOGICA`: el cálculo puede coincidir, pero método, supuestos o interpretación requieren especialista.
- `CORRECCION_APROBADA`: una persona autorizada aceptó la intervención y su impacto.
- `CONFLICTO_DE_INTEGRIDAD`: el hallazgo excede una corrección ordinaria y debe seguir la vía institucional o editorial.

No pasar de propuesta a corrección aplicada sin autorización explícita cuando cambien resultados empíricos.

### 7. Documentar cada hallazgo

Leer [informe de intervención](references/informe-intervencion.md). Cada error, inconsistencia o resultado no verificable debe tener un informe individual con:

- identificador y ubicación;
- resultado original;
- fuente de autoridad;
- procedimiento de verificación;
- estado y nivel de certeza;
- explicación de por qué está mal o no puede confirmarse;
- corrección propuesta;
- impacto en tablas, figuras, discusión, conclusiones y resumen;
- aprobación, responsable y fecha;
- cambio aplicado y evidencia posterior.

Mantener además un informe consolidado y el registro editable `assets/registro-intervenciones.csv`.

### 8. Corregir y verificar de nuevo

Aplicar únicamente cambios aprobados sobre una copia versionada. Después:

1. repetir el cálculo o la revisión;
2. actualizar todas las apariciones afectadas;
3. revisar interpretación, discusión, conclusiones y resumen;
4. comprobar tablas, figuras, notas y anexos;
5. registrar archivos antes/después y evidencia de cierre.

Una corrección numérica que no actualiza sus consecuencias narrativas sigue incompleta.

## Salidas

Entregar según el alcance:

- inventario de fuentes y resultados;
- registro estructurado para auditoría;
- informe consolidado;
- un informe por hallazgo;
- matriz original → verificación → propuesta → aprobación → aplicación;
- lista de resultados no verificables y evidencia requerida;
- manuscrito corregido solo si fue autorizado;
- lista de secciones derivadas que deben reabrirse.

## Coordinación

- `$constructor-tesis-academica`: mantiene coherencia entre objetivos, método, resultados y conclusiones.
- `$convertidor-tesis-a-libro`: transforma únicamente resultados ya verificados o claramente marcados con limitaciones.
- `$redaccion-articulo-cientifico-imryd`: integra resultados, discusión y limitaciones sin ampliar el alcance.
- `$gestor-tablas-figuras-pies`: conserva correspondencia y trazabilidad visual.
- `$gestor-ecuaciones-academicas`: revisa fórmulas, variables, unidades y derivaciones.
- `$respondedor-observaciones-academicas`: documenta cambios solicitados por tutor, jurado o revisores.
- `$editor-en-jefe`: decide el orden de intervención y reabre las fases afectadas.

Consultar [protocolo](references/protocolo-verificacion.md), [fuentes oficiales](references/fuentes-oficiales.md) y solo la referencia cuantitativa o cualitativa pertinente al caso.
