# Suficiencia, Cobertura, Actualidad, Impacto Y Novedad

## Índice

1. Principio metodológico
2. Selección y clasificación de fuentes
3. Suficiencia de la búsqueda
4. Umbrales operativos
5. Auditoría y estados
6. Excepciones
7. Actualidad y actualización
8. Impacto, novedad y diversidad

## 1. Principio Metodológico

Evaluar la revisión por pertinencia, cobertura, reproducibilidad, complementariedad, calidad metodológica, trazabilidad, transparencia y saturación razonable. El tamaño del corpus debe ser consecuencia de la evidencia disponible, no una cuota.

No considerar válida o inválida una revisión solo por la cantidad de fuentes, registros, textos completos o estudios incluidos. No incorporar estudios irrelevantes, duplicar publicaciones, mezclar fenómenos, relajar criterios ni ampliar alcance o periodo para alcanzar una cifra.

## 2. Selección Y Clasificación De Fuentes

Exigir como arquitectura mínima de cobertura:

1. una fuente multidisciplinaria;
2. una fuente especializada en el dominio principal;
3. una segunda fuente independiente que complemente la cobertura, o una justificación explícita de su ausencia;
4. búsqueda retrospectiva y prospectiva por referencias o citaciones, o método equivalente justificado;
5. justificación de cada fuente y de toda fuente relevante no consultada.

Recomendar cuatro a cinco fuentes principales bien seleccionadas, sin convertir la cantidad en condición universal.

Clasificar cada fuente como:

- `bibliographic_database`;
- `citation_index`;
- `specialized_digital_library`;
- `publisher_platform`;
- `academic_search_engine`;
- `repository`;
- `complementary_source`.

Registrar también su función: `multidisciplinary`, `domain_specialized`, `independent_complement` o `supporting`.

No contar automáticamente como fuentes independientes plataformas editoriales cuyos contenidos ya estén ampliamente indexados. Una búsqueda directa en ScienceDirect, SpringerLink o Wiley Online Library requiere justificar qué cobertura específica agrega frente a Scopus, Web of Science u otros índices consultados.

Para informática, ingeniería de software, inteligencia artificial o ciencias de la computación, considerar:

- Scopus o Web of Science como fuente multidisciplinaria;
- IEEE Xplore para ingeniería, electrónica e informática;
- ACM Digital Library para ciencias de la computación;
- Compendex, Inspec u otra fuente especializada cuando el tema lo requiera;
- OpenAlex como complemento abierto y para relaciones de citación;
- snowballing retrospectivo y prospectivo.

En revisiones interdisciplinarias, cubrir cada disciplina implicada o justificar por qué una fuente multidisciplinaria resulta suficiente.

## 3. Suficiencia De La Búsqueda

### Artículos Semilla

Definir, cuando sea posible, entre cinco y diez artículos conocidos y claramente pertinentes. Probar si cada cadena los recupera.

Registrar:

- artículo semilla;
- disponibilidad;
- fuente en la que debería aparecer;
- recuperación y fuente;
- causa probable de ausencia;
- ajuste de la cadena;
- fecha de comprobación.

Usar 90 % de recuperación como objetivo configurable y señal de revisión, nunca como bloqueo universal. Si no existen semillas conocidas, justificarlo.

### Aporte Marginal

Calcular por fuente, después de deduplicar:

- registros brutos;
- duplicados;
- registros únicos nuevos;
- registros evaluados;
- estudios incluidos;
- estudios incluidos aportados exclusivamente;
- porcentaje exclusivo sobre el corpus incluido.

Advertir cuando una fuente aporte poco o nada nuevo. No eliminarla automáticamente si estaba prevista en el protocolo.

### Saturación

Considerar cobertura razonable cuando, en conjunto:

- las nuevas fuentes producen un aporte elegible marginal;
- una ronda completa de snowballing retrospectivo y prospectivo no incorpora nuevos estudios;
- la recuperación de semillas es satisfactoria o sus ausencias están justificadas;
- las variantes terminológicas principales están cubiertas;
- no quedan vacíos disciplinares evidentes.

