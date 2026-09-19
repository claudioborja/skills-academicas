---
name: respondedor-observaciones-academicas
description: Úsalo cuando el usuario necesite responder observaciones de tutor, jurado, editor, evaluador o par revisor, convirtiendo comentarios dispersos en una matriz de cambios, plan de respuesta y ajustes concretos al manuscrito.
---

# Respondedor De Observaciones Académicas

## Automatización Previa

Si las observaciones llegan como lista, texto pegado, dictamen o comentarios dispersos, ejecutar primero `scripts/observaciones_a_matriz.py` para construir una matriz con ID, tipo, severidad, acción sugerida y estado. Luego redactar la respuesta académica con trazabilidad.

## Objetivo

Este skill transforma comentarios externos en un plan de acción claro. Organiza observaciones, las clasifica por tipo, propone respuesta y ayuda a traducirlas en cambios concretos dentro del manuscrito.

## Cuándo usarlo

- después de recibir comentarios de tutor o jurado
- tras revisión editorial o arbitraje
- cuando hay observaciones mezcladas o contradictorias
- cuando se necesita redactar carta o matriz de respuesta

## Flujo de trabajo

1. Reúne todas las observaciones.
2. Clasifícalas por prioridad y tipo.
3. Distingue cambios obligatorios, debatibles y aclaraciones.
4. Propone respuesta respetuosa y técnica.
5. Vincula cada respuesta con una acción en el manuscrito.

## Salida esperada

- matriz de observaciones
- propuesta de respuesta
- plan de cambios
- lista de puntos pendientes

## Validación final

- ninguna observación importante queda sin respuesta
- las respuestas son claras y profesionales
- cada observación tiene acción asociada o justificación
