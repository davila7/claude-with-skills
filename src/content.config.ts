import { defineCollection, z } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

const skillFrontmatter = z.object({
  name: z.string().optional(),
  'allowed-tools': z.union([z.string(), z.array(z.string())]).optional(),
  'disable-model-invocation': z.boolean().optional(),
  'user-invocable': z.boolean().optional(),
  'argument-hint': z.union([z.string(), z.array(z.string())]).optional(),
  arguments: z
    .union([z.array(z.string()), z.array(z.record(z.any())), z.record(z.any())])
    .optional(),
  paths: z.array(z.string()).optional(),
  shell: z.union([z.string(), z.record(z.any())]).optional(),
  context: z.string().optional(),
  agent: z.union([z.string(), z.record(z.any())]).optional(),
  hooks: z.record(z.any()).optional(),
  model: z.string().optional(),
  effort: z.string().optional(),
});

export const collections = {
  docs: defineCollection({
    loader: docsLoader(),
    schema: docsSchema({ extend: skillFrontmatter }),
  }),
};
