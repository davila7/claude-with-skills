---
title: "Lección 03: allowed tools"
---

El campo `allowed-tools` preaprueba un conjunto de tooling para que Claude no pida permiso al usarlo durante una ejecución del skill. Esta lección explica la sintaxis, el comportamiento exacto y los compromisos.

## Qué hace allowed-tools

Sin `allowed-tools`, cada llamada de tooling durante la ejecución de un skill dispara un prompt de permiso. El usuario ve "Claude wants to run `git status`. Allow?" antes de que ocurra nada.

Con `allowed-tools`, el tooling listado queda preaprobado durante la duración del skill. Claude lo usa sin pedir permiso. El usuario ya consintió al invocar el skill.

Esto importa sobre todo para skills con `disable-model-invocation: true`. Si el usuario tiene que responder a cinco prompts de permiso a mitad del flujo, el skill no es mejor que escribir los comandos a mano.

## Sintaxis

Nombres de tooling separados por espacios en el frontmatter:

```yaml
allowed-tools: Read Grep Glob
```

Para Bash, puedes acotar la aprobación a patrones de comando específicos:

```yaml
allowed-tools: Bash(git *) Bash(npm test) Read
```

- `Bash(git *)` — cualquier subcomando de git
- `Bash(npm test)` — solo `npm test`, no `npm install`
- `Bash(npx eslint *)` — cualquier invocación de eslint vía npx
- `Bash(find *)` — cualquier comando find

El patrón tras `Bash(` se compara contra la cadena de comando completa. Usa `*` como comodín.

## Qué NO hace allowed-tools

`allowed-tools` no restringe qué tooling puede usar Claude. Solo determina qué tooling se salta el prompt de permiso. Si el cuerpo del skill lleva a Claude a llamar a un tooling que no está en `allowed-tools`, ese tooling pedirá permiso como siempre — no será bloqueado.

Si quieres impedir que Claude use un tooling por completo, eso es una configuración distinta (permisos de proyecto, no frontmatter del skill).

## Patrones comunes

### Investigación de solo lectura

```yaml
allowed-tools: Read Grep Glob
```

Preaprueba el tooling necesario para explorar una base de código sin escribir nada. Claude puede leer archivos, buscar patrones y listar directorios sin pedir permiso.

### Operaciones de git

```yaml
allowed-tools: Bash(git *) Bash(git diff *) Bash(git log *)
```

Preaprueba todos los subcomandos de git. Útil para skills que inspeccionan el historial de git, comprueban el status o crean commits.

### npm acotado

```yaml
allowed-tools: Bash(npm test) Bash(npm run build) Bash(npm run lint)
```

Preaprueba scripts de npm específicos sin permitir comandos npm arbitrarios como `npm install` o `npm publish`.

## Project skills y el diálogo de confianza

Cuando un skill se instala con alcance de proyecto (`.claude/skills/`), el usuario ve un diálogo de confianza del workspace la primera vez que abre el proyecto en Claude Code. Aceptar el diálogo es lo que permite que `allowed-tools` tenga efecto para skills con alcance de proyecto. Los skills personales (`~/.claude/skills/`) no requieren este paso.

## Ejemplos

- `examples/safe-commit/` — operaciones de git preaprobadas para un flujo de commit
- `examples/readonly-research/` — tooling de solo lectura preaprobado para investigación de la base de código

## Siguiente lección

[Lección 04: argumentos](../lesson-04-arguments/)
