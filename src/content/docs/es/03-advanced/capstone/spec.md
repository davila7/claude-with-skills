---
title: "Especificación del Capstone"
---

Criterios de aceptación para cada componente del Code Quality Bot. Construye según estos criterios. La solución en `solution/` es la implementación de referencia.

---

## skill `code-quality-gate`

**Ubicación:** `.claude/skills/code-quality-gate/SKILL.md`

### Frontmatter requerido

| Campo | Valor requerido |
|---|---|
| `name` | `code-quality-gate` |
| `description` | Debe mencionar: ejecución de comprobaciones de calidad de código, PR, publicar un comentario en GitHub. Debe incluir una frase desencadenante para que Claude lo detecte automáticamente en contextos de revisión de código. |
| `disable-model-invocation` | `true` — este skill tiene efectos secundarios (publica un comentario) |
| `allowed-tools` | Debe incluir `Bash(gh pr *)` para la comprobación previa |

### Comportamiento requerido

1. **Pre-flight:** Ejecuta `gh pr view --json number,title,headRefName` para comprobar si existe un PR abierto. Si no se encuentra un PR, anótalo y planifica imprimir el informe en la terminal en lugar de publicarlo.

2. **Invoca `/security-scan`** y captura la salida.

3. **Invoca `/complexity-check`** y captura la salida.

4. **Invoca `/test-coverage-check`** y captura la salida.

5. **Invoca `@quality-reporter`** con un mensaje que incluya las tres secciones de hallazgos. El mensaje debe indicar al reporter que formatee y publique el informe.

6. **Confirma** que se devolvió una URL del comentario. Imprímela.

### Qué debe imprimirse

- Si existe un PR: la URL del comentario del PR.
- Si no existe un PR: el informe completo formateado impreso en la terminal.
- Siempre: una línea de resumen indicando cuántos hallazgos se encontraron en todas las comprobaciones.

### Validación

Ejecuta `/code-quality-gate` en un repositorio con un PR abierto. Confirma que aparece un comentario en el PR dentro de una sesión.

---

## skill `security-scan`

**Ubicación:** `.claude/skills/security-scan/SKILL.md`

### Frontmatter requerido

| Campo | Valor requerido |
|---|---|
| `name` | `security-scan` |
| `description` | Debe mencionar: escaneo de seguridad, secretos en código, inyección, XSS. Debe incluir palabras clave de auto-invocación. |
| `context` | `fork` |
| `agent` | `Explore` |
| `allowed-tools` | Debe incluir `Grep`, `Glob`, `Read`, `Bash(git diff *)`, `Bash(git log *)` |

### Comportamiento requerido

1. **Céntrate primero en los archivos modificados.** Inyecta `git diff --name-only HEAD~1` (o equivalente). Prioriza escanear los archivos de esta lista.

2. **Escanea cada uno de estos patrones:**
   - Secretos en código: `password=`, `api_key=`, `secret=`, `token=` seguido de un valor literal. Excluye archivos en `test/`, `spec/`, `*.example`, `*.sample`.
   - Riesgo de inyección SQL: f-strings, template literals o concatenación de cadenas que incrusten variables directamente en palabras clave SQL (`SELECT`, `INSERT`, `UPDATE`, `DELETE`, `WHERE`).
   - Vectores XSS: asignación directa a `innerHTML` en archivos `.js` o `.ts` sin sanitización.
   - Entradas sin validar: cuerpo o parámetros de la petición usados directamente en una llamada a base de datos sin validación explícita.
   - Valores por defecto inseguros: `DEBUG=True`, `CORS allow *`, `verify=False`.

3. **Formato de salida:** Debe ser exactamente:
   ```
   SECURITY FINDINGS:
   - [CRITICAL|HIGH|MEDIUM|LOW] <file>:<line> — <description>
   ```
   O, si no se encuentra nada: `SECURITY FINDINGS: none`

### Validación

Ejecuta `/security-scan` en un proyecto que no tenga problemas de seguridad evidentes. Confirma que la salida empieza con `SECURITY FINDINGS:` y termina con hallazgos o con `none`.

---

## skill `complexity-check`

**Ubicación:** `.claude/skills/complexity-check/SKILL.md`

### Frontmatter requerido

| Campo | Valor requerido |
|---|---|
| `name` | `complexity-check` |
| `description` | Debe mencionar: complejidad, funciones de más de 50 líneas, archivos de más de 300 líneas, anidamiento. |
| `context` | `fork` |
| `agent` | `Explore` |
| `allowed-tools` | Debe incluir `Grep`, `Glob`, `Read`, `Bash(find *)`, `Bash(wc *)` |

### Comportamiento requerido

1. **Céntrate en los archivos modificados** usando la misma inyección `git diff --name-only` que el skill de seguridad.

