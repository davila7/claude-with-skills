---
title: "Matriz de invocación y carga de context"
---

Cómo interactúan el modo de invocación del skill, la carga de context y el presupuesto de descripciones.

---

## Parte 1: La matriz de invocación

Dos campos de frontmatter controlan quién puede invocar un skill y qué puede ver Claude:

- `disable-model-invocation: true` — oculta el skill por completo a Claude
- `user-invocable: false` — oculta el skill del menú `/`

### Por defecto (ningún campo activado)

Tanto el usuario como Claude pueden invocar el skill. La descripción aparece en el context de Claude al inicio de la sesión. El cuerpo completo se carga cuando cualquiera de las partes lo invoca.

**Úsalo para:** Skills de propósito general, aumento de conocimiento, estándares de formato, guías de lenguaje. La mayoría de los skills pertenecen aquí.

**Ejemplo:** Un skill `/summarize-pr` que un developer puede invocar manualmente o que Claude puede disparar cuando detecta que la conversación trata sobre revisar un pull request.

### Solo `disable-model-invocation: true`

Solo el usuario puede invocar el skill mediante `/name`. Claude nunca ve la descripción y no puede auto-invocarlo.

**Úsalo para:** Flujos con efectos secundarios donde debes controlar el momento. Despliegues, envíos de email, escrituras a base de datos, eliminaciones. Si Claude pudiera auto-disparar estos, una mención casual de "deploy" en la conversación podría iniciar un despliegue a producción.

**Ejemplo:** Un skill `/deploy-production`. El usuario decide exactamente cuándo ejecutarlo. Claude no sabe que existe y no puede invocarlo por accidente.

### Solo `user-invocable: false`

Claude puede auto-invocar el skill, pero no aparece en el menú `/` para los usuarios.

**Úsalo para:** Experticia de fondo que enriquece el comportamiento de Claude sin saturar la lista de skills visible al usuario. Guías de estilo, estándares de código, conocimiento específico de dominio que Claude debería aplicar siempre cuando sea relevante.

**Ejemplo:** Un skill que codifica los estándares de revisión de código de tu equipo. Claude los aplica automáticamente al revisar código, pero los developers nunca necesitan invocar `/code-review-standards` manualmente.

### Ambos `disable-model-invocation: true` Y `user-invocable: false`

No hagas esto. El skill se vuelve permanentemente inaccesible — Claude no puede verlo y los usuarios no pueden invocarlo. No hay error ni advertencia; el skill simplemente no hace nada. Si quieres desactivar temporalmente un skill, renombra el archivo SKILL.md o elimina el directorio en su lugar.

---

## Parte 2: Qué se carga y cuándo

El contenido del skill entra en el context de Claude por etapas. Entender esto evita sorpresas sobre lo que Claude sabe y cuándo.

### Al inicio de la sesión

Claude Code escanea todos los directorios de skills y carga el `name` y la `description` de cada skill (más `when_to_use` si está definido) en una definición de herramienta. Esto cuesta aproximadamente 100 tokens por skill en un conjunto típico de skills.

Claude sabe que los skills existen y puede emparejar las peticiones del usuario con descripciones, pero todavía no ha leído ningún cuerpo de SKILL.md.

### Cuando se invoca un skill

El cuerpo completo del SKILL.md se inyecta en la conversación como un único mensaje, en el punto de invocación. A partir de ese momento, todas las instrucciones del cuerpo están activas para el resto de la sesión.

Escribe los cuerpos de los skills como reglas permanentes, no como instrucciones de configuración de una sola vez. "Always use 2-space indentation" funciona correctamente. "Set up your indentation preferences now" implica una acción única tras la cual la instrucción ya no se necesita — ese framing puede confundir al modelo.

### Archivos de apoyo

Los archivos adicionales en el directorio del skill (scripts, plantillas, archivos de configuración) no se cargan automáticamente. Solo se leen cuando Claude los lee explícitamente durante la ejecución del skill (mediante una llamada a la herramienta `Read` o un bloque `!`cmd`` que muestre su contenido). Refiérete a ellos usando rutas con `${CLAUDE_SKILL_DIR}` en el cuerpo del skill.

### Tras la compactación de context

Claude Code compacta automáticamente la conversación cuando el context se acerca al límite del modelo. Durante la compactación, la invocación más reciente de cada skill se vuelve a adjuntar al context compactado. El presupuesto para el contenido de skill re-adjuntado es de 5000 tokens por skill y 25000 tokens en total entre todos los skills.

