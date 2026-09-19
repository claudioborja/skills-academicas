# Descarga Y Revisión Manual De Todas Las Fuentes

## Regla De Admisibilidad

Una fuente solo puede adquirir estado `used`, `cited` o `included` cuando existe una copia completa, legítimamente obtenida, legible e inventariada dentro del proyecto. Aplicar la regla a estudios primarios, secundarios, metodológicos, normativos y contextuales.

No considerar texto completo:

- resumen o abstract;
- registro bibliográfico o metadatos;
- DOI o URL sin archivo;
- página de resultados;
- fragmento generado por un buscador;
- referencia citada por otra publicación;
- vista previa incompleta;
- archivo corrupto, cifrado o ilegible.

## Secuencia Obligatoria

1. Identificar la fuente con `source_id` y, para estudios primarios, `study_id`.
2. Obtener el texto completo por una vía legal: acceso abierto, suscripción institucional, repositorio autorizado, copia del autor o provisión legítima del usuario.
3. Registrar el archivo como `fulltext` mediante `register-source`; conservar ruta y SHA-256.
4. Abrir el archivo y comprobar que corresponde a la referencia, está completo y es legible.
5. Revisar manualmente contenido, tablas, figuras, anexos y referencias pertinentes.
6. Registrar revisor, fecha y resultado en `04_fuentes/04_metadatos/04-04_fuentes-usadas.csv`.
7. Vincular los estudios primarios incluidos mediante `fulltext_record_id` en `03_seleccion/01_registro-maestro/03-01_registros-maestros.csv`.
8. Registrar cada uso en el manuscrito en `09_auditorias/04_citas/09-04_auditoria-citas.csv`, con afirmación, localizador y verificación contra el archivo local.

## Recurso No Descargable

Agotar solo vías legítimas. No eludir controles de acceso ni descargar copias no autorizadas.

Si no se obtiene un texto completo utilizable:

- asignar `FT-NO-DESCARGADO`;
- registrar URL, DOI, intentos, fecha y motivo en `04_fuentes/05_inaccesibles/`;
- excluirlo del corpus;
- no evaluar su calidad;
- no extraer datos;
- no incorporarlo a la síntesis;
- no usarlo para respaldar afirmaciones ni citarlo como evidencia.

El registro de inaccesibilidad sirve para transparencia, no convierte la fuente en evidencia. La ausencia de descarga no admite excepción metodológica.

## Comprobaciones De Auditoría

La auditoría debe devolver `BLOCKED` cuando:

- un estudio incluido no tenga `fulltext_record_id`;
- el archivo inventariado no exista o su hash haya cambiado;
- una fuente usada no figure como `fulltext` e `included`;
- falte revisión manual de contenido o citas;
- falten revisor o fecha;
- calidad, extracción o mapa de evidencia mencionen estudios sin archivo local revisado;
- el informe se cierre sin auditar contra el archivo local cada fuente citada.
