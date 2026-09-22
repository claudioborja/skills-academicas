# Reorganización de la colección: 29 a 27 skills

Documento histórico de una reorganización anterior. El catálogo vigente contiene 30 skills e incorpora `revision-sistematica-prisma`; no usar este archivo como inventario actual.

- `desgenericador-humanizador-texto` se integra como modo de `humanizar-redaccion-academica`. Se conservan las referencias útiles y un único analizador.
- `gestor-referencias-apa7` y `gestor-referencias-ieee` se integran en `gestor-referencias-academicas`. Seleccionar APA 7 o IEEE dentro del flujo común.
- Los extractores `pdf_a_contexto_apa7.py` y `pdf_a_contexto_ieee.py` se sustituyen por `gestor-referencias-academicas/scripts/pdf_a_contexto.py`. Actualizar comandos externos; no quedan alias instalados que activen flujos antiguos.
- Permanecen independientes los auditores documentales y bibliográficos, la redacción IMRyD, las metodologías y las especialidades editoriales.

## Recuperación

El archivo `../assets/migraciones/antes-fusion-20260919.zip` conserva los 203 archivos originales y un manifiesto SHA-256, sin entornos virtuales ni cachés. Extraer fuera del directorio de skills activas para recuperar o comparar contenido. No cargar sus instrucciones como parte del flujo vigente.

Se retiraron del uso general cuatro scripts de humanización específicos de un libro: `aplicar_estilo_robbins_txt.py`, `generar_libro_final_robbins.py`, `humanizar_tablas_listas_txt.py` y `reforzar_identidad_autor_txt.py`. Permanecen íntegros en ese archivo. Su contenido temático requiere el proyecto original; no se transforma automáticamente en un motor general de redacción.

Los perfiles de estilo guardados como datos permanecen disponibles. La documentación de perfiles editoriales y el mapa del orquestador gobiernan las reglas compartidas de la colección activa.

La auditoría léxica de citas ahora recibe `--manifest` con referencias JSON y un vocabulario opcional. Ya no carga un generador Python de un libro particular ni presupone términos de educación. Los comandos externos de esa herramienta deben adaptarse al nuevo manifiesto.
