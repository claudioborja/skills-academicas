# Resumen operativo del estilo Jorge Briceño

## Origen

Perfil extraído desde `TesisDr.pdf`, atribuido a Jorge Briceño, priorizando las secciones en español de la tesis: portada, índice, introducción, resumen, conclusiones, bibliografía inicial y apéndice. Se excluyeron los artículos científicos publicados en inglés para evitar que el perfil de redacción académica en español quedara dominado por estructuras de paper anglosajón.

## Voz

La voz es académica, técnica y demostrativa. Tiende a explicar procedimientos, justificar decisiones metodológicas y valorar resultados con prudencia. No busca una prosa ensayística ni persuasiva, sino una exposición de laboratorio: precisa, acumulativa y orientada a evidencias.

## Rasgos dominantes

- Predominan oraciones de longitud media, con variación entre frases directas y periodos más densos.
- Los párrafos alternan explicación conceptual, descripción de procedimiento, comparación técnica y síntesis de resultados.
- La cohesión se apoya en conectores explícitos, sobre todo `además`, `también` y `sin embargo`.
- El estilo matiza con frecuencia mediante formas como `puede`, `cuando`, `parece`, `suele` y `según`.
- La argumentación avanza desde el problema técnico hacia la condición experimental, el resultado observado y la consecuencia metodológica.
- La terminología disciplinar se mantiene estable y se repite sin buscar sinónimos innecesarios cuando el concepto técnico lo exige.

## Cómo aplicar el estilo

1. Abrir cada apartado con una idea técnica clara, no con una frase decorativa.
2. Desarrollar la explicación mediante relaciones causales, condiciones de trabajo, contraste entre métodos o consecuencias observables.
3. Usar conectores explícitos con moderación; el perfil los admite, pero no conviene convertirlos en muletilla.
4. Mantener prudencia científica: preferir `puede`, `parece`, `permite`, `resulta`, `se observa` o `en estas condiciones` cuando el contenido no autorice una afirmación absoluta.
5. Cerrar los párrafos con un resultado, una implicación técnica o una limitación concreta.
6. Conservar datos, unidades, nombres de técnicas, siglas, citas, tablas, fórmulas, DOI y referencias sin reescritura ornamental.

## Qué evitar

- Copiar frases extensas del PDF modelo.
- Trasladar ejemplos, datos experimentales o resultados de la tesis a textos de otro tema.
- Imitar encabezados repetidos, residuos de extracción PDF o títulos de artículos.
- Convertir el estilo en prosa rígida con todos los párrafos del mismo tamaño.
- Reemplazar terminología técnica por sinónimos débiles solo para variar.

## Uso recomendado

Para comparar un borrador contra este perfil:

```powershell
python skills/humanizar-redaccion-academica/scripts/comparar_con_perfil_estilo.py "ruta/borrador.md" --profile "skills/humanizar-redaccion-academica/styles/jorge-briceno/perfil.json" --out "ruta/diagnostico_estilo.md" --json-out "ruta/diagnostico_estilo.json"
```

Después de comparar, reescribir por bloques. El perfil debe guiar ritmo, conectores, matizadores y arquitectura de párrafo, no funcionar como banco de frases copiables.
