# Skills académicas y editoriales para Codex

Colección de trabajo editorial, coordinada por **Editor en jefe** (`$editor-en-jefe`).

Colección de 33 skills coordinadas para planificar, investigar, redactar, revisar, diseñar y entregar tesis, libros, artículos científicos y revisiones sistemáticas. Incluye automatización reproducible para documentos, referencias, imágenes, ecuaciones, tablas, verificación de resultados, contribuciones y autoría, diseño profesional en Word, formato APA 7, IEEE y control de preentrega.

La colección está diseñada para trabajar de dos maneras:

- **Uso directo:** invocar una skill cuando la tarea está claramente delimitada.
- **Uso orquestado:** empezar con `editor-en-jefe` para que seleccione las especialidades necesarias y determine su orden sin repetir intervenciones.

## Qué resuelve

- Arquitectura y continuidad de libros, tesis y manuscritos extensos.
- Conversión de tesis en libros y redacción de artículos IMRyD.
- Revisión sistemática Kitchenham para ingeniería de software.
- [Revisión sistemática y metaanálisis con PRISMA](revision-sistematica-prisma/SKILL.md): PRISMA 2020, PRISMA-P, PRISMA-S y [extensiones/fuentes oficiales](revision-sistematica-prisma/references/fuentes-oficiales.md).
- Búsqueda, verificación y consistencia de referencias APA 7 e IEEE.
- [Verificación de resultados de investigación](verificador-resultados-investigacion/SKILL.md): controles reproducibles, revisión metodológica/interpretativa diferenciada e informe individual de cada intervención.
- [Contribuciones, autoría y metadatos](gestor-contribuciones-autoria/SKILL.md): selección contextual de CRediT, ICMJE, COPE, DataCite, CodeMeta/CFF, MARC, CRO y formatos de intercambio.
- Redacción académica en español latinoamericano, estilo y ortotipografía.
- Tablas, figuras, imágenes científicas y ecuaciones editables.
- Preprocesamiento de PDF, DOCX, HTML, TXT y Markdown.
- Diseño y maquetación profesional de libros en Word editable.
- Exportación y control final de documentos Word y representaciones de revisión.
- Auditorías mecánicas reproducibles que apoyan, pero no reemplazan, el juicio académico.

El [catálogo completo](docs/skills/README.md) contiene una ficha independiente por cada skill.

## Editor en jefe

`editor-en-jefe` es la entrada recomendada para encargos que afectan varias etapas o varios artefactos. Su función es identificar:

1. producto final: tesis, libro, artículo o revisión;
2. etapa real del trabajo;
3. método y norma aplicables;
4. materiales disponibles;
5. skills mínimas necesarias y orden de ejecución.

El orquestador no ejecuta todas las skills por rutina. Mantiene las fronteras entre metodología, evidencia, redacción, revisión, recursos visuales y maquetación. Consulta la [guía del orquestador](docs/orquestador.md) y su [mapa de responsabilidades](editor-en-jefe/references/mapa-responsabilidades.md).

Ejemplo:

