---
title: "Cheatsheet de Frontmatter"
---

Referencia rápida para todos los campos de frontmatter de SKILL.md.

---

## Todos los campos

### Estándar abierto AgentSkills.io (portable)

Estos campos están definidos por el estándar abierto AgentSkills.io. Los skills que usan solo estos campos siguen siendo portables entre runtimes compatibles.

| Campo | Tipo/Formato | Por defecto | Qué hace | Cuándo usarlo |
|---|---|---|---|---|
| `name` | string, minúsculas-guiones, máx. 64 caracteres | nombre del directorio | Nombre visible y alias del comando `/name` | Siempre — defínelo explícitamente para desacoplarlo del nombre del directorio |
| `description` | string, máx. 1024 caracteres | primer párrafo del cuerpo del SKILL.md | Le dice a Claude qué hace el skill y cuándo invocarlo | Siempre — Claude lee esto para decidir la auto-invocación |
| `license` | string | ninguno | Declara la licencia del contenido del skill | Al distribuir o publicar el skill públicamente |
| `compatibility` | string, máx. 500 caracteres | ninguno | Documenta requisitos del entorno como SO, runtime o tooling necesario | El skill requiere tooling, SO o entorno específicos que pueden no estar disponibles universalmente |
| `metadata` | mapa clave-valor | ninguno | Datos estructurados arbitrarios adjuntos al skill (versión, autor, tags, etc.) | Llevar control de versión, autoría o tags personalizados sin contaminar la description |
| `allowed-tools` | string de nombres de herramientas separados por espacios | ninguno | Pre-aprueba las herramientas listadas para que nunca pidan permiso durante el skill | El skill necesita herramientas específicas y las interrupciones romperían el flujo |

### Campos exclusivos de Claude Code

Estos campos los entiende Claude Code pero no forman parte del estándar portable de AgentSkills.io. Otros runtimes los ignorarán o producirán errores.

| Campo | Tipo/Formato | Por defecto | Qué hace | Cuándo usarlo |
|---|---|---|---|---|
| `when_to_use` | string | ninguno | Frases de disparo adicionales que se añaden a la description para la coincidencia en auto-invocación | Necesitas keywords extra sin hacer la description principal demasiado verbosa |
| `argument-hint` | string | ninguno | Hint corto mostrado en la UI de autocompletado junto al nombre del skill | El skill acepta argumentos y quieres que los usuarios sepan qué escribir |
| `arguments` | string o lista de strings | ninguno | Posiciones de argumentos con nombre mapeadas a variables `$name` en el cuerpo del skill | El skill toma múltiples argumentos distintos y las referencias con nombre son más claras que las basadas en índice |
| `disable-model-invocation` | boolean | `false` | Oculta el skill por completo a Claude; solo un usuario puede invocarlo con `/name` | Flujos con efectos secundarios (deploy, send, delete) donde debes controlar el momento |
| `user-invocable` | boolean | `true` | Cuando se pone a `false`, oculta el skill del menú `/` | Skills de conocimiento de fondo que Claude debe usar pero los usuarios nunca invocan directamente |
| `model` | string | hereda el modelo de la sesión | Sobrescribe el model usado para el turno de ejecución de este skill | Análisis profundo que necesita un modelo más grande (opus) o una tarea trivial que puede usar uno más barato (haiku) |
| `effort` | string: `low`, `medium`, `high`, `xhigh` o `max` | hereda el effort de la sesión | Sobrescribe el effort de razonamiento para el turno de este skill | Tareas que necesitan razonamiento de nivel ultrathink o generación simple que no necesita pensamiento extendido |
| `context` | string: `fork` | ninguno | Ejecuta el skill en un subagent aislado para que no contamine el context principal | Skills largos o exploratorios cuyos pasos intermedios no deben persistir en la conversación principal |
| `agent` | string | `general-purpose` | Especifica el tipo de subagent cuando se establece `context: fork` | Quieres un subagent de solo lectura estilo Explore u otro perfil específico de agent |
| `hooks` | mapa | ninguno | Hooks de ciclo de vida con scope a este skill (pre-tool, post-tool, on-exit, etc.) | Auto-formateo de salida, validación de resultados o envío de notificaciones al usar herramientas específicas |
| `paths` | lista de patrones glob | ninguno | Auto-activa o restringe el skill a sesiones que involucren archivos que coincidan | Skills específicos de lenguaje o dominio que solo deberían aparecer para archivos relevantes |
| `shell` | string: `bash` o `powershell` | `bash` | Sobrescribe el shell usado para bloques inline `!`cmd`` | Skills exclusivos de Windows que usan comandos de PowerShell |

---

## Matriz de modos de invocación

Controla quién puede invocar el skill y qué aparece en context.

| Frontmatter | Usuario `/name` | Claude auto-invoca | Description en context | Cuándo se carga el cuerpo completo |
|---|---|---|---|---|
| (por defecto) | Sí | Sí | Sí | Cuando lo invoca el usuario o Claude |
| `disable-model-invocation: true` | Sí | No | No | Cuando el usuario invoca con `/name` |
| `user-invocable: false` | No | Sí | Sí | Cuando Claude invoca automáticamente |
| Ambos `disable-model-invocation: true` Y `user-invocable: false` | No | No | No | Nunca — el skill es permanentemente inaccesible |

---

## Referencia rápida de sustitución de strings

| Sintaxis | Se expande a |
|---|---|
| `$ARGUMENTS` | String completo de argumentos tal como se escribió tras el nombre del skill |
| `$ARGUMENTS[0]` o `$0` | Primer argumento separado por espacios (índice 0, respeta el quoting de shell) |
| `$ARGUMENTS[1]` o `$1` | Segundo argumento |
| `$name` | Argumento con nombre desde la posición definida en el frontmatter `arguments` |
| `${CLAUDE_SESSION_ID}` | UUID que identifica la sesión actual de Claude Code |
| `${CLAUDE_EFFORT}` | String del nivel actual de effort: `low`, `medium`, `high`, `xhigh` o `max` |
| `${CLAUDE_SKILL_DIR}` | Ruta absoluta al directorio que contiene el archivo SKILL.md |

---

## Patrones comunes

Pre-flight check — ejecuta un comando de shell inline e incluye su salida en context:

```
!`git status --short`
```

Bloque shell multilínea — ejecuta múltiples comandos como un bloque:

````
```!
git fetch origin
git log --oneline origin/main..HEAD
```
````

Ejecuta un script incluido desde el directorio del skill — usa siempre `${CLAUDE_SKILL_DIR}` para que la ruta funcione en cualquier scope:

```
Bash: python3 ${CLAUDE_SKILL_DIR}/scripts/my_script.py
```

Skill que se ejecuta en un subagent aislado para evitar contaminar el context principal:

```yaml
context: fork
agent: Explore
```

El subagent precarga un skill para que esté disponible dentro del context forked — en el archivo de definición del agent, añade:

```yaml
skills: [skill-name]
```
