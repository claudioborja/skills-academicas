# Skills académicas y editoriales para Codex

Colección de 28 skills coordinadas para planificar, investigar, redactar, revisar y entregar tesis, libros, artículos científicos y revisiones sistemáticas. Incluye automatización reproducible para documentos, referencias, imágenes, ecuaciones, tablas, formato APA 7, IEEE y control de preentrega.

La colección está diseñada para trabajar de dos maneras:

- **Uso directo:** invocar una skill cuando la tarea está claramente delimitada.
- **Uso orquestado:** empezar con `workflow-maestro-academico-editorial` para que seleccione las especialidades necesarias y determine su orden sin repetir intervenciones.

## Qué resuelve

- Arquitectura y continuidad de libros, tesis y manuscritos extensos.
- Conversión de tesis en libros y redacción de artículos IMRyD.
- Revisión sistemática Kitchenham para ingeniería de software.
- Búsqueda, verificación y consistencia de referencias APA 7 e IEEE.
- Redacción académica en español latinoamericano, estilo y ortotipografía.
- Tablas, figuras, imágenes científicas y ecuaciones editables.
- Preprocesamiento de PDF, DOCX, HTML, TXT y Markdown.
- Exportación y control final de documentos Word/PDF.
- Auditorías mecánicas reproducibles que apoyan, pero no reemplazan, el juicio académico.

El [catálogo completo](docs/skills/README.md) contiene una ficha independiente por cada skill.

## El orquestador

`workflow-maestro-academico-editorial` es la entrada recomendada para encargos que afectan varias etapas o varios artefactos. Su función es identificar:

1. producto final: tesis, libro, artículo o revisión;
2. etapa real del trabajo;
3. método y norma aplicables;
4. materiales disponibles;
5. skills mínimas necesarias y orden de ejecución.

El orquestador no ejecuta todas las skills por rutina. Mantiene las fronteras entre metodología, evidencia, redacción, revisión, recursos visuales y maquetación. Consulta la [guía del orquestador](docs/orquestador.md) y su [mapa de responsabilidades](workflow-maestro-academico-editorial/references/mapa-responsabilidades.md).

Ejemplo:

```text
Usa $workflow-maestro-academico-editorial para diagnosticar este manuscrito, identificar la etapa actual y ejecutar solo las revisiones necesarias antes de entregarlo en Word.
```

## Uso directo

Cuando el alcance está claro, invoca la especialidad por nombre:

```text
Usa $gestor-ecuaciones-academicas para revisar las ecuaciones, unidades y referencias cruzadas de este capítulo.
```

```text
Usa $gestor-imagenes-academicas-libros para preparar una ilustración anatómica hiperrealista con trazabilidad editorial.
```

```text
Usa $gestor-referencias-academicas para verificar y normalizar estas referencias en IEEE.
```

Las instrucciones normativas están siempre en el `SKILL.md` de cada directorio. Las fichas de `docs/skills/` son guías de navegación y no sustituyen esas instrucciones.

## Estructura

```text
skills/
├── README.md
├── docs/
│   ├── orquestador.md
│   └── skills/
├── workflow-maestro-academico-editorial/
│   ├── SKILL.md
│   ├── scripts/
│   ├── references/
│   └── tests/
└── <skill>/
    ├── SKILL.md
    ├── agents/
    ├── scripts/
    ├── references/
    ├── assets/
    └── tests/
```

Cada script especializado permanece dentro de la skill que lo posee. El único lanzador general es `workflow-maestro-academico-editorial/scripts/ejecutar.py`.

## Instalación

Requisitos generales:

- Codex con soporte para skills locales.
- Python 3.10 o posterior para los scripts.
- Dependencias opcionales indicadas por los archivos `requirements*.txt` de cada skill.

Clona el repositorio en una ubicación de trabajo y copia los directorios de skills a `$CODEX_HOME/skills` o `~/.codex/skills`. No copies `docs/`, `.git/` ni los entornos `.runtime/`.

En Linux o macOS:

```text
cp -R <skill> "${CODEX_HOME:-$HOME/.codex}/skills/"
```

En PowerShell:

```text
Copy-Item -Recurse <skill> "$env:USERPROFILE\.codex\skills\"
```

Para usar el flujo completo deben instalarse juntos el orquestador y las skills que este pueda activar. La documentación detallada de portabilidad está en [`portabilidad.md`](workflow-maestro-academico-editorial/references/portabilidad.md).

## Automatización y portabilidad

Los scripts se ejecutan mediante Python y evitan depender del shell cuando la operación debe funcionar en Linux, Windows y macOS. El lanzador general protege entradas y salidas comunes:

```text
python workflow-maestro-academico-editorial/scripts/ejecutar.py <skill>/scripts/<script>.py [argumentos]
```

Consulta la ayuda del script específico antes de usarlo:

```text
python <skill>/scripts/<script>.py --help
```

## Validación

La validación unificada comprueba estructura, pruebas, dependencias y, opcionalmente, igualdad frente a otra instalación:

```text
python workflow-maestro-academico-editorial/scripts/validar_coleccion.py \
  --validator /ruta/a/skill-creator/scripts/quick_validate.py \
  --validator-python python \
  --out /ruta/fuera-del-repositorio/validacion.json
```

Para comparar esta colección con las skills instaladas, añade:

```text
--compare /ruta/a/.codex/skills
```

La salida 0 representa controles ejecutados sin fallos ni pruebas omitidas; no convierte una auditoría mecánica en certificación académica o científica.

## Regenerar la documentación

Las fichas de `docs/skills/` se generan desde los `SKILL.md` y recursos reales:

```text
python workflow-maestro-academico-editorial/scripts/generar_documentacion_skills.py \
  --root . \
  --out docs/skills \
  --overwrite
```

El generador no incluye directorios ocultos, entornos, cachés ni bytecode.

## Contribución

1. Mantén cada script dentro de su skill responsable.
2. Conserva compatibilidad entre Linux, Windows y macOS en automatizaciones repetibles.
3. Añade pruebas para comportamientos nuevos o correcciones.
4. Ejecuta la validación unificada.
5. Regenera `docs/skills/` cuando cambien nombres, descripciones o recursos.
6. No publiques credenciales, documentos privados, entornos locales, cachés ni salidas de usuario.

Este repositorio no incluye una licencia de reutilización. Hasta que se añada una licencia explícita, la publicación del código no concede permisos adicionales de copia o redistribución.
