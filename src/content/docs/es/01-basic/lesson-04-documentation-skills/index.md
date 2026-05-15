---
title: "Lección 04: Skills de documentación"
---

La documentación es el caso de uso más común para los skills. Casi todos los equipos tienen documentación que escriben repetidamente: READMEs para nuevos proyectos, ADRs para decisiones técnicas, JSDoc para funciones exportadas, notas de release, guías de onboarding.

## Qué distingue a la documentación de las tareas repetitivas

Los skills de tareas repetitivas tratan principalmente de **procedimiento** — haz estos pasos en este orden. Los skills de documentación tratan de **conocimiento más formato**.

Un buen skill de documentación codifica dos cosas:

1. **Qué información recopilar** — qué archivos leer, qué preguntas responder, qué contexto importa
2. **Cómo estructurar la salida** — orden de secciones, niveles de encabezado, contenido obligatorio, secciones opcionales

Sin un formato de salida opinado, los resultados se desvían. El README de un desarrollador tiene Installation primero, el de otro lo pone después de una introducción extensa. Un skill con una plantilla explícita elimina esa inconsistencia.

## La consistencia como valor principal

Cuando todo el equipo usa el mismo skill `adr-writer`, cada ADR del repository sigue la misma plantilla. Un lector que abra cualquier ADR sabe exactamente dónde encontrar el contexto, la decisión y las consecuencias. No necesita procesar mentalmente una disposición distinta cada vez.

Esta consistencia es lo que separa un skill de documentación de simplemente pedirle a Claude que "write a README". El skill es el acuerdo del equipo sobre cómo se ve un README, capturado una vez y reutilizado para siempre.

## Cuándo escribir un skill de documentación

- El mismo tipo de documentación se produce más de una vez (cada proyecto recibe un README, cada decisión significativa recibe un ADR)
- Personas distintas producen el mismo tipo de documento y los resultados son inconsistentes
- Un tipo de documento tiene secciones obligatorias que se olvidan a menudo (consideraciones de seguridad, licencia, notas de migración)
- El documento requiere recopilar contexto del codebase antes de escribir (el agente necesita leer archivos, no solo rellenar una plantilla)

## Ejemplos en esta lección

| Skill | Qué produce |
|-------|-----------------|
| `readme-generator` | Un README completo analizando el codebase |
| `jsdoc-writer` | Comentarios JSDoc para funciones sin documentar |
| `adr-writer` | Un Architecture Decision Record en formato MADR |

## Siguiente lección

[Lección 05: Invocar skills](../lesson-05-invoking/)
