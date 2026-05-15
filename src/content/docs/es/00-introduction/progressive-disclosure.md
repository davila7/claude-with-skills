---
title: "Carga progresiva: cómo se cargan los Skills en tres etapas"
---

Una de las propiedades más importantes del modelo de AgentSkills es que no carga todo de una vez. El context es un recurso finito, y cargar todos los skills completos al arranque sería un desperdicio y lento. En su lugar, los skills siguen un modelo de carga en tres etapas que mantiene el uso de context cercano a cero hasta que un skill realmente se necesita.

## Etapa 1 — Descubrimiento

Cuando Claude Code arranca, escanea los directorios de skills y carga solo los campos `name` y `description` del frontmatter de cada `SKILL.md`. Sin cuerpo, sin archivos de apoyo.

Coste: aproximadamente 100 tokens por skill.

Esto es suficiente para que el agente sepa qué skills existen y qué hacen. Cuando escribes una petición, Claude compara la petición con las descripciones que ya ha cargado y decide qué skill activar, si hay alguno.

Con 50 skills instalados, la Etapa 1 cuesta alrededor de 5.000 tokens — menos que un único mensaje de conversación de longitud media.

## Etapa 2 — Activación

Cuando el agente decide que un skill coincide con la tarea actual (ya sea porque lo invocaste por nombre con `/skill-name`, o porque la descripción coincidió con tu petición), carga el cuerpo completo de `SKILL.md`.

Tamaño recomendado del cuerpo: por debajo de 5.000 tokens / 500 líneas.

Aquí es donde vive tu procedimiento: los pasos, las reglas de decisión, el formato de salida, los casos límite. Una vez que el cuerpo está cargado, el agente sigue esas instrucciones para completar la tarea. En este punto, solo el skill que necesitas está en context — los otros 49 siguen en Etapa 1.

## Etapa 3 — Ejecución

Los archivos de apoyo — cualquier cosa en `references/`, `scripts/`, `assets/` u otros subdirectorios — no se cargan como parte de la Etapa 2. Solo se cargan cuando el agente los lee o los ejecuta explícitamente durante la ejecución de la tarea.

Esto significa que puedes tener un skill cuyo cuerpo tenga 200 líneas con cinco documentos de referencia que sumen 2.000 líneas, y nada del contenido de referencia se carga hasta que el agente llegue al paso que dice "lee references/api-conventions.md".

## Qué significa esto en la práctica

Puedes instalar tantos skills como necesites sin preocuparte por la inflación de context. El modelo de coste es:

- 50 skills instalados, ninguno activado: ~5.000 tokens (Etapa 1 para todos)
- 50 skills instalados, uno activado, sin referencias leídas: ~5.000 + tokens del cuerpo
- 50 skills instalados, uno activado, dos archivos de referencia leídos: ~5.000 + tokens del cuerpo + tokens de los archivos de referencia

El diseño te anima a escribir cuerpos de skill enfocados y a mover el detalle a archivos de referencia.

## Consejo práctico: cuándo mover contenido a references/

Si el cuerpo de tu skill crece más allá de unas 80 líneas, léelo y pregúntate qué partes son siempre necesarias y qué partes solo se necesitan para casos específicos. Mueve el detalle específico de cada caso a archivos en `references/`. Desde el cuerpo del skill, enlaza a ellos explícitamente:

```markdown
For the full list of supported API error codes, see references/error-codes.md.
```

Claude leerá ese archivo cuando llegue a esa instrucción. Hasta entonces, queda fuera del context. Esto mantiene la Etapa 2 rápida y deja más espacio para el contenido real de la tarea.
