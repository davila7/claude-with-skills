---
title: "Lección 06: Dominio de la ventana de contexto"
---

La ventana de contexto es finita. Cada descripción de skill cargada al inicio, cada cuerpo de skill invocado y cada resultado de tool compiten por el mismo espacio. Los autores avanzados de skills deben entender cómo funciona este presupuesto y cómo escribir skills que se mantengan eficientes a escala — cuando un proyecto tiene docenas de skills y un uso intensivo de tools.

---

## Etapa 1: El discovery budget

Cuando Claude Code arranca, carga un listado de todos los skills disponibles para que Claude pueda decidir cuál invocar. Este listado incluye:

- El `name` de cada skill — siempre incluido, sin excepciones
- El `description` y `when_to_use` de cada skill — incluidos hasta un presupuesto

**Presupuesto por defecto:** aproximadamente el 1% de la ventana de contexto del model.

Cuando el listado supera el presupuesto, Claude Code trunca las descripciones empezando por los skills usados menos recientemente. Los skills que invocas con frecuencia mantienen sus descripciones completas; los poco usados pueden truncarse a solo el nombre.

**Cómo comprobarlo:** Ejecuta `/doctor` en Claude Code. Reporta si el listado de skills está desbordando el presupuesto y qué skills están afectados.

**Qué significa el desbordamiento en la práctica:** A Claude se le puede seguir diciendo que invoque `/skill-name` directamente, pero no reconocerá automáticamente cuándo el skill es relevante porque la descripción que habría disparado el reconocimiento falta o está truncada.

---

## Etapa 2: El ciclo de vida del cuerpo

Cuando se invoca un skill, su cuerpo completo de `SKILL.md` entra en el contexto como un único mensaje. Ese mensaje permanece en el contexto durante el resto de la sesión — el cuerpo del skill no se vuelve a leer si invocas el skill de nuevo. La segunda invocación reutiliza el mismo mensaje.

**Escribe los cuerpos de skill como reglas permanentes, no como scripts de una sola vez.** Si un cuerpo de skill dice "Paso 1: haz X, Paso 2: haz Y", eso se lee bien en la primera invocación. En la segunda invocación, Claude ve esas mismas instrucciones y debe entender si se aplican a la nueva petición. Las instrucciones formuladas como reglas permanentes ("Siempre haz X antes que Y cuando este skill esté activo") sobreviven mejor a la re-invocación.

**Tras la auto-compactación:**

Cuando el contexto se aproxima al 95% de capacidad, Claude Code compacta automáticamente. La compactación resume la conversación y vuelve a adjuntar los cuerpos de skill que fueron invocados previamente, sujetos a un presupuesto:

- Hasta 5.000 tokens por skill
- Hasta 25.000 tokens en total entre todos los skills readjuntados
- Los skills se priorizan por recencia — los skills invocados más recientemente sobreviven a la compactación; los inactivos pueden descartarse

Si un skill deja de influir en Claude tras la compactación, re-invócalo con `/skill-name`.

---

## Etapa 3: Auto-compactación y supervivencia del skill

La auto-compactación no es opcional — ocurre automáticamente cuando el contexto se llena. Entenderla te permite diseñar skills que la superen con elegancia.

**Skills que sobreviven bien a la compactación:**
- Cuerpos cortos (menos de 80 líneas) — caben dentro del presupuesto de 5.000 tokens por skill
- Cuerpos autocontenidos — no dependen de turnos previos de la conversación para tener sentido
- Skills invocados recientemente — la recencia es el principal criterio de supervivencia

**Skills que pueden descartarse tras la compactación:**
- Skills rara vez invocados con cuerpos grandes
- Skills `user-invocable: false` de conocimiento de fondo que fueron cargados temprano y no se re-invocaron
- Skills cuyos cuerpos referencian estado externo de turnos previos en la conversación (el estado se pierde tras la compactación)

**Recuperación:** Si un skill que estaba influyendo en el comportamiento de Claude deja de hacerlo tras una sesión larga, ejecuta `/skill-name` de nuevo. Esto reinyecta el cuerpo del skill en la posición actual del contexto, donde se priorizará por recencia.

---

## Principios de diseño para la eficiencia de contexto

### 1. Mantén el SKILL.md corto

Apunta a menos de 80 líneas por skill. Si las instrucciones completas requieren más detalle, mueve el detalle a un directorio `references/` — Claude puede leer esos archivos cuando lo necesite en lugar de tenerlos siempre en el contexto.

```
.claude/skills/my-skill/
  SKILL.md              ← menos de 80 líneas, orquesta el trabajo
  references/
    edge-cases.md       ← se carga solo cuando Claude encuentra casos límite
    examples.md         ← se carga solo cuando Claude necesita ejemplos
```

El cuerpo de SKILL.md puede instruir a Claude: "Para casos límite, lee `${CLAUDE_SKILL_DIR}/references/edge-cases.md`."

### 2. Las descripciones son un coste siempre presente

