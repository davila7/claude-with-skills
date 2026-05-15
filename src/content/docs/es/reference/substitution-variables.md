---
title: "Variables de sustitución de strings"
---

Claude Code reemplaza los tokens de sustitución en los cuerpos de SKILL.md antes de pasar el contenido al modelo. Esta referencia cubre cada sustitución disponible con ejemplos prácticos.

---

## $ARGUMENTS

Contiene el string completo de argumentos exactamente como el usuario lo escribió tras el nombre del skill. Sin parseo, sin separación, sin procesamiento — es el resto crudo de la línea de invocación.

**Ejemplos:**

`/fix-issue 123`
- `$ARGUMENTS` = `"123"`

`/migrate-component SearchBar React Vue`
- `$ARGUMENTS` = `"SearchBar React Vue"`

`/deploy staging --dry-run`
- `$ARGUMENTS` = `"staging --dry-run"`

**Importante:** Si el cuerpo del skill no contiene `$ARGUMENTS` en ningún sitio, Claude Code añade automáticamente `ARGUMENTS: <value>` al final del contenido del skill cuando el usuario proporciona argumentos. Esto significa que no tienes que usar `$ARGUMENTS` explícitamente si solo quieres que Claude vea el valor — pero usarlo explícitamente te permite controlar la ubicación y la redacción.

---

## $ARGUMENTS[N] y $N

Acceso por índice a los argumentos separados por espacios. Se respeta el quoting de shell: los strings entre comillas con espacios cuentan como un único argumento.

Indexación basada en cero.

**Ejemplos:**

`/migrate-component "my widget" React Vue`
- `$ARGUMENTS[0]` = `"my widget"` (las comillas preservaron el espacio)
- `$ARGUMENTS[1]` = `"React"`
- `$ARGUMENTS[2]` = `"Vue"`
- `$0` = `"my widget"` (forma corta de `$ARGUMENTS[0]`)
- `$1` = `"React"`
- `$2` = `"Vue"`

**Fuera de rango:** Un índice que excede el número de argumentos proporcionados se expande a un string vacío. El skill debe manejar esto con elegancia, típicamente documentando los argumentos requeridos en el cuerpo.

---

## $name (argumentos con nombre)

Los argumentos con nombre requieren el campo de frontmatter `arguments` que lista los nombres de los argumentos en orden. Claude Code luego mapea los argumentos posicionales a esos nombres.

**Frontmatter:**

```yaml
arguments:
  - component
  - source_framework
  - target_framework
```

**Invocación:**

`/migrate-component SearchBar React Vue`

**Expansiones:**
- `$component` = `"SearchBar"`
- `$source_framework` = `"React"`
- `$target_framework` = `"Vue"`

Los argumentos con nombre son más legibles que el acceso por índice cuando un skill tiene más de uno o dos argumentos. Los nombres aparecen en el cuerpo del skill exactamente como se listan en el campo `arguments`, prefijados con `$`.

---

## ${CLAUDE_SESSION_ID}

Un UUID que identifica la sesión actual de Claude Code. Es estable durante toda la sesión y cambia cada vez que Claude Code inicia una nueva sesión (cada invocación de `claude` o nueva ventana de sesión).

**Casos de uso:**
- Nombrar archivos de log para que la salida de cada sesión vaya a su propio archivo
- Crear directorios temporales con scope a una sesión que puedan limpiarse después
- Correlacionar archivos de salida, resultados cacheados o artefactos intermedios entre múltiples invocaciones de skills en la misma sesión

**Ejemplo de uso en el cuerpo del skill:**

```
Log all output to /tmp/claude-${CLAUDE_SESSION_ID}/analysis.log for later review.
```

---

## ${CLAUDE_EFFORT}

El nivel de effort actual como string. Valores posibles: `low`, `medium`, `high`, `xhigh`, `max`.

El valor refleja la configuración de effort activa para la sesión, a menos que el frontmatter del skill lo sobrescriba con el campo `effort` — en cuyo caso `${CLAUDE_EFFORT}` refleja el valor sobrescrito.

**Caso de uso:** Adaptar el comportamiento del skill según el effort. En effort alto, producir razonamiento detallado y salida extensa. En effort bajo, producir resúmenes concisos.

**Ejemplo de uso en el cuerpo del skill:**

```
Current effort level: ${CLAUDE_EFFORT}

If effort is low or medium: produce a one-paragraph summary.
If effort is high, xhigh, or max: produce a full structured report with section headers, findings, and recommendations.
```

---

## ${CLAUDE_SKILL_DIR}

La ruta absoluta al directorio que contiene el archivo SKILL.md. Es estable independientemente de dónde esté instalado el skill (scope personal, scope de proyecto o un plugin).

**Valores de ejemplo por scope:**
- Personal: `/Users/you/.claude/skills/my-skill`
- Proyecto: `/Users/you/myproject/.claude/skills/my-skill`
- Plugin: `/Users/you/.claude/plugins/my-plugin/skills/my-skill`

**Regla crítica:** Usa siempre `${CLAUDE_SKILL_DIR}` al referenciar scripts incluidos, plantillas, archivos de configuración o cualquier otro recurso que viaje junto al SKILL.md. Nunca hardcodees una ruta absoluta — se romperá cuando el skill se instale en una ubicación diferente o por un usuario diferente.

**Ejemplo de uso en el cuerpo del skill:**

```
Run the analysis script:
Bash: python3 ${CLAUDE_SKILL_DIR}/scripts/analyze.py --input $0
```

---

## Ejemplo completo: skill session-report

Este skill de ejemplo usa los cinco tipos de sustitución juntos. Acepta argumentos con nombre para el formato del informe y la audiencia, escribe en un archivo con scope a la sesión, ajusta la verbosidad según el effort y delega en un script incluido.

**Estructura del directorio:**

```
session-report/
  SKILL.md
  scripts/
    collect_session_data.py
```

**SKILL.md:**

```markdown
---
name: session-report
description: Generate a session activity report summarizing what was done in this session. Use when the user asks for a session summary, activity log, or session report.
arguments:
  - format
  - audience
argument-hint: <format> <audience>
---

Generate a session activity report.

Format: $format
Audience: $audience
Full arguments string: $ARGUMENTS

Session ID: ${CLAUDE_SESSION_ID}
Effort level: ${CLAUDE_EFFORT}

Steps:

1. Run the data collection script and capture its output:
   Bash: python3 ${CLAUDE_SKILL_DIR}/scripts/collect_session_data.py --session ${CLAUDE_SESSION_ID}

2. Write the raw output to a session log file:
   Bash: mkdir -p /tmp/claude-sessions && python3 ${CLAUDE_SKILL_DIR}/scripts/collect_session_data.py --session ${CLAUDE_SESSION_ID} > /tmp/claude-sessions/${CLAUDE_SESSION_ID}.log

3. Produce the report in the requested $format for the $audience audience.

Verbosity rules based on effort level ${CLAUDE_EFFORT}:
- low: one paragraph, top three findings only
- medium: structured list, five to ten items
- high or above: full report with sections, timeline, and recommendations

Output only the report content. No preamble.
```

**Invocación:**

`/session-report markdown engineering-team`

**A qué se resuelve cada sustitución:**
- `$format` = `"markdown"`
- `$audience` = `"engineering-team"`
- `$ARGUMENTS` = `"markdown engineering-team"`
- `${CLAUDE_SESSION_ID}` = `"a3f2c1d8-..."` (UUID real de la sesión)
- `${CLAUDE_EFFORT}` = `"medium"` (o el effort actual de la sesión)
- `${CLAUDE_SKILL_DIR}` = ruta absoluta al directorio `session-report/`
