---
title: "Lección 03: Skills para tareas repetitivas"
---

La razón más común para crear un skill es una tarea que sigues haciendo de la misma manera. Si has pegado el mismo bloque de instrucciones en una conversación más de tres veces, ese bloque pertenece a un skill.

## El detonante "no paro de pegar esto"

Un buen candidato para un skill es cualquier tarea en la que te encuentras:

- Pegando un párrafo de instrucciones al inicio de una tarea ("When you write commit messages, always use conventional commits format, and keep the subject under 72 chars, and...")
- Copiando una sección de CLAUDE.md a una conversación porque se ha convertido en un procedimiento de varios pasos
- Explicando el mismo proceso a un miembro nuevo del equipo que usa Claude Code

Si el bloque de instrucciones es siempre el mismo, conviértelo en un skill. Si varía cada vez (porque el contexto de la tarea cambia), no es un buen candidato a skill.

## Cuándo extraer un skill de CLAUDE.md

CLAUDE.md se carga en cada sesión. Eso es correcto para hechos que aplican a todo: el stack, la arquitectura, el framework de testing. Es incorrecto para procedimientos largos que solo son relevantes de vez en cuando.

Extrae un procedimiento de CLAUDE.md a un skill cuando:

1. El procedimiento ha crecido más allá de tres o cuatro pasos
2. Solo es relevante para ocasiones específicas (release, revisión, commit)
3. Quieres hacerlo compartible con el equipo vía control de versiones sin abarrotar CLAUDE.md

## Antes y después

**Antes — pegar esto cada vez que quieres un commit message:**

> When writing a commit message, use the Conventional Commits format. The type should be one of feat, fix, docs, style, refactor, test, or chore. The scope is optional and goes in parentheses. The subject line must be in imperative mood and under 72 characters. If the change is complex, add a blank line and then bullet points explaining why, not what. Only output the commit message, nothing else.

**Después — escribe `/commit-message`.**

El skill almacena esas instrucciones una sola vez. Nunca las pegas otra vez. La salida es consistente porque las instrucciones son idénticas cada vez.

## Ejemplos en esta lección

| Skill | Qué hace |
|-------|--------------|
| `commit-message` | Genera un mensaje en formato Conventional Commits a partir de los cambios staged |
| `code-review-checklist` | Revisa código contra un checklist estructurado |
| `changelog-entry` | Redacta una entrada Keep a Changelog a partir del historial de git |
| `pr-description` | Escribe una descripción de PR con resumen, motivación y plan de pruebas |

Cada uno es un skill completo y funcional. Copia cualquiera de ellos a `~/.claude/skills/` o `.claude/skills/` para usarlo.

## Siguiente lección

[Lección 04: Skills de documentación](../lesson-04-documentation-skills/)
