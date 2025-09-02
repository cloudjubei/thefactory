import { ModelCostTable } from './types';

// Cost data (USD per 1K tokens). Values approximate based on public pricing as of 2024-10.
// Update these as providers change pricing.
export const OPENAI_MODEL_COSTS: ModelCostTable = {
  // GPT-4o family
  'gpt-4o': { inputCostPer1K: 0.005, outputCostPer1K: 0.015 },
  'gpt-4o-2024-05-13': { inputCostPer1K: 0.005, outputCostPer1K: 0.015 },
  'gpt-4o-mini': { inputCostPer1K: 0.00015, outputCostPer1K: 0.0006 },

  // GPT-4.1 family
  'gpt-4.1': { inputCostPer1K: 0.005, outputCostPer1K: 0.015 },
  'gpt-4.1-mini': { inputCostPer1K: 0.0003, outputCostPer1K: 0.0006 },

  // Legacy models (fallback)
  'gpt-4-turbo': { inputCostPer1K: 0.01, outputCostPer1K: 0.03 },
  'gpt-3.5-turbo': { inputCostPer1K: 0.0005, outputCostPer1K: 0.0015 },
};

export function getOpenAIModelCost(model: string) {
  return OPENAI_MODEL_COSTS[model];
}
