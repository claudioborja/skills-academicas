---
name: planificador-obra-academica
description: Úsalo cuando el usuario necesite convertir una idea, tema o borrador en la arquitectura completa de una obra académica o editorial, incluyendo propósito, alcance, lector, objetivos, índice, secuencia de capítulos, progresión argumentativa, distribución de extensión y estructura local de directorios capaz de sostener investigación, manuscrito, casos, recursos, revisión y entregables. Aplica a libros nuevos, tesis, informes extensos, manuales, artículos largos y proyectos editoriales que deban inicializarse o normalizarse.
---

# Planificador De Obra Académica

## Ejecución multiplataforma

Consultar [la guía común de ejecución](../workflow-maestro-academico-editorial/references/portabilidad.md) para elegir intérprete y preparar dependencias.

## Objetivo

Este skill diseña la estructura de una obra antes de redactarla. Organiza el proyecto intelectual, delimita su alcance y convierte intuiciones dispersas en un plan de escritura claro, viable y coherente.

## Cuándo usarlo

- cuando exista solo una idea general o un tema
- cuando el índice sea débil, desordenado o redundante
- cuando el usuario necesite definir capítulos, secciones y secuencia lógica
- cuando haya que transformar un borrador disperso en un proyecto de libro o tesis

## Flujo de trabajo

1. Identifica tema, propósito, lector y nivel académico.
2. Delimita alcance, exclusiones y profundidad esperada.
3. Formula la lógica global de la obra.
4. Propone índice, capítulos y subapartados.
5. Asigna función a cada bloque y evita redundancias.
6. Sugiere extensión relativa y orden de escritura.
   - Registrar el objetivo de extensión del proyecto; usar un perfil de libro extenso solo cuando corresponda al encargo.
   - Sustituir ese rango cuando el usuario, convocatoria, editorial o contexto maestro indique expresamente otro.
7. Para todo proyecto cuyo producto final sea un libro, inicializa antes de redactar la estructura canónica con `scripts/inicializar_proyecto_libro.py`.
8. Guarda cada artefacto en la carpeta correspondiente; no acumules manuscrito, fuentes, imágenes y entregables en la raíz.

## Perfil editorial predeterminado

Seleccionar y registrar el [perfil editorial del proyecto](../workflow-maestro-academico-editorial/references/perfiles-editoriales.md) antes de distribuir palabras o páginas por capítulo. Distinguir valores técnicos de maquetación, norma de citas y objetivo de extensión; no imponer un rango de libro a otros productos.

## Inicialización obligatoria de libros

El inicializador depende del helper `workflow-maestro-academico-editorial/scripts/archivos_seguros.py`. Antes de crear nada comprueba los destinos previstos: rechaza enlaces simbólicos dentro de la estructura y archivos/carpetas con tipos incompatibles. `--merge` conserva los archivos existentes; los nuevos se publican de forma exclusiva y atómica. La inicialización completa no es una transacción: un fallo de disco puede dejar una estructura parcial que se completa con `--merge`. No ejecutar inicializaciones concurrentes sobre el mismo proyecto.

Ejecutar al crear un libro nuevo:

```text
python skills/workflow-maestro-academico-editorial/scripts/ejecutar.py planificador-obra-academica/scripts/inicializar_proyecto_libro.py "ruta/del/libro" --title "Título del libro"
```

Para completar un proyecto existente sin sobrescribir archivos:

```text
python skills/workflow-maestro-academico-editorial/scripts/ejecutar.py planificador-obra-academica/scripts/inicializar_proyecto_libro.py "ruta/del/libro" --title "Título del libro" --merge
```

Usar `--dry-run` para revisar las operaciones previstas. Leer `references/estructura-directorios-libro.md` antes de decidir dónde guardar un artefacto.

## Validación final

- cada capítulo tiene una función clara
- el orden responde a una lógica pedagógica o argumentativa
- no hay solapamientos graves entre bloques
- la obra completa tiene hilo conductor visible
- la estructura canónica existe y permite recorrer el flujo editorial completo
- los entregables finales están separados de borradores y revisiones

## Referencias de apoyo

- Para diseño de índices y secuencias: lee [references/arquitectura-de-obra.md](references/arquitectura-de-obra.md).
- Para carpetas, responsabilidades y compatibilidad: lee [references/estructura-directorios-libro.md](references/estructura-directorios-libro.md).
