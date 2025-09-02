export type Role = 'system' | 'user' | 'assistant' | 'tool';

export interface ChatMessage {
  role: Role;
  content: string;
  // Optional tool metadata (for future multi-tool integrations)
  name?: string;
}

export interface ChatCompletionInput {
  model: string;
  messages: ChatMessage[];
  temperature?: number;
  maxTokens?: number;
  // Additional per-provider settings can be passed via this bag
  // Provider adapters should ignore unknown options.
  extra?: Record<string, unknown>;
}

export interface TokenUsage {
  promptTokens: number;
  completionTokens: number;
  totalTokens: number;
  // Whether these token counts are estimated (true) or exact from provider (false)
  isEstimated: boolean;
}

export interface CostBreakdown {
  inputCostPer1K: number | null; // USD per 1K tokens (prompt)
  outputCostPer1K: number | null; // USD per 1K tokens (completion)
  totalCostUSD: number | null; // Null if unknown
}

export interface UsageWithCost extends TokenUsage {
  cost: CostBreakdown;
}

export interface ChatCompletionResult {
  text: string;
  usage: UsageWithCost | null; // null if provider doesn't return usage and cannot estimate
  raw?: unknown; // Provider raw response for debugging
}

export type StreamEvent =
  | { type: 'delta'; content: string }
  | { type: 'message_start'; role: Role }
  | { type: 'message_end' }
  | { type: 'error'; error: Error };

export interface ChatStream {
  // Async iterable of stream events (deltas and lifecycle markers)
  stream: AsyncIterable<StreamEvent>;
  // Promise that resolves when stream completes with the final result
  final: Promise<ChatCompletionResult>;
}

export interface LLMUsageSnapshot extends UsageWithCost {
  // Timestamp of snapshot for monitoring
  at: number;
}

export interface LLMClient {
  readonly provider: string;
  readonly model: string;

  chatCompletionOnce(input: Omit<ChatCompletionInput, 'model'>): Promise<ChatCompletionResult>;
  chatCompletionStream(input: Omit<ChatCompletionInput, 'model'>): Promise<ChatStream>;

  // Running usage snapshot across calls for this client instance
  getUsage(): LLMUsageSnapshot;
}

export interface ModelCostInfo {
  // USD per 1K tokens
  inputCostPer1K: number | null;
  outputCostPer1K: number | null;
}

export type ModelCostTable = Record<string, ModelCostInfo>;

export function estimateTokensFromText(text: string): number {
  // Very rough heuristic: ~4 chars per token for English
  // This is only used when we cannot obtain exact usage (e.g., streaming).
  const chars = [...text].length; // handle unicode code points reasonably
  return Math.max(1, Math.round(chars / 4));
}

export function computeCost(usage: TokenUsage, model: string, costTable: ModelCostTable): CostBreakdown {
  const costs = costTable[model];
  if (!costs) {
    return { inputCostPer1K: null, outputCostPer1K: null, totalCostUSD: null };
  }
  const { inputCostPer1K, outputCostPer1K } = costs;
  const inputCost = inputCostPer1K != null ? (usage.promptTokens / 1000) * inputCostPer1K : null;
  const outputCost = outputCostPer1K != null ? (usage.completionTokens / 1000) * outputCostPer1K : null;
  const totalCostUSD = inputCost != null && outputCost != null ? inputCost + outputCost : (inputCost ?? outputCost);
  return { inputCostPer1K, outputCostPer1K, totalCostUSD: totalCostUSD ?? null };
}

export class UsageAccumulator {
  private usage: TokenUsage = { promptTokens: 0, completionTokens: 0, totalTokens: 0, isEstimated: true };
  private model = '';
  private costTable: ModelCostTable = {};

  constructor(model: string, costTable: ModelCostTable) {
    this.model = model;
    this.costTable = costTable;
  }

  add(u: TokenUsage) {
    this.usage.promptTokens += u.promptTokens;
    this.usage.completionTokens += u.completionTokens;
    this.usage.totalTokens += u.totalTokens;
    // If any addition is exact, overall estimation becomes false only if all exact; keep conservative
    if (!u.isEstimated && this.usage.isEstimated) {
      // we can't flip to exact unless we track exactness per-call; keep isEstimated true unless all exact
    }
  }

  snapshot(): LLMUsageSnapshot {
    const cost = computeCost(this.usage, this.model, this.costTable);
    return { ...this.usage, cost, at: Date.now() };
  }
}
