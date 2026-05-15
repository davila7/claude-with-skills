---
title: "Avanzado: Divulgación progresiva, scripts incluidos y orchestration de subagents"
---

Esta sección es para quienes ya hayan completado las secciones Básica e Intermedia. Ya conoces todos los campos de frontmatter. Esta sección trata sobre arquitectura: cómo estructurar skills que escalen, cómo empaquetar scripts reutilizables y cómo coordinar trabajo entre subagents aislados.

## Requisitos previos

Has completado la sección Intermedia o sabes escribir un SKILL.md con control completo del frontmatter, incluyendo `context: fork`, `agent`, `allowed-tools` y `user-invocable`. Te sientes cómodo con Python 3 y scripting básico de shell.

## Lo que aprenderás

| Lección | Tema |
|--------|-------|
| 01 — Divulgación progresiva | SKILL.md como navegador: mantén bajo el coste de contexto a medida que crece la complejidad del skill |
| 02 — Scripts incluidos | Empaqueta e invoca scripts desde dentro de los skills usando `${CLAUDE_SKILL_DIR}` |
| 03 — Skills que llaman a subagents | Usa `context: fork` y el campo `agent` para lanzar subagents aislados |
| 04 — Subagents que precargan skills | El campo `skills:` en las definiciones de subagent para conocimiento de dominio pre-inyectado |
| 05 — Skills orquestando skills | Un skill instruyendo a Claude para invocar otros skills en secuencia |
| 06 — Dominio de la ventana de contexto | Discovery budget, ciclo de vida del cuerpo, auto-compactación y mandos de ajuste |
| 07 — Hooks en skills | Hooks `PreToolUse` y `PostToolUse` definidos en el frontmatter del skill |
| 08 — Plugins y distribución | Empaquetar skills como un plugin con `plugin.json` para distribución en equipo |
| Capstone | Un bot de calidad de código multi-skill respaldado por subagents construido desde cero |

## Resultados de aprendizaje

Al finalizar esta sección serás capaz de:

1. Estructurar skills para divulgación progresiva de manera que el coste de contexto se mantenga bajo a escala — el patrón de navegador mantiene el SKILL.md por debajo de 80 líneas mientras hace que cientos de líneas de material de referencia estén disponibles bajo demanda.
2. Empaquetar e invocar scripts desde dentro de los skills usando `${CLAUDE_SKILL_DIR}`, la variable que siempre resuelve al directorio que contiene `SKILL.md` independientemente de la ubicación de instalación.
3. Lanzar subagents aislados desde un skill usando `context: fork` — entiende cuándo el contexto forked ayuda, cuándo perjudica y qué puede y qué no puede ver un subagent.
4. Precargar skills en el contexto de inicio de un subagent usando el campo `skills:` en un archivo de definición de subagent, para que el subagent lleve conocimiento de dominio desde el momento en que arranca.
5. Encadenar skills en un skill de orchestration — entiende qué patrones requieren la conversación principal y cuáles pueden delegarse a workers.
6. Gestionar el presupuesto de la ventana de contexto entre muchos skills activos — conoce las tres etapas de carga de contexto, el discovery budget y cómo ajustarlo mediante settings.
7. Añadir hooks de ciclo de vida a los skills para automatización — ejecuta comandos shell `PreToolUse` y `PostToolUse` fuera del turno de Claude.
8. Empaquetar skills en un plugin para distribución en equipo — el layout del directorio del plugin, el manifest `plugin.json` y las restricciones de seguridad.
9. Construir un sistema completo multi-skill respaldado por subagents desde cero en el proyecto capstone.

## Restricción clave a tener en cuenta

Los subagents no pueden lanzar otros subagents. Si un skill usa `context: fork`, el subagent forked no puede a su vez usar `context: fork` para lanzar más subagents. Todos los flujos de delegación deben pasar por la conversación principal. El orchestrator vive en la sesión principal; los workers viven en los subagents forked.

## Cómo usar esta sección

Cada directorio de lección contiene un `index.md` que explica el concepto y uno o más skills de ejemplo completos y funcionales. Los ejemplos están diseñados para ser instalados y probados, no solo leídos.

```bash
cp -r lesson-01-progressive-disclosure-in-practice/examples/pdf-toolkit ~/.claude/skills/
```

Las lecciones están ordenadas por dependencia conceptual: la lección 01 (disclosure) informa la lección 02 (scripts), las cuales alimentan las lecciones 03 y 04 (subagents).

## Lecciones

- [Lección 01: Divulgación progresiva en la práctica](lesson-01-progressive-disclosure-in-practice/)
- [Lección 02: Scripts incluidos con ${CLAUDE_SKILL_DIR}](lesson-02-supporting-scripts/)
- [Lección 03: Skills que llaman a subagents](lesson-03-skill-calls-subagent/)
- [Lección 04: Subagents que precargan skills](lesson-04-subagent-uses-skills/)
- [Lección 05: Skills orquestando skills](lesson-05-skills-orchestrating-skills/)
- [Lección 06: Dominio de la ventana de contexto](lesson-06-context-window-mastery/)
- [Lección 07: Hooks en skills](lesson-07-hooks-in-skills/)
- [Lección 08: Plugins y distribución](lesson-08-plugins-and-distribution/)
- [Capstone: Bot de calidad de código](capstone/)
