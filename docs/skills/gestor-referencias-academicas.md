# Gestor Referencias Academicas

Busca, verifica y utiliza fuentes académicas para respaldar afirmaciones y formatear citas y bibliografía en APA 7 o IEEE. Usar para fortalecer borradores, consultar fuentes completas, organizar evidencia o cambiar de norma bibliográfica; la selección de estudios de una revisión corresponde a su protocolo.

## Uso

Invócala directamente con `$gestor-referencias-academicas` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $gestor-referencias-academicas para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Selección del modo
- Reglas comunes
- Flujo
- Archivos
- Extractor común de PDF
- Glosarios y entrega

## Recursos incluidos

### Scripts

- [`scripts/pdf_a_contexto.py`](../../gestor-referencias-academicas/scripts/pdf_a_contexto.py)

### Referencias

- [`references/apa7-practico.md`](../../gestor-referencias-academicas/references/apa7-practico.md)
- [`references/busqueda-y-descarga.md`](../../gestor-referencias-academicas/references/busqueda-y-descarga.md)
- [`references/ieee-practico.md`](../../gestor-referencias-academicas/references/ieee-practico.md)

### Pruebas

- [`tests/test_descargas.py`](../../gestor-referencias-academicas/tests/test_descargas.py)
- [`tests/test_extractor.py`](../../gestor-referencias-academicas/tests/test_extractor.py)

### Configuración de interfaz

- [`agents/openai.yaml`](../../gestor-referencias-academicas/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `workflow-maestro-academico-editorial` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`gestor-referencias-academicas/SKILL.md`](../../gestor-referencias-academicas/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
