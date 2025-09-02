import { EventBus, RunEvent, RunHandle, RunId } from '../events/types';

export interface InternalRunRecord {
  runId: RunId;
  meta?: { projectId: string; taskId?: string; featureId?: string; createdAt: string; labels?: Record<string, string> };
  events: RunEvent[];
  usage?: any;
  proposals: Map<string, { summary?: any; diffs?: any[]; states?: Array<{ state: any; time?: string }> }>;
  commits: Array<{ proposalId: string; commitSha: string; message?: string; time?: string }>;
  error?: any;
  completed?: boolean;
  cancelled?: boolean;
}

const registry = new Map<RunId, InternalRunRecord>();
const unsubscribers = new Map<RunId, () => void>();

export function attachRunRecorder(handle: RunHandle): () => void {
  const id = handle.id;
  if (!registry.has(id)) {
    registry.set(id, { runId: id, events: [], proposals: new Map(), commits: [] });
  }
  const rec = registry.get(id)!;

  const unsubscribe = handle.onEvent((e: RunEvent) => {
    try {
      rec.events.push(e);
      switch (e.type) {
        case 'run/started':
          rec.meta = {
            projectId: e.payload.projectId,
            taskId: e.payload.taskId,
            featureId: e.payload.featureId,
            createdAt: e.time,
            labels: e.payload.meta?.labels as any,
          };
          break;
        case 'run/usage':
        case 'run/budget-exceeded':
          rec.usage = e.payload;
          break;
        case 'file/diff': {
          const p = rec.proposals.get(e.payload.proposalId) ?? {};
          p.summary = e.payload.summary;
          p.diffs = e.payload.files;
          rec.proposals.set(e.payload.proposalId, p);
          break;
        }
        case 'file/proposal-state': {
          const p = rec.proposals.get(e.payload.proposalId) ?? {};
          p.states = [...(p.states ?? []), { state: e.payload.state, time: e.time }];
          rec.proposals.set(e.payload.proposalId, p);
          break;
        }
        case 'git/commit':
          rec.commits.push({ proposalId: e.payload.proposalId, commitSha: e.payload.commitSha, message: e.payload.message, time: e.time });
          break;
        case 'run/error':
          rec.error = e.payload;
          break;
        case 'run/completed':
          rec.completed = true;
          break;
        case 'run/cancelled':
          rec.cancelled = true;
          break;
      }
    } catch {
      // keep recorder resilient
    }
  });

  unsubscribers.set(id, unsubscribe);
  return () => {
    unsubscribe();
    unsubscribers.delete(id);
  };
}

export function getRecordedRun(runId: RunId): InternalRunRecord | undefined {
  return registry.get(runId);
}

export function setImportedRun(runId: RunId, record: InternalRunRecord) {
  registry.set(runId, record);
}
