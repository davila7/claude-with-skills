---
title: "Guía de ajuste del presupuesto"
---

Una referencia práctica para medir y ajustar el uso del presupuesto del listado de skills. Aplica esto cuando `/doctor` reporte desbordamiento, cuando hayas acumulado más de diez skills en un proyecto o antes de una expansión planificada de tu conjunto de skills.

---

## Paso 1: Comprueba el estado actual del presupuesto

Ejecuta `/doctor` en Claude Code. Busca la sección del listado de skills en la salida. Reporta:

- Total de caracteres usados por las descripciones de skill
- Límite del presupuesto en caracteres
- Si el presupuesto se está desbordando
- Qué skills están truncados (si los hay)

Si no se reporta desbordamiento, tu conjunto actual de skills cabe dentro del presupuesto. Puedes detenerte aquí a menos que estés planeando añadir más skills.

---

## Paso 2: Identifica skills con descripciones pesadas

Para cada skill, cuenta la longitud combinada en caracteres de los campos `description` y `when_to_use`. El total de ambos campos es lo que cuenta contra el tope por skill (`maxSkillDescriptionChars`, por defecto 1.536) y el discovery budget global.

Una forma rápida de contar en todos los skills de un proyecto:

```bash
for f in .claude/skills/*/SKILL.md; do
  skill=$(basename $(dirname $f))
  chars=$(grep -A 200 "^---" "$f" | grep -E "^(description|when_to_use):" | wc -c)
  echo "$chars $skill"
done | sort -rn
```

Los skills en la parte superior de la salida ordenada están consumiendo más discovery budget. Estos son los primeros candidatos para recorte.

---

## Paso 3: El ajuste `skillOverrides`

`skillOverrides` en `.claude/settings.json` te permite controlar cómo aparece cada skill en el listado sin modificar los archivos del skill en sí. Esto es útil cuando no eres dueño de los archivos del skill (por ejemplo, vienen de un plugin compartido o un repository de equipo).

```json
{
  "skillOverrides": {
    "my-rarely-used-skill": "name-only",
    "legacy-deploy": "off",
    "team-conventions": "user-invocable-only"
  }
}
```

**`"name-only"`**
El skill aparece en el listado con su nombre pero sin su descripción. Claude sabe que el skill existe y los usuarios pueden invocar `/my-rarely-used-skill`, pero Claude no auto-detectará cuándo usarlo. Úsalo para: skills que los usuarios conocen e invocan manualmente, pero que no necesitan aparecer en la lógica de auto-activación de Claude.

**`"off"`**
El skill está completamente oculto del listado. No aparece en los recuentos de skill de `/doctor`, y Claude no puede referenciarlo a menos que se escriba explícitamente. Úsalo para: skills que están temporalmente deshabilitados, skills que se están probando antes de su lanzamiento o skills que existen solo para pipelines de modo headless.

**`"user-invocable-only"`**
El skill aparece en el menú `/` del usuario (el autocompletado de Claude Code) pero su descripción se excluye del listado de auto-detección de Claude. Este es el ajuste correcto para skills que quieres que sean descubribles por los usuarios pero que nunca deben activarse automáticamente. Úsalo para: skills con efectos secundarios que ya tienen `disable-model-invocation: true`, pero donde quieres una garantía adicional de que no aparecerán en el razonamiento de Claude.

Precedencia del archivo de settings (de mayor a menor):

1. `.claude/settings.local.json` del proyecto (no committeado, específico del desarrollador)
2. `.claude/settings.json` del proyecto (committeado, compartido por el equipo)
3. `~/.claude/settings.json` del usuario (global, todos los proyectos)

`skillOverrides` establecido en un archivo de mayor precedencia gana sobre archivos de menor precedencia para el mismo nombre de skill.

---

## Paso 4: `disable-model-invocation: true` como herramienta de presupuesto

Establecer `disable-model-invocation: true` en el frontmatter de un skill elimina la descripción de ese skill del listado de descubrimiento por completo. Claude nunca ve la descripción al inicio y no puede auto-activar el skill.