```text
Usa $editor-en-jefe para diagnosticar este manuscrito, identificar la etapa actual y ejecutar solo las revisiones necesarias antes de entregarlo en Word.
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

```text
Usa $revision-sistematica-prisma para preparar y auditar el protocolo, la búsqueda, el flujo y el reporte PRISMA 2020 de esta revisión.
```

```text
Usa $disenador-maquetador-word para convertir este manuscrito en un libro profesional en Word, con estilos editables y preparado para futuras adiciones o eliminaciones.
```

```text
Usa $gestor-contribuciones-autoria para preparar la declaración de contribuciones, comprobar los criterios de autoría y mapear los roles al formato exigido por la revista.
```

```text
Usa $verificador-resultados-investigacion para comprobar estos resultados, explicar cada error y preparar informes individuales antes de corregir el manuscrito.
```

Las instrucciones normativas están siempre en el `SKILL.md` de cada directorio. Las fichas de `docs/skills/` son guías de navegación y no sustituyen esas instrucciones.

## Modo de uso sugerido

1. Abre en Codex la carpeta del proyecto y proporciona el encargo y los materiales disponibles.
2. Invoca `$editor-en-jefe`, indicando producto, lector, alcance y formato final. Puedes comenzar con una idea, un índice o un manuscrito.
3. Si tienes un contexto de tipo de obra, indica su ruta. Es opcional: mejora la precisión, pero no es requisito para trabajar.
4. Editor en jefe aplica todo el contexto: propósito, objetivos, alcance, público, enfoque, convenciones y recursos. Distingue el índice publicable de las instrucciones de desarrollo y los controles internos.
5. Revisa el índice y los supuestos relevantes. Para trabajos extensos, desarrolla y revisa por capítulos manteniendo continuidad y trazabilidad de fuentes.
6. Si el encargo es un libro completo, la integración y preentrega forman parte del trabajo. La revisión incluye el documento exportado, no solo el Markdown; los pendientes y controles se entregan separados del manuscrito. Un encargo parcial conserva su alcance.

Con contexto:

```text
Usa $editor-en-jefe para desarrollar el libro descrito en contexto-tipo-de-obra.md.
Aplica todas sus directrices y conserva su estructura publicable. Integra las
consideraciones de redacción sin copiarlas como apartados. Entrega Word editable
y un informe separado de calidad, con revisión visual de la maquetación.
```

Sin contexto:

```text
Usa $editor-en-jefe para planificar un libro académico sobre [tema], dirigido a
[lector]. Dispongo de [materiales]. Propón índice y extensión razonados y registra
los supuestos antes de desarrollar los capítulos.
```

Para convertir una tesis:

```text
Usa $editor-en-jefe para convertir esta tesis en un libro académico de más de
100 páginas, centrado en sus hallazgos. Distribuye la evidencia según el argumento
de cada capítulo y planifica la extensión sin relleno.
```

`contexto-tipo-de-obra.md` representa un archivo que aporta el usuario; no se distribuye con la colección. Sus temas y cuotas no son valores predeterminados para otros libros. Las skills también pueden invocarse individualmente.

## Producción editorial eficiente

El objetivo es entregar una obra completa y revisada, con Word editable cuando se solicite, sin trasladar al lector los controles internos del proyecto. La [política de producción editorial](editor-en-jefe/references/produccion-editorial-eficiente.md) establece:

- Redacción y revisión integrada por capítulos, conservando una revisión global de continuidad, evidencia y presentación.
- Reutilización de extracciones y evidencia trazable mientras la fuente y su configuración sigan vigentes; ampliar el contexto cuando el fragmento no sea suficiente.
- Controles mecánicos mediante scripts y reapertura de las revisiones afectadas por cambios.
- Organización proporcional: `proyecto.md` y carpetas `fuentes/`, `manuscrito/`, `recursos/` y `entregables/`, creadas según necesidad. El inicializador existente conserva la estructura completa numerada; no tiene una opción compacta.

SQLite, búsqueda textual y embeddings son opciones de diseño, no un sistema RAG implementado por esta colección. Reducir tiempo sin aumentar tokens ni degradar calidad es un objetivo que requiere medición; no se afirma un ahorro demostrado. Las skills tampoco garantizan la aceptación de una editorial ni sustituyen la validación disciplinar.

## Estructura

```text
skills/
├── README.md
├── requirements.txt
├── docs/
│   ├── orquestador.md
│   └── skills/
├── editor-en-jefe/
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

Cada script especializado permanece dentro de la skill que lo posee. El único lanzador general es `editor-en-jefe/scripts/ejecutar.py`.

## Instalación de las skills

Requisitos generales:

- Codex con soporte para skills locales.
- Python 3.12 o posterior para instalar el conjunto completo (los scripts base admiten 3.10).
- Python con `pip`; `venv` y `ensurepip` solo para crear un entorno opcional.
- Acceso a los paquetes de Python para preparar las dependencias por primera vez.

Clona el repositorio en una ubicación de trabajo y copia los directorios de skills a `$CODEX_HOME/skills` o `~/.codex/skills`. No copies `docs/`, `.git/` ni los entornos `.runtime/`.

En Linux o macOS:

```text
cp -R <skill> "${CODEX_HOME:-$HOME/.codex}/skills/"
```

En PowerShell:

```text
Copy-Item -Recurse <skill> "$env:USERPROFILE\.codex\skills\"
```

Para usar el flujo completo deben instalarse juntos el orquestador y las skills que este pueda activar. La documentación detallada de portabilidad está en [`portabilidad.md`](editor-en-jefe/references/portabilidad.md).

## Automatización y portabilidad

### Instalación de requerimientos

El archivo [requirements.txt](requirements.txt) enumera directamente las **17 dependencias Python del conjunto completo**, incluidos gráficos y dependencias indirectas: no remite a otros archivos. El instalador pertenece a [Editor en jefe](editor-en-jefe/SKILL.md) y usa por defecto el Python con el que lo ejecutas, aprovechando las librerías ya instaladas que cumplen las versiones requeridas. El entorno virtual es opcional mediante `--entorno`.

| Uso | Librerías |
|---|---|
| PDF y conversión de recursos | PyMuPDF, pypdf |
| Word editable | python-docx, lxml, typing_extensions |
| Inspección de imágenes | Pillow |
| Gráficos y sus dependencias | Matplotlib, NumPy, contourpy, cycler, fonttools, kiwisolver, packaging, pyparsing, python-dateutil, six |
| Mantenimiento de skills | PyYAML |

Las demás importaciones pertenecen a la biblioteca estándar de Python o a módulos internos de la colección. Se conserva una copia plana idéntica dentro de Editor en jefe para distribuir las skills sin la raíz del repositorio; el instalador lee un solo archivo. Los locks especializados permanecen para las herramientas que comprueban perfiles parciales, pero no forman una cadena en la instalación general.

Desde la raíz de esta colección, en Linux o macOS:

