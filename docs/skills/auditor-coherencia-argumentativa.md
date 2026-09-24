# Auditor De Coherencia Argumentativa

Úsalo cuando el usuario necesite revisar si un texto tiene continuidad lógica, tesis clara, transiciones válidas, conclusiones derivadas del desarrollo y ausencia de contradicciones, repeticiones conceptuales o saltos argumentativos.

## Ejemplo de uso

```text
Usa $auditor-coherencia-argumentativa para revisar la solidez lógica y estructural de este texto.
```

## Guía operativa

### Objetivo

Este skill examina la solidez interna de un texto. Detecta problemas de lógica, desorden conceptual, repeticiones innecesarias, tesis débiles y conclusiones que no se desprenden del cuerpo del documento.

### Cuándo usarlo

- antes de cerrar un capítulo o manuscrito
- cuando el texto “suena bien” pero no termina de convencer
- cuando hay repeticiones o secciones que parecen desconectadas
- cuando el usuario necesita una lectura crítica de fondo

### Flujo de trabajo

1. Identifica tesis, propósito y recorrido del texto.
2. Revisa relaciones entre párrafos, apartados y conclusiones.
3. Detecta saltos lógicos, contradicciones y circularidades.
4. Señala repeticiones y bloques débiles.
5. Propone ajustes de estructura o argumentación.

### Salida esperada

- hallazgos priorizados
- explicación breve del problema
- sugerencia concreta de corrección

### Validación final

- la tesis es visible
- cada bloque contribuye al propósito global
- no hay afirmaciones importantes sin preparación argumentativa
- las conclusiones derivan del desarrollo

## Recursos incluidos

### Configuración de interfaz

| Recurso | Función |
| --- | --- |
| [`agents/openai.yaml`](../../auditor-coherencia-argumentativa/agents/openai.yaml) | Metadatos de interfaz e invocación de la skill. |

## Fuente normativa

Esta ficha se genera desde [`auditor-coherencia-argumentativa/SKILL.md`](../../auditor-coherencia-argumentativa/SKILL.md), que permanece como contrato normativo. Regenera la ficha después de modificar ese archivo.
