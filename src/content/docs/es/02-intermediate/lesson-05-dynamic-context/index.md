---
title: "Lección 05: inyección de context dinámico"
---

La inyección de context dinámico te permite ejecutar comandos de shell cuando se invoca un skill e incrustar la salida directamente en el cuerpo del skill antes de que Claude la vea. Es el mecanismo que hace a los skills conscientes del estado actual de git, versiones del entorno, pull requests abiertos o cualquier otro dato en vivo.

## La sintaxis

### Inline: comando único

Usa la sintaxis de backticks precedida por `!`:

```
!`git status --short`
```

Claude Code ejecuta este comando cuando se invoca el skill, captura stdout y reemplaza toda la expresión `` !`...` `` con la salida. Claude ve la salida, no el comando.

### Múltiples líneas: bloque de código cercado

Para comandos que abarcan varias líneas o producen salida estructurada, usa un bloque cercado abierto con `` ```! `` en vez del habitual `` ``` ``:

````
```!
echo "OS: $(uname -s)"
echo "Node: $(node --version)"
echo "Git: $(git version)"
```
````

Todo lo que está dentro del bloque se pasa al shell como un script. La stdout del script entero reemplaza al bloque.

## Lo que ve Claude

Tú escribes:
```
The current git status is:
!`git status --short`
```

Claude ve (en el momento de la invocación):
```
The current git status is:
 M src/auth.ts
 M src/routes/login.ts
?? src/temp.js
```

Claude nunca ve el comando original. Solo ve la salida.

## Cuándo se ejecuta la inyección

Los comandos se ejecutan en el momento de la invocación del skill, en el directorio del proyecto (el directorio donde se abrió Claude Code). Se ejecutan antes de que comience el turno de Claude. Claude no puede influir en qué comandos se ejecutan ni en qué salida producen.

## Fallos

Si un comando termina con un código distinto de cero, la salida de error (stderr) reemplaza al placeholder. Claude ve el mensaje de error y puede responder a él — por ejemplo, "git status failed: not a git repository" es visible para Claude y puede explicar el problema al usuario.

## Deshabilitar la inyección

Si `disableSkillShellExecution: true` está activado en la configuración de Claude Code, todos los placeholders `` !`cmd` `` se reemplazan con la cadena literal `[shell execution disabled]` en vez de ejecutar el comando. Los skills que dependen de la inyección aún se cargan, pero no tendrán datos en vivo.

## Casos de uso clave

**Estado de git**: inyecta `git status`, `git diff --stat` o `git log --oneline -10` para que Claude sepa exactamente qué ha cambiado sin preguntar.

**Información del entorno**: inyecta versión de Node, versión de Python, detalles del SO para depuración o comprobaciones de compatibilidad.

**Contenido de archivos**: inyecta un archivo de configuración o el campo version de package.json para evitar que Claude lo lea por separado.

**GitHub CLI**: inyecta la salida de `gh pr view`, `gh issue view` o `gh run list` para dar a Claude context en vivo sobre el estado de CI del proyecto.

## Ejemplos

- `examples/git-diff-summary/` — inyecta el diff staged y unstaged antes de pedir a Claude que lo resuma
- `examples/env-report/` — usa un bloque multilínea para capturar el entorno completo
- `examples/pr-summary/` — inyecta múltiples salidas de la CLI `gh` para una visión general completa del PR

## Siguiente lección

[Lección 06: paths y shell](../lesson-06-paths-and-shell/)
