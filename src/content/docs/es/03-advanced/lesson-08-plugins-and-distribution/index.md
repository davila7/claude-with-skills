---
title: "Lección 08: Plugins y distribución"
---

Cuando un conjunto de skills es maduro y útil para todo un equipo o para la comunidad en general, empaquetarlo como un plugin facilita la distribución. Un plugin agrupa skills, agents y otros activos en un único directorio con un manifest. Los usuarios instalan el paquete completo con un solo comando.

---

## Conceptos básicos de plugin

Un plugin es un directorio que contiene:

- `plugin.json` — el manifest
- `skills/` — un subdirectorio por skill, cada uno con un `SKILL.md`
- `agents/` — un subdirectorio por definición de agent (opcional)

El manifest declara lo que contiene el plugin y lo identifica por nombre y versión.

**Invocación de skill desde un plugin:**
Los skills en un plugin usan un comando con namespace: `/plugin-name:skill-name`

Si el plugin se llama `release-plugin` y contiene un skill llamado `release`, los usuarios lo invocan como:
```
/release-plugin:release
```

**Referencias a agent desde dentro de los skills del plugin:**
Los subagents definidos en el plugin se referencian como `@agent-plugin-name:agent-name`.

---

## Estructura de plugin.json

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin provides",
  "skills": [
    "skills/skill-one",
    "skills/skill-two"
  ],
  "agents": [
    "agents/my-agent"
  ]
}
```

- `name`: el namespace del plugin. Debe estar en minúsculas con solo guiones. Esto se convierte en el prefijo para todos los slash commands.
- `version`: cadena de versión semántica. Se usa para comprobaciones de actualización y resolución de conflictos.
- `description`: se muestra al listar los plugins instalados.
- `skills`: lista de rutas relativas a los directorios de skill. Cada ruta debe contener un `SKILL.md`.
- `agents`: lista de rutas relativas a los archivos de definición de agent (opcional).

---

## Opciones de distribución

**Instalación local:**
```bash
claude plugin add ./path/to/plugin-directory
```
Útil durante el desarrollo y para plugins internos del equipo almacenados en un repository compartido.

**URL de Git:**
```bash
claude plugin add https://github.com/org/repo
```
Claude Code clona el repository y lo instala como un plugin. Las actualizaciones se pueden hacer pull con `claude plugin update plugin-name`.

**Marketplace:**
Los plugins se pueden listar en el marketplace de plugins de Claude Code para distribución pública. Los usuarios los instalan por nombre: `claude plugin add plugin-name`.

**Ajustes gestionados (empresa):**
Las organizaciones pueden preinstalar plugins para todos los miembros especificándolos en los settings de Claude Code a nivel de organización. Los miembros reciben los plugins automáticamente cuando abren Claude Code.

---

## Restricciones de seguridad para skills de plugin

Los skills de plugin se ejecutan con confianza reducida en comparación con los skills de proyecto o de usuario. Los siguientes campos de frontmatter se ignoran silenciosamente en los skills de plugin:

- `hooks` — los plugins no pueden definir hooks de ciclo de vida
- `mcpServers` — los plugins no pueden provisionar conexiones a MCP servers
- `permissionMode` — los plugins no pueden anular el modo de permiso de la sesión

Estas restricciones protegen a los usuarios de plugins que podrían ejecutar código arbitrario a través de hooks o modificar sus permisos de tools.

**Workaround para hooks en plugins:**
Si un skill de plugin requiere hooks para funcionar correctamente, documenta la configuración de hook requerida en el README del plugin y proporciona un snippet JSON listo para pegar. Los usuarios que quieran el comportamiento de hook pueden añadir la configuración a su `.claude/settings.json` globalmente.

Alternativamente, documenta que los usuarios pueden copiar el skill fuera del directorio del plugin a `.claude/skills/` para obtener soporte completo de hooks. Un skill copiado se trata como un skill de proyecto con confianza completa.

---

## Ejemplo: release-plugin

El directorio `examples/release-plugin/` empaqueta los cuatro skills de release-flow de la lección 05 como un plugin distribuible.

**Estructura:**
```
release-plugin/
  plugin.json
  skills/
    release/SKILL.md
    changelog-entry/SKILL.md
    tag-version/SKILL.md
    publish/SKILL.md
```

**Instalar y usar:**
```bash
claude plugin add ./examples/release-plugin

# Invocar el orchestrator
/release-plugin:release 1.2.0

# O usar skills individuales
/release-plugin:changelog-entry
/release-plugin:tag-version patch
/release-plugin:publish
```

**Nota sobre el skill `release` del plugin:**
El cuerpo del orchestrator referencia `/changelog-entry`, `/tag-version` y `/publish` — los nombres sin cualificar. Al ejecutarse desde dentro de un contexto de plugin, Claude los resuelve como `/release-plugin:changelog-entry`, etc. Si los skills también están instalados como skills standalone del proyecto con los mismos nombres, las referencias sin cualificar se resolverán a los skills del proyecto en su lugar. Para evitar ambigüedad en entornos mixtos, usa nombres completamente cualificados en los cuerpos de los orchestrators del plugin: `/release-plugin:changelog-entry`.

---

## Versionado y actualizaciones

El campo `version` en `plugin.json` sigue el versionado semántico:

- Incrementa **patch** (1.0.0 → 1.0.1) para correcciones de bugs en cuerpos o descripciones de skill existentes.
- Incrementa **minor** (1.0.0 → 1.1.0) para nuevos skills añadidos al plugin.
- Incrementa **major** (1.0.0 → 2.0.0) para cambios disruptivos: renombrados de skill, skills eliminados, firmas de argumentos cambiadas o cambios de comportamiento que requieren que los usuarios actualicen cómo invocan los skills.

Al distribuir vía Git, tagea el commit del release con la versión: `v1.0.0`. Esto permite a los usuarios fijarse a una versión específica.

---

## Siguiente sección

[Capstone: Bot de calidad de código](../capstone/)