Cada descripción se carga en cada inicio de sesión. Una descripción de 512 caracteres cuesta 512 caracteres del discovery budget cada vez. Escribe descripciones que sean precisas sobre la condición de disparo, no completas sobre la implementación.

**Demasiado largo:**
```yaml
description: This skill runs npm outdated and npm audit to check the project's npm dependencies for packages that are not at their latest version and for packages that have known security vulnerabilities listed in the npm advisory database. It also checks pip dependencies if a requirements.txt is present. Use this skill when you want to know if your dependencies are up to date or when you are about to do a release and want to make sure there are no critical vulnerabilities.
```

**Mejor:**
```yaml
description: Audit npm and pip dependencies for outdated versions and known vulnerabilities. Use before releases, after adding packages, or when checking package health.
```

Ambas transmiten el disparador. La segunda usa 178 caracteres en lugar de 453.

### 3. Los skills de fondo también consumen presupuesto de descripción

Un skill con `user-invocable: false` sigue listándose en el discovery budget — su descripción aún se carga. Solo `disable-model-invocation: true` elimina un skill del listado por completo.

Usa `user-invocable: false` para: convenciones de fondo que Claude debe seguir pero que los usuarios no deben invocar directamente.

Usa `disable-model-invocation: true` para: skills con efectos secundarios que nunca deben ejecutarse automáticamente.

Si quieres un skill que sea puramente un archivo de configuración y no debe costar nada de presupuesto de descripción: establece `disable-model-invocation: true`. El skill se vuelve entonces invisible a la auto-detección de Claude y no consume discovery budget.

### 4. Muchos skills pequeños superan a un skill grande

Un único cuerpo de skill de 400 líneas cuesta 400 líneas en cada invocación y 400 caracteres de discovery budget por una descripción. Cuatro skills de 100 líneas cuestan 100 líneas en cada invocación individual (solo se carga el invocado) y 100 caracteres cada uno — pero sus cuatro descripciones enfocadas le dan a Claude cuatro puntos de disparo precisos.

El skill monolítico carga su cuerpo completo cuando se necesita cualquier parte de él. Los skills divididos cargan solo lo que es relevante para la petición actual.

### 5. El ajuste `skillOverrides`

En `.claude/settings.json`, puedes anular el comportamiento de listado por skill:

```json
{
  "skillOverrides": {
    "my-verbose-skill": "name-only",
    "retired-skill": "off"
  }
}
```

- `"name-only"`: el skill aparece en el listado con su nombre pero sin descripción. Claude no puede auto-detectar cuándo usarlo, pero los usuarios aún pueden invocarlo directamente.
- `"off"`: el skill está completamente oculto del listado. No existe en lo que a Claude respecta a menos que se invoque explícitamente por nombre.
- `"user-invocable-only"`: elimina el skill de la auto-detección de Claude pero lo mantiene en el menú `/` del usuario.

---

## Mandos de ajuste

En `.claude/settings.json`:

```json
{
  "skillListingBudgetFraction": 0.02,
  "maxSkillDescriptionChars": 512
}
```

**`skillListingBudgetFraction`** (por defecto: `0.01`)
La fracción de la ventana de contexto total del model reservada para descripciones de skill al inicio. Aumenta esto si `/doctor` reporta desbordamiento de forma consistente y tienes muchos skills importantes. Disminúyelo si quieres maximizar el contexto disponible para la conversación.

**`maxSkillDescriptionChars`** (por defecto: `1536`)
Tope por skill sobre el recuento combinado de caracteres de `description` + `when_to_use`. Los skills que superan esto se truncan en el listado. Bajar esto fuerza descripciones concisas en general.

**`SLASH_COMMAND_TOOL_CHAR_BUDGET`** (variable de entorno)
Anula el discovery budget total en caracteres. Tiene precedencia sobre `skillListingBudgetFraction`. Útil para probar el umbral exacto de desbordamiento durante el desarrollo de skills.

---

## Workflow práctico para medir el presupuesto

1. Abre Claude Code y ejecuta `/doctor`.
2. Comprueba la salida para ver el estado del "skill listing budget".
3. Si se reporta desbordamiento: identifica qué skills tienen las descripciones más largas (recuento combinado de caracteres de `description` + `when_to_use`).
4. Para skills que rara vez necesitan auto-detección: añade `"name-only"` bajo `skillOverrides` en settings.
5. Para skills con efectos secundarios que nunca deben auto-activarse: confirma que `disable-model-invocation: true` está establecido.
6. Vuelve a ejecutar `/doctor` para confirmar que el presupuesto ya no se desborda.

---

## Ejemplo: lightweight-orchestrator

El directorio `examples/lightweight-orchestrator/` contiene un skill `code-quality-audit` que demuestra cómo mantener mínimo el cuerpo de SKILL.md. El skill usa `context: fork` y `agent: Explore` para delegar una investigación exhaustiva a un subagent, manteniendo el cuerpo del skill por debajo de 40 líneas mientras produce una auditoría completa.

---

## Siguiente lección

[Lección 07: Hooks en skills](../lesson-07-hooks-in-skills/)
