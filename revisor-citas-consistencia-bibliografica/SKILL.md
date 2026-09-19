---
name: revisor-citas-consistencia-bibliografica
description: Úsalo cuando el usuario necesite comprobar que las citas del cuerpo coinciden con la bibliografía final, detectar referencias huérfanas, entradas faltantes, datos inconsistentes, fuentes sin DOI/acceso completo, revistas o editoriales depredadoras y mezclas de estilo bibliográfico dentro de un mismo documento.
---

# Revisor De Citas Y Consistencia Bibliográfica

## Automatización Previa

Si el documento está en Markdown/TXT o fue convertido por `$preprocesador-documentos`, ejecutar primero `$automatizador-referencias`, especialmente `scripts/auditar_citas_bibliografia.py` y `scripts/normalizar_referencias.py`, para obtener faltantes, DOI, referencias no citadas y señales de mezcla APA/IEEE antes de revisar con criterio editorial.

## Objetivo

Este skill audita la relación entre citas y referencias finales. Revisa integridad, consistencia formal y correspondencia entre cuerpo del texto y bibliografía.

## Cuándo usarlo

- al final del proceso de escritura
- cuando el manuscrito pasó por varias manos
- cuando existen sospechas de mezcla de estilos
- antes de entrega o publicación

## Flujo de trabajo

1. Identifica la norma bibliográfica activa.
   - En IEEE, cargar la guía de `gestor-referencias-academicas` y ejecutar el auditor numérico con `--style ieee --strict` sobre la obra completa. Revisar localizadores, números repetidos, orden de primera aparición y rangos heredados; no renumerar ni borrar automáticamente. No confundir formato numérico con cumplimiento IEEE integral.
2. Lista todas las citas del cuerpo.
3. Lista todas las entradas de la bibliografía.
4. Cruza ambos conjuntos y detecta faltantes o sobrantes.
5. Revisa inconsistencias de autor, año, título, DOI, revista/editorial y estilo.
6. Activa `$filtro-editoriales-depredadoras` si aparecen revistas, editoriales, congresos, plataformas o URLs dudosas.
7. Si existe una política editorial adicional, revisa también su cumplimiento y distingue entre error normativo y restricción editorial.

## Validación final

- toda cita tiene referencia
- toda referencia usada aparece citada
- no hay mezcla de estilos
- no hay años o autores inconsistentes
- no hay fuentes clasificadas en rojo por reputación editorial
- si existe una política editorial adicional, queda claramente separada de la norma bibliográfica base
