---
title: "Configuración: requisitos previos y preparación del entorno"
---

Esta página recorre todo lo que necesitas antes de ejecutar los ejemplos del curso.

## Requisitos previos

**Claude Code** debe estar instalado y autenticado.

Verifica tu instalación:

```bash
claude --version
```

Si el comando no se encuentra, instala Claude Code desde [claude.ai/code](https://claude.ai/code) y sigue los pasos de autenticación antes de continuar.

## Dónde pueden vivir los skills

Claude Code busca skills en cuatro ubicaciones, comprobadas en este orden. Un skill encontrado antes en la lista tiene prioridad sobre un skill con el mismo nombre encontrado más tarde.

| Scope | Ruta | A quién aplica |
|---|---|---|
| Enterprise | Definido por la configuración admin de tu organización | Todos los usuarios de la organización |
| Personal | `~/.claude/skills/` | Tú, en todos los proyectos |
| Project | `<project-root>/.claude/skills/` | Cualquiera que abra ese proyecto |
| Plugin | Provisto por un plugin de Claude Code | Usuarios que tengan el plugin instalado |

Para este curso, usarás el scope personal (`~/.claude/skills/`) para la mayoría de los ejemplos, de modo que los skills estén disponibles independientemente del directorio en el que estés.

## Instala el ejemplo hello-skill

### Instalación manual

```bash
# Crea el directorio personal de skills si no existe
mkdir -p ~/.claude/skills

# Copia el ejemplo hello-skill
cp -r examples/hello-skill ~/.claude/skills/
```

### Usando el script de instalación

El script `scripts/install-examples.sh` se encarga de la validación y la copia:

```bash
bash scripts/install-examples.sh examples/hello-skill personal
```

El script confirmará la ruta de instalación e imprimirá el comando para invocar el skill.

## Confirma que un skill está cargado

Abre Claude Code en modo interactivo:

```bash
claude
```

Luego escribe:

```
what skills are available?
```

Claude listará los skills que encontró al arrancar, incluyendo `hello-skill` si la instalación tuvo éxito. También puedes invocarlo directamente:

```
/hello-skill
```

## Conceptos básicos del modo headless

El modo headless (`claude -p`) ejecuta Claude Code de forma no interactiva — útil para scripts, pipelines de CI y encadenamiento de comandos. Claude procesa el prompt, escribe la salida en stdout y termina.

```bash
claude -p "summarize the last 5 git commits"
```

Usa el modo headless cuando quieras automatizar una tarea o integrar Claude en una pipeline de shell. Usa el modo interactivo cuando estés explorando, iterando o quieras tener una conversación de ida y vuelta.

## Invocar skills en modo headless

Hay tres patrones comunes:

**Patrón 1 — Invocar por nombre:**

```bash
claude -p "/hello-skill"
```

**Patrón 2 — Invocar con un argumento:**

```bash
claude -p "/hello-skill World"
```

**Patrón 3 — Pasar entrada por pipe como context:**

```bash
echo "some context or data" | claude -p "/hello-skill"
```

El contenido del pipe llega como stdin. Los skills pueden leerlo mediante el placeholder `${stdin}` o haciendo referencia a la entrada en sus instrucciones. Esto es útil cuando el skill necesita procesar un archivo, la salida de un comando o un bloque de texto que ya has preparado.

## Próximos pasos

Con tu entorno configurado y `hello-skill` funcionando correctamente, continúa con la primera sección:

- [01-basic](../01-basic/) — escribir tu primer skill real desde cero
