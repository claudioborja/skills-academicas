# Filtro Editoriales Depredadoras

Úsalo como filtro auxiliar antes de buscar, descargar, citar o validar fuentes académicas, cuando sea necesario evitar revistas, editoriales, congresos, plataformas o sitios clonados potencialmente depredadores, espurios o de reputación dudosa. Aplica especialmente en búsquedas bibliográficas APA 7, IEEE, revisión de bibliografía, selección de revistas, verificación de DOI, acceso abierto, indexación real, Scopus/WoS/DOAJ/SciELO/Redalyc/Latindex y evaluación de fuentes de América Latina, el Caribe e Iberoamérica.

## Uso

Invócala directamente con `$filtro-editoriales-depredadoras` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $filtro-editoriales-depredadoras para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Objetivo
- Regla central
- Cuándo activarlo
- Flujo de verificación
- Clasificación
- Salida esperada
- Validación final
- Referencias de apoyo

## Recursos incluidos

### Scripts

- [`scripts/check_editorial_risk.py`](../../filtro-editoriales-depredadoras/scripts/check_editorial_risk.py)

### Referencias

- [`references/criterios-verificacion.md`](../../filtro-editoriales-depredadoras/references/criterios-verificacion.md)
- [`references/lista-alerta-local.md`](../../filtro-editoriales-depredadoras/references/lista-alerta-local.md)
- [`references/watchlist.json`](../../filtro-editoriales-depredadoras/references/watchlist.json)

### Pruebas

- [`tests/test_coincidencias.py`](../../filtro-editoriales-depredadoras/tests/test_coincidencias.py)

### Configuración de interfaz

- [`agents/openai.yaml`](../../filtro-editoriales-depredadoras/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `editor-en-jefe` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`filtro-editoriales-depredadoras/SKILL.md`](../../filtro-editoriales-depredadoras/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
