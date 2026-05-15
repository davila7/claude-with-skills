---
title: "Solución de problemas con Skills"
---

Guía diagnóstica para los problemas más comunes con skills.

---

## El skill no aparece en el menú /

**Paso 1: Comprueba el nombre del directorio y el campo `name` del frontmatter.**

La especificación requiere que el nombre del directorio coincida con el campo `name`. Si difieren, el skill puede fallar al registrarse. Verifica ambos:

```bash
ls ~/.claude/skills/         # directory names
grep "^name:" ~/.claude/skills/*/SKILL.md   # name fields
```

**Paso 2: Verifica que SKILL.md exista directamente en el directorio del skill.**

El archivo debe estar en `skill-name/SKILL.md`, no anidado más profundo. `skill-name/src/SKILL.md` no se reconoce.

**Paso 3: Comprueba el valor de name.**

Los nombres válidos están en minúsculas, usan guiones como separadores, no contienen guiones consecutivos (`--`), no empiezan ni terminan con guion y tienen como máximo 64 caracteres. Un nombre como `my--skill` o `-skill` fallará al registrarse.

**Paso 4: Comprueba `user-invocable`.**

Si está definido `user-invocable: false`, el skill está intencionalmente oculto del menú `/`. Ese es el comportamiento correcto. Si lo quieres en el menú, elimina ese campo o ponlo a `true`.

**Paso 5: Reinicia Claude Code.**

Claude Code escanea los skills al arrancar. Si creaste un nuevo directorio de skills mientras Claude Code ya estaba en ejecución, el nuevo directorio no se detecta hasta el reinicio. Las ediciones a archivos SKILL.md existentes dentro de directorios ya conocidos se recargan en vivo sin reinicio. Los directorios nuevos requieren un reinicio.

---

## El skill no se dispara automáticamente

**Paso 1: Confirma que Claude puede ver el skill.**

Pregúntale a Claude directamente: "What skills are available?". Claude listará lo que puede ver, lo que revela si el skill está registrado y si su descripción está intacta.

**Paso 2: Revisa la descripción en busca de keywords de disparo.**

Claude empareja las peticiones del usuario con las descripciones de skill usando similitud semántica. Si la descripción usa jerga técnica pero los usuarios formulan las peticiones en lenguaje sencillo (o viceversa), Claude puede no hacer la conexión. Revisa la descripción para incluir las frases en lenguaje natural que los usuarios realmente escriben.

**Paso 3: Verifica que `disable-model-invocation` no esté activado.**

`disable-model-invocation: true` oculta el skill completamente a Claude. Si este campo está activado, Claude nunca lo auto-invocará, sin importar lo que diga el usuario.

**Paso 4: Comprueba el presupuesto de descripciones con `/doctor`.**

Ejecuta `/doctor` en Claude Code. Si el presupuesto de descripciones está desbordándose, algunas descripciones de skill están siendo descartadas. Un skill cuya descripción se descarte no puede auto-invocarse. Consulta la referencia de la matriz de invocación para opciones de ajuste.

**Paso 5: Prueba a reformular tu petición.**

Imita la descripción del skill más literalmente para probar si la descripción es el problema. Si invocar con una fraseología que refleja de cerca la descripción funciona pero la fraseología natural no, la descripción necesita más cobertura de keywords.

**Paso 6: Invoca directamente para confirmar que el skill funciona.**

Ejecuta `/skill-name` manualmente. Si funciona correctamente al invocarse manualmente, el cuerpo del skill está bien y solo el disparador de auto-invocación necesita mejorarse. Refuerza los campos `description` y `when_to_use`.

---

## El skill se dispara demasiado

**Paso 1: Haz la descripción más específica.**

Añade calificadores que estrechen el scope. "Only when the user explicitly asks to..." o "Specifically for tasks involving..." reducen los falsos positivos.

**Paso 2: Añade `disable-model-invocation: true`.**

Si la auto-invocación no se necesita en absoluto, desactívala. El skill permanece disponible para los usuarios vía `/name` sin que Claude lo dispare espontáneamente.

**Paso 3: Usa `paths` para restringir a archivos relevantes.**

Si el skill es específico de un tipo de archivo (por ejemplo, un formateador de Python), añade un campo `paths` para que solo aparezca cuando la sesión involucre archivos coincidentes:

```yaml
paths:
  - "**/*.py"
```

**Paso 4: Divide en dos skills.**

Crea una versión con `disable-model-invocation: true` para invocación controlada por el usuario y una versión separada con una descripción estrecha para auto-invocación en un disparador específico y bien definido. Esto es más limpio que intentar hacer que una única descripción sea lo suficientemente precisa como para auto-invocarse raramente.

---

## La salida de !`cmd` no aparece

**Paso 1: Comprueba `disableSkillShellExecution`.**

Si `disableSkillShellExecution: true` está activado en settings (proyecto o usuario), toda la ejecución inline de shell en skills está desactivada. Los bloques de shell producen silenciosamente cero salida. Elimínalo o ponlo a `false` para reactivarlo.

**Paso 2: Prueba el comando de forma independiente.**

Copia el comando del cuerpo del skill y ejecútalo en tu terminal. Si falla fuera del skill, fallará dentro del skill también. Arregla el comando primero.

**Paso 3: Comprueba el directorio de trabajo.**

Los comandos de shell en bloques de skill se ejecutan en el directorio del proyecto (el directorio en el que se abrió Claude Code), no en el directorio del skill. Los comandos que asumen que se ejecutan desde el directorio del skill fallarán o producirán una salida incorrecta. Usa `${CLAUDE_SKILL_DIR}` para referenciar archivos relativos al skill:

```
!`python3 ${CLAUDE_SKILL_DIR}/scripts/check.py`
```

**Paso 4: Comprueba stderr.**

