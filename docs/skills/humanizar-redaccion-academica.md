# Humanizar Redaccion Academica

Revisa prosa académica genérica, mecánica o fragmentada y la alinea con una voz definida, preservando evidencia, citas y desarrollo. Usar para desgenericar, recuperar continuidad o extraer y comparar perfiles de estilo; no sustituye la redacción de resultados ni la corrección ortográfica final.

## Uso

Invócala directamente con `$humanizar-redaccion-academica` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $humanizar-redaccion-academica para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Modos
- Flujo y protección
- Herramientas reutilizables
- Evidencia y reportes
- Límites de automatización

## Recursos incluidos

### Scripts

- [`scripts/analizar_marcas_ia.py`](../../humanizar-redaccion-academica/scripts/analizar_marcas_ia.py)
- [`scripts/analizar_reporte_compilatio.py`](../../humanizar-redaccion-academica/scripts/analizar_reporte_compilatio.py)
- [`scripts/auditar_respaldo_citas_pdf.py`](../../humanizar-redaccion-academica/scripts/auditar_respaldo_citas_pdf.py)
- [`scripts/comparar_con_perfil_estilo.py`](../../humanizar-redaccion-academica/scripts/comparar_con_perfil_estilo.py)
- [`scripts/conectar_prosa_final_txt.py`](../../humanizar-redaccion-academica/scripts/conectar_prosa_final_txt.py)
- [`scripts/documento_a_perfil_estilo.py`](../../humanizar-redaccion-academica/scripts/documento_a_perfil_estilo.py)
- [`scripts/limpiar_entrega_final_txt.py`](../../humanizar-redaccion-academica/scripts/limpiar_entrega_final_txt.py)
- [`scripts/perfilar_y_comparar_estilo.py`](../../humanizar-redaccion-academica/scripts/perfilar_y_comparar_estilo.py)
- [`scripts/resumir_alertas_respaldo_citas.py`](../../humanizar-redaccion-academica/scripts/resumir_alertas_respaldo_citas.py)

### Referencias

- [`references/auditoria-lexica-citas.md`](../../humanizar-redaccion-academica/references/auditoria-lexica-citas.md)
- [`references/estrategias.md`](../../humanizar-redaccion-academica/references/estrategias.md)
- [`references/patrones-de-genericidad.md`](../../humanizar-redaccion-academica/references/patrones-de-genericidad.md)
- [`references/perfil-de-estilo.md`](../../humanizar-redaccion-academica/references/perfil-de-estilo.md)
- [`references/tecnicas-de-especificacion.md`](../../humanizar-redaccion-academica/references/tecnicas-de-especificacion.md)

### Pruebas

- [`tests/test_configuracion.py`](../../humanizar-redaccion-academica/tests/test_configuracion.py)
- [`tests/test_conservacion.py`](../../humanizar-redaccion-academica/tests/test_conservacion.py)

### Configuración de interfaz

- [`agents/openai.yaml`](../../humanizar-redaccion-academica/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `workflow-maestro-academico-editorial` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`humanizar-redaccion-academica/SKILL.md`](../../humanizar-redaccion-academica/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
