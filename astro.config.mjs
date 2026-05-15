import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://claude-with-skills.vercel.app',
  integrations: [
    starlight({
      title: 'Claude with Skills',
      description: 'A progressive course teaching Agent Skills for Claude Code.',
      social: {
        github: 'https://github.com/davila7/claude-with-skills',
      },
      sidebar: [
        {
          label: 'Introduction',
          items: [
            { label: 'Overview', slug: '00-introduction' },
            { label: 'Setup', slug: '00-introduction/setup' },
            { label: 'Progressive disclosure', slug: '00-introduction/progressive-disclosure' },
            { label: 'Skills vs alternatives', slug: '00-introduction/skills-vs-alternatives' },
          ],
        },
        {
          label: 'Basic',
          items: [
            { label: 'Overview', slug: '01-basic' },
            { label: '01 — Anatomy of a SKILL.md', slug: '01-basic/lesson-01-anatomy' },
            { label: '02 — Where skills live', slug: '01-basic/lesson-02-where-skills-live' },
            { label: '03 — Repetitive tasks', slug: '01-basic/lesson-03-repetitive-tasks' },
            { label: '04 — Documentation skills', slug: '01-basic/lesson-04-documentation-skills' },
            { label: '05 — Invoking skills', slug: '01-basic/lesson-05-invoking' },
            {
              label: 'Exercises',
              items: [
                { label: '01 — Build your first skill', slug: '01-basic/exercises/01-first-skill' },
                { label: '02 — Headless run', slug: '01-basic/exercises/02-headless-run' },
              ],
            },
          ],
        },
        {
          label: 'Intermediate',
          items: [
            { label: 'Overview', slug: '02-intermediate' },
            { label: '01 — Frontmatter reference', slug: '02-intermediate/lesson-01-frontmatter-reference' },
            { label: '02 — Invocation control', slug: '02-intermediate/lesson-02-invocation-control' },
            { label: '03 — Allowed tools', slug: '02-intermediate/lesson-03-allowed-tools' },
            { label: '04 — Arguments', slug: '02-intermediate/lesson-04-arguments' },
            { label: '05 — Dynamic context', slug: '02-intermediate/lesson-05-dynamic-context' },
            { label: '06 — Paths and shell', slug: '02-intermediate/lesson-06-paths-and-shell' },
            { label: '07 — Model and effort', slug: '02-intermediate/lesson-07-model-and-effort' },
            { label: '08 — Combining options', slug: '02-intermediate/lesson-08-combining-options' },
          ],
        },
        {
          label: 'Advanced',
          items: [
            { label: 'Overview', slug: '03-advanced' },
            { label: '01 — Progressive disclosure in practice', slug: '03-advanced/lesson-01-progressive-disclosure-in-practice' },
            { label: '02 — Supporting scripts', slug: '03-advanced/lesson-02-supporting-scripts' },
            { label: '03 — Skill calls subagent', slug: '03-advanced/lesson-03-skill-calls-subagent' },
            { label: '04 — Subagent uses skills', slug: '03-advanced/lesson-04-subagent-uses-skills' },
            { label: '05 — Skills orchestrating skills', slug: '03-advanced/lesson-05-skills-orchestrating-skills' },
            { label: '06 — Context window mastery', slug: '03-advanced/lesson-06-context-window-mastery' },
            { label: '07 — Hooks in skills', slug: '03-advanced/lesson-07-hooks-in-skills' },
            { label: '08 — Plugins and distribution', slug: '03-advanced/lesson-08-plugins-and-distribution' },
            { label: 'Capstone', slug: '03-advanced/capstone' },
          ],
        },
        {
          label: 'Reference',
          autogenerate: { directory: 'reference' },
        },
      ],
    }),
  ],
});
