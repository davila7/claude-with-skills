---
title: "Lección 03: Skills que llaman a subagents"
---

Algunas tareas se aíslan mejor de tu conversación principal. Cuando un skill necesita leer docenas de archivos, escanear logs grandes o explorar un codebase en profundidad, ese trabajo abarrotaría tu contexto de trabajo con salida que puede ser irrelevante para lo que hagas después. `context: fork` resuelve esto ejecutando el skill en un subagent separado cuyo contexto está aislado del tuyo.

## Cómo funciona context: fork

Cuando invocas un skill que tiene `context: fork` en su frontmatter, Claude Code no ejecuta el skill de forma inline. En su lugar:

1. Crea un nuevo subagent con un contexto fresco (sin historial de conversación)
2. Envía el cuerpo renderizado del SKILL.md como prompt de tarea del subagent
3. Ejecuta el subagent hasta completarse
4. Devuelve un resumen del resultado a tu conversación principal

El contexto de trabajo completo del subagent — todos los archivos que lee, toda la salida de shell que ve — nunca entra en tu contexto principal. Recibes un resumen, no la salida cruda.

## El campo agent

El campo `agent` selecciona qué tipo de subagent ejecuta el skill:

| Agent | Tools disponibles | Model | Usar para |
|-------|----------------|-------|---------|
| `Explore` | Read, Grep, Glob, Bash (solo lectura) | Haiku | Investigación, exploración de codebase, análisis |
| `Plan` | Tools de solo lectura | Model de sesión | Comprobaciones previas, tareas de planificación |
| `general-purpose` | Todas las tools | Model de sesión | Tareas que necesitan escribir o ejecutar |
| Nombre personalizado | Definido en `.claude/agents/` | Según configuración | Workflows específicos del equipo |

Si se omite `agent` cuando `context: fork` está activo, se usa `general-purpose`.

## Qué puede y qué no puede ver el subagent

El subagent comienza con un contexto fresco. No ve:

- Tu historial de conversación
- Archivos que has leído en la sesión actual
- Salidas previas de skills
- Cualquier contexto de la conversación principal

Sí ve:

- El cuerpo renderizado del SKILL.md (con `$ARGUMENTS` sustituido)
- `CLAUDE.md` del proyecto y de los directorios de usuario (el mismo context de fondo que siempre cargaría)
- El sistema de archivos — puede leer cualquier archivo al que tengas acceso

**Implicación:** Escribe el cuerpo del SKILL.md como una tarea autocontenida. No asumas que el subagent sabe algo de lo que tú sabes. Si la tarea requiere una ruta de archivo específica, argumento o hecho de fondo, debe aparecer en el cuerpo o en `$ARGUMENTS`.

## El campo agent sin context: fork

Si estableces `agent` pero no `context: fork`, el campo `agent` se ignora. El skill se ejecuta de forma inline en tu conversación principal como de costumbre.

## La restricción clave: los subagents no pueden lanzar subagents

Un skill ejecutándose bajo `context: fork` no puede a su vez usar `context: fork` para lanzar más subagents. La delegación es de un solo nivel de profundidad. Toda la orchestration debe ocurrir en la conversación principal.

Esto significa: si quieres paralelizar trabajo entre múltiples subagents, el orchestrator debe ser un skill inline (sin `context: fork`) que instruya a la sesión principal de Claude a lanzar múltiples subagents. Consulta el ejemplo `parallel-investigator` abajo.

## Contraste: inline vs forked

| Comportamiento | Sin context: fork | context: fork |
|----------|-----------------|---------------|
| Ve el historial de conversación | Sí | No |
| Comparte contexto con el principal | Sí | No |
| La salida permanece en el contexto principal | Sí | Solo resumen |
| Puede lanzar más subagents | A través de la sesión principal | No |
| Bueno para | Tareas que necesitan historial | Tareas de investigación grandes |

## Ejemplos en esta lección

### deep-research

`examples/deep-research/SKILL.md` usa `context: fork` con `agent: Explore`. Invócalo con un tema o pregunta y produce un informe estructurado sobre cómo funciona ese sistema en el codebase. La salida de la investigación (potencialmente cientos de líneas de contenidos de archivos y resultados de grep) permanece en el subagent y nunca se carga en tu sesión principal.

```
/deep-research authentication middleware
```

### parallel-investigator

`examples/parallel-investigator/SKILL.md` NO usa `context: fork`. En su lugar, se ejecuta inline e instruye a la sesión principal de Claude a lanzar dos subagents Explore separados en paralelo. Este patrón permite al skill orquestar múltiples workers respetando la restricción de que los subagents forked no pueden a su vez forkear más.

Usa este patrón cuando necesites dos o más hilos de investigación y quieras los resultados combinados en un único informe comparativo.

## Siguiente lección

[Lección 04: Subagents que precargan skills](../lesson-04-subagent-uses-skills/)
