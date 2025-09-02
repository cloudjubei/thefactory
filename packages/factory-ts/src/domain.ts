import { z } from 'zod';

// ----- Shared primitives -----
export const StatusSchema = z.union([
  z.literal('+'), // Done
  z.literal('~'), // In Progress
  z.literal('-'), // Pending
  z.literal('?'), // Blocked
  z.literal('='), // Deferred
]);
export type Status = z.infer<typeof StatusSchema>;

export const ISODateString = z.string().refine((s) => !Number.isNaN(Date.parse(s)), {
  message: 'Expected an ISO date string',
});

// ----- Feature / Task (aligned to docs/tasks/task_format.py and task_example.json) -----
export const FeatureDefinitionSchema = z
  .object({
    id: z.string(),
    status: StatusSchema,
    title: z.string(),
    description: z.string().default(''),
    // The canonical schema defines `plan`; examples may include `action` as well.
    plan: z.string().optional(),
    action: z.string().optional(),
    context: z.array(z.string()).default([]),
    acceptance: z.array(z.string()).default([]),
    dependencies: z.array(z.string()).optional(), // e.g. ["{task_id}.{feature_id}","{task_id}"]
    rejection: z.string().optional(),
  })
  .passthrough();
export type FeatureDefinition = z.infer<typeof FeatureDefinitionSchema>;

export const TaskDefinitionSchema = z
  .object({
    id: z.string(),
    status: StatusSchema,
    title: z.string(),
    description: z.string(),
    features: z.array(FeatureDefinitionSchema),
    dependencies: z.array(z.string()).optional(), // ["{task_id}.{feature_id}","{task_id}"]
    rejection: z.string().optional(),
    featureIdToDisplayIndex: z.record(z.string(), z.number().int()),
  })
  .passthrough();
export type TaskDefinition = z.infer<typeof TaskDefinitionSchema>;

// ----- Project Config (inspired by docs/tasks/task_format.py ProjectSpec) -----
// Accept snake_case or camelCase for repoUrl.
const ProjectRequirementSchema = z
  .object({
    id: z.number().int(),
    status: StatusSchema,
    description: z.string(),
    tasks: z.array(z.string()),
  })
  .passthrough();
export type ProjectRequirement = z.infer<typeof ProjectRequirementSchema>;

const ProjectConfigBaseSchema = z
  .object({
    id: z.string(),
    title: z.string(),
    description: z.string().default(''),
    path: z.string(), // relative path to project root
    repoUrl: z.string().url().optional(),
    // For convenience when selecting and ordering tasks in UI
    taskIdToDisplayIndex: z.record(z.string(), z.number().int()).optional(),
    requirements: z.array(ProjectRequirementSchema).optional(),
    // Optionally list tasks directly
    tasks: z.array(z.string()).optional(),
  })
  .passthrough();

// Support snake_case `repo_url` by pre-processing to `repoUrl`.
export const ProjectConfigSchema = z.preprocess((val) => {
  if (val && typeof val === 'object' && !Array.isArray(val)) {
    const copy: any = { ...(val as any) };
    if (copy.repo_url && !copy.repoUrl) copy.repoUrl = copy.repo_url;
    return copy;
  }
  return val;
}, ProjectConfigBaseSchema);
export type ProjectConfig = z.infer<typeof ProjectConfigSchema>;

// ----- Agent Messaging / Steps / Runs -----
export const MessageRoleSchema = z.union([
  z.literal('system'),
  z.literal('user'),
  z.literal('assistant'),
  z.literal('tool'),
]);
export type MessageRole = z.infer<typeof MessageRoleSchema>;

export const MessageSchema = z
  .object({
    id: z.string().optional(),
    role: MessageRoleSchema,
    content: z.string().default(''),
    name: z.string().optional(),
    toolName: z.string().optional(),
    toolCallId: z.string().optional(),
    createdAt: ISODateString.optional(),
    metadata: z.record(z.any()).optional(),
  })
  .passthrough();
export type Message = z.infer<typeof MessageSchema>;

export const UsageMetricsSchema = z
  .object({
    promptTokens: z.number().int().nonnegative().default(0),
    completionTokens: z.number().int().nonnegative().default(0),
    totalTokens: z.number().int().nonnegative().default(0),
    timeMs: z.number().nonnegative().optional(),
    startedAt: ISODateString.optional(),
    completedAt: ISODateString.optional(),
  })
  .passthrough();
export type UsageMetrics = z.infer<typeof UsageMetricsSchema>;

export const CostBreakdownSchema = z
  .object({
    currency: z.string().default('USD'),
    inputTokens: z.number().int().nonnegative().default(0),
    outputTokens: z.number().int().nonnegative().default(0),
    inputCost: z.number().nonnegative().default(0),
    outputCost: z.number().nonnegative().default(0),
    totalCost: z.number().nonnegative().default(0),
    model: z.string().optional(),
  })
  .passthrough();
export type CostBreakdown = z.infer<typeof CostBreakdownSchema>;

// ----- File Changes & Diffs -----
export const DiffHunkSchema = z
  .object({
    oldStart: z.number().int().nonnegative(),
    oldLines: z.number().int().nonnegative(),
    newStart: z.number().int().nonnegative(),
    newLines: z.number().int().nonnegative(),
    lines: z.array(z.string()),
    // Optional header/context
    header: z.string().optional(),
  })
  .passthrough();
export type DiffHunk = z.infer<typeof DiffHunkSchema>;

export const FileWriteSchema = z
  .object({
    type: z.literal('write'),
    path: z.string(),
    content: z.string(),
    overwrite: z.boolean().optional(),
    // Optional diff view
    diff: z.array(DiffHunkSchema).optional(),
  })
  .passthrough();

