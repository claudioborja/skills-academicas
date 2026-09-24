# Gestor De Marco Teórico Y Estado Del Arte

Úsalo cuando el usuario necesite construir, ordenar o fortalecer un marco teórico o estado del arte, integrando autores, enfoques, debates, vacíos, antecedentes y líneas conceptuales sin convertir la sección en una lista de resúmenes aislados.

## Ejemplo de uso

```text
Usa $gestor-marco-teorico-estado-del-arte para convertir estas fuentes en un marco teórico o estado del arte analítico.
```

## Guía operativa

### Exploración Previa

Si el usuario todavía no tiene un tema cerrado, necesita comparar artículos similares, distinguir estudios originales de revisiones o proponer líneas investigables, activar primero `$explorador-temas-articulos`. Usar sus matrices y visualizaciones como entrada para organizar el estado del arte con criterio académico.

### Objetivo

Este skill organiza literatura y pensamiento previo en una estructura analítica. Su meta es que el marco teórico explique relaciones entre conceptos y autores, y que el estado del arte revele acuerdos, tensiones, vacíos y aportes.

### Cuándo usarlo

- cuando el usuario tenga muchas fuentes pero poco orden
- cuando el marco teórico esté enumerativo
- cuando el estado del arte no muestre debate ni vacíos
- cuando haya que integrar antecedentes y base conceptual

### Flujo de trabajo

1. Identifica tema, pregunta o problema central.
2. Agrupa autores y fuentes por enfoques, variables o corrientes.
3. Si se van a incorporar nuevas fuentes, coordina con `$gestor-referencias-academicas` y exige el filtro `$filtro-editoriales-depredadoras` antes de aceptar revistas o editoriales.
4. Distingue conceptos base, discusiones y vacíos.
5. Organiza la sección en bloques con lógica analítica.
6. Redacta transiciones y síntesis que conecten literatura y problema.

### Validación final

- no hay listado mecánico de autores
- cada bloque responde a una idea organizadora
- se distingue antecedente, teoría, debate y vacío
- la sección prepara el terreno para la investigación o la obra
- las fuentes nuevas no provienen de revistas o editoriales clasificadas en rojo

### Referencias de apoyo

- Para organizar literatura: lee [references/organizacion-de-literatura.md](../../gestor-marco-teorico-estado-del-arte/references/organizacion-de-literatura.md).

## Recursos incluidos

### Referencias

| Recurso | Función |
| --- | --- |
| [`references/organizacion-de-literatura.md`](../../gestor-marco-teorico-estado-del-arte/references/organizacion-de-literatura.md) | Organización de literatura |

### Configuración de interfaz

| Recurso | Función |
| --- | --- |
| [`agents/openai.yaml`](../../gestor-marco-teorico-estado-del-arte/agents/openai.yaml) | Metadatos de interfaz e invocación de la skill. |

## Fuente normativa

Esta ficha se genera desde [`gestor-marco-teorico-estado-del-arte/SKILL.md`](../../gestor-marco-teorico-estado-del-arte/SKILL.md), que permanece como contrato normativo. Regenera la ficha después de modificar ese archivo.
