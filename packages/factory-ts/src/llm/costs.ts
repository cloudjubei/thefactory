import { ModelCostTable } from './types';

// Minimal cost table for OpenAI models (example values; adjust as needed)
export const openAICostTable: ModelCostTable = {
  'gpt-4o-mini': { inputCostPer1K: 0.15, outputCostPer1K: 0.6 },
  'gpt-4o': { inputCostPer1K: 5.0, outputCostPer1K: 15.0 },
  'gpt-4-turbo': { inputCostPer1K: 10.0, outputCostPer1K: 30.0 },
  'gpt-3.5-turbo': { inputCostPer1K: 0.5, outputCostPer1K: 1.5 },
};
