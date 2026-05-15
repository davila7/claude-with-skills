---
title: "Referencia del modo headless"
---

Usando skills con `claude -p` para automatización, CI/CD y scripting.

---

## Qué es el modo headless

`claude -p "prompt"` ejecuta Claude Code de manera no interactiva: un prompt, una respuesta, salida. No hay conversación, ni continuidad de sesión, ni UI interactiva. Los skills se cargan y son invocables exactamente igual que en el modo interactivo, pero el context de ejecución es un proceso de una sola vez.

El modo headless es la opción adecuada para:
- Pipelines de CI/CD (descripciones de pull request, changelogs, notas de release)
- Hooks de git (generación de mensajes de commit, validación pre-commit)
- Scripts de shell que necesitan razonamiento de un modelo de lenguaje
- Automatización programada que se ejecuta sin un humano presente
- Cualquier flujo donde necesites la salida de Claude como entrada de otro comando

---

## Patrones básicos

Invoca un skill directamente:

```bash
claude -p "/summarize-changes"
```

Invoca un skill con un argumento:

```bash
claude -p "/fix-issue 123"
```

Pasa entrada a un skill por pipe — el contenido del pipe se antepone al prompt:

```bash
git diff HEAD | claude -p "/review-diff"
```

Guarda la salida en un archivo:

```bash
claude -p "/changelog-entry" > /tmp/changelog.md
```

Úsalo desde un hook de git — en `.git/hooks/prepare-commit-msg`:

```bash
#!/bin/bash
DIFF=$(git diff --staged)
echo "$DIFF" | claude -p "/commit-message" > "$1"
```

---

## Usar skills en CI

Ejemplo de GitHub Actions que genera una descripción de pull request desde un skill:

```yaml
- name: Generate PR description
  run: |
    claude -p "/pr-description" > pr-body.txt
    gh pr create \
      --body "$(cat pr-body.txt)" \
      --title "$(git log -1 --format=%s)"
```

Ejemplo con un diff pasado como entrada:

```yaml
- name: Review staged changes
  run: |
    git diff origin/main...HEAD | claude -p "/code-review" > review.txt
    cat review.txt
```

---

## Selección de modelo en modo headless

Sobrescribe el model por invocación usando `--model`:

```bash
# Fast and cheap for high-volume tasks
claude --model haiku -p "/commit-message"

# Powerful for complex analysis
claude --model opus -p "/deep-analysis"
```

Si el frontmatter del skill define `model:`, el valor del frontmatter tiene prioridad sobre el modelo por defecto de la sesión, pero es sobrescrito por una flag `--model` explícita en la línea de comandos.

---

## Modo de permisos en modo headless

Por defecto, Claude Code pedirá permisos de herramienta incluso en modo headless, lo cual hace que el proceso se bloquee. Usa `--allowedTools` para pre-aprobar herramientas específicas:

```bash
# Pre-approve git commands
claude -p "/safe-commit" --allowedTools "Bash(git *)"

# Pre-approve read-only file access
claude -p "/analyze-codebase" --allowedTools "Read Grep Glob"

# Pre-approve multiple tool categories
claude -p "/deploy" --allowedTools "Bash(git *) Bash(kubectl *) Read"
```

Para entornos totalmente automatizados donde el propio entorno es de confianza y la solicitud de permisos rompería la pipeline:

```bash
claude --dangerously-skip-permissions -p "/automated-task"
```

Usa `--dangerously-skip-permissions` solo en entornos aislados donde controles lo que hace el skill y confíes en la ruta completa de ejecución. No lo uses localmente como atajo de conveniencia general.

---

## Pasar múltiples contexts por pipe

Combina múltiples fuentes de entrada usando agrupamiento de shell:

```bash
# Error log and recent git history together
{ cat error.log; echo "---"; git log --oneline -10; } | claude -p "/diagnose-error"
```

```bash
# Two files compared
{ echo "=== BEFORE ==="; cat before.py; echo "=== AFTER ==="; cat after.py; } | claude -p "/explain-diff"
```

```bash
# Directory listing plus a specific file
{ ls -la src/; echo "---"; cat src/index.ts; } | claude -p "/suggest-refactor"
```

---

## Formato de salida

Los skills invocados de forma headless deberían producir una salida limpia que los comandos posteriores puedan consumir. Por defecto, Claude produce respuestas conversacionales con preámbulo y explicación. Para automatización, suprime esto en el cuerpo del skill.

Añade al cuerpo del skill para salida compatible con headless:

```
Output only the result. Do not include explanation, preamble, or any text other than the requested content.
```

Para salida JSON que se parseará después:

```
Output valid JSON with no markdown fencing, no explanation, and no additional text.
```

Para Markdown que se pasará a otra herramienta:

```
Output Markdown only. Do not include any explanation before or after the Markdown content.
```

Si quieres que un mismo skill funcione tanto en contextos interactivos como headless, puedes condicionar según el nivel de effort:

```
If CLAUDE_EFFORT is low: output a concise one-paragraph result.
Otherwise: output a full structured response.
```

Luego pasa `--effort low` en invocaciones headless donde quieras salida concisa.

---

## Variables de entorno para modo headless

| Variable | Propósito |
|---|---|
| `ANTHROPIC_API_KEY` | Requerida si no está definida globalmente en la configuración de Claude Code |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` | Desactiva los subagents en segundo plano; útil en entornos de CI con recursos limitados |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET` | Sobrescribe el presupuesto de descripciones de skill en caracteres; útil si muchos skills están instalados y algunos están siendo descartados |

Ejemplo combinando múltiples variables:

```bash
ANTHROPIC_API_KEY="sk-..." \
CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1 \
SLASH_COMMAND_TOOL_CHAR_BUDGET=4000 \
claude -p "/generate-report"
```

---

## Diseño de skills compatibles con headless

Los skills destinados al uso headless se benefician de estos patrones:

**Instrucciones explícitas de formato de salida.** Dile al skill exactamente qué formato producir y prohíbe el preámbulo. El comportamiento conversacional por defecto de Claude degrada las pipelines de automatización.

**Sin prompts interactivos.** El cuerpo del skill no debería hacer preguntas aclaratorias. Si falta información requerida, falla con un mensaje de error claro que vaya a stderr, no una pregunta interactiva.

**Códigos de salida.** `claude -p` termina con 0 en éxito y distinto de cero en fallo. Usa esto en scripts de shell:

```bash
if ! claude -p "/validate-config" < config.yaml; then
  echo "Config validation failed" >&2
  exit 1
fi
```

**Argumentos deterministas.** Documenta los argumentos requeridos claramente. En invocaciones headless, no hay oportunidad de corregir un argumento mal escrito de forma interactiva.

**Skills cortos para tareas de alto volumen.** Los cuerpos de skill más cortos cargan más rápido y cuestan menos tokens. Si un skill se ejecuta miles de veces al día en CI, cada token del cuerpo cuesta dinero. Mantén el cuerpo enfocado.
