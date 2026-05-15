---
title: "Lección 05: Skills orquestando skills"
---

Los skills no pueden llamarse directamente entre sí. Sin embargo, el cuerpo de un skill puede instruir a Claude para que invoque otros skills por nombre. Cuando Claude lee "ejecuta `/changelog-entry` primero, luego `/tag-version`", ejecuta esos slash commands en secuencia usando la Skill tool.

Esta lección cubre el patrón de orchestration, cuándo usarlo y un workflow de release realista que lo demuestra.

---

## Cómo los skills llaman a otros skills

Un skill orchestrator no contiene ningún mecanismo de invocación especial. Es lenguaje natural plano que le dice a Claude qué hacer. Claude, leyendo las instrucciones, reconoce las referencias `/skill-name` y las invoca.

**Por qué funciona esto:**

1. Claude lee el cuerpo del skill orchestrator.
2. El cuerpo instruye a Claude para que invoque `/other-skill-name`.
3. Claude usa la Skill tool para invocar ese skill.
4. El skill invocado se ejecuta completamente y retorna.
5. Claude lee la siguiente instrucción en el orchestrator y continúa.

Cada invocación se completa antes de que comience la siguiente. El orchestrator ve la salida completa de cada paso antes de avanzar.

**Un ejemplo mínimo:**

```markdown
## Cuerpo del orchestrator

Ejecuta el workflow de release:

1. Ejecuta `/changelog-entry` para generar la entrada del changelog.
2. Revisa la salida con el usuario — confirma que es precisa.
3. Ejecuta `/tag-version` para crear el tag de git.
4. Ejecuta `/publish` para empujar el tag y crear el release de GitHub.
```

Claude lee esto como una secuencia de instrucciones. Invoca cada skill en orden, espera los resultados y continúa.

---

## Cuándo orquestar versus consolidar

**Orquesta cuando:**

- Cada sub-skill también es útil por sí solo. Un desarrollador puede querer ejecutar `/changelog-entry` sin hacer un release completo, o `/publish` de forma independiente tras un tag manual.
- Diferentes personas usan diferentes pasos. Un release manager puede manejar el tagging; un job de CI puede manejar el publishing.
- Se necesita revisión humana entre pasos. Un orchestrator puede pausarse en cualquier paso y pedir confirmación antes de continuar.

**Consolida en un único skill cuando:**

- Los pasos siempre se ejecutan juntos sin variación.
- Nadie necesita las piezas individuales.
- Quieres la experiencia de usuario más simple posible.

Si puedes pensar en una razón para ejecutar cualquier paso de forma aislada, mantén los skills separados y escribe un orchestrator.

---

## Garantías de orden

Cada invocación de skill se completa antes de que se ejecute la siguiente instrucción. Esto significa:

- El orchestrator puede comprobar la salida del paso 1 antes de ejecutar el paso 2.
- Si un paso falla, Claude puede detenerse y reportar el fallo en lugar de continuar a ciegas.
- La lógica condicional es posible: "Si `/security-scan` devuelve algún hallazgo crítico, detente aquí y pregunta al usuario."

---

## Ejemplo: release-flow

El directorio `examples/release-flow/` contiene un workflow de release multi-paso completo:

| Skill | Lo que hace |
|---|---|
| `/release` | Orchestrator — invoca los otros tres en secuencia |
| `/changelog-entry` | Redacta una entrada Keep a Changelog a partir de commits recientes |
| `/tag-version` | Sube la versión y crea un tag de git anotado |
| `/publish` | Empuja a origin y crea un release de GitHub |

**Para probarlo:**

```bash
cp -r examples/release-flow/.claude/skills ~/.claude/skills
```

Abre Claude Code en un repository de git y ejecuta:

```
/release 1.2.0
```

Claude invocará `/changelog-entry`, te mostrará el resultado, pedirá confirmación, luego ejecutará `/tag-version 1.2.0` y `/publish` en secuencia.

**Para usar los skills individuales sin el orchestrator:**

```
/changelog-entry
/tag-version patch
/publish
```

Cada uno funciona de forma independiente. El orchestrator existe para encadenarlos cuando quieres el workflow completo en un solo comando.

---

## Cómo escribir orchestrators eficaces

**Sé explícito sobre qué debe hacer Claude con la salida de cada paso.**

Débil:

```markdown
1. Ejecuta `/security-scan`
2. Ejecuta `/complexity-check`
3. Ejecuta `/publish`
```

Mejor:

```markdown
1. Ejecuta `/security-scan`. Si se devuelven hallazgos CRITICAL, detente y avisa al usuario. No continúes al paso 2.
2. Ejecuta `/complexity-check`. Anota cualquier advertencia para el informe final.
3. Ejecuta `/publish` solo después de que el usuario confirme que quiere continuar.
```

**Pre-comprueba el entorno antes de invocar sub-skills.**

Usa una inyección dinámica de context en la parte superior del orchestrator para comprobar los prerrequisitos antes de gastar tiempo invocando sub-skills:

```markdown
Estado actual de git:
!`git status --short`

Tags actuales:
!`git tag --sort=-version:refname | head -5`

Si el working tree está sucio (cambios sin commitear en el status anterior), detente y dile al usuario que haga commit o stash antes de ejecutar el workflow de release.
```

**Nombra al orchestrator por el workflow, no por lo que hace internamente.**

- Bien: `release`, `deploy`, `code-quality-gate`
- Evita: `run-all-release-steps`, `invoke-changelog-then-tag`

El usuario piensa en el resultado, no en el mecanismo.

---

## Siguiente lección

[Lección 06: Dominio de la ventana de contexto](../lesson-06-context-window-mastery/)
