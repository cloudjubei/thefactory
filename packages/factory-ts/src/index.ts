export * from './review/reviewService';
export * from './files';
export * from './git';
export * from './db/store';
export * from './db/sqlite';
export * from './events';
export * from './utils/retry';
export * from './utils/abort';
export * from './errors/types';
export * from './errors/redact';

export class OverseerFactory {
  version: string
  constructor(opts: { version: string }) {
    this.version = opts.version
  }
  hello(name: string) {
    return `Hello, ${name}! This is OverseerFactory v${this.version}`
  }
}

export function createFactory(opts: { version: string }) {
  return new OverseerFactory(opts)
}
