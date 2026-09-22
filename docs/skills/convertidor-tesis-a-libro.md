# Convertidor Tesis A Libro

Úsalo cuando el usuario necesite transformar una tesis, tesina, trabajo de grado, disertación, informe de investigación o manuscrito universitario en un libro académico, divulgativo o profesional. Aplica para diagnosticar marcas de tesis, rediseñar índice, convertir objetivos e hipótesis en promesa editorial, adaptar marco teórico y metodología, reubicar resultados, crear capítulos legibles, eliminar lenguaje de tribunal/universidad, preparar prólogo, introducción, conclusiones, glosario, bibliografía, tablas, figuras y plan de publicación sin perder rigor ni alterar citas textuales, datos, fuentes o evidencias.

## Uso

Invócala directamente con `$convertidor-tesis-a-libro` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $convertidor-tesis-a-libro para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Objetivo
- Regla Central
- Diagnóstico Inicial
- Flujo De Transformación
- Qué Cambiar
- Qué Conservar
- Criterios De Decisión
- Salida Esperada
- Validación Final

## Recursos incluidos

### Herramientas automatizadas

- [`scripts/diagnosticar_tesis.py`](../../convertidor-tesis-a-libro/scripts/diagnosticar_tesis.py)

### Referencias

- [`references/arquitectura-libro-derivado.md`](../../convertidor-tesis-a-libro/references/arquitectura-libro-derivado.md)
- [`references/mapa-transformacion.md`](../../convertidor-tesis-a-libro/references/mapa-transformacion.md)
- [`references/marcas-de-tesis.md`](../../convertidor-tesis-a-libro/references/marcas-de-tesis.md)

### Pruebas

- [`tests/test_diagnosticar_tesis.py`](../../convertidor-tesis-a-libro/tests/test_diagnosticar_tesis.py)

### Configuración de interfaz

- [`agents/openai.yaml`](../../convertidor-tesis-a-libro/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `editor-en-jefe` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`convertidor-tesis-a-libro/SKILL.md`](../../convertidor-tesis-a-libro/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
