export interface FactoryOptions {
  version?: string;
}

export class OverseerFactory {
  constructor(public options: FactoryOptions = {}) {}

  hello(name = 'world'): string {
    return `@overseer/factory ready, ${name}!`;
  }
}

export function createFactory(options: FactoryOptions = {}) {
  return new OverseerFactory(options);
}

export default OverseerFactory;

// Domain types and schemas
export * from './domain';

// Project/task loader API
export * from './loaders/projectLoader';
