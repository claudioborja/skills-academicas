---
name: gestor-codigo-tecnico-editorial
description: Presenta y revisa listados de código, salidas de consola y fragmentos técnicos para libros, manuales y documentación de software. Úsalo cuando el código sea parte legible de la obra; no para desarrollar ni validar el software.
---

# Gestor de código técnico editorial

## Objetivo

Convertir código necesario para comprender una obra técnica en listados editoriales legibles, trazables y exportables, sin alterar su significado ni presentarlo como resultado ejecutado si no hay evidencia de ello.

## Decisiones editoriales

Antes de formatear, establecer con el autor o perfil editorial qué fragmentos merecen publicación, su lenguaje, lector previsto, versión o entorno cuando importe y si son código ejecutable, pseudocódigo, configuración, salida de consola o transcripción. Preferir fragmentos mínimos que expliquen una decisión; conservar archivos completos, repositorios y datos de prueba como material complementario cuando corresponda.

Cada listado publicable debe llevar numeración y título con función, por ejemplo `Listado 3.2. Validación de entrada del formulario.`. Introducirlo en el texto, explicarlo después y usar referencias cruzadas al número, no expresiones vagas como “el código anterior”. No convertir instrucciones para redactar o depurar en contenido publicable.

Mantener literalmente sintaxis, indentación, símbolos, comandos, rutas, variables, mensajes y bloques de salida salvo corrección autorizada y trazable. Diferenciar visualmente código, terminal, configuración, pseudocódigo, errores y resultados. Nunca inventar salidas, rendimiento, compatibilidad, licencias ni resultados de ejecución.

## Presentación

- Usar fuente monoespaciada, sangría estable, contraste suficiente y ajuste de línea solo si el perfil lo permite; no partir tokens, URLs, comandos o líneas de configuración de forma engañosa.
- Identificar el lenguaje en Markdown (` ```python `, ` ```bash `, ` ```json `) y distinguir el texto de salida del comando que lo generó.
- Numerar líneas únicamente si el análisis se refiere a líneas concretas; evitarlo en listados breves. Mantener la misma convención en toda la obra.
- Para fragmentos largos, extraer una porción autosuficiente, marcar con una elipsis editorial solo una omisión real y describir dónde está la versión completa. No ocultar condiciones que cambien el sentido del ejemplo.
- Atribuir código ajeno, comprobar licencia cuando se reproduzca de forma sustancial y no confundir código generado, adaptado o propio.

## Ejecución Python obligatoria

Usar Python para todos los controles, generación y exportación de esta skill. Cada script que necesita paquetes debe declarar un `requirements-lock.txt` local y el lanzador debe instalar ese lock automáticamente en `gestor-codigo-tecnico-editorial/.runtime/<sistema-arquitectura-python>/` en su primer uso. No reutiliza paquetes del Python del equipo ni sustituye esta ruta por LibreOffice.

La distribución incluye intérpretes completos para Linux x64, Windows x64, macOS Intel y macOS Apple Silicon en `runtime/python/`. Si está presente el de la plataforma actual, se usa para crear el entorno aislado. No copiar un único intérprete o `.runtime` entre sistemas: cada binario debe corresponder a su sistema y arquitectura. Para renovar los cuatro intérpretes y su manifiesto SHA-256, ejecutar `scripts/preparar_interpretes_portables.py` desde una máquina con red.

En un equipo sin Python ni Internet, usar el lanzador nativo de la skill: `./ejecutar.sh generar-listado ...` en Linux/macOS o `./ejecutar.ps1 generar-listado ...` en Windows. Los paquetes requeridos se entregan como ruedas offline en `runtime/python/wheels/`.

No usar LibreOffice. Para compatibilidad visual, validar la estructura mediante OOXML y reservar la inspección final del DOCX para Microsoft Word u otro motor autorizado expresamente.

## DOCX para fragmentos breves

Si se solicita un listado Word breve, generar un DOCX nativo con `python-docx`; no usar LibreOffice, renderizado de oficina ni una conversión de documento completo. El lanzador detecta el lock de esta herramienta y prepara el entorno Python en el primer uso. La instalación inicial puede descargar solo las ruedas declaradas por esta skill, pero las ejecuciones posteriores solo generan el archivo.

```text
python skills/editor-en-jefe/scripts/ejecutar.py gestor-codigo-tecnico-editorial/scripts/generar_listado_docx.py "ejemplos/validar_nombre.py" --out "entregables/listado-1-1.docx" --titulo "Listado 1.1. Validación de un nombre." --lenguaje Python
```

El archivo de entrada se conserva literalmente y el código queda como texto editable monoespaciado. Para un manuscrito completo o una revisión visual de maquetación, usar el flujo de `$maquetacion-academica-preentrega`; no aplicarlo a un fragmento aislado salvo que el usuario lo pida.

## Flujo y controles

Usar `$preprocesador-documentos` para preservar bloques de código al extraer material. Activar `$gestor-tablas-figuras-pies` si el perfil trata los listados como recursos numerados junto a tablas y figuras. Para la exportación, entregar a `$maquetacion-academica-preentrega` la decisión de conservar los listados como bloques monoespaciados; su limpieza general de Markdown no autoriza convertir código significativo en prosa ni eliminarlo.

Ejecutar este control sobre el manuscrito Markdown antes de exportar cuando contenga listados:

```text
python skills/editor-en-jefe/scripts/ejecutar.py gestor-codigo-tecnico-editorial/scripts/auditar_listados_codigo.py manuscrito.md --out auditoria-listados.md --json-out auditoria-listados.json
```

El auditor detecta bloques sin lenguaje, título editorial, cierre o con marcadores de trabajo. Es una señal mecánica: no verifica compilación, seguridad, exactitud técnica, licencia ni compatibilidad. Resolver cada hallazgo en el manuscrito o justificarlo en el registro editorial.

Leer [references/criterios-listados.md](references/criterios-listados.md) para decidir cuándo publicar código completo, fragmentos, pseudocódigo, configuración o salidas.
