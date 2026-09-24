# Constructor de Tesis Académica

Construye, diagnostica, organiza y revisa tesis, tesinas, trabajos de grado, proyectos de titulación y disertaciones desde el tema inicial hasta la preentrega. Usarlo para planteamiento del problema, objetivos, preguntas o hipótesis, justificación, marco teórico, metodología, resultados, discusión, conclusiones, recomendaciones, matriz de consistencia, operacionalización, coherencia entre secciones, normas universitarias o respuesta a tutor y jurado.

## Ejemplo de uso

```text
Usa $constructor-tesis-academica para diagnosticar y construir una tesis con coherencia entre problema, método, resultados y cierre.
```

## Guía operativa

### Objetivo

Construir o revisar la tesis como un sistema: problema, objetivos, teoría, método, resultados, discusión y cierre deben sostenerse mutuamente. Usar `$editor-en-jefe` para coordinar la ruta general y esta skill como guía especializada.

### Regla central

Diagnosticar la etapa real y la norma institucional antes de redactar. No rellenar secciones por plantilla. Proteger citas textuales, transcripciones, DOI, URL, tablas, figuras, anexos, instrumentos, código, fórmulas y datos empíricos.

### Flujo

1. Diagnosticar si existe idea, anteproyecto, secciones parciales, tesis completa, preentrega u observaciones.
2. Alinear título, problema, objetivo general, objetivos específicos, preguntas o hipótesis, variables o categorías y alcance.
3. Construir la matriz de consistencia cuando el enfoque o la institución la requieran. Leer `references/matriz-consistencia.md`.
4. Ordenar secciones conforme a la guía universitaria; si no existe, usar la estructura común como propuesta sujeta a adaptación.
5. Intervenir por capas: lógica y evidencia; redacción y continuidad; formato y preentrega.
6. Antes de cerrar discusión y conclusiones, activar `$verificador-resultados-investigacion` cuando existan cálculos, tablas, figuras, categorías o afirmaciones empíricas comprobables. Resolver o declarar errores, inconsistencias, límites de verificación y revisiones metodológicas pendientes.
7. Exigir que cada objetivo tenga soporte teórico, método, resultado, discusión y conclusión correspondientes. Si cambia un resultado, reabrir todos sus derivados.
8. Entregar versión revisada, cambios realizados, pendientes críticos, informe de verificación cuando corresponda y siguiente acción.

### Coordinación

- Usar `$humanizar-redaccion-academica` cuando el contenido sea suficiente pero la prosa resulte mecánica.
- Usar `$humanizar-redaccion-academica` cuando la redacción sea abstracta o intercambiable.
- Usar `$redaccion-articulo-cientifico-imryd` para convertir una contribución de la tesis en artículo.
- Usar `$verificador-resultados-investigacion` para comprobar resultados y documentar cada corrección; su automatización no sustituye revisión estadística, metodológica o disciplinar.
- No humanizar antes de resolver problema, objetivos, método, resultados y citas.

### Referencias

- Leer `references/diagnostico-tesis.md` para decidir etapa y riesgos.
- Leer `references/estructura-capitulos.md` para orientar la arquitectura.
- Leer `references/matriz-consistencia.md` para comprobar trazabilidad.

## Recursos incluidos

### Referencias

| Recurso | Función |
| --- | --- |
| [`references/diagnostico-tesis.md`](../../constructor-tesis-academica/references/diagnostico-tesis.md) | Diagnóstico de tesis |
| [`references/estructura-capitulos.md`](../../constructor-tesis-academica/references/estructura-capitulos.md) | Estructura común de tesis |
| [`references/matriz-consistencia.md`](../../constructor-tesis-academica/references/matriz-consistencia.md) | Matriz de consistencia |

### Configuración de interfaz

| Recurso | Función |
| --- | --- |
| [`agents/openai.yaml`](../../constructor-tesis-academica/agents/openai.yaml) | Metadatos de interfaz e invocación de la skill. |

## Fuente normativa

Esta ficha se genera desde [`constructor-tesis-academica/SKILL.md`](../../constructor-tesis-academica/SKILL.md), que permanece como contrato normativo. Regenera la ficha después de modificar ese archivo.
