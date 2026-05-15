---
title: "Ejercicio 01: Construye tu primer skill"
---

## Objetivo

Crea un skill llamado `explain-code` que le pida a Claude que explique un fragmento de código en lenguaje sencillo, como si hablara con alguien que no conoce el lenguaje de programación.

## Requisitos

Tu skill debe:

1. Tener un campo `name` válido: `explain-code` (minúsculas, solo guiones, coincide con el nombre del directorio)
2. Tener un campo `description` que incluya al menos dos o tres palabras clave de activación para que Claude lo auto-invoque de forma fiable
3. Tener un cuerpo con pasos claros que le digan a Claude qué hacer

## Qué poner en el cuerpo

Piensa en qué necesita Claude para hacer esto bien:

- **¿Qué código?** Claude necesita saber qué código explicar. El cuerpo debe decirle a Claude que lea el archivo o el código que se está discutiendo, o el último archivo mencionado en la conversación.
- **¿Para qué audiencia?** El skill es para alguien no familiarizado con el lenguaje. El cuerpo debe decirlo explícitamente.
- **¿Con qué profundidad?** El cuerpo debe especificar: propósito general, flujo principal de datos, cualquier lógica no obvia. También debe decir qué omitir — no sobreexplicar partes que son obvias por el nombrado.

## Pistas

- La description impulsa la auto-invocación. Un usuario que escriba "explain this code to me" o "walk me through this" debería disparar el skill. Incluye esas frases como guía en la description.
- El cuerpo debe guiar a Claude para que compruebe en qué lenguaje está escrito el código — el estilo de explicación difiere entre un script de bash y un componente de React.
- Usa una analogía solo si realmente ayuda. No fuerces una.

## Validación

1. Crea el archivo del skill en: `~/.claude/skills/explain-code/SKILL.md`
2. Abre Claude Code en cualquier proyecto que tenga código que quieras entender
3. Prueba la auto-invocación: escribe "explain this code to me" o "walk me through this function" y comprueba que el skill se activa
4. Prueba la invocación directa: escribe `/explain-code` y verifica que funciona
5. Comprueba la calidad de la salida: ¿está en lenguaje sencillo? ¿Cubre las tres áreas requeridas (propósito, flujo de datos, lógica no obvia)?

## Solución

Una solución de referencia está en `solutions/01-explain-code/SKILL.md`. Intenta escribir tu propia versión primero — no hay una única respuesta correcta, y tus palabras clave de description deberían reflejar cómo pides explicaciones de forma natural.
