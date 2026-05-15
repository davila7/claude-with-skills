---
title: "Lección 02: control de invocación"
---

Dos campos del frontmatter controlan quién puede invocar un skill y si aparece o no en el context de Claude. Acertar aquí marca la diferencia entre un skill que te protege de despliegues accidentales y uno que informa a Claude silenciosamente sin saturar el menú de slash commands.

## La matriz de invocación

| Frontmatter | Puedes invocarlo tú | Puede invocarlo Claude | Cargado en el context |
|---|---|---|---|
| (por defecto) | Sí | Sí | La description siempre en el context; el skill completo se carga al invocarlo |
| `disable-model-invocation: true` | Sí | No | La description NO está en el context; el skill completo se carga cuando TÚ lo invocas |
| `user-invocable: false` | No | Sí | La description siempre en el context; el skill completo se carga cuando Claude lo invoca |

Lee cada fila con atención. El comportamiento de la columna "Cargado en el context" es la parte más contraintuitiva.

Cuando `disable-model-invocation: true` está activado, Claude no ve la description del skill en absoluto al inicio. Esto significa que Claude no puede decidir invocar el skill por su cuenta — no sabe que el skill existe hasta que tú lo invocas directamente con `/skill-name`. Entonces el cuerpo completo del skill se carga para esa única invocación.

Cuando `user-invocable: false` está activado, la description del skill siempre está en el context de Claude (para que Claude pueda autoinvocarlo), pero no aparece en el menú `/`. El usuario no puede ejecutar `/skill-name` en una sesión interactiva.

## Cuándo usar `disable-model-invocation: true`

Úsalo para cualquier skill con efectos secundarios que no quieras que Claude dispare automáticamente:

- **Skills de despliegue**: no quieres que Claude decida desplegar porque dijiste "ship it" en un mensaje.
- **Skills de envío de mensajes**: un skill de Slack o de email no debería dispararse porque dijiste "notifica al equipo".
- **Operaciones destructivas**: cualquier cosa que llame a `rm`, borre una base de datos o haga push a una rama remota.
- **Operaciones de facturación**: cualquier skill que dispare acciones de pago en un servicio externo.

Regla general: si ejecutar este skill por accidente requeriría esfuerzo para deshacerlo, pon `disable-model-invocation: true`.

## Cuándo usar `user-invocable: false`

Úsalo para conocimiento de fondo que debe moldear silenciosamente el comportamiento de Claude en vez de ser una acción que el usuario ejecuta directamente:

- **Convenciones del equipo**: "Estas son nuestras convenciones de nombrado y formatos de respuesta de API REST." Claude las aplica al escribir código de API sin que el usuario necesite invocar nada.
- **Context de arquitectura**: "Este servicio es dueño del dominio de facturación y se comunica con estos tres servicios downstream." Claude usa esto al hablar de arquitectura sin que el usuario gestione un archivo de context aparte.
- **Notas de sistemas legacy**: "Este módulo está deprecado. No añadas nueva funcionalidad. Si te piden extenderlo, sugiere migrar al nuevo módulo." Claude aplica esto cada vez que toca el código legacy.

Regla general: si el skill es conocimiento más que una acción, pon `user-invocable: false`.

## El error del skill inaccesible

**Nunca pongas a la vez `disable-model-invocation: true` y `user-invocable: false` en el mismo skill.**

Con ambos activos:
- Claude no puede invocarlo (la description no está en el context)
- Tú no puedes invocarlo (no está en el menú `/`)

El skill se vuelve permanentemente inaccesible. Solo puede ejecutarse mediante `claude -p "/skill-name"` en modo headless, lo cual casi con seguridad no es lo que pretendías. Si quieres un skill exclusivo de headless, documenta esa intención explícitamente en la description.

## Ejemplos

- `examples/manual-only-deploy/` — usa `disable-model-invocation: true` para proteger un flujo de despliegue
- `examples/claude-only-context/` — usa `user-invocable: false` para proporcionar convenciones de API de fondo

## Siguiente lección

[Lección 03: allowed tools](../lesson-03-allowed-tools/)
