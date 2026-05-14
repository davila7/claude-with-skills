# Lesson 04: Arguments

Skills can accept arguments typed after the skill name. This lesson covers every way to access those arguments in the skill body.

## The full argument string: `$ARGUMENTS`

The simplest way to use arguments. `$ARGUMENTS` expands to the entire string the user typed after the skill name.

```
/fix-issue 42
```

In the body, `$ARGUMENTS` becomes `42`.

```
/search-docs "how does auth work"
```

In the body, `$ARGUMENTS` becomes `how does auth work` (without the quotes).

Use `$ARGUMENTS` when the skill takes a single free-form input and you do not need to split it into parts.

## Positional access: `$ARGUMENTS[N]` and `$N`

When you need to access individual arguments, use the 0-based index syntax.

```
/migrate-component MyButton React Vue
```

- `$ARGUMENTS[0]` or `$0` → `MyButton`
- `$ARGUMENTS[1]` or `$1` → `React`
- `$ARGUMENTS[2]` or `$2` → `Vue`

Both syntaxes are equivalent. `$0`, `$1`, `$2` is shorter and more readable in body text.

### Multi-word arguments with quoting

Arguments are split on whitespace by default. To pass a multi-word argument as a single value, quote it:

```
/migrate-component "My Button" React Vue
```

- `$0` → `My Button`
- `$1` → `React`
- `$2` → `Vue`

This follows standard shell-style quoting rules. Single quotes and double quotes both work.

## Named arguments: the `arguments` field

When a skill takes multiple positional arguments, names are clearer than indices. Declare named arguments in frontmatter:

```yaml
arguments: [old-name, new-name, scope]
```

Or as a space-separated string:

```yaml
arguments: old-name new-name scope
```

In the body, reference them by name: `$old-name`, `$new-name`, `$scope`.

Named arguments are mapped positionally. The first argument the user types maps to the first name in the list, the second to the second, and so on.

```
/rename-symbol MyClass MyService project
```

With `arguments: [old-name, new-name, scope]`:
- `$old-name` → `MyClass`
- `$new-name` → `MyService`
- `$scope` → `project`

## The argument-hint field

The `argument-hint` field controls what appears in the autocomplete UI when the user types `/skill-name`:

```yaml
argument-hint: [issue-number]
```

The hint is purely cosmetic — it helps users know what to type. It does not affect how `$ARGUMENTS` or named arguments behave.

Use square brackets for optional or positional descriptions, and plain text for anything more complex:

```yaml
argument-hint: [old-name] [new-name] [file|module|project]
```

## What happens when no `$ARGUMENTS` placeholder exists

If the skill body contains no `$ARGUMENTS` reference and the user types an argument, Claude Code appends the following to the bottom of the skill body before sending it to Claude:

```
ARGUMENTS: <the argument string>
```

Claude sees this and can still use the argument. However, the placement is less predictable than an explicit `$ARGUMENTS` reference. For clarity, always include `$ARGUMENTS` or a named argument reference in the body if you expect arguments.

## Examples

- `examples/fix-issue/` — single `$ARGUMENTS` for a GitHub issue number
- `examples/migrate-component/` — three positional arguments `$0`, `$1`, `$2`
- `examples/named-args/` — named arguments with `arguments: [issue, prefix]`

## Next lesson

[Lesson 05: Dynamic context injection](../lesson-05-dynamic-context/README.md)
