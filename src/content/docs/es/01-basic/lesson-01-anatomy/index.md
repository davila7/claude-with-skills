---
title: "Lección 01: La anatomía de un SKILL.md"
---

Un archivo `SKILL.md` tiene tres partes diferenciadas. Entender cada una es la base para escribir skills que funcionen de forma fiable.

## Parte 1: frontmatter YAML

El frontmatter se sitúa entre los delimitadores `---` al inicio del archivo. Es la única sección obligatoria que sigue un formato estricto. El agente lee el frontmatter al iniciar — antes de que llegue una tarea — para decidir si el skill es relevante.

```
---
name: my-skill
description: Does X. Use when the user asks about Y or Z.
---
```

El bloque de frontmatter se cierra con otra línea `---`. Todo lo que sigue a ese delimitador de cierre forma parte del cuerpo.

### El campo name

- Solo letras minúsculas, dígitos y guiones. Sin espacios, sin guiones bajos y sin mayúsculas.
- Máximo 64 caracteres.
- Debe coincidir con el nombre del directorio que contiene el archivo `SKILL.md`. Si tu directorio es `git-commit-helper/`, el campo name debe ser `git-commit-helper`.
- Debe ser único dentro de un directorio de skills (scope personal, scope de proyecto, etc.).

Ejemplos válidos: `commit-message`, `code-review-checklist`, `adr-writer`

Ejemplos inválidos: `Commit_Message`, `my skill`, `generate-a-conventional-commit-message-for-the-staged-changes`

### El campo description

- Texto plano. Máximo 1024 caracteres.
- Escríbelo para el modelo, no para humanos. El agente escanea las descripciones para decidir si activar un skill sin que se le pida explícitamente.
- Las descripciones más efectivas contienen dos cosas: **qué hace el skill** y **cuándo usarlo**. Incluye palabras clave que un usuario podría escribir de forma natural.

Buena descripción: `Generate a conventional commit message for the staged git changes. Use when the user wants to commit, asks for a commit message, or asks what to write for a commit.`

Descripción débil: `Helps with commits.`

La versión débil no tiene palabras clave de activación. Un usuario que escriba "what should my commit message say?" probablemente no la activará de forma fiable.

### Campos opcionales del frontmatter

Claude Code admite campos adicionales más allá del estándar de AgentSkills. Los más útiles a nivel básico:

- `allowed-tools`: una lista de tools que el skill puede usar. Restringir tools limita efectos secundarios accidentales y expone lo que el skill realmente necesita. Ejemplo: `allowed-tools: Bash(git diff *) Bash(git status *)`.

Una referencia completa está en `reference/frontmatter-cheatsheet.md` en la raíz de este repository.

## Parte 2: el cuerpo

Todo lo que viene después del `---` de cierre del frontmatter es el cuerpo. Es Markdown, y es donde escribes el procedimiento que seguirá el agente.

El cuerpo solo se carga cuando el skill se activa. Al iniciar, el agente paga aproximadamente 100 tokens por cada skill instalado (solo name + description). El cuerpo completo se carga bajo demanda, por lo que un procedimiento de 200 líneas no cuesta nada en sesiones donde el skill no se necesita.

Reglas prácticas para el contenido del cuerpo:

- Escribe los pasos en forma imperativa: "Run git diff --staged" en lugar de "You should run git diff --staged".
- Sé explícito sobre el formato de salida. Si quieres una lista con viñetas, dilo. Si quieres solo el commit message sin explicación adicional, dilo también.
- Mantén el cuerpo por debajo de 500 líneas. Los skills largos cargan despacio y son más difíciles de mantener.
- Usa encabezados para organizar procedimientos de varias fases (recopilar contexto, analizar, producir salida).

## Parte 3: archivos de soporte

Un directorio de skill puede contener archivos distintos a `SKILL.md`. Estos no se cargan automáticamente. El agente los lee solo cuando el cuerpo se lo indica explícitamente.

Una disposición típica podría verse así:

```
my-skill/
  SKILL.md
  references/
    style-guide.md
    error-codes.txt
  scripts/
    validate.sh
```

Si el cuerpo dice "Read references/style-guide.md before writing", el agente carga ese archivo bajo demanda. Esto mantiene bajo el coste de inicio mientras sigue ofreciendo material de referencia rico disponible.

## Estructura mínima válida

```
---
name: hello-skill
description: Does one specific thing. Use when the user asks for that thing or mentions these keywords.
---

## Instructions

1. Step one.
2. Step two.
3. Output the result.
```

Eso es un skill completo y desplegable. El ejemplo en `examples/hello-skill/` demuestra esta estructura mínima.

## Siguiente lección

[Lección 02: Dónde viven los skills](../lesson-02-where-skills-live/)
