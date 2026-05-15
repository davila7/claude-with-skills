---
title: "Lección 07: model y effort"
---

Dos campos del frontmatter te permiten elegir un model y un nivel de effort de razonamiento distintos para un skill específico, independientes de los valores por defecto de la sesión.

## El campo `model`

```yaml
model: haiku
```

Valores válidos: `haiku`, `sonnet`, `opus`, una cadena de ID de modelo completo (p. ej., `claude-opus-4-5`) o `inherit`.

`inherit` es el valor por defecto — el skill usa el model con el que esté corriendo la sesión actual.

### Cuándo sobrescribir el model

**Usa `haiku`** para tareas rápidas, bien definidas y que no requieren razonamiento complejo:
- Formatear un archivo según una guía de estilo
- Extraer campos específicos de datos estructurados
- Generar boilerplate a partir de una plantilla
- Transformaciones simples de un solo paso

**Usa `sonnet`** para la mayoría de tareas de programación. Es el valor por defecto para los skills incluidos con Claude Code porque equilibra bien capacidad y velocidad para la mayoría de flujos de desarrollo.

**Usa `opus`** para tareas que genuinamente requieren razonamiento extendido:
- Análisis arquitectónico o decisiones de diseño con compromisos significativos
- Auditorías de seguridad donde pasar por alto una vulnerabilidad sutil tiene consecuencias reales
- Análisis de causa raíz para bugs complejos donde intentos previos han fallado
- Revisión de cambios mayores en infraestructura crítica

### Compromiso de coste

Estos son multiplicadores ilustrativos, no precios exactos. Los precios reales varían según la generación del modelo y deberían verificarse en anthropic.com/pricing:

| Model | Coste relativo | Mejor para |
|---|---|---|
| Haiku | ~1x | Formateo, extracción, boilerplate |
| Sonnet | ~5x | La mayoría de tareas de programación (por defecto de sesión) |
| Opus | ~25x | Arquitectura, seguridad, debugging complejo |

Un skill que usa `model: opus` cuesta aproximadamente 25 veces más por invocación que uno de haiku. Para un skill que ejecutas una vez para una auditoría de seguridad seria, vale la pena. Para un skill que ejecutas tras cada edición de archivo, haiku es casi con seguridad la elección correcta.

### El override es temporal

El override del model se aplica solo al turno del skill. El siguiente prompt en la sesión usa el model de la sesión, no el del skill.

## El campo `effort`

```yaml
effort: high
```

Valores válidos: `low`, `medium`, `high`, `xhigh`, `max`.

El effort controla cuánto razonamiento extendido aplica el modelo antes de responder. Mayor effort tarda más y cuesta más, pero produce mejores resultados en tareas que se benefician de pensamiento más profundo.

### Cuándo sobrescribir el effort

**Usa `effort: low`** para tareas donde la respuesta es inmediata y mecánica: una transformación simple de cadena, una comprobación sí/no, una pasada de formateo de código.

**Usa `effort: high` o `xhigh`** para tareas que se benefician de que el modelo considere múltiples enfoques antes de responder: decisiones de arquitectura, análisis de seguridad, optimizar un algoritmo complejo o cualquier tarea donde el valor por defecto de la sesión produce resultados que pasan por alto consideraciones importantes.

**Usa `effort: max`** con moderación. Es el equivalente a pedirle al modelo que piense lo más fuerte que pueda. Resérvalo para problemas genuinamente difíciles donde un effort menor ya ha producido resultados insatisfactorios.

### Combinando model y effort

Los dos campos son independientes:

```yaml
model: opus
effort: high
```

Esto ejecuta el modelo más capaz con razonamiento extendido — apropiado para una auditoría de seguridad o una pregunta arquitectónica difícil. También es la combinación más cara.

```yaml
model: haiku
effort: low
```

Esta es la combinación más rápida y barata — apropiada para una pasada de formateo o una tarea simple de generación de código.

## Ejemplos

- `examples/deep-analysis/` — usa `model: opus` y `effort: high` para análisis arquitectónico y revisiones de seguridad

## Siguiente lección

[Lección 08: combinando opciones](../lesson-08-combining-options/)
