---
title: "Lección 04: argumentos"
---

Los skills pueden aceptar argumentos escritos tras el nombre del skill. Esta lección cubre todas las formas de acceder a esos argumentos en el cuerpo del skill.

## La cadena completa de argumentos: `$ARGUMENTS`

La forma más sencilla de usar argumentos. `$ARGUMENTS` se expande a la cadena entera que el usuario escribió tras el nombre del skill.

```
/fix-issue 42
```

En el cuerpo, `$ARGUMENTS` se convierte en `42`.

```
/search-docs "how does auth work"
```

En el cuerpo, `$ARGUMENTS` se convierte en `how does auth work` (sin las comillas).

Usa `$ARGUMENTS` cuando el skill recibe una única entrada de forma libre y no necesitas dividirla en partes.

## Acceso posicional: `$ARGUMENTS[N]` y `$N`

Cuando necesitas acceder a argumentos individuales, usa la sintaxis de índice base 0.

```
/migrate-component MyButton React Vue
```

- `$ARGUMENTS[0]` o `$0` → `MyButton`
- `$ARGUMENTS[1]` o `$1` → `React`
- `$ARGUMENTS[2]` o `$2` → `Vue`

Ambas sintaxis son equivalentes. `$0`, `$1`, `$2` es más corto y más legible en el texto del cuerpo.

### Argumentos de varias palabras con comillas

Los argumentos se dividen por defecto por espacios en blanco. Para pasar un argumento de varias palabras como un único valor, entrecomíllalo:

```
/migrate-component "My Button" React Vue
```

- `$0` → `My Button`
- `$1` → `React`
- `$2` → `Vue`

Esto sigue las reglas estándar de comillas estilo shell. Funcionan tanto las comillas simples como las dobles.

## Argumentos nombrados: el campo `arguments`

Cuando un skill recibe varios argumentos posicionales, los nombres son más claros que los índices. Declara los argumentos nombrados en el frontmatter:

```yaml
arguments: [old-name, new-name, scope]
```

O como una cadena separada por espacios:

```yaml
arguments: old-name new-name scope
```

En el cuerpo, refiérete a ellos por nombre: `$old-name`, `$new-name`, `$scope`.

Los argumentos nombrados se mapean posicionalmente. El primer argumento que el usuario escribe se mapea al primer nombre de la lista, el segundo al segundo, y así sucesivamente.

```
/rename-symbol MyClass MyService project
```

Con `arguments: [old-name, new-name, scope]`:
- `$old-name` → `MyClass`
- `$new-name` → `MyService`
- `$scope` → `project`

## El campo argument-hint

El campo `argument-hint` controla lo que aparece en la interfaz de autocompletado cuando el usuario escribe `/skill-name`:

```yaml
argument-hint: [issue-number]
```

La pista es puramente cosmética — ayuda a los usuarios a saber qué escribir. No afecta a cómo se comportan `$ARGUMENTS` o los argumentos nombrados.

Usa corchetes para descripciones opcionales o posicionales, y texto plano para cualquier cosa más compleja:

```yaml
argument-hint: [old-name] [new-name] [file|module|project]
```

## Qué pasa cuando no existe placeholder `$ARGUMENTS`

Si el cuerpo del skill no contiene ninguna referencia a `$ARGUMENTS` y el usuario escribe un argumento, Claude Code añade lo siguiente al final del cuerpo del skill antes de enviarlo a Claude:

```
ARGUMENTS: <la cadena de argumentos>
```

Claude lo ve y aún puede usar el argumento. Sin embargo, la ubicación es menos predecible que una referencia explícita a `$ARGUMENTS`. Para mayor claridad, incluye siempre `$ARGUMENTS` o una referencia a argumento nombrado en el cuerpo si esperas argumentos.

## Ejemplos

- `examples/fix-issue/` — un único `$ARGUMENTS` para el número de un issue de GitHub
- `examples/migrate-component/` — tres argumentos posicionales `$0`, `$1`, `$2`
- `examples/named-args/` — argumentos nombrados con `arguments: [issue, prefix]`

## Siguiente lección

[Lección 05: inyección de context dinámico](../lesson-05-dynamic-context/)
