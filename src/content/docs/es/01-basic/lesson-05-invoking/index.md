---
title: "Lección 05: Invocar skills"
---

Hay tres formas de invocar un skill. Cada una se adapta a una situación distinta.

## Los tres modos de invocación

| Modo | Cómo se dispara | Mejor para |
|------|---------------|----------|
| Auto-invocación | Escribe con naturalidad; Claude empareja palabras clave de la description | Uso interactivo cotidiano |
| Invocación directa | Escribe `/skill-name` en el prompt de Claude Code | Cuando sabes exactamente qué skill quieres |
| Modo headless | Ejecuta `claude -p "/skill-name"` en una terminal | Scripts, CI/CD, automatización |

## 1. Auto-invocación

Claude lee la description de cada skill instalado al iniciar. Cuando escribes una tarea, Claude compara tus palabras con esas descriptions y activa automáticamente el skill que mejor coincide.

Para que esto funcione de forma fiable, la description del skill necesita palabras clave de activación que coincidan con cómo formulas la tarea de forma natural:

```yaml
description: Generate a conventional commit message for the staged changes.
             Use when the user wants to commit, asks for a commit message,
             or asks what to write for a commit.
```

Con esta description, cualquiera de estos mensajes del usuario probablemente activaría el skill:

- "What should I write for my commit?"
- "Generate a commit message"
- "I want to commit these changes"

La auto-invocación es el modo más ergonómico para sesiones interactivas. No tienes que recordar nombres de skills.

## 2. Invocación directa

Escribe `/skill-name` para activar un skill inmediatamente, independientemente de si tu mensaje coincide con la description.

```
/commit-message
/code-review-checklist
/adr-writer
```

La invocación directa es útil cuando:

- Quieres un skill específico pero no formulaste la tarea de una manera que lo activaría automáticamente
- Varios skills podrían coincidir y quieres uno específico
- Estás probando un skill nuevo y quieres asegurarte de que se activa

## 3. Modo headless con `claude -p`

`claude -p` ejecuta Claude Code de forma no interactiva: un prompt entra, una respuesta sale, luego termina. Esto hace que los skills sean scriptables.

### Uso básico

```bash
# Invoke a skill from the command line
claude -p "/summarize-changes"

# Invoke a skill with an argument
claude -p "/fix-issue 123"
```

### Canalizar entrada

```bash
# Pipe code to a skill
cat src/utils.ts | claude -p "/code-review-checklist"

# Pipe an error log for analysis
cat error.log | claude -p "analyze this error and suggest a fix"

# Pipe git diff to get a commit message
git diff --staged | claude -p "/commit-message"
```

### Capturar la salida

```bash
# Save the output to a file
claude -p "/summarize-changes" > summary.txt

# Use the output in a script
COMMIT_MSG=$(claude -p "/commit-message")
git commit -m "$COMMIT_MSG"

# Run in CI to generate a changelog entry
claude -p "/changelog-entry" >> CHANGELOG.md
```

### Por qué `claude -p` termina tras un único turno

`claude -p` está diseñado para automatización. Lee el prompt, produce una respuesta y termina. No hay turno de seguimiento. Esto lo hace seguro de usar en scripts — el proceso siempre termina y el exit code refleja éxito o fallo.

Como no hay turno de seguimiento, los skills usados en modo headless deben producir una salida completa y autocontenida. Un skill que pregunta para aclarar es inutilizable en modo headless. Cuando escribas skills pensados tanto para uso interactivo como headless, haz que la salida sea completa sin interacción, y usa un comportamiento por defecto cuando el contexto sea ambiguo.

## El ejemplo de esta lección

`examples/summarize-changes/SKILL.md` demuestra la inyección dinámica de context — una característica de Claude Code en la que una línea del cuerpo del skill ejecuta un comando e inyecta su salida antes de que Claude lea el skill.

La línea:

```
!`git diff HEAD`
```

ejecuta `git diff HEAD` en el momento de activación del skill y reemplaza la línea con la salida real del diff. Claude lee el diff como parte del cuerpo del skill, no como una llamada a tool separada. Esto es útil para proporcionar context que el skill siempre necesita.

## Siguientes pasos

A estas alturas has cubierto los cinco conceptos básicos:

1. Cómo se ve un SKILL.md (anatomía)
2. Dónde instalar skills (scopes)
3. Cómo convertir prompts repetitivos en skills
4. Cómo codificar formato de documentación como un skill
5. Cómo invocar skills de forma interactiva y headless

Los ejercicios en `../exercises/` te ofrecen dos tareas prácticas para reforzar estos conceptos. Después, la sección `02-intermediate/` cubre el manejo de arguments, aislamiento de context y patrones de skills más avanzados.
