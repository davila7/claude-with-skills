import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://claude-with-skills.vercel.app',
  integrations: [
    starlight({
      title: 'Claude with Skills',
      description: 'A progressive course teaching Agent Skills for Claude Code.',
      defaultLocale: 'root',
      locales: {
        root: { label: 'English', lang: 'en' },
        es: { label: 'Español', lang: 'es' },
      },
      social: {
        github: 'https://github.com/davila7/claude-with-skills',
      },
      sidebar: [
        {
          label: 'Introduction',
          translations: { es: 'Introducción' },
          items: [
            { label: 'Overview', translations: { es: 'Resumen' }, slug: '00-introduction' },
            { label: 'Setup', translations: { es: 'Configuración' }, slug: '00-introduction/setup' },
            { label: 'Progressive disclosure', translations: { es: 'Carga progresiva' }, slug: '00-introduction/progressive-disclosure' },
            { label: 'Skills vs alternatives', translations: { es: 'Skills vs alternativas' }, slug: '00-introduction/skills-vs-alternatives' },
          ],
        },
        {
          label: 'Basic',
          translations: { es: 'Básico' },
          items: [
            { label: 'Overview', translations: { es: 'Resumen' }, slug: '01-basic' },
            { label: '01 — Anatomy of a SKILL.md', translations: { es: '01 — Anatomía de un SKILL.md' }, slug: '01-basic/lesson-01-anatomy' },
            { label: '02 — Where skills live', translations: { es: '02 — Dónde viven los skills' }, slug: '01-basic/lesson-02-where-skills-live' },
            { label: '03 — Repetitive tasks', translations: { es: '03 — Tareas repetitivas' }, slug: '01-basic/lesson-03-repetitive-tasks' },
            { label: '04 — Documentation skills', translations: { es: '04 — Skills de documentación' }, slug: '01-basic/lesson-04-documentation-skills' },
            { label: '05 — Invoking skills', translations: { es: '05 — Invocar skills' }, slug: '01-basic/lesson-05-invoking' },
            {
              label: 'Exercises',
              translations: { es: 'Ejercicios' },
              items: [
                { label: '01 — Build your first skill', translations: { es: '01 — Construye tu primer skill' }, slug: '01-basic/exercises/01-first-skill' },
                { label: '02 — Headless run', translations: { es: '02 — Ejecución headless' }, slug: '01-basic/exercises/02-headless-run' },
              ],
            },
          ],
        },
        {
          label: 'Intermediate',
          translations: { es: 'Intermedio' },
          items: [
            { label: 'Overview', translations: { es: 'Resumen' }, slug: '02-intermediate' },
            { label: '01 — Frontmatter reference', translations: { es: '01 — Referencia de frontmatter' }, slug: '02-intermediate/lesson-01-frontmatter-reference' },
            { label: '02 — Invocation control', translations: { es: '02 — Control de invocación' }, slug: '02-intermediate/lesson-02-invocation-control' },
            { label: '03 — Allowed tools', translations: { es: '03 — Herramientas permitidas' }, slug: '02-intermediate/lesson-03-allowed-tools' },
            { label: '04 — Arguments', translations: { es: '04 — Argumentos' }, slug: '02-intermediate/lesson-04-arguments' },
            { label: '05 — Dynamic context', translations: { es: '05 — Contexto dinámico' }, slug: '02-intermediate/lesson-05-dynamic-context' },
            { label: '06 — Paths and shell', translations: { es: '06 — Paths y shell' }, slug: '02-intermediate/lesson-06-paths-and-shell' },
            { label: '07 — Model and effort', translations: { es: '07 — Modelo y esfuerzo' }, slug: '02-intermediate/lesson-07-model-and-effort' },
            { label: '08 — Combining options', translations: { es: '08 — Combinar opciones' }, slug: '02-intermediate/lesson-08-combining-options' },
          ],
        },
        {
          label: 'Advanced',
          translations: { es: 'Avanzado' },
          items: [
            { label: 'Overview', translations: { es: 'Resumen' }, slug: '03-advanced' },
            { label: '01 — Progressive disclosure in practice', translations: { es: '01 — Carga progresiva en la práctica' }, slug: '03-advanced/lesson-01-progressive-disclosure-in-practice' },
            { label: '02 — Supporting scripts', translations: { es: '02 — Scripts de soporte' }, slug: '03-advanced/lesson-02-supporting-scripts' },
            { label: '03 — Skill calls subagent', translations: { es: '03 — Skill que llama a un subagente' }, slug: '03-advanced/lesson-03-skill-calls-subagent' },
            { label: '04 — Subagent uses skills', translations: { es: '04 — Subagente que usa skills' }, slug: '03-advanced/lesson-04-subagent-uses-skills' },
            { label: '05 — Skills orchestrating skills', translations: { es: '05 — Skills orquestando skills' }, slug: '03-advanced/lesson-05-skills-orchestrating-skills' },
            { label: '06 — Context window mastery', translations: { es: '06 — Dominio de la ventana de contexto' }, slug: '03-advanced/lesson-06-context-window-mastery' },
            { label: '07 — Hooks in skills', translations: { es: '07 — Hooks en skills' }, slug: '03-advanced/lesson-07-hooks-in-skills' },
            { label: '08 — Plugins and distribution', translations: { es: '08 — Plugins y distribución' }, slug: '03-advanced/lesson-08-plugins-and-distribution' },
            { label: 'Capstone', translations: { es: 'Proyecto final' }, slug: '03-advanced/capstone' },
          ],
        },
        {
          label: 'Reference',
          translations: { es: 'Referencia' },
          autogenerate: { directory: 'reference' },
        },
      ],
    }),
  ],
});