2. **Comprueba lo siguiente:**
   - Archivos de más de 300 líneas: usa `find . -name "*.py" -o -name "*.ts" -o -name "*.js" | xargs wc -l | sort -rn | head -20`. Excluye `node_modules`, `dist`, `.git`.
   - Funciones largas: estima la longitud de las funciones escaneando definiciones de función/método y midiendo el espacio hasta la siguiente definición. Marca las funciones que se estimen en más de 50 líneas.
   - Anidamiento profundo: busca con grep 4 o más niveles de indentación (16+ espacios o 4+ tabulaciones) dentro de condicionales o bucles.
   - Números mágicos: literales numéricos distintos de 0, 1, -1 usados directamente en condiciones o cálculos sin una constante con nombre.

3. **Formato de salida:** Debe ser exactamente:
   ```
   COMPLEXITY FINDINGS:
   - <file>:<line> — <description>
   ```
   O, si no se encuentra nada: `COMPLEXITY FINDINGS: none`

### Validación

Ejecuta `/complexity-check` en un proyecto. Confirma que la salida empieza con `COMPLEXITY FINDINGS:` y que cualquier elemento listado incluye referencias `file:line`.

---

## skill `test-coverage-check`

**Ubicación:** `.claude/skills/test-coverage-check/SKILL.md`

### Frontmatter requerido

| Campo | Valor requerido |
|---|---|
| `name` | `test-coverage-check` |
| `description` | Debe mencionar: cobertura de pruebas, archivos de pruebas, archivos modificados. |
| `context` | `fork` |
| `agent` | `Explore` |
| `allowed-tools` | Debe incluir `Grep`, `Glob`, `Read`, `Bash(git diff *)`, `Bash(find *)` |

### Comportamiento requerido

1. **Obtén los archivos fuente modificados:** Inyecta `git diff --name-only HEAD~1` y filtra los archivos de pruebas, `.md`, `.json`, `.yaml`.

2. **Para cada archivo fuente modificado:**
   - Deriva los nombres esperados de los archivos de pruebas usando convenciones comunes:
     - `src/utils/parser.ts` → `src/utils/parser.test.ts`
     - `src/utils/parser.ts` → `src/utils/__tests__/parser.ts`
     - `src/utils/parser.ts` → `tests/utils/parser.test.ts`
     - `src/utils/parser.ts` → `tests/utils/parser.spec.ts`
   - Usa Glob para comprobar si alguno de estos archivos existe.
   - Si se encuentra un archivo de pruebas, comprueba si importa o menciona el nombre del archivo fuente.

3. **Formato de salida:** Debe ser exactamente:
   ```
   COVERAGE FINDINGS:
   - <source-file> — no test file found
   - <source-file> — test file exists but may not cover new changes
   ```
   O, si todos los archivos tienen pruebas: `COVERAGE FINDINGS: none`

### Validación

Ejecuta `/test-coverage-check` en un proyecto con algunos archivos probados y otros sin probar. Confirma que identifica correctamente qué archivos no tienen pruebas.

---

## subagent `quality-reporter`

**Ubicación:** `.claude/agents/quality-reporter.md`

### Frontmatter requerido

| Campo | Valor requerido |
|---|---|
| `name` | `quality-reporter` |
| `description` | Debe mencionar: formatear hallazgos de calidad de código, publicar comentario en PR de GitHub. |
| `tools` | Solo `Bash(gh pr comment *)` y `Bash(gh pr view *)` — sin herramientas de lectura, sin herramientas de escritura |
| `model` | `haiku` — este es un trabajo de formato y publicación, no de razonamiento |

### Comportamiento requerido

Cuando se invoca con un mensaje que contiene los hallazgos de los tres escaneos:

1. **Formatea los hallazgos** en un comentario de PR en markdown con:
   - Una tabla de resumen mostrando el estado de cada comprobación (número de hallazgos, o "Clean" si no hay)
   - Una sección por comprobación con la lista completa de hallazgos
   - Una línea de pie de página: `Generated by code-quality-gate`

2. **Publica el comentario:**
   ```bash
   gh pr comment --body "<formatted comment>"
   ```

3. **Devuelve la URL del comentario** desde la salida de `gh pr comment`.

### Cómo debe verse el comentario

El comentario debe contener como mínimo:

- El texto `## Code Quality Report`
- Una tabla o lista mostrando el número o el estado de las comprobaciones de Seguridad, Complejidad y Cobertura de Pruebas
- Los hallazgos completos para cada comprobación (o "No issues found")
- El pie de página `Generated by code-quality-gate`

### Validación

Tras ejecutar `/code-quality-gate` en un repositorio con un PR abierto, abre el PR en GitHub. El comentario debería aparecer con el formato correcto y las tres secciones rellenas.

---

## Prueba de integración

Ejecuta el sistema completo de extremo a extremo:

1. Abre un repositorio con al menos un commit, un archivo fuente y un pull request abierto.
2. Ejecuta `/code-quality-gate`.
3. Confirma:
   - Que los tres skills de escaneo se ejecutaron (sus secciones `FINDINGS:` aparecen en la salida de la sesión)
   - Que se invocó a `@quality-reporter`
   - Que se imprimió una URL del comentario del PR
   - Que el comentario en GitHub tiene el formato esperado
4. Vuelve a ejecutarlo en un PR limpio. Confirma que cada sección muestra "none" o "No issues found" según corresponda.
