# Workflow Maestro Académico Editorial

`workflow-maestro-academico-editorial` coordina la colección. Se usa cuando el encargo combina varias fases, cuando todavía no está claro qué especialidad corresponde o cuando un cambio puede afectar evidencia, redacción, referencias, recursos y entrega.

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
4. **Investigar y redactar.** Resolver evidencia y método antes de pulir estilo.
5. **Revisar.** Aplicar coherencia, continuidad, terminología, referencias, ecuaciones y recursos visuales según el alcance.
6. **Cerrar.** Corregir estilo, resumen y maquetación; renderizar artefactos cuando el formato visual importe.
7. **Responder observaciones.** Abrir una ronda trazable sin rehacer fases que no fueron afectadas.

## Reglas operativas

- La instrucción del usuario delimita la intervención: diagnosticar no autoriza reescribir.
- Citas, datos, DOI, fórmulas, tablas, código y transcripciones son contenido protegido.
- Los scripts producen señales e inventarios; no certifican coherencia científica ni suficiencia de evidencia.
- Kitchenham gobierna completamente las revisiones sistemáticas de ingeniería de software cuando está activo.
- El perfil institucional o editorial prevalece sobre valores genéricos cuando ha sido suministrado y no contradice el método.
- Cada script especializado permanece dentro de su skill; `scripts/ejecutar.py` es el lanzador transversal.

## Ejemplos

```text
Usa $workflow-maestro-academico-editorial para revisar este libro desde el diagnóstico hasta la preentrega y detente ante cualquier decisión metodológica no documentada.
```

```text
Usa $workflow-maestro-academico-editorial para convertir esta tesis en un libro, conservar la evidencia y coordinar referencias, imágenes, ecuaciones y Word final.
```

```text
Usa $workflow-maestro-academico-editorial para identificar qué falta antes de enviar este artículo a la revista indicada.
```

## Mantenimiento

El orquestador contiene dos utilidades generales:

- `scripts/ejecutar.py`: valida colisiones comunes y lanza scripts especializados.
- `scripts/validar_coleccion.py`: comprueba estructura, pruebas, dependencias y sincronización.

El [mapa de responsabilidades](../workflow-maestro-academico-editorial/references/mapa-responsabilidades.md) define la frontera de cada skill. El [`SKILL.md`](../workflow-maestro-academico-editorial/SKILL.md) sigue siendo el contrato normativo completo.
