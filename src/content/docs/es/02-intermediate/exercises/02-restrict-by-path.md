---
title: "Ejercicio 02: restringe un skill por path"
---

Crea un skill que se autoactive solo cuando el usuario está trabajando con archivos de migración de base de datos. Este ejercicio se centra en el campo `paths` y en escribir un cuerpo de skill que haga cumplir convenciones estructurales.

## Objetivo

El skill debe:

1. Autoactivarse cuando el usuario abre, edita o referencia un archivo que coincide con:
   - `migrations/**` (cualquier archivo bajo un directorio de migraciones)
   - `*.sql` (cualquier archivo SQL en la raíz del proyecto)
   - `db/migrate/**` (directorio de migraciones estilo Rails)

2. Comprobar convenciones de nombrado de archivos de migración:
   - Formato con prefijo de timestamp: `YYYYMMDDHHMMSS_description.sql` (p. ej., `20260513143207_add_user_roles.sql`)
   - Formato secuencial: `NNNN_description.sql` (p. ej., `0042_add_user_roles.sql`)
   - Reportar nombres no conformes como advertencia

3. Avisar sobre operaciones SQL potencialmente peligrosas:
   - `DROP TABLE` sin una comprobación previa (como `DROP TABLE IF EXISTS`)
   - `DELETE` sin una cláusula `WHERE`
   - `UPDATE` sin una cláusula `WHERE`
   - `TRUNCATE` en cualquier tabla
   - Eliminación de columnas (`DROP COLUMN`) — la marca como aviso, no necesariamente como error

4. Buscar un rollback o un comentario que marque la migración como irreversible.

## Qué escribir

Crea `SKILL.md` en un nuevo directorio. Piensa en:

- ¿Qué patrones `paths` cubren las tres convenciones de directorio de migración anteriores?
- ¿Debería ser `user-invocable: false` o dejarse por defecto?
- ¿Necesita este skill algún `allowed-tools`?
- ¿Debería estar `disable-model-invocation` activado?

## Formato de salida

El skill debe producir un checklist:

```
Migration review: 20260513143207_add_user_roles.sql

[ ] Naming convention: PASS / FAIL: <reason>
[ ] Rollback present: YES / NO / MARKED IRREVERSIBLE
[ ] Dangerous operations: NONE / WARNING: <list each one with line number>
```

## Validación

1. Crea un archivo de migración de prueba con al menos una operación peligrosa y un nombre no conforme.
2. Abre ese archivo en Claude Code.
3. Confirma que el skill se activa automáticamente (sin que tú escribas `/skill-name`).
4. Confirma que la salida coincide con el formato de checklist esperado.
5. Confirma también que el skill NO se activa cuando abres un archivo TypeScript o Python normal.

## Solución

Una solución desarrollada está en `solutions/02-migration-guard/SKILL.md`.
