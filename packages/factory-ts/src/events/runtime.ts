import { EventBus, RunEvent, RunHandle, UUID } from './types'

export class SimpleEventBus implements EventBus<RunEvent> {
  private listeners = new Map<string, Set<Function>>()

  on<T extends RunEvent['type']>(type: T, listener: (event: Extract<RunEvent, { type: T }>) => void): () => void {
    let set = this.listeners.get(type)
    if (!set) {
      set = new Set()
      this.listeners.set(type, set)
    }
    set.add(listener)
    return () => {
      set!.delete(listener)
    }
  }

  emit(event: RunEvent): void {
    const set = this.listeners.get(event.type)
    if (set) {
      for (const l of Array.from(set)) {
        try {
          ;(l as any)(event)
        } catch (err) {
          // avoid breaking emitter due to listener error
          // eslint-disable-next-line no-console
          console.error('Event listener error', err)
        }
      }
    }
  }
}

export class DefaultRunHandle implements RunHandle {
  runId: UUID
  bus: EventBus<RunEvent>
  private controller: AbortController

  constructor(runId?: UUID, bus?: EventBus<RunEvent>, controller?: AbortController) {
    this.runId = runId ?? randomId()
    this.bus = bus ?? new SimpleEventBus()
    this.controller = controller ?? new AbortController()
  }

  get signal(): AbortSignal {
    return this.controller.signal
  }

  stop(reason?: string): void {
    if (!this.controller.signal.aborted) {
      try {
        // @ts-expect-error reason is supported in newer runtimes
        this.controller.abort(reason ?? 'aborted')
      } catch {
        this.controller.abort()
      }
    }
  }
}

export function randomId(): UUID {
  return 'run_' + Math.random().toString(36).slice(2, 10)
}
