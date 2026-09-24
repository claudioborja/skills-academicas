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

## Mapa de especialidades

| Área | Skills |
| --- | --- |
| Preparación y arquitectura | [`planificador-obra-academica`](skills/planificador-obra-academica.md), [`preprocesador-documentos`](skills/preprocesador-documentos.md), [`auditor-documental-academico`](skills/auditor-documental-academico.md) |
| Tesis y libros | [`constructor-tesis-academica`](skills/constructor-tesis-academica.md), [`convertidor-tesis-a-libro`](skills/convertidor-tesis-a-libro.md), [`gestor-continuidad-libro`](skills/gestor-continuidad-libro.md), [`gestor-marco-teorico-estado-del-arte`](skills/gestor-marco-teorico-estado-del-arte.md) |
| Artículos y revisiones | [`explorador-temas-articulos`](skills/explorador-temas-articulos.md), [`redaccion-articulo-cientifico-imryd`](skills/redaccion-articulo-cientifico-imryd.md), [`auditor-articulo-imryd`](skills/auditor-articulo-imryd.md), [`revision-sistematica-kitchenham`](skills/revision-sistematica-kitchenham.md), [`revision-sistematica-prisma`](skills/revision-sistematica-prisma.md) |
| Evidencia y bibliografía | [`verificador-resultados-investigacion`](skills/verificador-resultados-investigacion.md), [`gestor-referencias-academicas`](skills/gestor-referencias-academicas.md), [`automatizador-referencias`](skills/automatizador-referencias.md), [`revisor-citas-consistencia-bibliografica`](skills/revisor-citas-consistencia-bibliografica.md), [`ajustes-editoriales-bibliograficos`](skills/ajustes-editoriales-bibliograficos.md), [`filtro-editoriales-depredadoras`](skills/filtro-editoriales-depredadoras.md) |
| Redacción y revisión | [`gestor-redaccion-latinoamerica`](skills/gestor-redaccion-latinoamerica.md), [`humanizar-redaccion-academica`](skills/humanizar-redaccion-academica.md), [`correccion-estilo-ortotipografica`](skills/correccion-estilo-ortotipografica.md), [`auditor-coherencia-argumentativa`](skills/auditor-coherencia-argumentativa.md), [`normalizador-terminologia-glosario`](skills/normalizador-terminologia-glosario.md), [`revisor-resumen-abstract-palabras-clave`](skills/revisor-resumen-abstract-palabras-clave.md), [`respondedor-observaciones-academicas`](skills/respondedor-observaciones-academicas.md) |
| Recursos técnicos | [`gestor-tablas-figuras-pies`](skills/gestor-tablas-figuras-pies.md), [`gestor-imagenes-academicas-libros`](skills/gestor-imagenes-academicas-libros.md), [`gestor-ecuaciones-academicas`](skills/gestor-ecuaciones-academicas.md), [`gestor-codigo-tecnico-editorial`](skills/gestor-codigo-tecnico-editorial.md) |
| Cierre editorial | [`gestor-contribuciones-autoria`](skills/gestor-contribuciones-autoria.md), [`disenador-maquetador-word`](skills/disenador-maquetador-word.md), [`maquetacion-academica-preentrega`](skills/maquetacion-academica-preentrega.md) |

El [mapa de responsabilidades](../editor-en-jefe/references/mapa-responsabilidades.md) define la frontera exacta de cada especialidad. Las fichas enlazadas explican entradas, flujo, entregables, límites, comandos y recursos.

## Flujo de decisión

1. **Situar el producto.** Distinguir tesis, libro, artículo y revisión sistemática. En revisiones, separar Kitchenham de PRISMA y, para PRISMA, declarar además el método de conducción.
2. **Preparar los insumos.** Preprocesar documentos largos o crear inventarios mecánicos cuando reduzca lectura innecesaria.
3. **Planificar.** Definir arquitectura y entregables sin imponer la estructura de un libro a otros productos.
4. **Investigar y redactar.** Reutilizar evidencia trazable vigente y desarrollar capítulos completos con revisión integrada de respaldo, argumento y estilo.
5. **Revisar el conjunto.** Verificar los resultados comprobables con [`verificador-resultados-investigacion`](../verificador-resultados-investigacion/SKILL.md), resolver o declarar hallazgos y reabrir discusión/conclusiones cuando cambien los datos. Comprobar continuidad, terminología, referencias, ecuaciones y recursos visuales; la revisión local no sustituye la global. Resolver contribuciones y autoría con la política aplicable antes del cierre.
6. **Cerrar.** Si el libro requiere dirección visual profesional, diseñarlo con `disenador-maquetador-word`; después comprobar requisitos y entrega con `maquetacion-academica-preentrega`. Validar el OOXML y realizar la inspección visual final en Microsoft Word u otro motor autorizado; no usar LibreOffice. Mantener controles y pendientes fuera de la obra. Si hay bloqueos, identificarla como borrador.
7. **Responder observaciones.** Abrir una ronda trazable sin rehacer fases que no fueron afectadas.

## Reglas operativas

- La instrucción del usuario delimita la intervención: diagnosticar no autoriza reescribir.
- Citas, datos, DOI, fórmulas, tablas, código y transcripciones son contenido protegido.
- Los scripts producen señales e inventarios; no certifican coherencia científica ni suficiencia de evidencia.
- [`verificador-resultados-investigacion`](../verificador-resultados-investigacion/SKILL.md) separa control mecánico, revisión metodológica e interpretación; conserva fuentes y deja un informe individual por hallazgo antes de cualquier corrección autorizada.
- Kitchenham gobierna completamente las revisiones sistemáticas de ingeniería de software cuando está activo.
- [`revision-sistematica-prisma`](../revision-sistematica-prisma/SKILL.md) gobierna PRISMA 2020, sus extensiones, el flujo y la lista de comprobación; el método de conducción debe declararse por separado y no se mezcla con Kitchenham por defecto.
- [`disenador-maquetador-word`](../disenador-maquetador-word/SKILL.md) gobierna la identidad visual, los estilos y la composición editable de libros en Word; la preentrega conserva ese diseño y verifica los requisitos finales.
- [`gestor-contribuciones-autoria`](../gestor-contribuciones-autoria/SKILL.md) selecciona CRediT y perfiles especializados, separa contribución de autoría y prepara el mapeo al esquema técnico del destino.
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

```text
Usa $revision-sistematica-prisma para auditar este protocolo, las búsquedas, el flujo de selección y la lista PRISMA 2020 sin inventar artefactos faltantes.
```

```text
Usa $gestor-contribuciones-autoria para documentar quién hizo qué, aplicar la política de autoría de la revista y preparar los roles para JATS y Crossref.
```

```text
Usa $verificador-resultados-investigacion para comprobar estos resultados, explicar cada discrepancia y corregir solo lo autorizado con una segunda verificación.
```

## Mantenimiento

Entre las utilidades generales del orquestador están:

- `scripts/ejecutar.py`: valida colisiones comunes y lanza scripts especializados.
- `scripts/validar_coleccion.py`: comprueba estructura, pruebas, dependencias y sincronización.
- `scripts/generar_documentacion_skills.py`: regenera el catálogo y las fichas; no modifica los README generales.
- `scripts/instalar_requisitos.py`: comprueba o instala las dependencias fijadas.
- `scripts/preparar_runtime_portable.py`: prepara intérpretes y wheels opcionales para distribución separada.

El [mapa de responsabilidades](../editor-en-jefe/references/mapa-responsabilidades.md) define la frontera de cada skill. El [`SKILL.md`](../editor-en-jefe/SKILL.md) sigue siendo el contrato normativo completo.
