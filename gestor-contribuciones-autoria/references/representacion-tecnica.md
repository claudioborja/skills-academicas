# Representación técnica

Leer únicamente las secciones de los destinos realmente solicitados.

## JATS XML

Usar elementos `<role>` repetibles para múltiples funciones y atributos de vocabulario para vincular el término canónico con CRediT u otra taxonomía. No confundir `contrib-type` con la descripción granular de todas las contribuciones. Validar contra la versión JATS exigida.

## Crossref

Depositar roles admitidos por la versión vigente del esquema. Conservar vocabulario y tipo; comprobar si la versión permite múltiples roles y CRediT antes de generar XML. Incluir ORCID autenticado cuando esté disponible y autorizado.

## DataCite

Usar sus `contributorType` para funciones relacionadas con datasets, software y otros recursos con DOI, por ejemplo recopilación o curación de datos, administración del proyecto, supervisión, traducción o alojamiento. Mantener CRediT si también se necesita una declaración científica de contribuciones.

## ORCID

ORCID identifica a la persona y puede transportar roles compatibles. Preferir identificadores autenticados; no inventar, corregir ni atribuir un ORCID por coincidencia nominal. ORCID no decide autoría.

## CodeMeta y Citation File Format

- CodeMeta: describir software mediante JSON-LD, personas, organizaciones y relaciones como autoría, colaboración o mantenimiento.
- CFF: preparar `CITATION.cff` para indicar cómo citar el software o dataset y sus autores.

No convertir automáticamente un mantenedor técnico en autor de un artículo ni viceversa.

## MARC Relator Terms

Usar términos y códigos mantenidos por Library of Congress para vincular agentes con libros y otros recursos: autor, editor, compilador, traductor, ilustrador, diseñador, analista, entre otros. Conservar el código canónico cuando el catálogo lo requiera.

## CRO y PROV-O

CRO amplía la clasificación de roles para usos ontológicos. PROV-O relaciona agentes, actividades y entidades para expresar procedencia. No añadir estas capas si el destino solo necesita una declaración legible en el manuscrito.

## Dublin Core

Usar `creator` y `contributor` únicamente cuando el repositorio o intercambio lo exija. Su granularidad es insuficiente para reemplazar CRediT, DataCite, MARC u otro vocabulario detallado; conservar el mapeo original para evitar pérdida semántica.

## Verificación de exportación

1. Validar sintaxis y versión del esquema.
2. Comprobar que cada rol conserva vocabulario, identificador y persona correctos.
3. Verificar múltiples roles y caracteres Unicode.
4. Comparar el depósito o exportación con la matriz aprobada.
5. Reportar pérdidas de información o mapeos locales; no ocultarlos bajo `Other` sin explicación.