Esto es principalmente un ajuste de seguridad para skills con efectos secundarios. Como efecto secundario, libera exactamente `len(description) + len(when_to_use)` caracteres del discovery budget.

Úsalo como herramienta de presupuesto cuando:

- Un skill tiene una descripción larga y detallada pero siempre necesita invocación explícita (la descripción existe para documentación, no para auto-detección)
- Un skill es parte de un pipeline de orchestration y el usuario nunca lo invoca directamente

No lo uses como herramienta de presupuesto cuando la auto-detección del skill por Claude sea valiosa. Los ahorros vienen al coste de que el skill nunca se active a menos que sea llamado explícitamente.

---

## Paso 5: Tras la compactación — qué skills sobreviven

Cuando se ejecuta la auto-compactación, los cuerpos de skill que fueron invocados previamente son elegibles para readjunción. Los criterios de selección:

- **La recencia gana**: los skills invocados más tarde en la sesión tienen más probabilidades de sobrevivir
- **Tope de tamaño**: cada cuerpo de skill readjuntado se topa en 5.000 tokens
- **Tope total**: todos los skills readjuntados juntos se topan en 25.000 tokens a lo largo de la sesión

Para comprobar qué skills están activos tras una sesión larga: observa el comportamiento de Claude. Si un skill que estaba influyendo en la salida de Claude deja de hacerlo, probablemente ha sido descartado. Para confirmar, pregunta: "¿Qué skills están actualmente activos en esta sesión?"

Para recuperar un skill descartado:

```
/skill-name
```

Re-invocar el skill inyecta su cuerpo en la posición actual en el contexto. Se convierte en la invocación más reciente y sobrevivirá al siguiente ciclo de compactación.

---

## Paso 6: Ubicaciones de archivos de settings y jerarquía

**Nivel de usuario (global entre todos los proyectos):**
```
~/.claude/settings.json
```

**Nivel de proyecto (committeado, compartido con el equipo):**
```
<project-root>/.claude/settings.json
```

**Nivel de proyecto (local, no committeado):**
```
<project-root>/.claude/settings.local.json
```

Para establecer una fracción de presupuesto de listado personalizada para un proyecto:

```json
// .claude/settings.json
{
  "skillListingBudgetFraction": 0.02
}
```

Esto duplica el discovery budget por defecto. Añade esto cuando:

- `/doctor` reporta desbordamiento y no puedes recortar más las descripciones
- El proyecto tiene más de 20 skills que necesitan todos auto-detección activa
- Estás usando un model con una ventana de contexto muy grande y el 1% es un tope innecesariamente ajustado

Para establecer un tope de caracteres por skill más estricto que fuerce descripciones concisas en general:

```json
{
  "maxSkillDescriptionChars": 384
}
```

Esto evita que cualquier skill individual consuma más de 384 caracteres de presupuesto de descripción. Es un instrumento contundente — prefiere primero recortar descripciones individuales.

---

## Referencia: aritmética del presupuesto

Para un model con una ventana de contexto de 200.000 tokens (aproximadamente 800.000 caracteres):

| Ajuste | Valor | Caracteres para listados de skills |
|---|---|---|
| `skillListingBudgetFraction` por defecto | 0.01 | ~8.000 caracteres |
| Duplicado a 0.02 | 0.02 | ~16.000 caracteres |
| Con `maxSkillDescriptionChars` por defecto 1536 | — | ~5 skills con longitud máxima de descripción caben en el presupuesto por defecto |
| Con descripciones recortadas (200 caracteres de media) | — | ~40 skills caben en el presupuesto por defecto |

La conclusión práctica: con descripciones ajustadas con una media de 200 caracteres, el presupuesto por defecto maneja aproximadamente 40 skills cómodamente. Más allá de eso, o aumenta `skillListingBudgetFraction` o usa `skillOverrides` para reducir el peso de listado de los skills menos importantes.
