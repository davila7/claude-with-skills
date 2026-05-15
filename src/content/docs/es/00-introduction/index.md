---
title: "Introducción: ¿Qué son los Agent Skills?"
---

Un Agent Skill es un archivo `SKILL.md` que empaqueta conocimiento procedimental para un agente de IA. En lugar de pegar el mismo bloque de instrucciones en cada conversación, escribes esas instrucciones una sola vez, las guardas en un directorio bien conocido, y el agente las carga bajo demanda cuando la tarea lo requiere.

El concepto está definido por el [estándar abierto AgentSkills.io](https://agentskills.io), lo que significa que un skill que escribas hoy funcionará en Claude Code, Cursor, GitHub Copilot, Gemini CLI y cualquier otra herramienta que adopte el estándar. Claude Code implementa el estándar completo y añade un superconjunto de campos adicionales para un control más fino sobre la invocación, el aislamiento de context y el tooling.

## La idea central

Un skill es una unidad autocontenida de conocimiento. El archivo `SKILL.md` le indica al agente qué hacer y cómo hacerlo. Cuando instalas un skill y aparece la tarea adecuada, el agente lee el archivo y sigue las instrucciones — de la misma manera en que tú leerías un runbook antes de ejecutar un procedimiento que no haces todos los días.

## Las tres secciones de un SKILL.md

**Frontmatter** — YAML entre delimitadores `---` al principio del archivo. Como mínimo, incluye un `name` y una `description`. La description es lo que el agente lee al arrancar para decidir si activa el skill. Otros campos controlan las herramientas permitidas, el modo de invocación, el manejo de argumentos y más.

**Cuerpo** — Instrucciones en Markdown después del frontmatter. Aquí es donde escribes el procedimiento: pasos, reglas de decisión, expectativas sobre el formato de salida, notas para el manejo de errores. Mantenlo por debajo de 500 líneas para que cargue rápido y se mantenga enfocado.

**Archivos de apoyo** — Cualquier archivo en subdirectorios junto al `SKILL.md` (típicamente `references/`, `scripts/`, `assets/`). Estos no se cargan automáticamente; el agente solo los lee cuando las instrucciones los referencian explícitamente. Esto mantiene bajo el coste de arranque.

## ¿Por qué Skills en lugar de CLAUDE.md?

`CLAUDE.md` se carga en cada sesión. Es la opción correcta para hechos del proyecto, convenciones de código y decisiones arquitectónicas que aplican a todo lo que el agente hace en un repo determinado. Es la opción incorrecta para procedimientos largos que solo son relevantes ocasionalmente — consumen tokens de context tanto si los necesitas como si no.

Los skills se cargan bajo demanda. El agente paga aproximadamente 100 tokens por skill al arrancar (solo el nombre y la descripción), y luego carga el cuerpo completo solo cuando llega una tarea que coincide. Si tienes 20 skills instalados y solo dos son relevantes hoy, los otros 18 cuestan casi nada.

## El estándar abierto y la portabilidad

El estándar abierto AgentSkills.io define los campos portables mínimos: `name`, `description` y `allowed-tools`. Si usas solo estos campos, tu skill funciona sin cambios en cada herramienta compatible. Claude Code añade campos extra — `disable-model-invocation`, `user-invocable`, `argument-hint`, `arguments`, `paths`, `shell`, `context`, `agent`, `hooks`, `model`, `effort` e inyección dinámica de context — pero esos campos son ignorados elegantemente por las herramientas que no los soportan.

## Continúa leyendo

- [Carga progresiva: cómo se cargan los Skills en tres etapas](progressive-disclosure.md)
- [Skills frente a alternativas: CLAUDE.md, subagents, MCP, slash commands](skills-vs-alternatives.md)
- [Configuración: requisitos previos y preparación del entorno](setup.md)
