// Node CLI for running agents via the factory-ts orchestrator
// Outputs JSONL events to stdout, exit code 0 on success and non-zero on error

/*
Accepted args:
--project-id string (required)
--task-id string (required)
--feature-id string (optional)
--llm-config string (path to JSON or inline JSON)
--budget number (optional)
--db-path string (optional)
--project-root string (optional)

Example:
  npm run run:agent -- \
    --project-id child-project-1 \
    --task-id 42 \
    --feature-id 1 \
    --llm-config ./overseer_llm.json \
    --budget 5 \
    --db-path ./.thefactory/history.sqlite \
    --project-root .
*/

import fs from 'node:fs';
import path from 'node:path';

function printJSONL(obj: any) {
  try {
    process.stdout.write(JSON.stringify(obj) + "\n");
  } catch (e) {
    // Best effort; avoid throwing here to keep stream resilient.
  }
}

function printErrorEvent(err: unknown, context?: Record<string, any>) {
  const payload = serializeError(err);
  printJSONL({ type: 'error/occurred', ts: new Date().toISOString(), payload, context: context || {} });
}

function serializeError(err: unknown) {
  if (!err) return { name: 'Error', message: 'Unknown error' };
  if (err instanceof Error) {
    return {
      name: err.name,
      message: err.message,
      stack: err.stack,
    };
  }
  return { name: 'Error', message: String(err) };
}

function parseArgs(argv: string[]) {
  // Simple parser: supports --key value and --key=value
  const out: Record<string, any> = {};
  const args = argv.slice(2);
  for (let i = 0; i < args.length; i++) {
    const token = args[i];
    if (!token.startsWith('--')) continue;
    const eqIdx = token.indexOf('=');
    if (eqIdx !== -1) {
      const key = token.slice(2, eqIdx);
      const val = token.slice(eqIdx + 1);
      out[toCamel(key)] = val;
    } else {
      const key = token.slice(2);
      const next = args[i + 1];
      if (next && !next.startsWith('--')) {
        out[toCamel(key)] = next;
        i += 1;
      } else {
        out[toCamel(key)] = true;
      }
    }
  }
  return out;
}

function toCamel(s: string) {
  return s.replace(/-([a-z])/g, (_, c) => c.toUpperCase());
}

function parseNumberMaybe(val: any): number | undefined {
  if (val === undefined || val === null || val === '') return undefined;
  const n = Number(val);
  return Number.isFinite(n) ? n : undefined;
}

function parseLLMConfig(val: string | undefined) {
  if (!val) return undefined;
  // If looks like JSON, parse.
  const trimmed = val.trim();
  if (trimmed.startsWith('{') || trimmed.startsWith('[')) {
    try {
      return JSON.parse(trimmed);
    } catch (e) {
      throw new Error(`Failed to parse --llm-config as JSON: ${(e as Error).message}`);
    }
  }
  // Else treat as path; resolve relative to cwd.
  const filePath = path.resolve(process.cwd(), val);
  if (!fs.existsSync(filePath)) {
    // As a last resort, pass the string through (could be a model name in future adapters)
    return val;
  }
  const content = fs.readFileSync(filePath, 'utf8');
  try {
    return JSON.parse(content);
  } catch (e) {
    throw new Error(`Failed to parse --llm-config file as JSON (${filePath}): ${(e as Error).message}`);
  }
}

async function dynamicImportOrchestrator() {
  // Try a few plausible import targets to work in both src and built contexts.
  const candidates = [
    // Built dist default
    pathToImport('packages/factory-ts/dist/orchestrator.js'),
    pathToImport('packages/factory-ts/dist/index.js'),
    // Source
    pathToImport('packages/factory-ts/src/orchestrator.ts'),
    pathToImport('packages/factory-ts/src/orchestrator.js'),
    // Package entry
    'packages/factory-ts',
    '@thefactory/factory-ts',
    'factory-ts',
  ].filter(Boolean) as string[];

  let lastErr: unknown;
  for (const target of candidates) {
    try {
      // eslint-disable-next-line no-await-in-loop
      const mod = await import(target);
      return mod;
    } catch (e) {
      lastErr = e;
      continue;
    }
  }
  throw new Error(`Unable to load orchestrator module. Tried: ${candidates.join(', ')}. Last error: ${String(lastErr)}`);
}

function pathToImport(rel: string) {
  const abs = path.resolve(process.cwd(), rel);
  return fs.existsSync(abs) ? pathToFileURL(abs) : undefined;
}

function pathToFileURL(p: string) {
  let pathName = path.resolve(p).replace(/\\/g, '/');
  if (!pathName.startsWith('/')) {
    pathName = `/${pathName}`;
  }
  return encodeURI(`file://${pathName}`);
}

