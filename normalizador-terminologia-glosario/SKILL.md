---
name: normalizador-terminologia-glosario
description: Úsalo cuando el usuario necesite uniformar términos técnicos, conceptos, nombres de variables, siglas, traducciones, categorías o etiquetas a lo largo de un manuscrito, y construir un glosario o banco terminológico consistente.
---

# Normalizador De Terminología Y Glosario

## Automatización Previa

Si el manuscrito es extenso, ejecutar primero `$auditor-documental-academico`, especialmente `scripts/auditar_terminologia.py`, con términos clave o siglas esperadas. Usar el reporte de frecuencias y variantes antes de normalizar definiciones o glosario.

## Objetivo

Este skill detecta variaciones terminológicas que erosionan claridad y consistencia. Su función es unificar vocabulario técnico y, cuando convenga, construir un glosario operativo para la obra.

## Cuándo usarlo

- cuando un mismo concepto aparece con varios nombres
- cuando hay siglas mal introducidas o inconsistentes
- cuando se mezclan traducciones o equivalencias
- cuando el manuscrito requiere glosario

## Flujo de trabajo

1. Identifica términos clave, siglas y categorías recurrentes.
2. Detecta duplicidades, variantes y conflictos.
3. Elige una forma principal para cada concepto.
4. Uniforma usos en todo el documento.
5. Construye glosario o tabla de control si es útil.

## Validación final

- cada concepto central tiene una forma estable
- las siglas están bien introducidas
- no hay cambios arbitrarios de denominación
- el glosario refleja el uso real del manuscrito
