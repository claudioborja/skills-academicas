# Revisión Sistemática PRISMA

Planifica, documenta, audita y redacta revisiones sistemáticas y metaanálisis con PRISMA 2020, PRISMA-P y PRISMA-S, seleccionando extensiones oficiales cuando corresponda. Usar para protocolos, búsquedas reproducibles, cribado, diagramas de flujo, matrices de cumplimiento, síntesis y reporte transparente; no usar como sustituto de un método de conducción disciplinar ni para revisiones Kitchenham.

## Uso

Invócala directamente con `$revision-sistematica-prisma` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $revision-sistematica-prisma para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Autoridad y límite metodológico
- Enrutamiento
- Resultado esperado
- Flujo de trabajo
- Auditoría y bloqueos
- Coordinación

## Recursos incluidos

### Herramientas automatizadas

- [`scripts/auditar_prisma.py`](../../revision-sistematica-prisma/scripts/auditar_prisma.py)

### Referencias

- [`references/evaluacion-sintesis.md`](../../revision-sistematica-prisma/references/evaluacion-sintesis.md)
- [`references/flujo-trazabilidad.md`](../../revision-sistematica-prisma/references/flujo-trazabilidad.md)
- [`references/fuentes-oficiales.md`](../../revision-sistematica-prisma/references/fuentes-oficiales.md)
- [`references/matriz-reporte-prisma-2020.md`](../../revision-sistematica-prisma/references/matriz-reporte-prisma-2020.md)
- [`references/protocolo-busqueda.md`](../../revision-sistematica-prisma/references/protocolo-busqueda.md)
- [`references/seleccion-guia-extension.md`](../../revision-sistematica-prisma/references/seleccion-guia-extension.md)

### Plantillas y recursos

- [`assets/conteos-flujo-ejemplo.json`](../../revision-sistematica-prisma/assets/conteos-flujo-ejemplo.json)
- [`assets/exclusiones-texto-completo.csv`](../../revision-sistematica-prisma/assets/exclusiones-texto-completo.csv)
- [`assets/matriz-prisma-2020.csv`](../../revision-sistematica-prisma/assets/matriz-prisma-2020.csv)
- [`assets/registro-busquedas.csv`](../../revision-sistematica-prisma/assets/registro-busquedas.csv)

### Pruebas

- [`tests/test_auditar_prisma.py`](../../revision-sistematica-prisma/tests/test_auditar_prisma.py)

### Configuración de interfaz

- [`agents/openai.yaml`](../../revision-sistematica-prisma/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `editor-en-jefe` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`revision-sistematica-prisma/SKILL.md`](../../revision-sistematica-prisma/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
