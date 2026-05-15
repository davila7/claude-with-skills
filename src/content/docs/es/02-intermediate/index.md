---
title: "Intermedio: frontmatter, argumentos y contexto dinámico"
---

Esta sección enseña la referencia completa del frontmatter de los skills de Claude Code y cómo combinar campos para construir skills fiables y con calidad de producción. Al final podrás escribir skills que controlen su propia invocación, preaprueben tooling, inyecten contexto en vivo, se restrinjan a paths relevantes y sobrescriban el model y el nivel de effort para la tarea en cuestión.

## Prerrequisitos

Has completado la sección Básica, o ya sabes escribir un `SKILL.md` funcional con `name`, `description` y un cuerpo que hace algo útil.

## Lo que aprenderás

| Lección | Tema |
|--------|-------|
| 01 — Referencia de frontmatter | Cada campo, su tipo, valor por defecto y cuándo usarlo |
| 02 — Control de invocación | La matriz de `disable-model-invocation` y `user-invocable` |
| 03 — Allowed tools | Preaprobar tooling para que Claude no pida permiso durante la ejecución del skill |
| 04 — Argumentos | Args posicionales, args nombrados, `argument-hint` y comillas estilo shell |
| 05 — Contexto dinámico | La sintaxis `` !`command` `` para inyectar salida de shell en vivo |
| 06 — Paths y shell | Autoactivación por path de archivo y elección de un shell para los comandos de inyección |
| 07 — Model y effort | Sobrescribir model y effort de razonamiento por skill |
| 08 — Combinando opciones | Un marco de decisión y ejemplos completos del mundo real |

## Cómo usar esta sección

Cada ejemplo es un skill completo y ejecutable. Copia cualquier directorio de ejemplo a `~/.claude/skills/` o al `.claude/skills/` de tu proyecto e invócalo de inmediato.

```bash
cp -r lesson-02-invocation-control/examples/manual-only-deploy ~/.claude/skills/
```

Luego abre Claude Code y escribe `/manual-only-deploy`.

Las lecciones se construyen unas sobre otras, pero cada una hace referencia solo a los campos específicos que introduce, así que puedes leerlas de forma independiente. Si ya entiendes el control de invocación, salta a la lección 03.

## Ejercicios

El directorio `exercises/` al final de esta sección contiene tres retos prácticos con soluciones desarrolladas. Intenta el ejercicio antes de leer la solución.
