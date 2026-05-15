---
title: "Lección 02: Scripts incluidos con ${CLAUDE_SKILL_DIR}"
---

Los skills pueden hacer más que instruir a Claude — pueden enviar código funcional junto a esas instrucciones. Cuando una tarea implica generación compleja de archivos, salida binaria o lógica de procesamiento reutilizable, un script incluido es la herramienta adecuada. Esta lección explica cuándo incluir un script, cómo funciona la resolución de rutas y cómo estructurar scripts que cooperen con Claude de forma eficaz.

## La variable ${CLAUDE_SKILL_DIR}

`${CLAUDE_SKILL_DIR}` siempre está disponible en el cuerpo del skill y en cualquier bloque de context dinámico `` !`command` ``. Resuelve a la ruta absoluta del directorio que contiene el archivo `SKILL.md` del skill — es decir, el directorio raíz del skill.

Esta variable es crítica para los scripts incluidos. Sin ella, tendrías que codificar rutas de instalación de forma rígida:

```bash
# Incorrecto — falla cuando el skill se instala en cualquier lugar que no sea esta ruta exacta
python3 ~/.claude/skills/my-skill/scripts/generate.py

# Incorrecto — falla cuando el skill se instala en el scope de proyecto o en un plugin
python3 .claude/skills/my-skill/scripts/generate.py

# Correcto — funciona en scope de usuario, scope de proyecto, scope de plugin, cualquier ubicación
python3 ${CLAUDE_SKILL_DIR}/scripts/generate.py
```

La variable la establece Claude Code en el momento de carga del skill, no al iniciar el shell. No necesitas exportarla ni añadirla a tu configuración de shell.

## Cuándo incluir un script

Incluye un script cuando la tarea:

- **Genera salida no textual.** Archivos HTML, imágenes, formatos binarios — estos no pueden producirse con Claude describiendo instrucciones. Un script generador funcional es el único enfoque fiable.
- **Tiene lógica reutilizable significativa.** Un script que parsea un formato de log personalizado, aplica un algoritmo de puntuación o realiza transformaciones de archivos multi-paso vale la pena enviarlo con el skill en lugar de hacer que Claude re-derive la lógica en cada invocación.
- **Requiere reproducibilidad exacta.** Si la misma entrada debe siempre producir la misma salida, codifica la lógica en un script en lugar de confiar en que Claude aplique instrucciones consistentes.
- **Procesa muchos archivos en un bucle.** Claude puede escribir un bucle de shell, pero un script de Python con manejo adecuado de errores, salida de progreso y escrituras atómicas es más robusto.

Escribe instrucciones inline (sin un script) cuando:

- La tarea es de una sola línea o un pipeline simple de shell
- La lógica es diferente cada vez y no puede plantillarse
- El script sería más corto que la explicación de lo que hace

## Pautas de lenguaje para scripts

**Python 3** es la mejor opción por defecto para scripts incluidos. Está disponible en cada plataforma donde se ejecuta Claude Code, la biblioteca estándar cubre I/O de archivos, JSON, HTTP y generación de HTML sin instalación, y el código es lo suficientemente legible para que los usuarios lo auditen.

- Declara las dependencias explícitamente. Si el script requiere librerías de terceros, compruébalas al principio e imprime un comando `pip install` si faltan. Consulta `extract.py` en la lección 01 para ver este patrón.
- Usa solo la biblioteca estándar cuando sea posible. Un script sin dependencias externas se instala de inmediato.
- Añade un docstring de módulo con instrucciones de uso. Claude las lee cuando decide cómo invocar el script.

**Bash scripts** funcionan bien para pipelines de shell donde la lógica trata principalmente de combinar herramientas Unix estándar. Decláralos en `allowed-tools` con `Bash(bash ${CLAUDE_SKILL_DIR}/scripts/*.sh)` o un glob similar.

## Cómo usa Claude los scripts incluidos

Claude invoca scripts usando la tool `Bash`, no la tool `Read`. El código fuente del script no entra en el contexto de Claude a menos que se lea explícitamente con `Read`. Esta es una forma de divulgación progresiva: la implementación es gratuita hasta que alguien pregunta cómo funciona.

El cuerpo del skill le dice a Claude:
1. Qué hace el script
2. Cómo invocarlo (el comando exacto, argumentos y flags)
3. Qué hacer con su salida

Claude ejecuta el comando y usa la salida. No necesita entender la implementación.

## El ejemplo codebase-visualizer

El directorio `examples/codebase-visualizer/` demuestra este patrón con un generador de salida visual. El cuerpo del skill tiene 20 líneas. El script son ~150 líneas de código de generación de HTML que sería poco práctico describir en instrucciones. Claude invoca el script con un comando y reporta la ruta de salida.

Instálalo y pruébalo:

```bash
cp -r examples/codebase-visualizer ~/.claude/skills/
```

Abre Claude Code en cualquier proyecto y escribe `/codebase-visualizer`. El script genera un archivo HTML interactivo y lo abre en el navegador.

## Siguiente lección

[Lección 03: Skills que llaman a subagents](../lesson-03-skill-calls-subagent/)
