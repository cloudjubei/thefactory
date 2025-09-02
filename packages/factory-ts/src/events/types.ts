// Typed event payloads and public types for the run lifecycle event bus
// All types must be IPC-serializable (plain JSON-friendly data only)

export type UUID = string;
export type ISODateTime = string; // new Date().toISOString()

export type RunId = UUID;
export type StepId = UUID;
export type MessageId = UUID;

// Generic primitives
export interface Usage {
  // token counts are optional as some providers only report total
  promptTokens?: number;
  completionTokens?: number;
  totalTokens?: number;
  // monetary cost in USD
  costUSD?: number;
}

export interface CostBreakdown {
  // map of model name -> costUSD
  models?: Record<string, number>;
  totalUSD?: number;
}

export interface FileChangeSummary {
  created: number;
  modified: number;
  deleted: number;
  moved: number;
}

export interface FilePath {
  // workspace-relative path using POSIX separators
  path: string;
}

export interface FileProposal {
  // Proposal groups multiple intended changes as a single review unit
  proposalId: UUID;
  title?: string;
  description?: string;
  // The list of file operations the agent wants to apply
  operations: Array<
    | { kind: "create"; file: FilePath; content: string }
    | { kind: "modify"; file: FilePath; diff?: string; newContent?: string }
    | { kind: "delete"; file: FilePath }
    | { kind: "move"; from: FilePath; to: FilePath }
  >;
  // A high-level summary for UX
  summary?: FileChangeSummary;
  createdAt: ISODateTime;
}

export interface FileDiffEntry {
  file: FilePath;
  // Unified diff format (e.g. git-style), or empty for binary
  unifiedDiff?: string;
  // Optional fields for more structured diffs if available
  // chunks?: Array<...> // intentionally omitted to keep it simple
}

export interface FileDiffPayload {
  proposalId?: UUID; // link to a proposal when relevant
  entries: FileDiffEntry[];
  createdAt: ISODateTime;
}

// LLM messaging and streaming
export type Role = "system" | "user" | "assistant" | "tool";

export interface LLMMessage {
  id: MessageId;
  runId: RunId;
  stepId?: StepId;
  role: Role;
  content: string; // aggregated text content for non-stream events
  createdAt: ISODateTime;
  model?: string; // which model produced this message
  // For tool messages, include tool metadata
  toolName?: string;
  toolCallId?: string;
  // Optional token/usage info if known per message
  usage?: Usage;
}

export interface LLMStreamDelta {
  id: MessageId; // stream id (same for the message being streamed)
  runId: RunId;
  stepId?: StepId;
  model?: string;
  role?: Role; // may be absent on mid-stream deltas
  delta: string; // text delta chunk
  createdAt: ISODateTime;
}

// Run/Step high-level state
export type RunStatus = "idle" | "running" | "paused" | "completed" | "cancelled" | "error";
export type StepStatus = "pending" | "running" | "paused" | "completed" | "error";

export interface RunMetadata {
  runId: RunId;
  projectId?: string;
  taskId?: string;
  featureId?: string;
  rootPath?: string; // workspace root
  llmModel?: string; // primary model used
  createdAt: ISODateTime;
}

export interface RunState {
  status: RunStatus;
  // Aggregate usage and costs so far
  usage?: Usage;
  costs?: CostBreakdown;
  // Optional human-readable summary
  summary?: string;
  // Freeform labels for filtering/searching
  labels?: Record<string, string>;
  updatedAt: ISODateTime;
}

export interface StepInfo {
  stepId: StepId;
  name?: string;
  description?: string;
  index?: number;
  createdAt: ISODateTime;
}

export interface StepState {
  status: StepStatus;
  // Optional progress between 0 and 1
  progress?: number;
  updatedAt: ISODateTime;
}

export interface ErrorPayload {
  runId: RunId;
  stepId?: StepId;
  message: string;
  code?: string;
  // Optional stack if available; keep string for IPC
  stack?: string;
  occurredAt: ISODateTime;
}

// Event Map
export interface RunEventMap {
  // lifecycle
  "run:started": { meta: RunMetadata; state: RunState };
  "run:updated": { runId: RunId; state: RunState };
  "run:completed": { runId: RunId; state: RunState };
  "run:cancelled": { runId: RunId; state: RunState };

  // steps
  "step:started": { runId: RunId; step: StepInfo; state: StepState };
  "step:updated": { runId: RunId; stepId: StepId; state: StepState };

  // llm
  "llm:message": LLMMessage;
  "llm:stream": LLMStreamDelta;

  // usage
  "usage:updated": { runId: RunId; usage: Usage; costs?: CostBreakdown; updatedAt: ISODateTime };

  // files
  "file:proposal": { runId: RunId; proposal: FileProposal };
  "file:diff": { runId: RunId; diff: FileDiffPayload };

  // errors
  error: ErrorPayload;
}

// Subscription utils
export type EventName = keyof RunEventMap;
export type EventPayload<K extends EventName> = RunEventMap[K];

export type EventListener<K extends EventName> = (payload: EventPayload<K>) => void | Promise<void>;

export interface Unsubscribe {
  (): void;
}

export interface EventBus {
  on<K extends EventName>(event: K, listener: EventListener<K>): Unsubscribe;
  once<K extends EventName>(event: K, listener: EventListener<K>): Unsubscribe;
  off<K extends EventName>(event: K, listener: EventListener<K>): void;
  emit<K extends EventName>(event: K, payload: EventPayload<K>): void;
  removeAllListeners(): void;
}

export interface RunControl {
  pause(): void;
  resume(): void;
  cancel(): void;
}

export interface RunHandle extends RunControl {
  runId: RunId;
  bus: EventBus;
  on<K extends EventName>(event: K, listener: EventListener<K>): Unsubscribe;
  once<K extends EventName>(event: K, listener: EventListener<K>): Unsubscribe;
}
