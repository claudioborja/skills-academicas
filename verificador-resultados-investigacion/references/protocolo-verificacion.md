# Protocolo de verificación

## Alcance inicial

Definir antes de revisar:

- producto y versión;
- resultados incluidos y excluidos;
- fuentes disponibles;
- autoridad de cada fuente;
- controles mecánicos y revisiones sustantivas previstas;
- tolerancia de redondeo;
- responsables de verificar, aprobar y aplicar;
- criterio de cierre y tratamiento de conflictos.

No ampliar el alcance silenciosamente desde verificación aritmética hacia una auditoría de integridad.

## Jerarquía de evidencia

La autoridad depende del proyecto, pero debe documentarse. Una jerarquía orientativa es:

1. datos originales preservados y diccionario de datos;
2. código o consulta versionada que genera el resultado;
3. salida original del software con parámetros;
4. tabla o matriz de análisis aprobada;
5. manuscrito fuente;
6. copias adaptadas para artículo, libro o presentación.

Una capa inferior no corrige por sí sola una superior. Si dos fuentes del mismo nivel difieren, clasificar como inconsistencia hasta resolverla.

## Esquema del auditor mecánico

Campos comunes:

- `id`: identificador seguro y único;
- `ubicacion`: sección, tabla, figura o página;
- `afirmacion`: texto que comunica el resultado;
- `tipo`: `porcentaje`, `suma`, `media`, `total_grupos` o `consistencia`;
- `reportado`: valor presentado;
- `fuente`: artefacto declarado como respaldo.

Campos por tipo:

- porcentaje: `numerador`, `denominador`;
- suma: `componentes`;
- media: `valores`;
- total de grupos: `grupos`;
- consistencia: `apariciones`, cada una con `ubicacion` y `valor`.

Los valores del JSON son insumos declarados, no evidencia independiente. Antes de aceptar una corrección, contrastarlos con la fuente real.

## Puertas de decisión

- Si faltan insumos: no verificable.
- Si el cálculo coincide: verificado mecánicamente, no científicamente certificado.
- Si no coincide y la fuente es inequívoca: error confirmado y propuesta.
- Si las fuentes difieren: inconsistente, sin elegir por mayoría.
- Si el problema afecta método o interpretación: revisión metodológica.
- Si existe sospecha seria sobre integridad: conservar evidencia y escalar; no investigar informalmente dentro de una edición.