export const FileDeleteSchema = z
  .object({
    type: z.literal('delete'),
    path: z.string(),
  })
  .passthrough();

export const FileMoveSchema = z
  .object({
    type: z.literal('move'),
    fromPath: z.string(),
    toPath: z.string(),
  })
  .passthrough();

export const FileRenameSchema = z
  .object({
    type: z.literal('rename'),
    fromPath: z.string(),
    toPath: z.string(),
  })
  .passthrough();

export const FileChangeSchema = z.discriminatedUnion('type', [
  FileWriteSchema,
  FileDeleteSchema,
  FileMoveSchema,
  FileRenameSchema,
]);
export type FileChange = z.infer<typeof FileChangeSchema>;

// ----- Run / Step -----
export const RunStatusSchema = z.union([
  z.literal('queued'),
  z.literal('running'),
  z.literal('succeeded'),
  z.literal('failed'),
  z.literal('cancelled'),
  z.literal('timeout'),
  z.literal('partial'),
]);
export type RunStatus = z.infer<typeof RunStatusSchema>;

export const AgentStepSchema = z
  .object({
    id: z.string(),
    index: z.number().int().nonnegative(),
    stepType: z.union([
      z.literal('plan'),
      z.literal('llm_call'),
      z.literal('tool_call'),
      z.literal('file_change'),
      z.literal('review'),
    ]),
    status: z.union([
      z.literal('pending'),
      z.literal('in_progress'),
      z.literal('completed'),
      z.literal('failed'),
    ]),
    createdAt: ISODateString,
    updatedAt: ISODateString.optional(),
    input: z.any().optional(),
    output: z.any().optional(),
    messages: z.array(MessageSchema).optional(),
    fileChanges: z.array(FileChangeSchema).optional(),
    usage: UsageMetricsSchema.optional(),
    cost: CostBreakdownSchema.optional(),
    error: z.any().optional(),
    metadata: z.record(z.any()).optional(),
  })
  .passthrough();
export type AgentStep = z.infer<typeof AgentStepSchema>;

export const AgentRunSchema = z
  .object({
    id: z.string(),
    projectId: z.string(),
    taskId: z.string().optional(),
    featureId: z.string().optional(),
    rootPath: z.string(),
    status: RunStatusSchema,
    model: z.string().optional(),
    createdAt: ISODateString,
    updatedAt: ISODateString.optional(),
    startedAt: ISODateString.optional(),
    completedAt: ISODateString.optional(),
    steps: z.array(AgentStepSchema).default([]),
    messages: z.array(MessageSchema).default([]),
    usage: UsageMetricsSchema.optional(),
    cost: CostBreakdownSchema.optional(),
    aggregatedFileChanges: z.array(FileChangeSchema).optional(),
    metadata: z.record(z.any()).optional(),
  })
  .passthrough();
export type AgentRun = z.infer<typeof AgentRunSchema>;

// ----- Error Types -----
export const FactoryErrorCodeSchema = z.union([
  z.literal('VALIDATION_ERROR'),
  z.literal('SCHEMA_MISMATCH'),
  z.literal('IO_ERROR'),
  z.literal('LLM_ERROR'),
  z.literal('RUNTIME_ERROR'),
  z.literal('CANCELLED'),
  z.literal('TIMEOUT'),
]);
export type FactoryErrorCode = z.infer<typeof FactoryErrorCodeSchema>;

export const FactoryErrorSchema = z
  .object({
    code: FactoryErrorCodeSchema,
    message: z.string(),
    cause: z.unknown().optional(),
    details: z.record(z.any()).optional(),
    at: ISODateString.optional(),
  })
  .passthrough();
export type FactoryError = z.infer<typeof FactoryErrorSchema>;

// ----- Helpers: parsing/validation -----
export function parseTaskDefinition(input: unknown): TaskDefinition {
  const parsed = TaskDefinitionSchema.parse(input);
  return parsed;
}

export function parseFeatureDefinition(input: unknown): FeatureDefinition {
  return FeatureDefinitionSchema.parse(input);
}

export function parseProjectConfig(input: unknown): ProjectConfig {
  return ProjectConfigSchema.parse(input);
}

export function parseAgentRun(input: unknown): AgentRun {
  return AgentRunSchema.parse(input);
}

export function parseAgentStep(input: unknown): AgentStep {
  return AgentStepSchema.parse(input);
}

export function parseFileChange(input: unknown): FileChange {
  return FileChangeSchema.parse(input);
}

// Convenience: derive totals from usage/cost
export function computeTotals(steps: AgentStep[]) {
  const usage: UsageMetrics = {
    promptTokens: 0,
    completionTokens: 0,
    totalTokens: 0,
  };
  const cost: CostBreakdown = {
    currency: 'USD',
    inputTokens: 0,
    outputTokens: 0,
    inputCost: 0,
    outputCost: 0,
    totalCost: 0,
  };
  for (const s of steps) {
    if (s.usage) {
      usage.promptTokens += s.usage.promptTokens ?? 0;
      usage.completionTokens += s.usage.completionTokens ?? 0;
      usage.totalTokens += s.usage.totalTokens ?? 0;
      if (s.usage.timeMs) usage.timeMs = (usage.timeMs ?? 0) + s.usage.timeMs;
    }
    if (s.cost) {
      cost.inputTokens += s.cost.inputTokens ?? 0;
      cost.outputTokens += s.cost.outputTokens ?? 0;
      cost.inputCost += s.cost.inputCost ?? 0;
      cost.outputCost += s.cost.outputCost ?? 0;
      cost.totalCost += s.cost.totalCost ?? 0;
      cost.currency = s.cost.currency ?? cost.currency;
      cost.model = s.cost.model ?? cost.model;
    }
  }
  return { usage, cost };
}
