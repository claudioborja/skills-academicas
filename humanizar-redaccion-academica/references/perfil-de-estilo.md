# Perfil De Estilo Para Reescritura Natural

## Proposito

Usar documentos modelo del propio autor, docente, institucion o proyecto para extraer rasgos de voz: ritmo, conectores, longitud de oraciones, formas de matizar, modo de cerrar parrafos y grado de concrecion. El objetivo es conservar coherencia editorial y reducir prosa mecanica, no copiar frases ni garantizar resultados frente a detectores.

## Regla De Seguridad Editorial

No imitar literalmente ni transferir oraciones largas del documento modelo. Usar el perfil como mapa de decisiones: ritmo, transiciones, densidad, matices y estrategias de parrafo. Preservar citas, referencias, DOI, URLs, tablas, codigo, formulas y transcripciones.

## Flujo Recomendado

1. Convertir el documento modelo o extraer perfil:

```powershell
python skills/editor-en-jefe/scripts/ejecutar.py humanizar-redaccion-academica/scripts/documento_a_perfil_estilo.py "modelo.docx" --out perfil.md --json-out perfil.json
```

Para crear un estilo reutilizable dentro del skill, preferir:

```powershell
python skills/editor-en-jefe/scripts/ejecutar.py humanizar-redaccion-academica/scripts/perfilar_y_comparar_estilo.py --style-name "nombre del estilo" --model "modelo.docx" --draft "borrador.docx"
```

Cada estilo queda en `skills/humanizar-redaccion-academica/styles/<nombre-del-estilo>/`.

2. Analizar el borrador que se quiere reescribir:

```powershell
python skills/editor-en-jefe/scripts/ejecutar.py humanizar-redaccion-academica/scripts/comparar_con_perfil_estilo.py "borrador.md" --profile perfil.json --out diagnostico.md --json-out diagnostico.json
```

3. Reescribir por bloques, no todo de una vez. Mantener encabezados y contenido protegido.
4. Volver a ejecutar el comparador sobre la version editada.

## Que Debe Imitarse

- variacion de longitud de oraciones;
- modo de empezar parrafos;
- conectores preferidos y relaciones logicas;
- presencia de matizadores;
- alternancia entre abstraccion y ejemplo;
- ritmo de cierres;
- densidad conceptual;
- nivel de formalidad.

## Que No Debe Imitarse

- frases completas del documento modelo;
- citas textuales;
- errores de estilo, ortografia o puntuacion;
- muletillas sobreusadas;
- marcas institucionales que no correspondan al nuevo texto;
- experiencias, datos o ejemplos ajenos.

## Criterio Frente A Reportes De IA

Los reportes externos deben orientar la revision, no dictarla. Si un texto sigue marcando alto porcentaje, priorizar introducciones y conclusiones simetricas, parrafos que empiezan igual, conectores genericos repetidos, falta de detalles concretos, frases intercambiables y uniformidad extrema de longitud. No reescribir bibliografia, citas, DOI, URLs, tablas, glosarios tecnicos correctos ni nombres propios para reducir un porcentaje.
