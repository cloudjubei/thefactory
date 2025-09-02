export type UUID = string

export type RunEvent =
  | { type: 'run/started'; runId: UUID; at: number }
  | { type: 'run/stopped'; runId: UUID; at: number; reason: 'budget-exceeded' | 'aborted' | 'completed' | 'error'; details?: string }
  | { type: 'budget/exceeded'; runId: UUID; at: number; metric: 'cost' | 'tokens'; value: number; limit: number }
  | { type: 'telemetry/updated'; runId: UUID; at: number; snapshot: TelemetrySnapshot }
  | { type: 'llm/request/started'; runId: UUID; at: number; requestId: UUID; model: string }
  | { type: 'llm/request/stream'; runId: UUID; at: number; requestId: UUID; model: string; deltaTokensOut: number }
  | { type: 'llm/request/finished'; runId: UUID; at: number; requestId: UUID; model: string; usage: LLMUsage }
  | { type: 'error/occurred'; runId: UUID; at: number; code: string; message: string; stepIndex?: number | null }
  | { type: 'error/retry'; runId: UUID; at: number; attempt: number; delayMs: number; code: string; message: string; stepIndex?: number | null }

export interface EventBus<E extends { type: string } = RunEvent> {
  on<T extends E['type']>(type: T, listener: (event: Extract<E, { type: T }>) => void): () => void
  emit(event: E): void
}

export interface RunHandle {
  runId: UUID
  bus: EventBus<RunEvent>
  signal: AbortSignal
  stop(reason?: string): void
}

export interface LLMUsage {
  promptTokens: number
  completionTokens: number
  totalTokens?: number
}

export interface TelemetrySnapshot {
  startedAt: number
  updatedAt: number
  totalRequests: number
  totalPromptTokens: number
  totalCompletionTokens: number
  totalTokens: number
  costUsd: number
  perModel: Record<string, {
    requests: number
    promptTokens: number
    completionTokens: number
    costUsd: number
  }>
  status: 'running' | 'stopped'
  stopReason?: string
  budget?: RunBudget
}

export interface RunBudget {
  maxTokens?: number
  maxCostUsd?: number
}
