# Flujo PRISMA 2020 y trazabilidad

## Elegir la plantilla

El sitio oficial ofrece cuatro familias:

1. revisión nueva con bases y registros;
2. revisión nueva con bases/registros y otras fuentes;
3. revisión actualizada con bases y registros;
4. revisión actualizada con bases/registros y otras fuentes.

Elegir la plantilla por el proceso real, no por la que tenga menos casillas.

## Entidades

- **Registro:** entrada recuperada de una fuente antes de obtener el documento.
- **Informe:** documento que comunica información de un estudio.
- **Estudio:** investigación subyacente; puede tener varios informes.

No usar los tres términos como sinónimos. La diferencia explica por qué el número de informes incluidos puede superar el de estudios.

## Transiciones mínimas

Para una revisión nueva, comprobar:

```text
registros identificados en bases y registros
- duplicados eliminados
- registros eliminados por automatización
- otros registros eliminados antes del cribado
= registros cribados

registros cribados - registros excluidos = informes buscados
informes buscados en esa ruta - informes no recuperados = informes evaluados de bases/registros

informes identificados por otros métodos = informes buscados por otros métodos
informes buscados por otros métodos - no recuperados = informes evaluados por otros métodos

informes evaluados de ambas rutas - informes excluidos con razón en ambas rutas = informes incluidos
estudios incluidos <= informes incluidos
```

## Otras fuentes

Mantener la procedencia de sitios web, organizaciones, búsqueda de citas, referencias y contactos. En la plantilla oficial con otras fuentes, esta ruta comienza con informes identificados y permanece separada de los registros de bases/registros hasta la inclusión. No inventar un “registro” para una fuente que no produjo uno.

## Revisiones actualizadas

Separar evidencia de la versión anterior y nuevos resultados. Conservar estudios incluidos previamente, informes anteriores, resultados de actualización, nuevos incluidos y reclasificaciones con motivo. No sumar sin explicación conteos históricos y nuevos.

## Razones de exclusión

- Asignar una razón primaria por informe excluido a texto completo.
- Usar categorías específicas vinculadas a elegibilidad.
- Conservar detalle suficiente para responder una auditoría.
- No usar “no pertinente” si puede indicarse población, intervención, diseño, resultado o periodo.
- Publicar la lista cuando la política y la protección de datos lo permitan.

## Auditoría mecánica

Copiar `assets/conteos-flujo-ejemplo.json`, sustituir valores y ejecutar `scripts/auditar_prisma.py flow-check`. Para revisiones actualizadas, el archivo audita el tramo nuevo; documentar por separado su integración con la versión anterior y trasladarla a la plantilla oficial.

`PASS` significa que las transiciones declaradas son aritméticamente coherentes. No prueba que los conteos sean verdaderos, que las razones sean correctas ni que la revisión cumpla PRISMA.
