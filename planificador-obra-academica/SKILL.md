---
name: planificador-obra-academica
description: Úsalo cuando el usuario necesite convertir una idea, tema o borrador en la arquitectura completa de una obra académica o editorial, incluyendo propósito, alcance, lector, objetivos, índice, secuencia de capítulos, progresión argumentativa, distribución de extensión y estructura local de directorios capaz de sostener investigación, manuscrito, casos, recursos, revisión y entregables. Aplica a libros nuevos, tesis, informes extensos, manuales, artículos largos y proyectos editoriales que deban inicializarse o normalizarse.
---

# Planificador De Obra Académica

## Ejecución multiplataforma

Consultar [la guía común de ejecución](../editor-en-jefe/references/portabilidad.md) para elegir intérprete y preparar dependencias.

## Objetivo

Este skill diseña la estructura de una obra antes de redactarla. Organiza el proyecto intelectual, delimita su alcance y convierte intuiciones dispersas en un plan de escritura claro, viable y coherente.

## Cuándo usarlo

- cuando exista solo una idea general o un tema
- cuando el índice sea débil, desordenado o redundante
- cuando el usuario necesite definir capítulos, secciones y secuencia lógica
- cuando haya que transformar un borrador disperso en un proyecto de libro o tesis

## Flujo de trabajo

El contexto maestro es opcional. En su ausencia, planificar desde el encargo, los materiales y las preferencias conocidas; proponer el índice cuando falte y registrar los supuestos relevantes. No exigir al usuario una ficha o archivo adicional ni heredar requisitos particulares de otra obra. Ajustar el detalle de planificación al tamaño del trabajo.

Si existe un contexto maestro, leer [interpretación del contexto editorial](../editor-en-jefe/references/interpretacion-contexto-editorial.md) antes de diseñar el índice. La sección que el usuario identifique como estructura general gobierna los capítulos y temas. Las plantillas de desarrollo y checklists orientan la escritura y revisión; no generan apartados automáticamente. Conservar el índice suministrado y proponer aparte cualquier ampliación que cambie su alcance.

1. Identifica tema, propósito, lector y nivel académico.
2. Delimita alcance, exclusiones y profundidad esperada.
3. Formula la lógica global de la obra.
4. Conserva el índice suministrado o propone uno cuando falte; deriva los subapartados del contenido autorizado, sin copiar encabezados operativos del contexto.
5. Asigna función a cada bloque y evita redundancias.
6. Sugiere extensión relativa y orden de escritura.
   - Registrar el objetivo de extensión del proyecto; usar un perfil de libro extenso solo cuando corresponda al encargo.
   - Sustituir ese rango cuando el usuario, convocatoria, editorial o contexto maestro indique expresamente otro.
7. Para libros, elegir una estructura proporcional según `references/estructura-directorios-libro.md`. Crear solo carpetas necesarias; usar `scripts/inicializar_proyecto_libro.py` únicamente cuando corresponda la estructura completa.
8. Guarda cada artefacto en la carpeta correspondiente; no acumules manuscrito, fuentes, imágenes y entregables en la raíz.

Para libros inicializados, usar `01_planificacion_editorial/03_registro_editorial.md` como continuidad breve entre sesiones. Registrar decisiones vigentes, estado de capítulos, requisitos/controles y la siguiente acción solo cuando una intervención cambie el proyecto de forma sustantiva. No reemplaza la ficha editorial, matrices de evidencia, planes visuales ni los informes de revisión.

## Perfil editorial predeterminado

Derivar del contexto completo una matriz de cobertura: cada inclusión, objetivo y relación requerida debe tener ubicación prevista dentro del índice. Registrar exclusiones, lector, enfoque, recursos y criterios globales de resultado. Resolver huecos o contradicciones sin ampliar silenciosamente la estructura. Fijar niveles de títulos, numeración y piezas visibles para que redacción y maquetación no infieran el diseño de las marcas del archivo de instrucciones.

Seleccionar y registrar el [perfil editorial del proyecto](../editor-en-jefe/references/perfiles-editoriales.md) antes de distribuir palabras o páginas por capítulo. Distinguir valores técnicos de maquetación, norma de citas y objetivo de extensión; no imponer un rango de libro a otros productos.

## Inicialización opcional de la estructura completa

Aplicar [producción editorial integrada](../editor-en-jefe/references/produccion-editorial-eficiente.md) al planificar libros completos. Definir requisitos de publicación desde el inicio y un registro único de estado; evitar artefactos duplicados y plantillas vacías sin utilidad. En proyectos compactos, el registro puede ser `proyecto.md`; no exigir las matrices y rutas canónicas como documentos adicionales.

El inicializador depende del helper `editor-en-jefe/scripts/archivos_seguros.py`. Antes de crear nada comprueba los destinos previstos: rechaza enlaces simbólicos dentro de la estructura y archivos/carpetas con tipos incompatibles. `--merge` conserva los archivos existentes; los nuevos se publican de forma exclusiva y atómica. La inicialización completa no es una transacción: un fallo de disco puede dejar una estructura parcial que se completa con `--merge`. No ejecutar inicializaciones concurrentes sobre el mismo proyecto.

Ejecutar si se eligió la estructura completa. El script actual siempre crea esa estructura; no tiene una opción compacta:

```text
python skills/editor-en-jefe/scripts/ejecutar.py planificador-obra-academica/scripts/inicializar_proyecto_libro.py "ruta/del/libro" --title "Título del libro"
```

Para completar un proyecto existente sin sobrescribir archivos:

```text
python skills/editor-en-jefe/scripts/ejecutar.py planificador-obra-academica/scripts/inicializar_proyecto_libro.py "ruta/del/libro" --title "Título del libro" --merge
```

Usar `--dry-run` para revisar las operaciones previstas. Leer `references/estructura-directorios-libro.md` antes de decidir dónde guardar un artefacto.

## Validación final

- los capítulos y temas corresponden a la estructura publicable del contexto o a cambios autorizados
- las instrucciones de desarrollo están cubiertas dentro del texto y los controles se documentan fuera del manuscrito

- cada capítulo tiene una función clara
- el orden responde a una lógica pedagógica o argumentativa
- no hay solapamientos graves entre bloques
- la obra completa tiene hilo conductor visible
- la estructura elegida permite localizar originales, evidencia, manuscrito, recursos y entregables sin carpetas vacías obligatorias
- los entregables finales están separados de borradores y revisiones

## Referencias de apoyo

- Para diseño de índices y secuencias: lee [references/arquitectura-de-obra.md](references/arquitectura-de-obra.md).
- Para carpetas, responsabilidades y compatibilidad: lee [references/estructura-directorios-libro.md](references/estructura-directorios-libro.md).
