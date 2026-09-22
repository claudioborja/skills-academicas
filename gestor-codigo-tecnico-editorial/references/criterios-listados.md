# Criterios para listados de código

## Selección

Publicar código cuando permita entender una decisión, un algoritmo, una integración o un procedimiento que el texto por sí solo no explica. Usar pseudocódigo cuando la lógica importe más que una implementación concreta. Remitir a un repositorio, anexo o recurso complementario cuando la extensión completa no contribuya a la lectura principal.

No publicar secretos, tokens, datos personales, credenciales, rutas privadas, volcados completos de registros ni dependencias sin función explicativa. Reemplazar información sensible con marcadores inequívocos, por ejemplo `<TOKEN_DE_EJEMPLO>`, y declarar que es un valor simulado.

## Clases de listado

| Clase | Señal recomendada | Tratamiento |
| --- | --- | --- |
| Código fuente | Lenguaje identificado | Indicar versión o contexto si afecta la comprensión. |
| Comando | `bash`, `powershell` o equivalente | Separar comando, salida y explicación. |
| Configuración | `json`, `yaml`, `toml`, `ini` | Mostrar solo claves pertinentes y ocultar secretos. |
| Pseudocódigo | `text` o rótulo explícito | No presentarlo como sintaxis ejecutable. |
| Salida/error | `text` con rótulo de salida | Conservar únicamente evidencia real o declararla simulada. |

## Relación con la maqueta

La exportación final debe conservar un estilo de carácter monoespaciado, fondo o borde solo si el perfil lo contempla, y evitar que un listado se parta entre páginas cuando sea razonablemente posible. Revisar visualmente en DOCX/PDF las líneas largas, sangrías, símbolos, viudas, numeración y pies. Si la herramienta de exportación no conserva bloques de código, corregir la plantilla o el conversor antes de declarar lista la entrega.
