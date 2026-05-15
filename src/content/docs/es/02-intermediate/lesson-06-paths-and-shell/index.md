---
title: "Lección 06: paths y shell"
---

Dos campos controlan dónde y cómo se activa un skill: `paths` restringe la autoactivación a contextos de archivo específicos, y `shell` establece el intérprete usado para los comandos de inyección de context dinámico.

## El campo `paths`

### Qué hace

Cuando `paths` está configurado, el skill solo se autoactiva cuando el usuario está trabajando con archivos que coinciden con uno de los patrones glob. "Trabajando con" significa que el archivo está abierto, siendo editado o referenciado en la tarea actual.

```yaml
paths:
  - "src/components/**"
  - "src/pages/**"
```

Un skill con esta configuración no se autoactivará cuando el usuario esté editando un archivo de migración o una ruta de backend. Solo aflora cuando el context involucra archivos de componentes o páginas.

### Qué NO hace

`paths` no te impide invocar el skill directamente. Si escribes `/frontend-only-lint` mientras editas un archivo de backend, el skill se ejecuta. Las restricciones de paths solo afectan a la autoinvocación — cuando Claude decide por su cuenta activar un skill basándose en su description.

### Por qué usarlo

Sin restricciones de path, las palabras clave de la description de un skill podrían coincidir con contextos en los que el skill no es útil. Un skill de "comprobar props de componentes React" que se activa durante una sesión de debugging de Python es ruido. `paths` hace que la autoinvocación sea precisa.

### Sintaxis de patrones glob

Los patrones siguen convenciones estándar de glob:
- `*` — coincide con cualquier carácter dentro de un único segmento de path
- `**` — coincide con cualquier número de segmentos de path (incluido cero)
- `?` — coincide con exactamente un carácter
- `{a,b}` — coincide con `a` o `b`

Ejemplos:
- `"src/components/**"` — cualquier archivo en cualquier lugar bajo `src/components/`
- `"**/*.sql"` — cualquier archivo `.sql` en cualquier directorio
- `"migrations/**"` — cualquier archivo bajo un directorio `migrations/` a cualquier profundidad
- `"**/*.{test,spec}.{ts,js}"` — cualquier archivo de test en TypeScript o JavaScript
- `"db/migrate/**"` — archivos bajo `db/migrate/` específicamente

### Combinando múltiples patrones

Lista varios patrones para cubrir ubicaciones relacionadas:

```yaml
paths:
  - "src/components/**"
  - "src/pages/**"
  - "src/hooks/**"
```

El skill se autoactiva si el archivo actual coincide con cualquiera de los patrones listados.

---

## El campo `shell`

### Qué hace

`shell` establece el intérprete usado para ejecutar los comandos de inyección de context dinámico (los bloques `` !`cmd` `` y `` ```! `` en el cuerpo del skill).

```yaml
shell: bash
```

```yaml
shell: powershell
```

### Por defecto

`bash` es el valor por defecto. En macOS y Linux, deja este campo sin definir.

### Cuándo poner `shell: powershell`

En Windows, si tus comandos de inyección de context dinámico usan sintaxis de PowerShell (por ejemplo, `$env:PATH`, `Get-ChildItem` o `Select-Object`), pon `shell: powershell`.

La inyección con PowerShell también requiere que la variable de entorno `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` esté configurada. Sin ella, el campo se acepta pero podría no surtir efecto.

### Nota sobre portabilidad

Los skills que usan `shell: powershell` no se ejecutan correctamente en macOS o Linux. Si quieres un skill multiplataforma, escribe los comandos de inyección en sintaxis de shell POSIX y deja `shell` sin definir.

---

## Ejemplos

- `examples/frontend-only-lint/` — usa `paths` para restringir la autoactivación a archivos de componentes de frontend

## Siguiente lección

[Lección 07: model y effort](../lesson-07-model-and-effort/)
