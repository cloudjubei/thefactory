import { openDatabase, HistoryStore, type DBOptions } from './sqlite';

// Convenience factory that opens DB and returns HistoryStore with handle attached.
export function createHistoryStore(opts: DBOptions = {}) {
  const handle = openDatabase(opts);
  const store = new HistoryStore(handle);
  return { store, handle };
}

export * from './sqlite';
