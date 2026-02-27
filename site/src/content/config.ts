import { defineCollection, z } from 'astro:content';

const journalCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.string().optional(),
    threads: z.array(z.string()).optional(),
    order: z.number().optional(),
  }),
});

const madeCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    form: z.string(),
    threads: z.array(z.string()).optional(),
  }),
});

const curiositiesCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
  }),
});

export const collections = {
  journal: journalCollection,
  made: madeCollection,
  curiosities: curiositiesCollection,
};
