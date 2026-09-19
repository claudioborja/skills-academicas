# Planificador Obra Academica

Úsalo cuando el usuario necesite convertir una idea, tema o borrador en la arquitectura completa de una obra académica o editorial, incluyendo propósito, alcance, lector, objetivos, índice, secuencia de capítulos, progresión argumentativa, distribución de extensión y estructura local de directorios capaz de sostener investigación, manuscrito, casos, recursos, revisión y entregables. Aplica a libros nuevos, tesis, informes extensos, manuales, artículos largos y proyectos editoriales que deban inicializarse o normalizarse.

## Uso

Invócala directamente con `$planificador-obra-academica` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $planificador-obra-academica para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Ejecución multiplataforma
- Objetivo
- Cuándo usarlo
- Flujo de trabajo
- Perfil editorial predeterminado
- Inicialización obligatoria de libros
- Validación final
- Referencias de apoyo

## Recursos incluidos

### Scripts

- [`scripts/inicializar_proyecto_libro.py`](../../planificador-obra-academica/scripts/inicializar_proyecto_libro.py)

### Referencias

- [`references/arquitectura-de-obra.md`](../../planificador-obra-academica/references/arquitectura-de-obra.md)
- [`references/estructura-directorios-libro.md`](../../planificador-obra-academica/references/estructura-directorios-libro.md)

### Pruebas

- [`tests/test_inicializacion_segura.py`](../../planificador-obra-academica/tests/test_inicializacion_segura.py)

### Configuración de interfaz

- [`agents/openai.yaml`](../../planificador-obra-academica/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `workflow-maestro-academico-editorial` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`planificador-obra-academica/SKILL.md`](../../planificador-obra-academica/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
