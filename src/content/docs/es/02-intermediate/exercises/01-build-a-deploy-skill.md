---
title: "Ejercicio 01: construye un skill de despliegue personalizado"
---

Construye un skill de despliegue adaptado a un proyecto de tu elección. Este ejercicio reúne los campos cubiertos en las lecciones 02, 03, 04 y 05 en un único skill funcional.

## Requisitos

Tu skill debe:

1. Poner `disable-model-invocation: true` — desplegar nunca debería ocurrir automáticamente.
2. Incluir un `argument-hint` que muestre qué argumento debe proporcionar el usuario (típicamente el nombre de un entorno: staging, production, etc.).
3. Poner `allowed-tools` solo con los comandos que tu flujo de despliegue realmente necesita. No uses `Bash(*)`.
4. Usar al menos una inyección `` !`cmd` `` para una comprobación previa que se ejecute antes de que Claude haga nada más.

## Elige tu stack

Elige uno de estos o adáptalo a tu propio proyecto:

### Node.js / npm
Comprobación previa: `git status`, `git log --oneline -3`
Build: `npm run build`
Tests: `npm test`
Publicar: `git tag` + `git push`

### Python / pip
Comprobación previa: `git status`, `git log --oneline -3`
Tests: `pytest`
Build: `python -m build`
Publicar: `git tag` + `git push`

### Docker
Comprobación previa: `git status`, `docker info`
Build: `docker build`
Push: `docker push`
Desplegar: `docker compose up -d` (o tu herramienta de orquestación)

### Sitio estático (Netlify, Vercel, etc.)
Comprobación previa: `git status`, `git log --oneline -3`
Build: `npm run build`
Desplegar: `netlify deploy --prod` o `vercel --prod`

## Validación

Tras escribir el skill, instálalo en tu directorio personal de skills:

```bash
mkdir -p ~/.claude/skills/my-deploy
cp SKILL.md ~/.claude/skills/my-deploy/
```

Luego abre Claude Code en un proyecto y prueba estos dos escenarios:

**Escenario A: cambios sin commitear**

1. Edita cualquier archivo sin commitearlo.
2. Invoca el skill: `/my-deploy staging`
3. Confirma que el skill detecta los cambios sin commitear a partir de la salida de `` !`git status` `` y aborta con un mensaje de error claro. No debería pasar a ejecutar tests ni build.

**Escenario B: árbol de trabajo limpio**

1. Commitea todos los cambios pendientes.
2. Invoca el skill: `/my-deploy staging`
3. Confirma que el skill ejecuta el flujo completo en orden.

## Checklist

- [ ] `disable-model-invocation: true` está activado
- [ ] `argument-hint` está presente
- [ ] `allowed-tools` lista comandos específicos, no `Bash(*)`
- [ ] Al menos una inyección `` !`cmd` `` está en el cuerpo
- [ ] Escenario A: el skill aborta con cambios sin commitear
- [ ] Escenario B: el skill ejecuta el flujo completo en un árbol limpio

## Solución

Una solución desarrollada para un proyecto Python está en `solutions/01-deploy-skill/SKILL.md`. Lee el ejercicio antes de mirar la solución.
