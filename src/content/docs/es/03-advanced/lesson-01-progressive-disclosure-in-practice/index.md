---
title: "Lección 01: Divulgación progresiva en la práctica"
---

La especificación de skills recomienda mantener el SKILL.md por debajo de 500 líneas. Ese es un techo, no un objetivo. Esta lección trata sobre por qué 80 líneas es un mejor objetivo para el patrón de navegador, y cómo estructurar un skill de modo que el contenido que los usuarios rara vez necesitan nunca llegue a cargarse.

## El modelo de carga de contexto

Los skills se cargan en tres etapas:

**Etapa 1 — Solo nombre y descripción.** Esto es lo que Claude ve cuando escanea todos los skills disponibles para decidir su relevancia. Coste: aproximadamente 100 tokens por skill, independientemente de lo largo que sea el cuerpo.

**Etapa 2 — Cuerpo del SKILL.md.** Esto se carga cuando Claude decide que el skill es relevante para la tarea actual. Coste: proporcional a la longitud del SKILL.md.

**Etapa 3 — Referencias y archivos de soporte.** Estos se cargan solo si el cuerpo del skill le indica explícitamente a Claude que los lea. Coste: proporcional al tamaño del archivo, y solo se paga cuando surge esa subtarea.

Un SKILL.md monolítico de 500 líneas paga el coste de la Etapa 2 en cada invocación. Un SKILL.md tipo navegador de 60 líneas con cuatro archivos de referencia de 120 líneas paga el coste de la Etapa 2 cada vez, pero el coste de la Etapa 3 solo cuando se necesita esa subtarea específica. Si los usuarios invocan un skill de extracción de PDF principalmente para extracción de texto y rara vez para rellenar formularios, la referencia de formularios casi nunca se carga.

## El patrón de navegador

El SKILL.md navegador hace tres cosas:

1. Describe lo que el skill puede hacer (un párrafo corto o una lista de viñetas)
2. Apunta a cada archivo de referencia con una descripción de una frase sobre cuándo leerlo
3. Proporciona una tabla de referencia rápida de los comandos más comunes

La descripción de una frase para cada referencia es la pieza crítica. Claude necesita decidir qué referencia leer basándose en lo que el usuario pidió — sin leer ninguna primero. Si la descripción es vaga, Claude carga todo por seguridad. Si la descripción es precisa, Claude carga exactamente una.

**Buena descripción de referencia:** `consulta la [guía de extracción](references/extraction.md) — cómo manejar layouts multi-columna, rangos de página específicos y extracción de tablas`

**Mala descripción de referencia:** `consulta la [guía de extracción](references/extraction.md) — más detalles`

## Estructura recomendada

```
my-skill/
├── SKILL.md              <- vista general + navegación (objetivo: menos de 80 líneas)
├── references/
│   ├── subtask-a.md      <- se carga cuando surge la tarea A
│   ├── subtask-b.md      <- se carga cuando surge la tarea B
│   └── subtask-c.md      <- se carga cuando surge la tarea C
└── scripts/
    └── helper.py         <- ejecutado por Claude, no leído en el contexto
```

Los scripts en el directorio `scripts/` se ejecutan con `Bash` — su código fuente no se carga en el contexto a menos que Claude los lea explícitamente con la tool `Read`. Esta es otra forma de divulgación progresiva: los detalles de implementación de un script son gratuitos hasta que alguien pregunta cómo funciona el script.

## Cómo escribir archivos de referencia

Como los archivos de referencia se cargan bajo demanda y llevan información detallada, pueden y deben ser exhaustivos. Incluye:

- Comandos exactos con flags copiables y pegables
- Casos límite y cómo manejarlos
- Mensajes de error que el usuario podría ver y qué significan
- Qué hacer cuando el enfoque principal falla

Un archivo de referencia de 150 líneas para una subtarea poco usada no es un problema — se carga con poca frecuencia y le da a Claude todo lo que necesita cuando se carga.

## El ejemplo pdf-toolkit

El directorio `examples/pdf-toolkit/` demuestra el patrón de navegador para un skill realista con múltiples capacidades. El SKILL.md tiene 35 líneas. Tres archivos de referencia cubren extracción, rellenado de formularios y fusión en detalle. Tres scripts de Python manejan las operaciones reales sobre los archivos.

Instálalo y prueba el patrón:

```bash
cp -r examples/pdf-toolkit ~/.claude/skills/
```

Luego prueba:
- `/pdf-toolkit extract my-file.pdf` — Claude lee el navegador SKILL.md y la referencia de extracción; las referencias de fusión y formularios nunca se cargan
- `/pdf-toolkit fill my-form.pdf output.pdf name="Jane Smith"` — Claude lee SKILL.md y la referencia de formularios; las otras dos permanecen frías

Observa el coste de contexto en la sesión — se mantiene proporcional a lo que realmente pediste.

## Siguiente lección

[Lección 02: Scripts incluidos con ${CLAUDE_SKILL_DIR}](../lesson-02-supporting-scripts/)
