# Gestor de contribuciones y autoría

Selecciona, aplica y audita taxonomías de contribución, criterios de autoría y formatos de metadatos según la obra y su destino. Usar para declaraciones de contribuciones, orden y elegibilidad de autoría, reconocimientos, datasets, software, libros, traducciones, JATS, Crossref, DataCite, ORCID o grafos de procedencia; no usar CRediT como criterio automático de autoría ni para resolver disputas sin la política aplicable.

## Uso

Invócala directamente con `$gestor-contribuciones-autoria` o permite que el orquestador la seleccione según el encargo.

Ejemplo:

```text
Usa $gestor-contribuciones-autoria para [describe aquí la tarea y los archivos de entrada].
```

## Cobertura

- Responsabilidad
- Información mínima
- Selección del perfil
- Flujo de trabajo
- Controles
- Coordinación

## Recursos incluidos

### Herramientas automatizadas

- [`scripts/seleccionar_perfil.py`](../../gestor-contribuciones-autoria/scripts/seleccionar_perfil.py)

### Referencias

- [`references/autoria-responsabilidad.md`](../../gestor-contribuciones-autoria/references/autoria-responsabilidad.md)
- [`references/fuentes-oficiales.md`](../../gestor-contribuciones-autoria/references/fuentes-oficiales.md)
- [`references/representacion-tecnica.md`](../../gestor-contribuciones-autoria/references/representacion-tecnica.md)
- [`references/roles-credit.md`](../../gestor-contribuciones-autoria/references/roles-credit.md)
- [`references/seleccion-perfiles.md`](../../gestor-contribuciones-autoria/references/seleccion-perfiles.md)

### Plantillas y recursos

- [`assets/contexto-ejemplo.json`](../../gestor-contribuciones-autoria/assets/contexto-ejemplo.json)
- [`assets/matriz-contribuciones.csv`](../../gestor-contribuciones-autoria/assets/matriz-contribuciones.csv)

### Pruebas

- [`tests/test_seleccionar_perfil.py`](../../gestor-contribuciones-autoria/tests/test_seleccionar_perfil.py)

### Configuración de interfaz

- [`agents/openai.yaml`](../../gestor-contribuciones-autoria/agents/openai.yaml)

## Integración

Para una tarea aislada puede invocarse directamente. En proyectos académicos completos, usa `editor-en-jefe` para decidir el orden y evitar intervenciones duplicadas.

Consulta las instrucciones normativas en [`gestor-contribuciones-autoria/SKILL.md`](../../gestor-contribuciones-autoria/SKILL.md). Esta ficha es una guía de navegación y no reemplaza ese contrato.
