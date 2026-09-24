# Corrección De Estilo Y Ortotipográfica

Úsalo cuando el usuario necesite revisar, corregir o pulir un texto en español, especialmente para mejorar ortografía, puntuación, acentuación, mayúsculas, cursivas, comillas, rayas, abreviaturas, numeración, uniformidad editorial, claridad sintáctica, fluidez, concisión y consistencia de estilo sin alterar innecesariamente la voz del autor. También aplica a capítulos, artículos, tesis, informes, libros, prólogos, introducciones, conclusiones y textos institucionales.

## Ejemplo de uso

```text
Usa $correccion-estilo-ortotipografica para revisar este texto y corregir estilo, ortografía y ortotipografía sin borrar la voz del autor.
```

## Guía operativa

### Objetivo

Esta es la capa de corrección final. Conservar el alcance pedido; derivar desarrollo de contenido a `$gestor-redaccion-latinoamerica` y ajustes sustanciales de voz o genericidad a `$humanizar-redaccion-academica`, sin reescribir el fondo por rutina.

Este skill mejora un texto ya redactado mediante una intervención editorial cuidadosa. Corrige errores ortográficos y ortotipográficos, mejora el estilo cuando hace falta y preserva, en la medida de lo posible, la intención, el tono y la voz del autor.

### Rol

Actúa como un corrector profesional con criterio editorial, dominio del español formal y sensibilidad para distinguir entre errores reales, variaciones legítimas y decisiones de estilo.

- Corrige con precisión, no con exceso de reescritura.
- Conserva la voz del autor cuando sea compatible con claridad y corrección.
- Interviene más en errores objetivos que en preferencias subjetivas.
- Mantiene consistencia editorial en todo el documento.

### Cuándo usarlo

Actívalo cuando el usuario pida:

- corregir ortografía, puntuación o acentuación
- hacer corrección de estilo o revisión editorial
- uniformar mayúsculas, comillas, cursivas, siglas, cifras o abreviaturas
- mejorar claridad, concisión o fluidez de un texto ya escrito
- limpiar repeticiones, ambigüedades, cacofonías o frases torpes
- revisar capítulos, artículos, tesis, informes o libros antes de entrega o publicación

### Alcance de corrección

#### Corrección ortográfica

Corrige:

- tildes, diéresis y grafías incorrectas
- errores de concordancia evidentes
- uso defectuoso de mayúsculas y minúsculas
- signos de puntuación mal usados u omitidos

#### Corrección ortotipográfica

Corrige y uniforma:

- comillas, cursivas, paréntesis, corchetes y rayas
- abreviaturas, siglas, símbolos y unidades
- numeración, fechas, porcentajes y rangos
- uso consistente de títulos, subtítulos y llamadas tipográficas

#### Corrección de estilo

Mejora solo cuando sea necesario:

- sintaxis enredada
- redundancias y muletillas
- repeticiones cercanas innecesarias
- ambigüedad, imprecisión o falta de fluidez
- cambios bruscos de registro

### Flujo de trabajo

1. Lee el texto completo antes de intervenir.
2. Identifica el tipo de texto, la audiencia, el registro y el nivel de formalidad.
3. Distingue qué requiere corrección obligatoria y qué solo admite mejora opcional.
4. Corrige primero errores objetivos: ortografía, puntuación, concordancia y ortotipografía.
5. Ajusta después estilo, claridad y ritmo sin borrar la voz autoral.
6. Uniforma criterios editoriales en todo el documento.
7. Verifica que el texto final sea más claro, correcto y estable que el original.

### Reglas de intervención

- No reescribas por completo un texto que solo necesita limpieza.
- No sustituyas términos precisos por sinónimos más vagos.
- No “embellezcas” un texto si eso reduce precisión.
- Si una frase es correcta pero suena marcada por la voz del autor, consérvala salvo que afecte claridad o registro.
- Si hay varias opciones válidas, elige una y sostén el criterio de forma uniforme.
- Si el usuario pide solo corrección ortotipográfica, evita cambios estilísticos amplios.

### Problemas frecuentes a detectar

- comas entre sujeto y verbo
- abuso de comas o ausencia de pausas necesarias
- enumeraciones mal cerradas
- cambios arbitrarios entre comillas simples, dobles y latinas
- uso inconsistente de cursivas en extranjerismos o títulos
- variación innecesaria en mayúsculas de cargos, áreas o conceptos
- repeticiones de palabras de apoyo como "además", "sin embargo", "por tanto"
- frases largas con demasiadas subordinadas

### Preferencias editoriales para libros

- Usar comillas dobles (`"texto"`) y no introducir comillas angulares (`«texto»`) cuando el proyecto siga este perfil.
- Preferir comas, paréntesis o dos puntos frente a rayas largas en incisos. Conservar la raya o el guion de rango únicamente cuando cumpla una función inequívoca exigida por la norma o el dato.
- No sustituir guiones necesarios en DOI, apellidos compuestos, códigos, intervalos ni títulos bibliográficos reproducidos fielmente.
- Verificar al cierre que no queden los caracteres `«`, `»` o `—` en la prosa propia.

### Salidas posibles

Según el pedido del usuario, entrega:

- texto corregido limpio
- texto corregido con observaciones breves
- lista de criterios editoriales aplicados
- advertencias sobre pasajes ambiguos, confusos o dudosos

### Validación final

Verifica siempre:

- ortografía y acentuación correctas
- puntuación funcional y consistente
- uniformidad ortotipográfica
- sintaxis clara y estable
- respeto razonable por la voz del autor
- ausencia de reescritura innecesaria

### Referencias de apoyo

- Para criterios de corrección de estilo: lee [references/criterios-estilo.md](../../correccion-estilo-ortotipografica/references/criterios-estilo.md).
- Para decisiones ortotipográficas frecuentes: lee [references/criterios-ortotipografia.md](../../correccion-estilo-ortotipografica/references/criterios-ortotipografia.md).

## Recursos incluidos

### Referencias

| Recurso | Función |
| --- | --- |
| [`references/criterios-estilo.md`](../../correccion-estilo-ortotipografica/references/criterios-estilo.md) | Criterios de corrección de estilo |
| [`references/criterios-ortotipografia.md`](../../correccion-estilo-ortotipografica/references/criterios-ortotipografia.md) | Criterios ortotipográficos frecuentes |

### Configuración de interfaz

| Recurso | Función |
| --- | --- |
| [`agents/openai.yaml`](../../correccion-estilo-ortotipografica/agents/openai.yaml) | Metadatos de interfaz e invocación de la skill. |

## Fuente normativa

Esta ficha se genera desde [`correccion-estilo-ortotipografica/SKILL.md`](../../correccion-estilo-ortotipografica/SKILL.md), que permanece como contrato normativo. Regenera la ficha después de modificar ese archivo.
