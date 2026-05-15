---
title: "Capstone: Bot de calidad de código"
---

Este capstone construye un sistema multi-skill respaldado por subagents que ejecuta comprobaciones de calidad de código sobre el PR actual y publica los hallazgos como un comentario en el PR de GitHub. Aplica cada técnica de la sección Avanzada:

- Skills orquestando otros skills (lección 05)
- Diseño de skills eficiente en contexto (lección 06)
- Subagents haciendo investigación aislada (lecciones intermedias, aplicadas aquí a escala)
- Un subagent construido a propósito para formateo y publicación de salida (lección intermedia 04)

---

## Lo que vas a construir

Una puerta de calidad de código compuesta por cinco componentes:

| Componente | Tipo | Lo que hace |
|---|---|---|
| `code-quality-gate` | Skill orchestrator | Invoca los tres skills de escaneo en secuencia, luego pide a `@quality-reporter` que publique los hallazgos combinados |
| `security-scan` | Skill de investigación | Busca secretos hardcodeados, vectores de inyección, XSS, defaults inseguros |
| `complexity-check` | Skill de investigación | Encuentra archivos grandes, funciones largas, anidamiento profundo, números mágicos |
| `test-coverage-check` | Skill de investigación | Comprueba si los archivos fuente cambiados tienen archivos de test correspondientes |
| `quality-reporter` | Subagent | Formatea los hallazgos combinados en un comentario de PR de GitHub y lo publica |

---

## Arquitectura

```
El usuario invoca /code-quality-gate
  |
  +-- Claude ejecuta /security-scan
  |     (subagent Explore en contexto forked, solo lectura)
  |     devuelve: SECURITY FINDINGS: ...
  |
  +-- Claude ejecuta /complexity-check
  |     (subagent Explore en contexto forked, solo lectura)
  |     devuelve: COMPLEXITY FINDINGS: ...
  |
  +-- Claude ejecuta /test-coverage-check
  |     (subagent Explore en contexto forked, solo lectura)
  |     devuelve: COVERAGE FINDINGS: ...
  |
  +-- Claude invoca @quality-reporter con todos los hallazgos
        (model haiku, contexto mínimo, una sola tarea)
        publica: gh pr comment
        devuelve: URL del comentario de PR
```

Cada skill de escaneo se ejecuta en un contexto forked para que su exploración no infle la conversación principal. El subagent `quality-reporter` es un especialista limitado — recibe los hallazgos como su prompt y tiene exactamente una tool: `gh pr comment`.

---

## Lo que vas a construir

Completa el proyecto creando estos cinco archivos:

1. `.claude/skills/code-quality-gate/SKILL.md` — orchestrator
2. `.claude/skills/security-scan/SKILL.md`
3. `.claude/skills/complexity-check/SKILL.md`
4. `.claude/skills/test-coverage-check/SKILL.md`
5. `.claude/agents/quality-reporter.md`

Lee `spec.md` para los criterios de aceptación de cada componente.

Una implementación de referencia completa está en `solution/`. Intenta construir tu propia versión antes de leer la solución — la especificación en `spec.md` te da suficiente detalle para construir el sistema completo sin mirar la solución.

---

## Requisitos previos

- Claude Code instalado y funcionando
- Un repository de git con al menos un commit y un pull request abierto (o una rama desde la que puedas abrir un PR)
- `gh` CLI instalado y autenticado (`gh auth status`)

---

## Validación

Tras instalar los skills y el agent:

1. Abre Claude Code en un repository con un PR abierto.
2. Ejecuta `/code-quality-gate`.
3. Verifica que:
   - Los tres skills de escaneo se ejecutan y cada uno produce una sección de hallazgos.
   - `@quality-reporter` se invoca con los hallazgos combinados.
   - Se publica un comentario de PR (comprueba el PR en GitHub).
   - La URL del comentario se imprime en la sesión de Claude Code.

Si no hay PR abierto, el orchestrator debe recurrir a imprimir el informe en la terminal.

---

## Retos de extensión

Tras completar el capstone base:

1. **Añade un skill `lint-check`** — ejecuta ESLint o flake8 sobre los archivos cambiados y añade la salida como una cuarta sección en el informe de calidad.
2. **Puerta por severidad** — modifica `code-quality-gate` para detenerse y pedir confirmación antes de publicar si se encuentran hallazgos CRITICAL.
3. **Empaqueta como plugin** — crea un `plugin.json` y convierte los cinco componentes en un plugin distribuible siguiendo la lección 08.
4. **Añade un hook `PostToolUse`** — añade un hook a `code-quality-gate` que registre la ejecución en un archivo en `~/.claude/quality-gate-runs.log` con el timestamp y el número de PR.
