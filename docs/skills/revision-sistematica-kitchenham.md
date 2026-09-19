# Revision Sistematica Kitchenham

Planifica, ejecuta, documenta, respalda, analiza y redacta revisiones sistemáticas de literatura siguiendo exclusivamente Kitchenham y Charters para ingeniería de software. Use when Codex needs to desarrollar una revisión desde la pregunta hasta el informe; validar protocolo; seleccionar fuentes por cobertura disciplinar y complementariedad; ejecutar búsquedas reproducibles y snowballing; probar artículos semilla; medir aporte marginal y saturación; descargar localmente, preservar y revisar manualmente todas las fuentes utilizadas; excluir recursos sin texto completo descargable; deduplicar y cribar; evaluar calidad, actualidad, impacto y novedad; extraer y sintetizar evidencia; mantener hashes y snapshots; actualizar búsquedas; o auditar suficiencia metodológica sin imponer cuotas universales de estudios.

## Uso

Invócala directamente con `$revision-sistematica-kitchenham` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $revision-sistematica-kitchenham para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Ejecución multiplataforma
- Autoridad Metodológica
- Regla De Ejecución
- Convención Obligatoria De Numeración
- Regla Absoluta De Descarga Y Uso
- Suficiencia Y Umbrales
- Inicio Obligatorio
- Fases Y Puertas
- Auditoría Metodológica
- Excepciones Y Requisitos Externos
- Respaldo Y Bloqueos
- Entrega Obligatoria

## Recursos incluidos

### Scripts

- [`scripts/kitchenham_workspace.py`](../../revision-sistematica-kitchenham/scripts/kitchenham_workspace.py)

### Referencias

- [`references/artefactos-respaldos.md`](../../revision-sistematica-kitchenham/references/artefactos-respaldos.md)
- [`references/cobertura-impacto-novedad.md`](../../revision-sistematica-kitchenham/references/cobertura-impacto-novedad.md)
- [`references/coordinacion-skills.md`](../../revision-sistematica-kitchenham/references/coordinacion-skills.md)
- [`references/descarga-revision-manual.md`](../../revision-sistematica-kitchenham/references/descarga-revision-manual.md)
- [`references/evaluacion-calidad-sintesis.md`](../../revision-sistematica-kitchenham/references/evaluacion-calidad-sintesis.md)
- [`references/fuentes-base.md`](../../revision-sistematica-kitchenham/references/fuentes-base.md)
- [`references/metodologia-kitchenham.md`](../../revision-sistematica-kitchenham/references/metodologia-kitchenham.md)

### Plantillas y recursos

- [`assets/aporte-marginal-fuentes.csv`](../../revision-sistematica-kitchenham/assets/aporte-marginal-fuentes.csv)
- [`assets/articulos-semilla.csv`](../../revision-sistematica-kitchenham/assets/articulos-semilla.csv)
- [`assets/auditoria-busqueda.md`](../../revision-sistematica-kitchenham/assets/auditoria-busqueda.md)
- [`assets/auditoria-citas.csv`](../../revision-sistematica-kitchenham/assets/auditoria-citas.csv)
- [`assets/cribado.csv`](../../revision-sistematica-kitchenham/assets/cribado.csv)
- [`assets/criterios-cobertura-impacto.md`](../../revision-sistematica-kitchenham/assets/criterios-cobertura-impacto.md)
- [`assets/datos-extraidos.csv`](../../revision-sistematica-kitchenham/assets/datos-extraidos.csv)
- [`assets/desviaciones.csv`](../../revision-sistematica-kitchenham/assets/desviaciones.csv)
- [`assets/distribucion-temporal.csv`](../../revision-sistematica-kitchenham/assets/distribucion-temporal.csv)
- [`assets/evaluacion-calidad.csv`](../../revision-sistematica-kitchenham/assets/evaluacion-calidad.csv)
- [`assets/evaluacion-protocolo.md`](../../revision-sistematica-kitchenham/assets/evaluacion-protocolo.md)
- [`assets/evaluacion-saturacion.csv`](../../revision-sistematica-kitchenham/assets/evaluacion-saturacion.csv)
- [`assets/excepciones-metodologicas.csv`](../../revision-sistematica-kitchenham/assets/excepciones-metodologicas.csv)
- [`assets/exclusiones-texto-completo.csv`](../../revision-sistematica-kitchenham/assets/exclusiones-texto-completo.csv)
- [`assets/formulario-extraccion.md`](../../revision-sistematica-kitchenham/assets/formulario-extraccion.md)
- [`assets/fuentes-consultadas.csv`](../../revision-sistematica-kitchenham/assets/fuentes-consultadas.csv)
- [`assets/fuentes-inaccesibles.csv`](../../revision-sistematica-kitchenham/assets/fuentes-inaccesibles.csv)
- [`assets/fuentes-no-consultadas.csv`](../../revision-sistematica-kitchenham/assets/fuentes-no-consultadas.csv)
- [`assets/fuentes-usadas.csv`](../../revision-sistematica-kitchenham/assets/fuentes-usadas.csv)
- [`assets/instrumento-calidad.md`](../../revision-sistematica-kitchenham/assets/instrumento-calidad.md)
- [`assets/manuscrito.md`](../../revision-sistematica-kitchenham/assets/manuscrito.md)
- [`assets/mapa-evidencia.csv`](../../revision-sistematica-kitchenham/assets/mapa-evidencia.csv)
- [`assets/matriz-brechas-novedad.csv`](../../revision-sistematica-kitchenham/assets/matriz-brechas-novedad.csv)
- [`assets/matriz-impacto-novedad.csv`](../../revision-sistematica-kitchenham/assets/matriz-impacto-novedad.csv)
- [`assets/plan.md`](../../revision-sistematica-kitchenham/assets/plan.md)
- [`assets/protocolo.md`](../../revision-sistematica-kitchenham/assets/protocolo.md)
- [`assets/registro-busquedas.csv`](../../revision-sistematica-kitchenham/assets/registro-busquedas.csv)
- [`assets/registros-maestros.csv`](../../revision-sistematica-kitchenham/assets/registros-maestros.csv)
- [`assets/snowballing.csv`](../../revision-sistematica-kitchenham/assets/snowballing.csv)

### Pruebas

- [`tests/test_escritura_segura.py`](../../revision-sistematica-kitchenham/tests/test_escritura_segura.py)

### Configuración de interfaz

- [`agents/openai.yaml`](../../revision-sistematica-kitchenham/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `workflow-maestro-academico-editorial` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`revision-sistematica-kitchenham/SKILL.md`](../../revision-sistematica-kitchenham/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
