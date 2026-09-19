# Workflow Maestro Academico Editorial

Coordina las skills académicas y editoriales según el producto y la etapa del manuscrito. Usar para organizar proyectos de libro, tesis, artículo o revisión y seleccionar apoyos sin duplicar intervenciones.

## Uso

Invócala directamente con `$workflow-maestro-academico-editorial` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $workflow-maestro-academico-editorial para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Responsabilidad
- Reglas compartidas
- Ruta de trabajo
- Entregables y recursos
- Recursos bajo demanda
- Cierre

## Recursos incluidos

### Scripts

- [`scripts/archivos_seguros.py`](../../workflow-maestro-academico-editorial/scripts/archivos_seguros.py)
- [`scripts/ejecutar.py`](../../workflow-maestro-academico-editorial/scripts/ejecutar.py)
- [`scripts/generar_documentacion_skills.py`](../../workflow-maestro-academico-editorial/scripts/generar_documentacion_skills.py)
- [`scripts/requirements-mantenimiento.txt`](../../workflow-maestro-academico-editorial/scripts/requirements-mantenimiento.txt)
- [`scripts/validar_coleccion.py`](../../workflow-maestro-academico-editorial/scripts/validar_coleccion.py)

### Referencias

- [`references/auditoria-automatizacion.md`](../../workflow-maestro-academico-editorial/references/auditoria-automatizacion.md)
- [`references/diagnostico-por-etapa.md`](../../workflow-maestro-academico-editorial/references/diagnostico-por-etapa.md)
- [`references/mapa-responsabilidades.md`](../../workflow-maestro-academico-editorial/references/mapa-responsabilidades.md)
- [`references/migracion-27-skills.md`](../../workflow-maestro-academico-editorial/references/migracion-27-skills.md)
- [`references/perfiles-editoriales.md`](../../workflow-maestro-academico-editorial/references/perfiles-editoriales.md)
- [`references/portabilidad.md`](../../workflow-maestro-academico-editorial/references/portabilidad.md)
- [`references/ruta-de-trabajo.md`](../../workflow-maestro-academico-editorial/references/ruta-de-trabajo.md)

### Plantillas y recursos

- [`assets/migraciones/antes-fusion-20260919.zip`](../../workflow-maestro-academico-editorial/assets/migraciones/antes-fusion-20260919.zip)
- [`assets/migraciones/apa7-previo-20260919.zip`](../../workflow-maestro-academico-editorial/assets/migraciones/apa7-previo-20260919.zip)

### Pruebas

- [`tests/test_flujos_seguros.py`](../../workflow-maestro-academico-editorial/tests/test_flujos_seguros.py)
- [`tests/test_generar_documentacion.py`](../../workflow-maestro-academico-editorial/tests/test_generar_documentacion.py)
- [`tests/test_informes_seguros.py`](../../workflow-maestro-academico-editorial/tests/test_informes_seguros.py)
- [`tests/test_portabilidad.py`](../../workflow-maestro-academico-editorial/tests/test_portabilidad.py)
- [`tests/test_publicacion_stream.py`](../../workflow-maestro-academico-editorial/tests/test_publicacion_stream.py)
- [`tests/test_registros_seguros.py`](../../workflow-maestro-academico-editorial/tests/test_registros_seguros.py)
- [`tests/test_salidas_restantes.py`](../../workflow-maestro-academico-editorial/tests/test_salidas_restantes.py)
- [`tests/test_seguridad.py`](../../workflow-maestro-academico-editorial/tests/test_seguridad.py)
- [`tests/test_validar_coleccion.py`](../../workflow-maestro-academico-editorial/tests/test_validar_coleccion.py)

### Configuración de interfaz

- [`agents/openai.yaml`](../../workflow-maestro-academico-editorial/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `workflow-maestro-academico-editorial` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`workflow-maestro-academico-editorial/SKILL.md`](../../workflow-maestro-academico-editorial/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