No afirmar exhaustividad absoluta. Usar expresiones como “cobertura bibliográfica alcanzada”, “búsqueda amplia y reproducible” o “limitaciones de cobertura”.

## 4. Umbrales Operativos

Mantener, por defecto, estas referencias configurables:

| Señal | Valor esperado inicial |
|---|---:|
| Registros únicos | 300 |
| Textos completos evaluados | 100 |
| Estudios incluidos | 50 |
| Evidencia de los últimos cinco años | 60 % |
| Antigüedad recomendada de la búsqueda final | 90 días |

Configurar estos valores con `enforcement: advisory`. Su incumplimiento activa una auditoría metodológica, no un bloqueo.

Solo usar `enforcement: external_requirement` cuando el usuario identifique expresamente una norma institucional, editorial o contractual. Registrar la autoridad y diferenciar el incumplimiento externo de la validez metodológica Kitchenham.

## 5. Auditoría Y Estados

Ante un volumen inesperadamente bajo, revisar en este orden:

1. estrechez de las preguntas;
2. suficiencia de sinónimos;
3. errores de sintaxis;
4. campos de búsqueda;
5. pertinencia de fuentes;
6. recuperación de artículos semilla;
7. restricciones de idioma;
8. justificación temporal;
9. criterios excesivamente restrictivos;
10. evidencia realmente disponible.

Permitir como decisiones:

- mantener el protocolo y documentar un campo estrecho;
- corregir cadenas;
- añadir una fuente;
- ampliar vocabulario;
- modificar justificadamente el periodo;
- enmendar el alcance;
- registrar una excepción metodológica.

Usar estos estados:

- `PASS`: cobertura y trazabilidad suficientes;
- `PASS_WITH_WARNINGS`: revisión válida con limitaciones documentadas;
- `REQUIRES_SEARCH_AUDIT`: señales inesperadas o fallos de cobertura por revisar;
- `REQUIRES_PROTOCOL_AMENDMENT`: cambios de alcance, periodo, fuentes o criterios pendientes;
- `BLOCKED`: búsquedas no reproducibles, archivos faltantes o alterados, criterios no definidos, datos inventados o inclusión deliberada de estudios irrelevantes.

No usar `BLOCKED` únicamente por no alcanzar un valor esperado.

## 6. Excepciones

Cuando el corpus final quede por debajo de una expectativa, generar una excepción con:

- identificador;
- fecha;
- responsable;
- umbral;
- valor esperado y obtenido;
- revisiones realizadas;
- cambios aplicados;
- justificación;
- riesgo metodológico;
- impacto en conclusiones;
- decisión;
- aprobación o validación.

La excepción documenta el juicio metodológico; no es un permiso para inflar el corpus.

## 7. Actualidad Y Actualización

Tratar la proporción reciente como señal configurable. Considerar la velocidad del campo, estudios fundacionales, fecha de aparición de la tecnología, necesidad histórica y evidencia disponible.

Reportar:

- porcentaje de evidencia dentro de la ventana;
- distribución por año;
- estudios fundacionales;
- justificación del periodo;
- posible sesgo por actualidad.

No excluir un estudio pertinente solo por antigüedad.

Recomendar actualizar la búsqueda antes del envío. Tratar 90 días como referencia configurable. Si se supera:

1. advertir;
2. ejecutar una actualización cuando corresponda;
3. registrar resultados nuevos;
4. deduplicar contra el corpus;
5. evaluar solo registros nuevos;
6. actualizar tablas y flujo;
7. documentar si aparecieron inclusiones.

## 8. Impacto, Novedad Y Diversidad

Evaluar impacto mediante pertinencia, calidad, influencia académica verificada, confiabilidad del medio, adopción práctica, diversidad y carácter seminal. No usar citas o cuartil como criterio único.

Evaluar novedad frente a revisiones previas y al corpus: contradicciones, tecnologías recientes, contextos subrepresentados, falta de replicación, cambios temporales y combinaciones aún no sintetizadas.

Registrar impacto en `03_seleccion/07_impacto-novedad/03-07_matriz-impacto-novedad.csv` y brechas en `07_sintesis/07_brechas-novedad/07-07_matriz-brechas-novedad.csv`.
