# Ejecución en Linux, Windows y macOS

Requiere Python 3.10 o posterior. Los scripts de esta colección usan Python; no necesitan Bash ni PowerShell si se invocan mediante `ejecutar.py`.

El instalador de Editor en jefe usa por defecto el Python actual y requiere pip. Crear un entorno opcional con `--entorno` requiere además `venv` y `ensurepip`; algunas distribuciones Linux los separan en un paquete como `python3-venv`. La primera descarga requiere acceso al índice de paquetes. En Windows, el lanzador `preprocesador-documentos/scripts/preprocesar_documento.ps1` puede instalar Python 3.12 con `winget` para el usuario actual cuando no encuentre Python compatible; la entrada Python y el lanzador POSIX requieren un intérprete previamente instalado.

Desde la raíz de la colección de skills, preparar las dependencias PDF/Word una vez:

```sh
# Linux y macOS
python3 editor-en-jefe/scripts/ejecutar.py --preparar
```

```powershell
# Windows
py -3 editor-en-jefe/scripts/ejecutar.py --preparar
```

Ejecutar una herramienta:

```sh
python3 editor-en-jefe/scripts/ejecutar.py auditor-documental-academico/scripts/inventariar_documento.py "ruta/manuscrito.md"
python3 editor-en-jefe/scripts/ejecutar.py preprocesador-documentos/scripts/preprocesar_documento.py "ruta/documento.pdf" "ruta/salida"
```

En Windows sustituir `python3` por `py -3` o `python`. Desde otra carpeta, usar la ruta absoluta a `ejecutar.py`. La ruta del script se resuelve respecto a la colección; las rutas de documentos y salidas siguen siendo relativas al directorio de trabajo. Usar comillas para espacios y barras `/` en ejemplos compartidos entre sistemas.

El lanzador usa UTF-8, conserva los argumentos y códigos de salida y evita ejecutar mediante un shell. Sin `SKILLS_RUNTIME_DIR`, prioriza el Python actual cuando cumple las dependencias base. Si no las cumple, mantiene el mecanismo anterior: sin `--preparar`, usa el entorno local si existe o el intérprete actual; con preparación, crea o comprueba un entorno local. `SKILLS_RUNTIME_DIR` selecciona expresamente otro entorno. Los scripts de texto no requieren paquetes. El preprocesador reutiliza la base del Python actual si está lista antes de recurrir a su preparación automática.

Los entornos se crean en `preprocesador-documentos/.runtime/<sistema-arquitectura-python>/`. Si la colección es de solo lectura, definir `SKILLS_RUNTIME_DIR` con una carpeta escribible. Un entorno no se debe copiar entre equipos ni reutilizar tras moverlo; elegir una nueva carpeta para reconstruirlo. El antiguo entorno Windows se conserva pero no se utiliza.

Los gráficos PNG de `tabular_visualizar.py` son opcionales: requieren `matplotlib` instalado en el intérprete utilizado. Sin él, el script conserva las tablas CSV/JSON/Markdown. Se puede usar directamente un entorno propio con las dependencias necesarias:

```text
python -X utf8 ruta/skill/scripts/herramienta.py argumentos
```

Las skills que invocan scripts de otras skills deben distribuirse junto con esas dependencias. `ejecutar.py` requiere `preprocesador-documentos/scripts/runtime_portable.py`.

## Protección de informes