Si el comando termina con código distinto de cero, Claude recibe la salida de error en lugar de la salida esperada. Esto suele ser más informativo que la salida esperada original — Claude típicamente describirá el error. Aborda el error de fondo del comando.

---

## La sustitución $ARGUMENTS no funciona

**Paso 1: Confirma que los tokens de sustitución aparecen en el cuerpo, no solo en el frontmatter.**

`$ARGUMENTS`, `$0`, `$1` y `$name` se sustituyen solamente en el texto del cuerpo del SKILL.md. No tienen efecto en los campos del frontmatter. Si quieres que Claude conozca el valor del argumento, debe aparecer en algún lugar del cuerpo.

**Paso 2: Comprueba la configuración de argumentos con nombre.**

Si usas la sintaxis `$name`, verifica que exista el campo de frontmatter `arguments:` y que liste los nombres de los argumentos en orden. Los nombres deben coincidir exactamente — `$component` requiere `component` en la lista de arguments. Una discrepancia deja `$component` como un string literal en vez de expandirlo.

**Paso 3: Pon entre comillas los argumentos de varias palabras.**

Los argumentos se separan por espacios. `/my-skill hello world` da `$0 = "hello"` y `$1 = "world"`. Si pretendes que `hello world` sea un único argumento, invoca con comillas: `/my-skill "hello world"`, lo que da `$0 = "hello world"`.

---

## Desbordamiento del presupuesto de descripciones de skill

**Síntoma:** Claude deja de auto-invocar skills que solían funcionar. Los skills aparecen en `/doctor` como truncados o descartados.

**Paso 1: Ejecuta `/doctor`.**

Este comando reporta el uso actual del presupuesto de descripciones, qué skills tienen descripciones truncadas y por cuánto se excede el presupuesto.

**Paso 2: Pon los skills de baja prioridad en modo solo-nombre.**

En `.claude/settings.local.json`, marca los skills que Claude raramente necesita auto-invocar:

```json
{
  "skillOverrides": {
    "my-reference-skill": "name-only",
    "my-seldom-used-skill": "name-only"
  }
}
```

Los skills solo-nombre siguen apareciendo en el menú `/` y siguen funcionando cuando se invocan, pero sus descripciones no se incluyen en el context de Claude, liberando presupuesto para skills de mayor prioridad.

**Paso 3: Aumenta la fracción de presupuesto.**

En `.claude/settings.json`:

```json
{
  "skillListingBudgetFraction": 0.02
}
```

El valor por defecto es `0.01` (1% del context). Doblarlo a `0.02` da a las descripciones el doble de espacio.

**Paso 4: Recorta el texto de la descripción.**

Pon la frase de disparo clave al principio de cada descripción. Recorta clichés como "This skill is designed to..." o "Use this skill when you want to...". Cada carácter cuenta para el tope por skill de 1536 caracteres.

---

## El skill deja de influir en el comportamiento tras la primera respuesta

El cuerpo del skill no caduca del context. Sigue ahí. El modelo está eligiendo otro comportamiento. Hay tres causas comunes:

**Causa 1: La compactación recortó el cuerpo del skill.**

Tras la auto-compactación, los skills se re-adjuntan con un tope de 5000 tokens por skill y 25000 tokens en total. Si el cuerpo del skill era más largo que 5000 tokens, la versión truncada puede carecer de instrucciones críticas. Re-invoca el skill con `/skill-name` para restaurar el contenido completo.

**Causa 2: El context competidor está pesando más que el skill.**

En una sesión larga, muchos mensajes y contenidos de archivos se acumulan en context. El context más reciente tiene más influencia. Si las instrucciones del skill se cargaron temprano en la sesión y ha ocurrido mucho desde entonces, el modelo puede priorizar el context reciente. Re-invoca el skill para mover su contenido a la posición actual en context.

**Causa 3: La descripción o el cuerpo necesitan un lenguaje de instrucción más fuerte.**

Añade lenguaje de instrucción explícito al cuerpo del skill: "Always...", "Every time you...", "Without exception...". Las orientaciones vagas como "consider using..." son fáciles de descartar para el modelo cuando otras señales apuntan en una dirección distinta.

---

## allowed-tools no pre-aprueba una herramienta

**Paso 1: Acepta el diálogo de confianza del workspace.**

Para skills con scope de proyecto (`.claude/skills/`), Claude Code requiere que aceptes un prompt de confianza del workspace para la carpeta del proyecto antes de que `allowed-tools` surta efecto. Si no has aceptado la confianza para este proyecto, la pre-aprobación de herramientas está silenciosamente inactiva.

**Paso 2: Comprueba la sintaxis.**

`allowed-tools` es un string separado por espacios con nombres de herramienta sensibles a mayúsculas y minúsculas. Errores comunes:

```yaml
# Wrong — lowercase bash
allowed-tools: bash read write

# Correct — title case
allowed-tools: Bash Read Write
```

Para combinaciones herramienta+patrón:

```yaml
# Wrong — no space around parens
allowed-tools: Bash(git*)

# Correct — space before paren pattern
allowed-tools: Bash(git *)
```

**Paso 3: Recuerda que allowed-tools pre-aprueba, no restringe.**

Las herramientas listadas en `allowed-tools` se ejecutan sin un prompt de permisos. Las herramientas no listadas siguen funcionando pero piden permiso de forma normal. Si ves prompts para herramientas que no están en tu lista, ese es el comportamiento esperado.

**Lista completa de nombres de herramienta para referencia:**

`Read`, `Write`, `Edit`, `MultiEdit`, `Bash`, `Grep`, `Glob`, `LS`, `WebFetch`, `WebSearch`, `Skill`, `Agent`, `TodoRead`, `TodoWrite`

Se requiere capitalización exacta.