Implicaciones prácticas:
- Los cuerpos de skill largos (más allá de 5000 tokens) serán truncados tras la compactación.
- Si muchos skills están activos, algunos pueden recortarse para encajar dentro del presupuesto agregado de 25000 tokens.
- Si Claude deja de seguir las instrucciones de un skill tras una sesión larga, la causa más probable es que la compactación haya recortado el cuerpo del skill. Re-invocar el skill restaura el contenido completo.

---

## Parte 3: El presupuesto de descripciones

Todas las descripciones de skill deben caber dentro de un presupuesto compartido. Cuando el presupuesto se desborda, Claude pierde visibilidad de algunos skills y no puede auto-invocarlos.

### Tamaño del presupuesto

El presupuesto por defecto es el 1% de la ventana de context del modelo activo. Para un context de 200.000 tokens, eso son 2000 tokens para todas las descripciones de skill combinadas.

### Comportamiento ante desbordamiento

Cuando las descripciones exceden el presupuesto:
- Las descripciones de los skills menos recientemente invocados se descartan primero.
- Los nombres siempre se conservan aunque las descripciones se descarten.
- Un skill cuya descripción se ha descartado no se auto-invocará, pero un usuario aún puede invocarlo con `/name`.

### Tope de caracteres por skill

El texto combinado de `description` y `when_to_use` para un único skill está limitado a 1536 caracteres. El contenido más allá de ese tope se trunca en la definición de herramienta que Claude ve.

Escribe la frase de disparo más importante al principio en ambos campos. Si la descripción se trunca, el inicio sobrevive.

### Ajustar el presupuesto

Aumenta la fracción global del presupuesto en `.claude/settings.json`:

```json
{
  "skillListingBudgetFraction": 0.02
}
```

Aumenta el tope de caracteres por skill:

```json
{
  "maxSkillDescriptionChars": 2048
}
```

Establece un skill específico en modo solo-nombre en `.claude/settings.local.json`:

```json
{
  "skillOverrides": {
    "my-low-priority-skill": "name-only"
  }
}
```

Sobrescribe el presupuesto total en caracteres usando la variable de entorno:

```bash
SLASH_COMMAND_TOOL_CHAR_BUDGET=4000 claude
```

### Comprobar el presupuesto

Ejecuta `/doctor` dentro de Claude Code. Reporta:
- Presupuesto total de descripciones en tokens
- Uso actual
- Si alguna descripción de skill está siendo truncada
- Qué skills están afectados

---

## Parte 4: Ciclo de vida del contenido del skill

### Persistencia dentro de una sesión

Una vez que el cuerpo de un SKILL.md se carga en context, permanece allí durante el resto de la sesión. No hay expiración. Los skills no se recargan en cada invocación — la primera invocación es el único momento en el que se inyecta el cuerpo.

Esto significa que re-invocar un skill a mitad de sesión no añade una segunda copia al context. Es una operación nula para la carga de contenido, pero puede señalar a Claude que reaplique las instrucciones del skill.

### Por qué un skill puede dejar de influir en el comportamiento

Un skill que funcionaba puede parecer que deja de funcionar por varias razones:

1. **Fuerza de la descripción:** La auto-invocación de Claude depende de que la descripción coincida con la fraseología del usuario. Si la petición se formula de manera muy diferente a las keywords de la descripción, Claude puede no conectar ambas. Refuerza la descripción o re-invoca manualmente.

2. **Context competidor:** En una sesión larga con muchos archivos, mensajes y otras instrucciones en context, las instrucciones del skill pueden quedar eclipsadas por context más reciente o más prominente. Re-invoca el skill para acercar su contenido al punto actual en context.

3. **Compactación:** Tras la auto-compactación, el cuerpo del skill se vuelve a adjuntar con un tope de 5000 tokens. Si el cuerpo original era más largo de 5000 tokens, la versión truncada puede carecer de instrucciones críticas. Re-invoca el skill para recargar el cuerpo completo.

4. **Elección de modelo:** Algunos modelos siguen instrucciones mejor que otros. Si cambias a un modelo más pequeño a mitad de sesión, el cumplimiento de instrucciones detalladas del skill puede disminuir.

### Práctica recomendada

Trata el cuerpo del skill como un prompt de sistema persistente para el dominio de ese skill. Escribe reglas que deberían aplicar a lo largo de la sesión sin necesidad de re-enunciarse. Re-invoca los skills cuando empieces un nuevo área de tarea o tras un largo lapso en una sesión.
