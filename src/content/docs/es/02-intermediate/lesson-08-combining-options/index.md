---
title: "Lección 08: combinando opciones"
---

Los campos individuales del frontmatter son directos. El reto es decidir qué combinación usar para un skill específico. Esta lección ofrece un marco de decisión y documenta los errores más comunes.

## Marco de decisión

Trabaja estas cuatro preguntas en orden:

### 1. ¿Tiene este skill efectos secundarios?

Los efectos secundarios incluyen: hacer push a un remoto, enviar mensajes, escribir a servicios externos, borrar archivos, ejecutar despliegues, disparar jobs de CI.

Si sí: pon `disable-model-invocation: true`. No quieres que Claude lo dispare automáticamente.

Si no: déjalo sin definir. La autoinvocación es segura y útil.

### 2. ¿Es esto un skill o conocimiento de fondo?

Si el skill es una acción (haz X, genera Y, despliega Z): deja `user-invocable` en su valor por defecto (true). El usuario debería poder invocarlo.

Si el skill es conocimiento que moldea el comportamiento de Claude (aplica estas convenciones, usa este formato de respuesta, ten en cuenta estas restricciones): pon `user-invocable: false`. No debería aparecer en el menú `/`.

### 3. ¿Necesita este skill datos en vivo?

Si sí: añade inyección `` !`cmd` `` para los datos específicos que necesita (estado de git, información del entorno, status de PR, valores de configuración). Inyecta solo lo que Claude necesita — evita inyectar salidas grandes que inflen el tamaño del context.

Si no: omite la inyección.

### 4. ¿Debería este skill activarse solo para ciertos tipos de archivo?

Si sí: pon `paths` con los patrones glob apropiados.

Si no: déjalo sin definir.

Tras responder estas cuatro preguntas, añade `allowed-tools` para cualquier tooling que el skill necesite usar sin pedir permiso, y considera `model` y `effort` solo si este skill tiene un requisito de coste/capacidad claramente distinto al de la sesión por defecto.

---

## Patrones comunes

### Flujo de despliegue seguro

```yaml
disable-model-invocation: true      # tiene efectos secundarios
argument-hint: [environment]        # el usuario especifica el destino
allowed-tools: Bash(npm *) Bash(git *)  # preaprobar los comandos necesarios
```

El cuerpo usa `$ARGUMENTS` para el entorno de destino y `` !`git status` `` para una comprobación previa.

### Skill de conocimiento de fondo

```yaml
user-invocable: false               # conocimiento, no una acción
# la description cubre todas las palabras clave de activación
```

El cuerpo contiene las convenciones, reglas o context. Sin argumentos, sin necesidad de inyección.

### Formateador consciente de path

```yaml
paths: ["src/**", "lib/**"]         # solo relevante para archivos fuente
allowed-tools: Bash(npx prettier *) # preaprobar el formateador
user-invocable: false               # activado por Claude tras ediciones
```

El cuerpo describe las reglas de formateo e instruye a Claude para ejecutar prettier tras las ediciones.

### Skill de investigación aislada

```yaml
context: fork                       # ejecutar en subagent aislado
agent: Explore                      # usar el subagent Explore
allowed-tools: Read Grep Glob       # tooling de solo lectura
```

El cuerpo describe la tarea de investigación. El fork evita que la salida grande de investigación contamine el context principal.

---

## Errores comunes

### Poner a la vez `disable-model-invocation: true` y `user-invocable: false`

```yaml
# No hagas esto
disable-model-invocation: true
user-invocable: false
```

Con ambos activos, el skill es inaccesible:
- Claude no puede invocarlo (la description no está en el context de Claude)
- Tú no puedes invocarlo (no está en el menú `/`)

La única manera de ejecutarlo es `claude -p "/skill-name"` en modo headless. Si eso es intencional, documéntalo explícitamente en la description. Si no es intencional, has creado un skill que nadie puede usar.

### Olvidar `allowed-tools` en un skill con `disable-model-invocation: true`

```yaml
disable-model-invocation: true
# allowed-tools omitido
```

Sin `allowed-tools`, Claude pedirá permiso antes de cada llamada de tooling durante la ejecución del skill. Para un flujo de despliegue con cinco comandos de git y dos de npm, son siete prompts. El usuario tiene que pulsar a través de todos ellos. Anula el propósito de un flujo estructurado; añade `allowed-tools` para los comandos específicos que necesita el skill.

### Dar permisos en exceso a `allowed-tools`

```yaml
allowed-tools: Bash(*)    # permite cualquier comando bash
```

Esto preaprueba cualquier comando de shell posible. Anula el propósito de acotar. Lista solo los comandos específicos que necesita el skill, usando los patrones más estrechos que aún funcionen:

```yaml
allowed-tools: Bash(npm test) Bash(npm run build) Bash(git status) Bash(git tag *) Bash(git push *)
```

### Usar `paths` para skills dirigidos al usuario

Si un usuario espera escribir `/my-skill` y que funcione en cualquier sitio, no pongas `paths`. Las restricciones de path solo reducen falsos positivos de autoinvocación — no añaden corrección. Un skill de despliegue no debería tener `paths` definido; debería funcionar desde cualquier context.

---

## Ejemplos

- `examples/safe-deploy/` — combina `disable-model-invocation`, `argument-hint`, `allowed-tools` e inyección dinámica en un flujo de despliegue completo
- `examples/on-edit-formatter/` — combina `paths`, `allowed-tools` y `user-invocable: false` para un formateador de fondo que se ejecuta tras ediciones
