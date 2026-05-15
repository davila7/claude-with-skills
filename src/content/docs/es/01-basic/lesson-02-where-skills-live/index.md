---
title: "Lección 02: Dónde viven los skills"
---

Los skills pueden instalarse en cuatro scopes diferentes. El scope determina qué proyectos pueden usar un skill y quién lo controla.

## Los cuatro scopes

| Scope | Directorio | Disponibilidad | Quién lo gestiona |
|-------|-----------|--------------|----------------|
| Enterprise | Establecido por política de la organización | Todos los usuarios de la organización | Administrador de la plataforma |
| Personal | `~/.claude/skills/` | Todos los proyectos en tu máquina | Tú |
| Proyecto | `.claude/skills/` (en la raíz del repo) | Solo este proyecto | Cualquiera con acceso al repo |
| Plugin | Cargado por un plugin MCP | Depende del plugin | Autor del plugin |

En la práctica, la mayoría de los desarrolladores individuales usan dos scopes: personal para herramientas que siempre quieren disponibles, y proyecto para flujos de trabajo compartidos con el equipo.

## Orden de prevalencia

Cuando dos skills comparten el mismo nombre, ganan los scopes superiores. El orden de mayor a menor prioridad es:

```
Enterprise > Personal > Project > Plugin
```

Si tienes un skill personal llamado `code-review-checklist` y el proyecto también tiene `.claude/skills/code-review-checklist/SKILL.md`, se usa tu versión personal. Esto te permite sobrescribir skills compartidos con tus propias versiones sin modificar el proyecto.

Esto también significa que un autor de skills que publique un skill de proyecto no puede sobrescribir el skill personal de un desarrollador con el mismo nombre — lo cual es intencional.

## Skills personales

Instala un skill en `~/.claude/skills/<skill-name>/SKILL.md`.

Los skills personales están disponibles en cada proyecto que abres. Usa este scope para skills que tienen que ver con tu flujo de trabajo y no con un proyecto específico — preferencias de revisión de código, estilo de commit message, atajos personales de productividad.

```
~/.claude/skills/
  commit-message/
    SKILL.md
  code-review-checklist/
    SKILL.md
  explain-code/
    SKILL.md
```

## Skills de proyecto

Instala un skill en `.claude/skills/<skill-name>/SKILL.md` dentro de un repository.

Los skills de proyecto son visibles para todos los que trabajan en el proyecto. Comitea el directorio `.claude/skills/` al control de versiones para que el skill viaje con el código. Usa este scope para conocimiento de flujo de trabajo específico de este proyecto — procedimientos de release, convenciones de arquitectura, checklists de revisión específicos del equipo.

```
my-project/
  .claude/
    skills/
      deploy-staging/
        SKILL.md
      generate-migration/
        SKILL.md
  src/
  ...
```

## Comportamiento de recarga en vivo

Editar un archivo `SKILL.md` que ya está en un directorio vigilado surte efecto en la sesión actual de Claude Code sin reiniciar. El agente vuelve a leer el archivo la próxima vez que se invoca el skill.

Crear un directorio de skills completamente nuevo (por ejemplo, añadir `.claude/skills/` a un proyecto que no lo tenía antes) requiere reiniciar Claude Code. El watcher se configura al inicio de la sesión y no detectará un directorio raíz recién creado a mitad de sesión.

Resumen:
- Editar un archivo de skill existente -> surte efecto inmediato en la siguiente invocación
- Crear un nuevo directorio de skills -> requiere reinicio

## Ejemplos

El directorio `examples/` en esta lección contiene un skill para cada uno de los dos scopes individuales más comunes:

- `examples/personal/SKILL.md` — un skill pensado para instalarse en `~/.claude/skills/`
- `examples/project/SKILL.md` — un skill pensado para comitearse en `.claude/skills/`

Ambos son totalmente funcionales. Copia cualquiera de ellos al directorio apropiado para verlo funcionar.

## Siguiente lección

[Lección 03: Convertir tareas repetitivas en skills](../lesson-03-repetitive-tasks/)
