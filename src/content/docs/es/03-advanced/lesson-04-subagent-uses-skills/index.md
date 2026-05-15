---
title: "Lección 04: Subagents que precargan skills"
---

La lección anterior mostró cómo un skill puede lanzar un subagent. Esta lección invierte la relación: un subagent se define con una lista de skills para inyectar en su contexto de inicio. El subagent arranca conociendo ya esas convenciones, patrones y procedimientos — no necesita descubrirlos durante la ejecución.

## El campo skills en definiciones de subagent

Los subagents se definen como archivos Markdown en `.claude/agents/`. El frontmatter soporta un campo `skills`:

```yaml
---
name: api-developer
description: Implement REST API endpoints following team conventions.
tools: Read, Edit, Write, Bash, Grep, Glob
model: sonnet
skills:
  - api-conventions
  - error-handling
---
```

Cuando Claude Code arranca este subagent, inyecta el contenido completo de cada skill listado en el contexto del subagent antes de que el subagent comience su tarea. El subagent puede referenciar esos skills inmediatamente, sin necesidad de leer archivos, invocar skills o pedir orientación.

## Cuándo usar este patrón

Usa `skills:` en una definición de subagent cuando:

- **El subagent siempre necesita convenciones específicas.** Un subagent `code-reviewer` siempre debe conocer la guía de estilo de código del equipo. Codificar de forma rígida esa dependencia en la definición del subagent es más fiable que esperar que el subagent descubra el skill correcto.

- **Quieres experiencia precargada, no descubrimiento en runtime.** Cuando el contenido del skill es corto y siempre relevante, inyectarlo al inicio es más barato que esperar a que el subagent detecte que es necesario y lo cargue a mitad de tarea.

- **El skill es `user-invocable: false`.** Los skills de conocimiento de fondo — notas de arquitectura, convenciones de API, guías de estilo — no están pensados para que los usuarios los invoquen directamente. Pero un subagent puede precargarlos aunque los usuarios no puedan. El campo `skills:` evita la restricción de cara al usuario.

## Qué significa precargar

`skills:` controla qué se inyecta en el contexto de inicio del subagent. No restringe qué skills puede usar el subagent. El subagent todavía puede descubrir e invocar cualquier otro skill de proyecto o usuario a través de la Skill tool durante la ejecución. `skills:` trata sobre lo que el subagent sabe desde el inicio, no sobre lo que se le permite usar después.

## Restricciones

- **No se pueden precargar skills con `disable-model-invocation: true`.** Esos skills están explícitamente marcados como no invocables por Claude. El mecanismo de precarga usa el mismo pool de skills invocables por Claude.
- **Los skills faltantes se omiten.** Si un skill listado no está instalado en el proyecto o en el scope de usuario, Claude Code lo omite con una advertencia. El subagent arranca de todos modos, sin el contenido de ese skill.
- **El contenido precargado cuenta contra el contexto.** Cada skill que precargas se inyecta en el contexto de inicio del subagent. Precarga solo lo que sea genuinamente siempre-necesario. Si un skill solo se necesita en el 20% de los casos, deja que el subagent lo descubra bajo demanda en lugar de pagar el coste de contexto en cada ejecución.

## Comparación con context: fork

| Dimensión | `context: fork` en un skill | `skills:` en un subagent |
|-----------|---------------------------|------------------------|
| Quién establece la relación | El frontmatter del skill | El frontmatter del subagent |
| Con qué arranca el subagent | El cuerpo del SKILL.md como tarea | El cuerpo markdown del subagent como system prompt |
| Contenido pre-inyectado | Solo CLAUDE.md | Skills listados (contenido completo) |
| Quién lanza a quién | El skill lanza un subagent | La sesión principal delega al subagent |

Los dos patrones pueden trabajar juntos: un skill puede usar `context: fork` para lanzar un subagent que está definido con `skills:`. El subagent tiene entonces tanto la tarea del cuerpo del skill como la experiencia precargada de su lista `skills:`.

## El ejemplo api-developer

El directorio `examples/api-developer/` contiene un ejemplo completo y funcional de este patrón. Incluye:

- `.claude/agents/api-developer.md` — la definición del subagent, que precarga dos skills
- `.claude/skills/api-conventions/SKILL.md` — convenciones de REST API (no invocable por el usuario)
- `.claude/skills/error-handling/SKILL.md` — patrones de manejo de errores (no invocable por el usuario)

Instala el ejemplo en un proyecto:

```bash
cp -r examples/api-developer/.claude /path/to/your/project/.claude
```

Cuando Claude Code delega trabajo al subagent `api-developer`, el subagent arranca con ambos skills de convenciones ya cargados. Los aplica sin que se le diga que los busque.

## Próximos pasos

Las lecciones avanzadas restantes (05-08) cubren:
- Encadenar skills en un skill de orchestration
- Gestión del presupuesto de la ventana de contexto entre muchos skills activos
- Hooks de ciclo de vida para automatización
- Empaquetar skills en un plugin para distribución en equipo

## Volver

[Vista general de la sección avanzada](../)
