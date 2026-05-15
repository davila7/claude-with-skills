---
title: "Lección 01: referencia completa del frontmatter"
---

Esta lección documenta cada campo del frontmatter disponible en los skills de Claude Code. Para cada campo encontrarás su tipo, valor por defecto, un caso de uso concreto y un contrapunto: cuándo el campo es la elección equivocada.

## Campos del estándar AgentSkills vs campos solo de Claude Code

Los skills siguen el [estándar abierto AgentSkills.io](https://agentskills.io). Los campos definidos por ese estándar son portables: funcionan en Cursor, GitHub Copilot, Gemini CLI y cualquier otra herramienta compatible. Claude Code implementa el estándar completo y añade un superconjunto de campos para un control más fino.

**Campos del estándar AgentSkills** (portables, funcionan en cualquier herramienta compatible):
- `name`
- `description`
- `allowed-tools`

**Campos solo de Claude Code** (ignorados silenciosamente por otras herramientas, se degradan con elegancia):
- `when_to_use`
- `argument-hint`
- `arguments`
- `disable-model-invocation`
- `user-invocable`
- `model`
- `effort`
- `context`
- `agent`
- `hooks`
- `paths`
- `shell`

Si la portabilidad te importa —quieres que tu skill se ejecute en herramientas distintas de Claude Code— usa solo los campos estándar. Si estás escribiendo flujos específicos de Claude Code, usa el superconjunto completo.

---

## Referencia de campos

### `name`

- **Tipo:** cadena. Solo letras minúsculas, guiones y dígitos. Máximo 64 caracteres.
- **Por defecto:** el nombre del directorio que contiene el archivo `SKILL.md`.
- **Estándar:** AgentSkills
- **Úsalo cuando:** quieras que el slash command difiera del nombre del directorio, o quieras ser explícito sobre el nombre canónico en el propio archivo.
- **Evítalo cuando:** el nombre del directorio ya coincide con lo que quieres — el campo es opcional.
- **Ejemplo:**
  ```yaml
  name: dependency-audit
  ```

---

### `description`

- **Tipo:** cadena de texto plano. Máximo recomendado de 1.024 caracteres.
- **Por defecto:** ninguno. Claude no tiene contexto sobre el skill si se omite.
- **Estándar:** AgentSkills
- **Úsalo cuando:** siempre. Este es el campo más importante. Claude escanea las descripciones para decidir si un skill es relevante sin ser invocado explícitamente. Incluye lo que hace el skill y las palabras clave que un usuario escribiría de forma natural.
- **Evítalo cuando:** no hay una descripción significativa — en ese caso, el skill no debería existir.
- **Ejemplo:**
  ```yaml
  description: Audit npm dependencies for outdated packages and known vulnerabilities. Use when checking package versions, running dependency health checks, or preparing for a release.
  ```

---

### `when_to_use`

- **Tipo:** cadena de texto plano. Combinado con `description`, tope de 1.536 caracteres en total.
- **Por defecto:** ninguno.
- **Estándar:** solo Claude Code
- **Úsalo cuando:** la `description` ya está en el límite recomendado de 1.024 caracteres y necesitas añadir más contexto de activación — por ejemplo, una lista de palabras clave adicionales o casos límite en los que el skill debe activarse.
- **Evítalo cuando:** tu `description` ya cubre cuándo invocar el skill. Añadir `when_to_use` cuando no se necesita divide el contexto de activación entre dos campos sin razón.
- **Ejemplo:**
  ```yaml
  when_to_use: Also use when the user asks about security advisories, CVEs, or wants to know if any packages need upgrading before a production deploy.
  ```

---

### `argument-hint`

- **Tipo:** cadena mostrada en la interfaz de autocompletado.
- **Por defecto:** ninguno. El slash command aparece sin pista.
- **Estándar:** solo Claude Code
- **Úsalo cuando:** el skill espera uno o más argumentos y quieres mostrar al usuario qué escribir. La pista aparece en el menú `/` junto al nombre del skill.
- **Evítalo cuando:** el skill no recibe argumentos, o la descripción ya hace que la entrada esperada sea completamente obvia.
- **Ejemplo:**
  ```yaml
  argument-hint: [package-name]
  ```

---

### `arguments`

- **Tipo:** cadena separada por espacios o lista YAML de nombres.
- **Por defecto:** ninguno. Los argumentos están disponibles como `$ARGUMENTS` o `$ARGUMENTS[N]` sin este campo.
- **Estándar:** solo Claude Code
- **Úsalo cuando:** el skill recibe múltiples argumentos posicionales y quieres referenciarlos por nombre en el cuerpo en vez de por índice. Los argumentos nombrados hacen el cuerpo más fácil de leer y mantener.
- **Evítalo cuando:** el skill recibe un único argumento de forma libre — usa `$ARGUMENTS` directamente y ahórrate la sobrecarga de declarar un nombre.
- **Ejemplo:**
  ```yaml
  arguments: [component-name, from-framework, to-framework]
  ```
  En el cuerpo, refiérete a `$component-name`, `$from-framework`, `$to-framework`.

---

### `disable-model-invocation`

- **Tipo:** booleano.
- **Por defecto:** `false`. Claude puede invocar el skill automáticamente.
- **Estándar:** solo Claude Code
- **Úsalo cuando:** el skill tiene efectos secundarios — despliega, envía mensajes, borra archivos, hace push a un remoto o modifica estado externo. No quieres que Claude lo dispare automáticamente en respuesta al mensaje de un usuario.
- **Evítalo cuando:** el skill es informativo o analítico. La autoinvocación para skills de solo lectura es una característica, no un riesgo.
- **Ejemplo:**
  ```yaml
  disable-model-invocation: true
  ```

---

### `user-invocable`

- **Tipo:** booleano.
- **Por defecto:** `true`. El skill aparece en el menú `/` y los usuarios pueden invocarlo por nombre.
- **Estándar:** solo Claude Code
- **Úsalo cuando:** `false` — cuando el skill es conocimiento de fondo que debe informar el comportamiento de Claude en vez de una acción que el usuario ejecuta. Ejemplos: convenciones de API del equipo, contexto de arquitectura del código, notas sobre sistemas legacy.
- **Evítalo cuando:** el skill es algo que los usuarios deberían poder llamar directamente. Ocultar un skill dirigido al usuario en el menú `/` confunde.
- **Ejemplo:**
  ```yaml
  user-invocable: false
  ```

---

### `allowed-tools`

- **Tipo:** lista de nombres de tooling separada por espacios. `Bash` acepta un patrón glob opcional entre paréntesis: `Bash(git *)`.
- **Por defecto:** ninguno. Claude pide permiso antes de cada uso de tooling.
- **Estándar:** AgentSkills (el nombre del campo es compartido; la sintaxis `Bash(pattern)` con alcance es comportamiento específico de Claude Code)
- **Úsalo cuando:** el skill necesita tooling específico y quieres que Claude lo use sin pedir permiso. Esto es especialmente importante para skills con `disable-model-invocation: true`, donde un prompt de permiso a mitad de un flujo es disruptivo.
- **Evítalo cuando:** realmente no sabes qué tooling necesitará el skill. Adivinar y dar permisos en exceso es peor que dejar que el prompting por defecto lo gestione.
- **Ejemplo:**
  ```yaml
  allowed-tools: Read Grep Glob Bash(npm outdated) Bash(npm audit)
  ```

---

### `model`

- **Tipo:** `haiku`, `sonnet`, `opus`, una cadena de ID de modelo completo, o `inherit`.
- **Por defecto:** `inherit` — usa el model con el que esté corriendo la sesión actual.
- **Estándar:** solo Claude Code
- **Úsalo cuando:** la tarea tiene un requisito de coste/capacidad claramente distinto al de la sesión por defecto. Usa `haiku` para formateo rápido o extracción de metadatos. Usa `opus` para análisis arquitectónico, revisiones de seguridad, o cuando el modelo estándar falla repetidamente en algo.
- **Evítalo cuando:** el skill hace cosas variadas y ningún modelo único es siempre el adecuado. Sobrescribir a nivel de skill fija todas las invocaciones a ese modelo.
- **Ejemplo:**
  ```yaml
  model: opus
  ```

---

### `effort`

- **Tipo:** `low`, `medium`, `high`, `xhigh` o `max`.
- **Por defecto:** hereda el effort de la sesión.
- **Estándar:** solo Claude Code
- **Úsalo cuando:** el skill exige un razonamiento más profundo que el de la sesión por defecto — una auditoría de seguridad, análisis de causa raíz o un refactor complejo. O un razonamiento más ligero que el predeterminado — generación de código simple, renombrar archivos, extracción de metadatos.
- **Evítalo cuando:** el valor por defecto de la sesión ya es apropiado para lo que hace el skill.
- **Ejemplo:**
  ```yaml
  effort: high
  ```

---

### `context`

- **Tipo:** `fork`.
- **Por defecto:** ninguno. El skill se ejecuta en el context actual.
- **Estándar:** solo Claude Code
- **Úsalo cuando:** el skill hace investigación a gran escala que contaminaría el context de la conversación principal — explorar muchos archivos, leer documentos largos, ejecutar muchos comandos de shell. Hacer fork evita que la salida del skill desplace el context de trabajo del usuario.
- **Evítalo cuando:** el skill necesita acceso al historial de la conversación actual, o el resultado necesita fluir de forma natural de regreso a una tarea en curso.
- **Ejemplo:**
  ```yaml
  context: fork
  ```

---

### `agent`

- **Tipo:** cadena que nombra un subagent (p. ej., `Explore`).
- **Por defecto:** ninguno. Se usa en combinación con `context: fork`.
- **Estándar:** solo Claude Code
- **Úsalo cuando:** `context: fork` está activado y quieres que un tipo específico de subagent ejecute el skill.
- **Evítalo cuando:** `context: fork` no está activado — el campo `agent` no tiene efecto sin él.
- **Ejemplo:**
  ```yaml
  context: fork
  agent: Explore
  ```

---

### `hooks`

- **Tipo:** mapa YAML de eventos del ciclo de vida a comandos de shell.
- **Por defecto:** ninguno.
- **Estándar:** solo Claude Code
- **Úsalo cuando:** necesitas ejecutar setup o teardown alrededor de la ejecución del skill — por ejemplo, arrancar un servidor local antes de que se ejecute un skill de pruebas, o enviar una notificación a Slack tras un skill de despliegue.
- **Evítalo cuando:** el setup puede hacerse dentro del propio cuerpo del skill. Los hooks añaden complejidad; úsalos solo cuando necesites efectos secundarios que se ejecutan fuera del turno de Claude.
- **Ejemplo:**
  ```yaml
  hooks:
    after: echo "Skill completed at $(date)" >> ~/.claude/skill-log.txt
  ```

---

### `paths`

- **Tipo:** lista de patrones glob.
- **Por defecto:** ninguno. El skill está disponible en todos los contextos.
- **Estándar:** solo Claude Code
- **Úsalo cuando:** el skill debe autoactivarse solo cuando el usuario está trabajando con tipos de archivo o directorios específicos. Un skill de linting de frontend no debería activarse al editar una migración de Python. Las restricciones de paths hacen precisa la autoinvocación.
- **Evítalo cuando:** el skill es de propósito general. Restringir paths le impide activarse en contextos legítimos.
- **Ejemplo:**
  ```yaml
  paths:
    - "src/components/**"
    - "src/pages/**"
  ```

---

### `shell`

- **Tipo:** `bash` o `powershell`.
- **Por defecto:** `bash`.
- **Estándar:** solo Claude Code
- **Úsalo cuando:** `powershell` — en entornos Windows donde la inyección de context dinámico (bloques `` !`cmd` ``) usa sintaxis de PowerShell. Requiere `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` en el entorno.
- **Evítalo cuando:** estás en macOS o Linux, o tus comandos de inyección son shell POSIX puro. El valor por defecto `bash` es correcto en esos casos.
- **Ejemplo:**
  ```yaml
  shell: powershell
  ```

---

## Referencia de sustituciones de cadenas

Estas sustituciones están disponibles en el cuerpo del skill:

| Sustitución | Valor |
|---|---|
| `$ARGUMENTS` | La cadena completa de argumentos tal como la escribió el usuario |
| `$ARGUMENTS[N]` o `$N` | Argumento posicional con índice base 0 (se aplican comillas estilo shell) |
| `$name` | Argumento nombrado declarado en el campo `arguments` |
| `${CLAUDE_SESSION_ID}` | El identificador de la sesión actual de Claude Code |
| `${CLAUDE_EFFORT}` | El nivel de effort actual |
| `${CLAUDE_SKILL_DIR}` | Path absoluto al directorio que contiene este `SKILL.md` |

---

## Ejemplos

El directorio `examples/` contiene un skill que muestra cómo combinar los campos más habitualmente pareados en una herramienta práctica.

- `examples/well-documented-skill/` — un skill de auditoría de dependencias que usa `name`, `description`, `when_to_use`, `argument-hint` y `allowed-tools`

Consulta el README en ese directorio para una explicación campo por campo de las decisiones.

## Siguiente lección

[Lección 02: control de invocación](../lesson-02-invocation-control/)
