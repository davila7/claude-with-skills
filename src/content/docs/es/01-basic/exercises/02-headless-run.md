---
title: "Ejercicio 02: Ejecuta un skill sin la UI"
---

## Objetivo

Usa `claude -p` para invocar el skill `summarize-changes` desde la terminal sin abrir la interfaz interactiva de Claude Code.

## Requisitos previos

- El skill `summarize-changes` instalado en `~/.claude/skills/summarize-changes/SKILL.md`
  (cópialo desde `../lesson-05-invoking/examples/summarize-changes/`)
- Un repository de git con al menos un cambio sin commitear
- `claude` disponible en tu PATH

## Paso 1: prepara un repository con cambios

Encuentra un repository de git en el que estés trabajando, o crea uno desechable:

```bash
mkdir /tmp/skill-test && cd /tmp/skill-test
git init
echo "hello" > hello.txt
git add hello.txt
git commit -m "initial"
echo "world" >> hello.txt
```

Ahora `hello.txt` tiene un cambio sin stagear. El skill lo resumirá.

## Paso 2: ejecuta el skill en modo headless

Desde dentro del directorio del repository:

```bash
claude -p "/summarize-changes"
```

Claude Code arranca, activa el skill, inyecta la salida del diff, produce un resumen y termina. Deberías ver el resumen impreso por stdout.

## Paso 3: captura la salida en un archivo

```bash
claude -p "/summarize-changes" > summary.txt
cat summary.txt
```

La salida ahora está en `summary.txt`. Esto es útil en pipelines de CI donde quieres un resumen del diff guardado como artefacto.

## Paso 4: ejecuta el skill commit-message y usa la salida

Instala el skill `commit-message` si aún no lo has hecho:

```bash
cp -r path/to/lesson-03-repetitive-tasks/examples/commit-message ~/.claude/skills/
```

Stagea un cambio y ejecuta:

```bash
git add hello.txt
COMMIT_MSG=$(claude -p "/commit-message")
echo "$COMMIT_MSG"
```

Si la salida tiene buena pinta, úsala:

```bash
git commit -m "$COMMIT_MSG"
```

## Qué hace `claude -p` de forma distinta

`claude -p` termina tras un turno. No hay ida y vuelta. Esto significa:

- Los skills que hacen preguntas para aclarar no funcionan bien en modo headless — Claude hará una pregunta y el proceso terminará antes de que puedas responder
- La salida se imprime por stdout, así que puede canalizarse o capturarse con herramientas estándar de shell
- El exit code es 0 si hay éxito y distinto de cero en caso de error, así que puedes usar `&&` y `||` en scripts
- Es seguro usarlo en CI/CD porque el proceso siempre termina

## Reto adicional

Escribe un alias de shell que stagee todos los cambios y genere un commit message en un solo comando:

```bash
alias smart-commit='git add -A && git commit -m "$(claude -p "/commit-message")"'
```

Añádelo a tu perfil de shell para hacerlo permanente. Nota: ten cuidado con `git add -A` en proyectos reales — revisa lo que está staged antes de comitear.
