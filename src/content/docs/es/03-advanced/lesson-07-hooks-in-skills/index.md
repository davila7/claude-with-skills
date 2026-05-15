---
title: "Lección 07: Hooks en skills"
---

Los skills pueden definir hooks que se ejecutan durante el ciclo de vida del skill. Los hooks son comandos de shell disparados por eventos de uso de tools. Se ejecutan fuera del turno de Claude — no son llamadas a LLM — lo que los hace fiables, rápidos y adecuados para efectos secundarios que deben ocurrir en cada uso de tool coincidente independientemente de lo que esté haciendo Claude.

---

## Eventos de hook disponibles

**`PreToolUse`**
Se ejecuta antes de que Claude use una tool. El hook recibe el nombre de la tool y la entrada por stdin. Puede:
- Salir 0: permitir que el uso de la tool continúe
- Salir 1: registrar un error, pero el uso de la tool continúa
- Salir 2: bloquear el uso de la tool — stderr se devuelve a Claude como mensaje de error

Usa `PreToolUse` para: validación, rate limiting, confirmación de operaciones peligrosas, logging.

**`PostToolUse`**
Se ejecuta después de que Claude haya usado una tool y recibido la respuesta. El hook recibe el nombre de la tool, la entrada y la respuesta por stdin. No puede bloquear (el uso de la tool ya se ha completado), pero puede disparar efectos secundarios.

Usa `PostToolUse` para: formatear código tras ediciones, enviar notificaciones, logging, actualizar sistemas externos.

**`Stop`**
Se ejecuta cuando el subagent del skill se completa. Solo es significativo para skills con `context: fork` — se mapea a `SubagentStop` en runtime.

Usa `Stop` para: limpieza tras un skill de investigación forked, enviar una notificación de resumen cuando un skill de larga ejecución termina.

---

## Formato de hook en el frontmatter del skill

```yaml
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/format.sh"
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-bash.sh"
  Stop:
    - hooks:
        - type: command
          command: "./scripts/on-complete.sh"
```

Cada evento acepta una lista de entradas de matcher. Cada entrada tiene un `matcher` y una lista de `hooks` debajo. El `matcher` es una cadena que soporta `|` para OR — coincide con el nombre de la tool.

**Ejemplos de matchers:**

| Matcher | Coincide con |
|---|---|
| `"Edit"` | Solo la tool Edit |
| `"Write"` | Solo la tool Write |
| `"Edit\|Write"` | Edit o Write |
| `"Bash"` | Cualquier llamada a Bash |
| `"Read"` | Solo la tool Read |

---

## Formato de entrada del hook

Los hooks reciben un objeto JSON por stdin. La estructura depende del evento:

**PreToolUse:**
```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.ts",
    "old_string": "...",
    "new_string": "..."
  }
}
```

**PostToolUse:**
```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.ts",
    "old_string": "...",
    "new_string": "..."
  },
  "tool_response": {
    "filePath": "/path/to/file.ts"
  }
}
```

La estructura de `tool_response` varía según la tool. Para `Edit` y `Write`, incluye `filePath`. Para `Bash`, incluye `stdout` y `stderr`.

---

## Códigos de salida

| Código | Efecto |
|---|---|
| 0 | Éxito — continúa normalmente |
| 1 | Error no fatal — se registra, pero la ejecución continúa |
| 2 | Bloquear (solo PreToolUse) — stderr se envía a Claude como mensaje de error |

Los hooks `PostToolUse` siempre deben salir 0. No hay nada que bloquear después de que la tool ya se haya ejecutado, y un código de salida distinto de cero es engañoso.

---

## La variable `${CLAUDE_SKILL_DIR}`

Los comandos de hook tienen acceso a `${CLAUDE_SKILL_DIR}`, que es la ruta absoluta al directorio que contiene el archivo `SKILL.md`. Úsala para referenciar scripts empaquetados con el skill:

```yaml
command: "bash ${CLAUDE_SKILL_DIR}/scripts/format.sh"
```

Esto asegura que el script se encuentre independientemente del directorio de trabajo cuando se ejecute el hook.

---

## Ejemplo: auto-format-on-edit

El directorio `examples/auto-format-on-edit/` contiene un skill que ejecuta Prettier y ESLint automáticamente tras cada edición de archivo. Este es un hook `PostToolUse` que se dispara en cada llamada a la tool `Edit` o `Write`.

**Características clave:**
- `user-invocable: false` — los usuarios no invocan esto directamente; se ejecuta en segundo plano cada vez que Claude edita un archivo
- El script del hook sale 0 incondicionalmente — no debe bloquear
- El hook comprueba si los formatters están instalados antes de ejecutarlos; las tools faltantes se omiten en silencio
- El hook extrae la ruta del archivo de la entrada JSON de PostToolUse y solo formatea archivos con extensiones reconocidas

**Para activar el skill:**

```bash
cp -r examples/auto-format-on-edit/.claude/skills/auto-format-on-edit ~/.claude/skills/
```

Una vez instalado, cada vez que Claude edite un archivo `.ts`, `.js`, `.jsx`, `.tsx`, `.css`, `.json` o `.md`, el hook ejecuta automáticamente Prettier (y ESLint para archivos de script) sobre el archivo editado.

---

## Restricción importante: hooks en skills de plugins

Los skills distribuidos como plugins no pueden definir hooks. Esto es una restricción de seguridad — los plugins se ejecutan con confianza limitada, y los hooks tienen acceso al entorno shell completo.

Si un skill que usa hooks necesita ser distribuido, documenta los hooks esperados en el README del plugin e instruye a los usuarios para que añadan esos hooks a su `.claude/settings.json` globalmente. Alternativamente, los usuarios pueden copiar el skill fuera del directorio del plugin a `.claude/skills/` para obtener soporte de hooks.

---

## Siguiente lección

[Lección 08: Plugins y distribución](../lesson-08-plugins-and-distribution/)