async function main() {
  const args = parseArgs(process.argv);
  const required = ['projectId', 'taskId'];
  for (const k of required) {
    if (!args[k]) {
      const msg = `Missing required argument --${k.replace(/[A-Z]/g, m => '-' + m.toLowerCase())}`;
      printErrorEvent(new Error(msg));
      process.exitCode = 2;
      return;
    }
  }

  const projectId = String(args.projectId);
  const taskId = String(args.taskId);
  const featureId = args.featureId !== undefined ? String(args.featureId) : undefined;
  const budget = parseNumberMaybe(args.budget);
  const dbPath = args.dbPath ? path.resolve(String(args.dbPath)) : undefined;
  const projectRoot = args.projectRoot ? path.resolve(String(args.projectRoot)) : process.cwd();
  const llmConfig = parseLLMConfig(args.llmConfig);

  const abortController = new AbortController();
  const signal = abortController.signal;

  process.on('SIGINT', () => {
    printJSONL({ type: 'run/aborting', ts: new Date().toISOString(), payload: { reason: 'SIGINT' } });
    abortController.abort();
  });

  printJSONL({
    type: 'cli/started',
    ts: new Date().toISOString(),
    payload: {
      projectId,
      taskId,
      featureId,
      budget,
      dbPath,
      projectRoot,
      llmConfigProvided: llmConfig !== undefined,
    },
  });

  let orchestratorMod: any;
  try {
    orchestratorMod = await dynamicImportOrchestrator();
  } catch (e) {
    printErrorEvent(e, { stage: 'import-orchestrator' });
    process.exitCode = 3;
    return;
  }

  const runOptions: any = {
    projectId,
    taskId,
    featureId,
    llmConfig,
    budget,
    dbPath,
    projectRoot,
    signal,
  };

  let handle: any;
  let hadError = false;

  try {
    const runTask = orchestratorMod.runTask || orchestratorMod.default?.runTask || orchestratorMod.orchestrator?.runTask;
    const runFeature = orchestratorMod.runFeature || orchestratorMod.default?.runFeature || orchestratorMod.orchestrator?.runFeature;

    if (featureId && typeof runFeature === 'function') {
      handle = await runFeature(runOptions);
    } else if (typeof runTask === 'function') {
      handle = await runTask(runOptions);
    } else if (typeof runFeature === 'function') {
      // If runTask not exposed, fall back to runFeature with undefined feature
      handle = await runFeature(runOptions);
    } else {
      throw new Error('Orchestrator module does not expose runTask or runFeature');
    }

    // Try to subscribe to events in a flexible way.
    const listenersAttached = attachEventListeners(handle, (evt: any) => {
      // Normalize event to { type, ts, payload }
      const out = normalizeEvent(evt);
      printJSONL(out);
      if (out.type === 'error/occurred' || out.type === 'run/error') {
        hadError = true;
      }
    });

    if (!listenersAttached) {
      // Emit a notice so downstream knows no internal events will be streamed.
      printJSONL({ type: 'cli/warn', ts: new Date().toISOString(), payload: { message: 'No event listeners attached; orchestrator events may not be streaming.' } });
    }

    // Await completion if the handle exposes a done promise.
    if (handle?.done && typeof handle.done.then === 'function') {
      await handle.done;
    } else if (handle?.waitForCompletion && typeof handle.waitForCompletion === 'function') {
      await handle.waitForCompletion();
    } else if (handle?.result && typeof handle.result.then === 'function') {
      await handle.result; // generic promise
    } else {
      // No completion handle; wait until aborted or a small delay
      await new Promise<void>((resolve) => {
        const t = setTimeout(() => resolve(), 100); // minimal fallback
        if (signal.aborted) {
          clearTimeout(t);
          resolve();
        } else {
          signal.addEventListener('abort', () => { clearTimeout(t); resolve(); });
        }
      });
    }

    if (hadError) {
      printJSONL({ type: 'run/completed', ts: new Date().toISOString(), payload: { status: 'error' } });
      process.exitCode = 1;
    } else {
      printJSONL({ type: 'run/completed', ts: new Date().toISOString(), payload: { status: 'success' } });
      process.exitCode = 0;
    }
  } catch (e) {
    printErrorEvent(e, { stage: 'run' });
    process.exitCode = 1;
  }
}

function attachEventListeners(handle: any, onAny: (evt: any) => void): boolean {
  if (!handle) return false;

  // Common patterns to try:
  // 1) handle.events.on('*', cb)
  if (handle.events && typeof handle.events.on === 'function') {
    try {
      handle.events.on('*', onAny);
      return true;
    } catch {}
  }
  // 2) handle.on('*', cb)
  if (typeof handle?.on === 'function') {
    try {
      handle.on('*', onAny);
      return true;
    } catch {}
  }
  // 3) handle.subscribe(cb)
  if (typeof handle?.subscribe === 'function') {
    try {
      handle.subscribe(onAny);
      return true;
    } catch {}
  }
  // 4) events emitter with onAny
  if (handle.events && typeof handle.events.onAny === 'function') {
    try {
      handle.events.onAny(onAny);
      return true;
    } catch {}
  }
  return false;
}

function normalizeEvent(evt: any) {
  if (!evt || typeof evt !== 'object') {
    return { type: 'event/unknown', ts: new Date().toISOString(), payload: { raw: evt } };
  }
  // Preferred structure
  if (evt.type && evt.ts) return evt;
  // Try to coerce known fields
  const type = evt.type || evt.event || 'event/unknown';
  const ts = evt.ts || evt.timestamp || new Date().toISOString();
  const payload = evt.payload !== undefined ? evt.payload : evt.data !== undefined ? evt.data : evt;
  return { type, ts, payload };
}

main().catch((e) => {
  printErrorEvent(e, { stage: 'main' });
  process.exitCode = 1;
});
