# Verificador de resultados de investigación

Verifica resultados cuantitativos y cualitativos antes de reutilizarlos, publicarlos o convertirlos en capítulos, distingue errores confirmados de aspectos no verificables y documenta cada intervención. Usar para tesis, artículos, informes, libros derivados, tablas, figuras y conclusiones cuando deban comprobarse cálculos, consistencia, trazabilidad, interpretación o correspondencia con método y objetivos; no usar una comprobación mecánica como certificación científica ni corregir datos sin fuente y autorización.

## Uso

Invócala directamente con `$verificador-resultados-investigacion` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $verificador-resultados-investigacion para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Responsabilidad
- Límites y protección de evidencia
- Activación y alcance
- Flujo de verificación
- Salidas
- Coordinación

## Recursos incluidos

### Herramientas automatizadas

- [`scripts/verificar_resultados.py`](../../verificador-resultados-investigacion/scripts/verificar_resultados.py)

### Referencias

- [`references/fuentes-oficiales.md`](../../verificador-resultados-investigacion/references/fuentes-oficiales.md)
- [`references/informe-intervencion.md`](../../verificador-resultados-investigacion/references/informe-intervencion.md)
- [`references/protocolo-verificacion.md`](../../verificador-resultados-investigacion/references/protocolo-verificacion.md)
- [`references/revision-cualitativa.md`](../../verificador-resultados-investigacion/references/revision-cualitativa.md)
- [`references/revision-cuantitativa.md`](../../verificador-resultados-investigacion/references/revision-cuantitativa.md)

### Plantillas y recursos

- [`assets/registro-intervenciones.csv`](../../verificador-resultados-investigacion/assets/registro-intervenciones.csv)
- [`assets/registro-resultados-ejemplo.json`](../../verificador-resultados-investigacion/assets/registro-resultados-ejemplo.json)

### Pruebas

- [`tests/test_verificar_resultados.py`](../../verificador-resultados-investigacion/tests/test_verificar_resultados.py)

### Configuración de interfaz

- [`agents/openai.yaml`](../../verificador-resultados-investigacion/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `editor-en-jefe` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`verificador-resultados-investigacion/SKILL.md`](../../verificador-resultados-investigacion/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
