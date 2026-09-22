# Editor en jefe

`editor-en-jefe` coordina la colección. Se usa cuando el encargo combina varias fases, cuando todavía no está claro qué especialidad corresponde o cuando un cambio puede afectar evidencia, redacción, referencias, recursos y entrega.

## Responsabilidad

El orquestador identifica el producto, la etapa, el método, la norma y los materiales disponibles. Después activa únicamente las skills necesarias. No redacta por inercia, no repite revisiones ya cerradas y no permite que una herramienta auxiliar cambie el método de investigación.

## Cuándo usarlo

- Desarrollo o revisión integral de una tesis, libro o artículo.
- Conversión de tesis a libro.
- Preentrega de un manuscrito con referencias, tablas, imágenes o ecuaciones.
- Diagnóstico de un proyecto académico sin una ruta de trabajo definida.
- Coordinación de varias skills con límites y entregables distintos.

Para una corrección aislada —por ejemplo, normalizar una bibliografía IEEE o auditar ecuaciones— puede invocarse directamente la skill responsable.

## Flujo de decisión

1. **Situar el producto.** Distinguir tesis, libro, artículo y revisión sistemática.
2. **Preparar los insumos.** Preprocesar documentos largos o crear inventarios mecánicos cuando reduzca lectura innecesaria.
3. **Planificar.** Definir arquitectura y entregables sin imponer la estructura de un libro a otros productos.
4. **Investigar y redactar.** Reutilizar evidencia trazable vigente y desarrollar capítulos completos con revisión integrada de respaldo, argumento y estilo.
5. **Revisar el conjunto.** Comprobar continuidad, terminología, referencias, ecuaciones y recursos visuales; la revisión local no sustituye la global.
6. **Cerrar.** Integrar el manuscrito y verificar el artefacto exportado mediante renderizado e inspección visual; entregar controles y pendientes fuera de la obra. Si hay bloqueos, identificarla como borrador.
7. **Responder observaciones.** Abrir una ronda trazable sin rehacer fases que no fueron afectadas.

## Reglas operativas

- La instrucción del usuario delimita la intervención: diagnosticar no autoriza reescribir.
- Citas, datos, DOI, fórmulas, tablas, código y transcripciones son contenido protegido.
- Los scripts producen señales e inventarios; no certifican coherencia científica ni suficiencia de evidencia.
- Kitchenham gobierna completamente las revisiones sistemáticas de ingeniería de software cuando está activo.
- El perfil institucional o editorial prevalece sobre valores genéricos cuando ha sido suministrado y no contradice el método.
- Cada script especializado permanece dentro de su skill; `scripts/ejecutar.py` es el lanzador transversal.
- La [política de producción editorial eficiente](../editor-en-jefe/references/produccion-editorial-eficiente.md) exige preservar calidad y medir el consumo total antes de afirmar ahorros.
- Las carpetas se crean según necesidad; el inicializador completo es opcional. SQLite y embeddings no son requisitos ni un RAG ya implementado.

## Ejemplos

```text
Usa $editor-en-jefe para revisar este libro desde el diagnóstico hasta la preentrega y detente ante cualquier decisión metodológica no documentada.
```

```text
Usa $editor-en-jefe para convertir esta tesis en un libro, conservar la evidencia y coordinar referencias, imágenes, ecuaciones y Word final.
```

```text
Usa $editor-en-jefe para identificar qué falta antes de enviar este artículo a la revista indicada.
```

## Mantenimiento

Entre las utilidades generales del orquestador están:

- `scripts/ejecutar.py`: valida colisiones comunes y lanza scripts especializados.
- `scripts/validar_coleccion.py`: comprueba estructura, pruebas, dependencias y sincronización.
- `scripts/generar_documentacion_skills.py`: regenera el catálogo y las fichas; no modifica los README generales.
- `scripts/instalar_requisitos.py`: comprueba o instala las dependencias fijadas.
- `scripts/preparar_runtime_portable.py`: prepara intérpretes y wheels opcionales para distribución separada.

El [mapa de responsabilidades](../editor-en-jefe/references/mapa-responsabilidades.md) define la frontera de cada skill. El [`SKILL.md`](../editor-en-jefe/SKILL.md) sigue siendo el contrato normativo completo.
