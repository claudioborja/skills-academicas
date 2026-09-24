# Documentación

Esta documentación tiene tres niveles:

1. El [README principal](../README.md) explica instalación, mapa completo, automatización y distribución.
2. El [orquestador](orquestador.md) ayuda a elegir la ruta cuando intervienen varias especialidades.
3. El [catálogo agrupado](skills/README.md) conduce a fichas operativas generadas desde cada `SKILL.md`.

## Rutas rápidas

| Necesidad | Punto de entrada |
| --- | --- |
| Proyecto integral o alcance incierto | [`editor-en-jefe`](skills/editor-en-jefe.md) |
| Tesis que seguirá siendo tesis | [`constructor-tesis-academica`](skills/constructor-tesis-academica.md) |
| Transformar tesis en libro | [`convertidor-tesis-a-libro`](skills/convertidor-tesis-a-libro.md) |
| Controlar admisibilidad, front matter o prepublicación de un libro | [`gestor-control-editorial-libros`](skills/gestor-control-editorial-libros.md) |
| Artículo científico | [`redaccion-articulo-cientifico-imryd`](skills/redaccion-articulo-cientifico-imryd.md) |
| Revisión Kitchenham | [`revision-sistematica-kitchenham`](skills/revision-sistematica-kitchenham.md) |
| Reporte PRISMA | [`revision-sistematica-prisma`](skills/revision-sistematica-prisma.md) |
| Verificar resultados antes de publicarlos | [`verificador-resultados-investigacion`](skills/verificador-resultados-investigacion.md) |
| Diseñar y entregar un libro Word editable | [`disenador-maquetador-word`](skills/disenador-maquetador-word.md) → [`maquetacion-academica-preentrega`](skills/maquetacion-academica-preentrega.md) |

## Guías transversales

- [Orquestador académico editorial](orquestador.md)
- [Catálogo de skills](skills/README.md)
- [Mapa de responsabilidades](../editor-en-jefe/references/mapa-responsabilidades.md)
- [Portabilidad y validación](../editor-en-jefe/references/portabilidad.md)
- [Producción editorial eficiente y criterios de entrega](../editor-en-jefe/references/produccion-editorial-eficiente.md)
- [Revisión sistemática PRISMA](../revision-sistematica-prisma/SKILL.md)
- [Fuentes oficiales PRISMA](../revision-sistematica-prisma/references/fuentes-oficiales.md)
- [Diseño y maquetación profesional en Word](../disenador-maquetador-word/SKILL.md)
- [Contribuciones, autoría y metadatos](../gestor-contribuciones-autoria/SKILL.md)
- [Control editorial de libros](../gestor-control-editorial-libros/SKILL.md)
- [Verificación de resultados e informes de intervención](../verificador-resultados-investigacion/SKILL.md)
- [Organización proporcional del proyecto de libro](../planificador-obra-academica/references/estructura-directorios-libro.md)
- [Instalación y distribución de la colección](../README.md)

El catálogo contiene 34 skills. Cada ficha conserva la guía operativa, el ejemplo real de invocación, los límites, la coordinación, los comandos presentes en el `SKILL.md` y una tabla descriptiva de recursos. Las fichas se regeneran; los `SKILL.md` siguen siendo las instrucciones normativas. El README principal y esta guía se mantienen manualmente.

Para revisiones, Kitchenham y PRISMA son rutas separadas: Kitchenham gobierna su metodología en ingeniería de software; PRISMA gobierna el reporte y exige declarar aparte el método de conducción. Para contribuciones, CRediT describe tareas, mientras la política del destino gobierna la autoría y los esquemas técnicos gobiernan la exportación. Para resultados, los controles automáticos reproducen operaciones y consistencia; la revisión humana conserva la decisión metodológica, disciplinar e interpretativa.

Los flujos Word usan generación nativa con Python y controles OOXML. La inspección visual final corresponde a Microsoft Word u otro motor autorizado expresamente; LibreOffice no se utiliza.

La reutilización de evidencia y la revisión integrada son reglas de trabajo. No implican que exista una implementación RAG/SQLite ni que se hayan demostrado ahorros de tokens o aceptación editorial.