```sh
python3 editor-en-jefe/scripts/instalar_requisitos.py
```

En Windows (PowerShell o CMD):

```powershell
py -3 editor-en-jefe/scripts/instalar_requisitos.py
```

Opciones (sustituye `python` por el comando de tu sistema):

```text
python editor-en-jefe/scripts/instalar_requisitos.py --comprobar
python editor-en-jefe/scripts/instalar_requisitos.py --entorno "ruta/entorno-nuevo"
```

`--comprobar` no instala ni crea archivos: devuelve 0 si las dependencias están listas y 1 si faltan o hay errores. Los gráficos se incluyen por defecto; `--graficos` se conserva por compatibilidad con comandos anteriores. Las ejecuciones posteriores comprueban versiones e importaciones, omiten la instalación si todo está correcto y ejecutan `pip check`. Si encuentran versiones incompatibles o importaciones dañadas, informan el problema y permiten elegir un entorno nuevo sin reemplazar paquetes existentes.

No es necesario activar el entorno para usar `ejecutar.py`. Si eliges `--entorno`, define `SKILLS_RUNTIME_DIR` con esa misma ruta en futuras ejecuciones (`export SKILLS_RUNTIME_DIR="ruta"` en Linux/macOS; `$env:SKILLS_RUNTIME_DIR="ruta"` en PowerShell).

Python y pip deben estar instalados previamente. Por defecto se añaden los paquetes faltantes al Python actual, que puede ser del sistema o un entorno ya activado. Si el sistema bloquea pip por permisos o por un entorno administrado externamente, el instalador informa el error; no fuerza privilegios ni `--break-system-packages`. Puedes elegir `--entorno` en ese caso. Para revisar visualmente Word/PDF también necesitas un renderizador, por ejemplo LibreOffice y Poppler; el script informa su detección en PATH, pero no los instala. Fuentes tipográficas y otras herramientas externas dependen de la maqueta requerida.

La implementación utiliza Python y rutas nativas para Windows, Linux y macOS; la validación ejecutada en Linux no sustituye las pruebas nativas en los otros sistemas. La disponibilidad de los paquetes fijados depende de que existan wheels compatibles con tu versión de Python y arquitectura.

### Ejecución de herramientas

Los scripts se ejecutan mediante Python y evitan depender del shell cuando la operación debe funcionar en Linux, Windows y macOS. El lanzador general protege entradas y salidas comunes:

```text
python editor-en-jefe/scripts/ejecutar.py <skill>/scripts/<script>.py [argumentos]
```

Consulta la ayuda del script específico antes de usarlo:

```text
python <skill>/scripts/<script>.py --help
```

## Validación

La validación unificada comprueba estructura, pruebas, dependencias e igualdad frente a otra instalación. Requiere ambas rutas:

```text
python editor-en-jefe/scripts/validar_coleccion.py \
  --compare /ruta/a/.codex/skills \
  --validator /ruta/a/skill-creator/scripts/quick_validate.py \
  --validator-python python \
  --out /ruta/fuera-del-repositorio/validacion.json
```

La salida 0 representa controles ejecutados sin fallos ni pruebas omitidas; no convierte una auditoría mecánica en certificación académica o científica.

## Regenerar la documentación

Las fichas de `docs/skills/` se generan desde los `SKILL.md` y recursos reales:

```text
python editor-en-jefe/scripts/generar_documentacion_skills.py \
  --root . \
  --out docs/skills \
  --overwrite
```

El generador no incluye directorios ocultos, entornos, cachés ni bytecode. Al regenerar desde una copia de trabajo con respaldos históricos, puede incorporarlos al catálogo: antes de distribuirlo, sustituye esos enlaces locales por una nota de exclusión, o genera las fichas desde una copia limpia de las fuentes.

Los entornos locales, credenciales y manuscritos privados quedan fuera del repositorio. Las dependencias instaladas en `.runtime/` no deben copiarse entre equipos.

## Distribución y carga del repositorio

La distribución Git incluye instrucciones, scripts, pruebas, documentación y versiones fijadas de dependencias. Excluye entornos instalados, intérpretes portables, wheels, cachés y respaldos históricos ZIP. El manifiesto del runtime se conserva como referencia; los binarios no están incluidos en el paquete de fuentes.

Para preparar los intérpretes y wheels opcionales consulta `python editor-en-jefe/scripts/preparar_runtime_portable.py --help`. Esta preparación descarga recursos externos; no es necesaria para instalar las dependencias con el procedimiento anterior. Se han preparado recursos para Linux x86_64, Windows x86_64 y macOS Intel/ARM, pero la ejecución nativa en Windows y macOS sigue pendiente.

Antes de publicar, revisa el contenido que se añadirá a Git: `.gitignore` no retira archivos ya versionados y no detecta por sí solo documentos privados. No se incluyen manuscritos de ejemplo ni se configura automáticamente un destino remoto. Los paquetes locales de entrega se guardan en `dist/`, excluido de Git.
