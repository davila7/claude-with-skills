---
title: "Skills frente a alternativas"
---

Claude Code te ofrece varias formas de codificar conocimiento y comportamiento para el agente. Cada mecanismo tiene un modelo de carga, un scope y un propósito distintos. Entender las diferencias te ayuda a elegir la herramienta adecuada para cada situación.

## Tabla comparativa

| Mecanismo | Se carga cuando | Mejor para | Coste de context |
|---|---|---|---|
| `CLAUDE.md` | En cada sesión | Hechos del proyecto, convenciones, reglas siempre activas | Siempre se paga |
| Agent Skills (`SKILL.md`) | Bajo demanda, cuando la tarea coincide | Procedimientos y flujos invocados ocasionalmente | ~100 tokens al arrancar; cuerpo completo al activarse |
| Subagents | Lanzados explícitamente | Tareas que inundarían tu context con salida | Aislado — no toca tu ventana de context |
| Servidores MCP | Cuando las herramientas se registran | Dar a Claude funciones invocables (APIs, bases de datos, CLIs) | Esquema de herramienta al arrancar; sin cuerpo |
| Slash commands (legacy) | Al invocarse | Lo mismo que los Skills — los comandos son Skills en `.claude/commands/` | Cuerpo completo al invocarse |

## CLAUDE.md frente a Skills

`CLAUDE.md` es el lugar adecuado para cosas que son siempre relevantes: el lenguaje de programación y la guía de estilo de un proyecto, decisiones arquitectónicas, los nombres de los archivos clave, cómo ejecutar la suite de tests. Claude lo lee al inicio de cada sesión en ese directorio.

Los skills son el lugar adecuado para cosas que son a veces relevantes: el procedimiento para escribir un anuncio de release, los pasos para auditar una API por problemas de seguridad, un flujo para triar reportes de bugs. Si pones un procedimiento de 300 líneas en `CLAUDE.md`, pagas por esas 300 líneas en cada sesión las necesites o no. Ponlo en un skill y pagas ~100 tokens al arrancar y el cuerpo completo solo cuando el procedimiento realmente se dispara.

La regla práctica: si recurrirías al procedimiento menos de la mitad de las veces que abres un proyecto dado, ponlo en un skill.

## Skills frente a Subagents

Cuando un skill se activa, se ejecuta de manera inline en tu conversación actual. Claude lee el cuerpo del skill y aplica esas instrucciones a la tarea en curso. Todo ocurre en la misma ventana de context — las instrucciones, la tarea y la salida aparecen todas en el mismo hilo.

Los subagents se ejecutan en un context aislado. Claude lanza un agente separado con su propia ventana de context, le delega una tarea y recibe un resultado. El trabajo intermedio — cada llamada a herramienta, cada lectura intermedia de archivo, cada paso de razonamiento — se queda en el context del subagent y no inunda tu conversación principal.

Usa un skill cuando quieras que Claude siga un procedimiento sobre tu tarea actual y quieras ver cada paso. Usa un subagent cuando la tarea implique procesar una gran cantidad de salida intermedia (escanear cientos de archivos, llamar a una API repetidamente, generar un informe largo) y solo te interese el resultado final.

## Skills frente a servidores MCP

Los servidores MCP (Model Context Protocol) le dan a Claude funciones invocables — el equivalente a añadir nuevas herramientas a la caja de herramientas del agente. Un servidor MCP podría exponer una función para consultar una base de datos, enviar un mensaje a Slack o ejecutar un comando de shell con parámetros específicos. Claude llama a la función; el servidor MCP la ejecuta y devuelve un resultado.

Los skills le dan a Claude instrucciones — no nuevas capacidades, sino guía sobre cómo usar las capacidades existentes. Un skill puede indicarle a Claude exactamente cómo estructurar un mensaje de commit de git, qué preguntas hacer antes de escribir una feature o cómo formatear la descripción de un pull request. Los skills y los servidores MCP se complementan: podrías tener un servidor MCP que dé a Claude acceso a tu issue tracker, y un skill que le indique a Claude cómo triar issues usando esa herramienta.

## Skills frente a los slash commands legacy

El mecanismo original de Claude Code para instrucciones bajo demanda era `.claude/commands/`, donde cada archivo Markdown se convertía en un slash command invocable. Ese mecanismo sigue funcionando. La diferencia es que los archivos en `.claude/commands/` son comandos — soportan invocación básica pero carecen de los campos de frontmatter que soportan los skills.

Los skills en `.claude/skills/` obtienen el conjunto completo de funcionalidades: frontmatter estructurado con control de invocación (`user-invocable`, `disable-model-invocation`), declaraciones de argumentos (`arguments`, `argument-hint`), aislamiento de context (`context: fork`), integración con hooks, y el modelo de carga progresiva en tres etapas descrito en [progressive-disclosure.md](progressive-disclosure.md).

Si tienes archivos en `.claude/commands/` ya existentes, siguen funcionando como antes. Cuando quieras las funcionalidades adicionales, muévelos a `.claude/skills/` y añade un bloque de frontmatter.
