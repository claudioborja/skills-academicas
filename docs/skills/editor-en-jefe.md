# Editor en jefe

Coordina las skills académicas y editoriales según el producto y la etapa del manuscrito. Usar para organizar proyectos de libro, tesis, artículo o revisión y seleccionar apoyos sin duplicar intervenciones.

## Uso

Invócala directamente con `$editor-en-jefe` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $editor-en-jefe para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Responsabilidad
- Reglas compartidas
- Ruta de trabajo
- Entregables y recursos
- Recursos bajo demanda
- Cierre

## Recursos incluidos

### Herramientas automatizadas

- [`scripts/archivos_seguros.py`](../../editor-en-jefe/scripts/archivos_seguros.py)
- [`scripts/ejecutar.py`](../../editor-en-jefe/scripts/ejecutar.py)
- [`scripts/generar_documentacion_skills.py`](../../editor-en-jefe/scripts/generar_documentacion_skills.py)
- [`scripts/instalar_requisitos.py`](../../editor-en-jefe/scripts/instalar_requisitos.py)
- [`scripts/preparar_runtime_portable.py`](../../editor-en-jefe/scripts/preparar_runtime_portable.py)
- [`scripts/requirements-mantenimiento.txt`](../../editor-en-jefe/scripts/requirements-mantenimiento.txt)
- [`scripts/requirements.txt`](../../editor-en-jefe/scripts/requirements.txt)
- [`scripts/validar_coleccion.py`](../../editor-en-jefe/scripts/validar_coleccion.py)

### Referencias

- [`references/auditoria-automatizacion.md`](../../editor-en-jefe/references/auditoria-automatizacion.md)
- [`references/diagnostico-por-etapa.md`](../../editor-en-jefe/references/diagnostico-por-etapa.md)
- [`references/interpretacion-contexto-editorial.md`](../../editor-en-jefe/references/interpretacion-contexto-editorial.md)
- [`references/mapa-responsabilidades.md`](../../editor-en-jefe/references/mapa-responsabilidades.md)
- [`references/migracion-27-skills.md`](../../editor-en-jefe/references/migracion-27-skills.md)
- [`references/perfiles-editoriales.md`](../../editor-en-jefe/references/perfiles-editoriales.md)
- [`references/portabilidad.md`](../../editor-en-jefe/references/portabilidad.md)
- [`references/produccion-editorial-eficiente.md`](../../editor-en-jefe/references/produccion-editorial-eficiente.md)
- [`references/ruta-de-trabajo.md`](../../editor-en-jefe/references/ruta-de-trabajo.md)

### Plantillas y recursos

- [`assets/migraciones/antes-fusion-20260919.zip`](../../editor-en-jefe/assets/migraciones/antes-fusion-20260919.zip)
- [`assets/migraciones/apa7-previo-20260919.zip`](../../editor-en-jefe/assets/migraciones/apa7-previo-20260919.zip)

### Pruebas

- [`tests/test_flujos_seguros.py`](../../editor-en-jefe/tests/test_flujos_seguros.py)
- [`tests/test_generar_documentacion.py`](../../editor-en-jefe/tests/test_generar_documentacion.py)
- [`tests/test_informes_seguros.py`](../../editor-en-jefe/tests/test_informes_seguros.py)
- [`tests/test_instalar_requisitos.py`](../../editor-en-jefe/tests/test_instalar_requisitos.py)
- [`tests/test_portabilidad.py`](../../editor-en-jefe/tests/test_portabilidad.py)
- [`tests/test_publicacion_stream.py`](../../editor-en-jefe/tests/test_publicacion_stream.py)
- [`tests/test_registros_seguros.py`](../../editor-en-jefe/tests/test_registros_seguros.py)
- [`tests/test_runtime_portable_assets.py`](../../editor-en-jefe/tests/test_runtime_portable_assets.py)
- [`tests/test_runtime_portable_bundle.py`](../../editor-en-jefe/tests/test_runtime_portable_bundle.py)
- [`tests/test_salidas_restantes.py`](../../editor-en-jefe/tests/test_salidas_restantes.py)
- [`tests/test_seguridad.py`](../../editor-en-jefe/tests/test_seguridad.py)
- [`tests/test_validar_coleccion.py`](../../editor-en-jefe/tests/test_validar_coleccion.py)

### Configuración de interfaz

- [`agents/openai.yaml`](../../editor-en-jefe/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `editor-en-jefe` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`editor-en-jefe/SKILL.md`](../../editor-en-jefe/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
