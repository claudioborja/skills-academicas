# Localización de candidatos de respaldo

`scripts/auditar_respaldo_citas_pdf.py` trabaja con citas numéricas y un manifiesto de fuentes. No extrae automáticamente citas APA autor-año ni verifica si una conclusión está sustentada. La búsqueda léxica ayuda a localizar pasajes; revisar siempre contexto, negaciones, diseño y población.

El manifiesto JSON contiene una lista:

```json
[
  {"id": 1, "label": "Fuente consultada", "pdf": "fuentes/estudio.pdf", "reference": "Referencia verificada", "references_start_page": 12}
]
```

`id` y `pdf` son obligatorios. Las rutas relativas de PDF se resuelven desde la carpeta del proyecto. `label`, `reference` y `references_start_page` son opcionales; este último excluye del análisis las páginas de bibliografía cuando se conoce su inicio. No inventar ese dato.

```text
python skills/workflow-maestro-academico-editorial/scripts/ejecutar.py humanizar-redaccion-academica/scripts/auditar_respaldo_citas_pdf.py "ruta/proyecto" --manifest "ruta/referencias.json" --book "ruta/manuscrito.md" --out "ruta/auditoria.txt"
```

`--vocabulary "ruta/vocabulario.json"` permite añadir equivalencias específicas, por ejemplo `{"aprendizaje": ["learning"]}`. Sin este argumento no se presupone un área temática ni traducciones. No cargar código Python del proyecto para obtener referencias.

Los informes conservan alertas históricas de "respaldo débil" para compatibilidad: significan afinidad léxica baja, no un veredicto de validez. Una puntuación alta tampoco prueba respaldo. El resumen de alertas es una lista de comprobaciones pendientes, no una instrucción de borrar citas.
