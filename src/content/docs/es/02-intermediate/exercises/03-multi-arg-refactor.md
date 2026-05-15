---
title: "Ejercicio 03: renombrado de símbolo con varios argumentos"
---

Crea un skill que reciba tres argumentos nombrados y renombre un símbolo dentro de un alcance especificado. Este ejercicio se centra en el campo `arguments`, en las referencias a argumentos nombrados en el cuerpo y en una lógica segura de buscar y reemplazar.

## Objetivo

El skill recibe tres argumentos:
1. `old-name` — el nombre actual del símbolo
2. `new-name` — el nombre con el que reemplazarlo
3. `scope` — dónde buscar: `file`, `module` o `project`

Ejemplos de invocaciones:
```
/rename-symbol MyClass MyService file
/rename-symbol getUserById fetchUserById module
/rename-symbol legacyConfig appConfig project
```

## Qué escribir

El skill debe:

1. Declarar argumentos nombrados en el frontmatter: `arguments: [old-name, new-name, scope]`
2. Usar `$old-name`, `$new-name` y `$scope` en el cuerpo (no `$0`, `$1`, `$2`)
3. Poner `disable-model-invocation: true` — renombrar es una acción con efectos secundarios
4. Poner `argument-hint: [old-name] [new-name] [file|module|project]`
5. Incluir `allowed-tools` para el tooling que necesita (grep, sed, git diff, etc.)

## Definiciones de alcance

**`file`**: renombra solo dentro del archivo actual o del archivo mencionado explícitamente en la tarea.

**`module`**: renombra dentro del directorio que contiene el archivo actual y sus subdirectorios inmediatos.

**`project`**: renombra a lo largo de todo el proyecto, excluyendo `node_modules/`, `.git/`, `dist/` y `build/`.

## Requisitos de seguridad

El skill NO debe renombrar subcadenas. `MyClass` no debe renombrar `MyClassExtended` ni `loadMyClass`. Usa patrones con límite de palabra en tus comandos grep y sed.

El skill debe mostrar al usuario una vista previa antes de hacer cualquier cambio, y pedir confirmación.

## Validación

Escribe el skill y pruébalo en un proyecto pequeño:
1. Crea un archivo con un símbolo usado en tres sitios.
2. Invoca el skill con alcance `file`.
3. Confirma que muestra correctamente la vista previa de los cambios.
4. Confirma que no renombra coincidencias parciales.
5. Confirma que `git diff` muestra solo los cambios esperados tras la confirmación.

## Solución

Una solución desarrollada está en `solutions/03-rename-symbol/SKILL.md`.
