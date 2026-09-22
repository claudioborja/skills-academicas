# Gestor Imagenes Academicas Libros

Genera, localiza, evalúa, descarga y documenta imágenes para libros académicos, tesis, artículos y materiales educativos. Usar cuando Codex deba crear ilustraciones originales, diagramas o imágenes conceptuales; buscar figuras, mapas, fotografías o gráficos en fuentes académicas e institucionales confiables; comprobar licencia y atribución; preparar pies de figura; o integrar recursos visuales con trazabilidad editorial sin confundir ilustración con evidencia científica.

## Uso

Invócala directamente con `$gestor-imagenes-academicas-libros` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $gestor-imagenes-academicas-libros para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Principio rector
- Regla de necesidad y orden de preferencia
- Puerta de procedencia antes de generar
- Flujo operativo
- Registro de trazabilidad
- Selección de ruta y coordinación con imagegen
- Ruta A: localizar y descargar
- Ruta B: generar una imagen original
- Pies, atribución y archivo
- Integración con otras skills
- Criterios de cierre

## Recursos incluidos

### Scripts

- [`scripts/inspeccionar_imagen.py`](../../gestor-imagenes-academicas-libros/scripts/inspeccionar_imagen.py)
- [`scripts/registrar_imagen.py`](../../gestor-imagenes-academicas-libros/scripts/registrar_imagen.py)
- [`scripts/requirements-lock.txt`](../../gestor-imagenes-academicas-libros/scripts/requirements-lock.txt)

### Referencias

- [`references/fuentes-y-licencias.md`](../../gestor-imagenes-academicas-libros/references/fuentes-y-licencias.md)
- [`references/pies-y-trazabilidad.md`](../../gestor-imagenes-academicas-libros/references/pies-y-trazabilidad.md)

### Pruebas

- [`tests/test_inspeccionar_imagen.py`](../../gestor-imagenes-academicas-libros/tests/test_inspeccionar_imagen.py)
- [`tests/test_registrar_imagen.py`](../../gestor-imagenes-academicas-libros/tests/test_registrar_imagen.py)

### Configuración de interfaz

- [`agents/openai.yaml`](../../gestor-imagenes-academicas-libros/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `editor-en-jefe` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`gestor-imagenes-academicas-libros/SKILL.md`](../../gestor-imagenes-academicas-libros/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