Los apartados de [dependencias fijadas](#dependencias-fijadas) y [validación unificada](#validación-unificada) describen el mantenimiento de los entornos y la colección.

Los generadores de informes de la colección requieren el helper `editor-en-jefe/scripts/archivos_seguros.py`, incluso al ejecutarlos directamente. Validan todas las salidas declaradas antes de escribir: no pueden coincidir entre sí ni con entradas, ni ocupar directorios necesarios para otra salida. Rechazan salidas existentes salvo `--overwrite`; esta opción nunca permite reemplazar originales, perfiles, manifiestos de entrada o PDFs utilizados.

El preprocesador valida sus seis salidas antes de iniciar las etapas y propaga `--overwrite` a los tres scripts. Para repetirlo desde Windows con reemplazo autorizado usar la entrada Python (`py -3 .../preprocesar_documento.py entrada salida --overwrite`); el wrapper PowerShell conserva su interfaz anterior. El flujo de perfiles valida el destino canónico y la copia auxiliar antes de publicar; no persiste el perfil intermedio. Tabulación valida CSV, JSON, Markdown y posibles PNG antes de producirlos. Los prefijos de archivo no admiten rutas.

`inventario_fuentes.py` protege cada archivo inventariado: guardar informes fuera del directorio de fuentes si se quiere reemplazarlos en ejecuciones posteriores. `doi_a_referencia.py --from-file` comprueba colisiones antes de consultar la red.

Los registradores de imágenes y tablas conservan la operación de añadir registros, sin `--overwrite`: `atomic_append` copia los bytes anteriores a un temporal y publica el archivo completo. Manifiesto y anexo deben ser distintos, y no pueden sustituir el recurso registrado. El registrador de imágenes rechaza identificadores repetidos; para recursos asistidos publica el anexo primero y el manifiesto al final, y restaura el anexo si falla la publicación del manifiesto. Kitchenham serializa también las nuevas filas CSV antes de reemplazar el registro. Estos flujos requieren un solo proceso escritor y no ofrecen bloqueo.

Al usar el lanzador, autorizar el reemplazo en ambos niveles: `ejecutar.py --permitir-sobrescritura skill/scripts/herramienta.py entrada --out informe --overwrite`. Sin necesidad de reemplazo, omitir ambas opciones.

La publicación es atómica por archivo, no una transacción del sistema de archivos entre varios informes. El registrador de imágenes aplica la compensación descrita para su par anexo-manifiesto; otros flujos con varias salidas pueden dejar publicada la primera si falla la siguiente. La compensación tampoco cubre concurrencia ni un fallo durante la propia reversión. La creación exclusiva usa enlaces duros: en un sistema de archivos que no los admita fallará sin reemplazar el destino. La protección presupone rutas estables, no directorios modificados simultáneamente por terceros. No es un aislamiento frente a programas externos ni cubre las escrituras internas de instalación de paquetes/entornos. No se conservan necesariamente permisos o metadatos del archivo reemplazado.

Pruebas reproducibles en los tres sistemas:

```text
python -m unittest discover -s editor-en-jefe/tests -v
python -m unittest discover -s preprocesador-documentos/tests -v
python -m unittest discover -s humanizar-redaccion-academica/tests -v
python -m unittest discover -s gestor-referencias-academicas/tests -v
```

Las pruebas usan carpetas temporales y no descargan dependencias. Incluyen rutas con espacios y tildes, ejecución desde otra carpeta, preservación del documento de entrada y propagación de errores. La ejecución local en un sistema no sustituye la validación nativa en los otros dos.

Las pruebas del orquestador comprueban la integración entre herramientas; las del preprocesador comprueban la preparación del entorno. Ejecutarlas después de modificar esas herramientas, no durante cada tarea editorial.

## Instalador de requerimientos

`python editor-en-jefe/scripts/instalar_requisitos.py` prepara el conjunto completo, incluidos gráficos, en el Python actual, reutilizando librerías compatibles. En Linux/macOS usar `python3`; en Windows `py -3`. Requiere Python 3.12+ y pip. `--graficos` es una opción de compatibilidad sin efecto adicional; `--comprobar` no crea ni instala nada. `--entorno RUTA` permite crear o usar un entorno aislado opcional (venv/ensurepip necesarios para crearlo); para que el lanzador lo use posteriormente, definir `SKILLS_RUNTIME_DIR=RUTA`. No se usan privilegios elevados ni se omiten protecciones de un Python administrado externamente; si pip lo bloquea, elegir un entorno opcional.

El `requirements.txt` de la raíz es una lista plana de las 17 librerías directas e indirectas, sin inclusiones de otros archivos. `editor-en-jefe/scripts/requirements.txt` es una copia idéntica para distribuir las skills sin la raíz; el instalador lee la lista de la raíz cuando existe y, en su ausencia, la copia empaquetada. Las pruebas comprueban igualdad y cobertura de los locks parciales. Antes de instalar se comprueban versiones e importaciones; si están listas se omite pip install. Un desajuste o una importación dañada requiere un entorno nuevo o reparación explícita; no se sobrescribe automáticamente. Se comprueba la lista y `pip check` después de instalar. No instala aplicaciones de oficina, Poppler ni fuentes. La detección de una aplicación instalada no autoriza su uso; LibreOffice está excluido del flujo. Sin wheels compatibles, red o permisos suficientes devuelve error.

## Dependencias fijadas

- Base PDF/Word: `preprocesador-documentos/scripts/requirements-lock.txt`, Python 3.10+. Fija PyMuPDF, pypdf, python-docx y sus dependencias transitivas lxml/typing_extensions. `requirements.txt` remite al mismo lock. `--preparar` instala con `--only-binary=:all:`: sin wheel compatible, falla sin compilar bibliotecas nativas.
- Gráficos opcionales: `explorador-temas-articulos/scripts/requirements-graficos-lock.txt`, Python 3.12+ por NumPy. Incluye Matplotlib y dependencias transitivas. No altera el mínimo de la base ni impide tabular sin gráficos.
- Inspección raster: `gestor-imagenes-academicas-libros/scripts/requirements-lock.txt`, Python 3.10+. Fija Pillow para verificar integridad, dimensiones, transparencia y PPI efectivo; el script y su dependencia permanecen con la skill propietaria.
- Mantenimiento: `editor-en-jefe/scripts/requirements-mantenimiento.txt` fija PyYAML para el validador oficial. Puede usarse en el intérprete de pruebas o en otro explícito.

Instalar los perfiles opcionales en el Python elegido, del sistema o de un entorno aislado, respetando sus permisos y compatibilidad. Desde la raíz:

```text
python -m pip install --only-binary=:all: -r explorador-temas-articulos/scripts/requirements-graficos-lock.txt -r gestor-imagenes-academicas-libros/scripts/requirements-lock.txt -r editor-en-jefe/scripts/requirements-mantenimiento.txt
python -m pip check
python preprocesador-documentos/scripts/dependencias.py
python preprocesador-documentos/scripts/dependencias.py --lock explorador-temas-articulos/scripts/requirements-graficos-lock.txt
python preprocesador-documentos/scripts/dependencias.py --lock gestor-imagenes-academicas-libros/scripts/requirements-lock.txt
```

Si hay versiones distintas, preparar otra carpeta con `SKILLS_RUNTIME_DIR`; no actualizar el entorno existente automáticamente. `--preparar` verifica versiones e importaciones y ejecuta `pip check`. Sin `--preparar`, no se instalan paquetes. El diagnóstico de dependencias informa versiones distintas, ausencias o importaciones rotas; no es un escaneo de vulnerabilidades.

Los locks fijan versiones, no hashes de cada wheel: no garantizan identidad binaria, disponibilidad futura del índice ni resultados visuales idénticos entre sistemas. Microsoft Word, Poppler, las fuentes y cualquier herramienta de inspección autorizada pertenecen al entorno externo, fuera de estos perfiles; LibreOffice no se usa. Una actualización requiere cambiar el lock y repetir pruebas. Se probó instalación limpia en Linux/Python 3.12; Windows/macOS requieren validación nativa. Véase [instalaciones repetibles de pip](https://pip.pypa.io/en/stable/topics/repeatable-installs/).

## Runtime portable empaquetado

`editor-en-jefe/runtime/python/` contiene intérpretes CPython 3.14 y cachés offline de las 17 dependencias para Linux x86_64, Windows x86_64, macOS Intel y macOS Apple Silicon. `MANIFEST.json` registra la fuente, la versión y los SHA-256 de cada descarga y rueda. La reconstrucción confirma que las ruedas pueden descargarse para los cuatro destinos; la instalación offline y las importaciones se verificaron en Linux. La ejecución nativa de los lanzadores en Windows, macOS Intel y macOS Apple Silicon sigue siendo una validación pendiente y no debe inferirse desde Linux.

## Validación unificada

Desde la raíz, reemplazar las rutas por las del equipo:

```text
python editor-en-jefe/scripts/ejecutar.py editor-en-jefe/scripts/validar_coleccion.py --compare "ruta/a/skills-instaladas" --validator "ruta/a/skill-creator/scripts/quick_validate.py" --validator-python "ruta/al/python-con-PyYAML" --out "ruta/fuera-de-las-skills/validacion.json"
```

El intérprete seleccionado por el lanzador ejecuta las pruebas; `--test-python` permite elegir otro. `--validator-python` ejecuta el validador oficial y requiere PyYAML (por defecto usa el mismo intérprete). La validación completa requiere los perfiles base, gráficos, imágenes y mantenimiento; gráficos exige Python 3.12+. `--root` cambia la colección de origen. No hay rutas personales codificadas.

Para las pruebas y sus subprocesos, el validador establece `SKILLS_RUNTIME_DIR` al `sys.prefix` del intérprete de pruebas; usar un entorno virtual previamente preparado con los perfiles indicados. Esto evita que busquen o creen otro runtime. Esta selección solo afecta a los subprocesos de la validación. Si se ejecuta `unittest` directamente, definir esa variable con la ruta del entorno preparado.

Ejecuta el validador oficial y todas las suites `tests/` presentes en ambas copias, comprueba perfiles en los intérpretes seleccionados y ejecuta `pip check` en el de pruebas. Compara hashes, incluidos archivos faltantes y sobrantes dentro de las skills del origen. Ignora `.runtime`, `__pycache__`, `.git` y skills instaladas ajenas; el origen define el alcance, por lo que no detecta una skill ya ausente de ese origen. Rechaza raíces iguales/anidadas y enlaces dentro de las skills comparadas.

Ejecuta tests de confianza: no es un aislamiento frente a código externo. No instala, sincroniza ni borra archivos de las colecciones; usa temporales propios y caché gráfica aislada. El informe opcional debe estar fuera de ambas raíces y no existir. Sin `--out`, imprime JSON. Registra progreso, salidas, conteos y omisiones. `--timeout` limita cada subproceso a 180 segundos por defecto.

Salida **0**: controles ejecutados sin diferencias, fallos ni tests omitidos. **1**: diferencias, pruebas fallidas/omitidas, suites vacías, desajustes de dependencias o errores de subprocesos. **2**: argumentos/rutas inválidos. Las skills sin suite reciben validación estructural, sin inventar cobertura funcional. La regresión visual APA se declara **no ejecutada**: usar el comando específico de maquetación con un renderizador explícito.

El helper `atomic_output` permite producir binarios grandes en un temporal en disco y publicarlos únicamente cuando termina el productor; `atomic_write` lo usa para texto y bytes. Ambos eliminan el temporal al fallar. Kitchenham lo usa también para copiar fuentes y construir ZIP, sin cargar todo el archivo en memoria. Las importaciones PDF usan `pymupdf`, incluido el sondeo del entorno; no instalar el paquete independiente llamado `fitz`.
