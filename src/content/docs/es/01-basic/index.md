---
title: "Básico: Entender y escribir skills"
---

Esta sección enseña los fundamentos de los skills de Claude Code. Al final sabrás cómo se ve un skill, dónde colocarlo, por qué existen los skills y cómo invocarlos tanto de forma interactiva como desde scripts.

## Lo que aprenderás

| Lección | Tema |
|--------|-------|
| 01 — Anatomía | Las tres partes de un archivo SKILL.md: frontmatter, cuerpo, archivos de soporte |
| 02 — Dónde viven los skills | Los cuatro scopes, cómo funciona el orden de prevalencia y el comportamiento de recarga en vivo |
| 03 — Tareas repetitivas | Convertir un prompt pegado en un skill reutilizable |
| 04 — Skills de documentación | Codificar el formato de salida junto con el conocimiento para obtener resultados consistentes |
| 05 — Invocar skills | Auto-invocación, invocación directa con `/skill-name` y modo headless con `claude -p` |

## Requisitos previos

- Claude Code instalado y disponible en tu terminal (`claude --version` debería imprimir un número de versión)
- Una terminal y un editor de texto
- Familiaridad básica con YAML (no necesitas ser experto — el frontmatter son simples pares clave-valor)

## Cómo usar esta sección

Cada ejemplo de esta sección es un skill completo y funcional. Puedes copiar cualquier directorio de ejemplo directamente a `~/.claude/skills/` e invocarlo de inmediato.

```
cp -r lesson-01-anatomy/examples/hello-skill ~/.claude/skills/
```

Luego abre Claude Code en cualquier proyecto y escribe `/hello-skill`.

Las lecciones están diseñadas para leerse en orden, pero cada una se sostiene por sí misma si ya conoces los conceptos previos. Empieza por la lección 01 si los skills son nuevos para ti, o salta a la lección 05 si solo necesitas entender la invocación.
