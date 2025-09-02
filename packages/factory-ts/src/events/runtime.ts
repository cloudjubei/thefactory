// Runtime implementation of a small typed event bus and RunHandle
import { EventBus, EventListener, EventName, EventPayload, RunControl, RunHandle, RunId } from "./types";

// Lightweight, framework-agnostic event emitter (no Node built-ins)
export class TypedEventBus implements EventBus {
  private listeners: Map<EventName, Set<EventListener<any>>> = new Map();
  private onceListeners: Map<EventName, Set<EventListener<any>>> = new Map();

  on<K extends EventName>(event: K, listener: EventListener<K>) {
    let set = this.listeners.get(event);
    if (!set) {
      set = new Set();
      this.listeners.set(event, set);
    }
    set.add(listener as EventListener<any>);
    return () => this.off(event, listener);
  }

  once<K extends EventName>(event: K, listener: EventListener<K>) {
    let set = this.onceListeners.get(event);
    if (!set) {
      set = new Set();
      this.onceListeners.set(event, set);
    }
    set.add(listener as EventListener<any>);
    return () => this.offOnce(event, listener);
  }

  off<K extends EventName>(event: K, listener: EventListener<K>) {
    const set = this.listeners.get(event);
    if (set) {
      set.delete(listener as EventListener<any>);
      if (set.size === 0) this.listeners.delete(event);
    }
    this.offOnce(event, listener);
  }

  private offOnce<K extends EventName>(event: K, listener: EventListener<K>) {
    const setOnce = this.onceListeners.get(event);
    if (setOnce) {
      setOnce.delete(listener as EventListener<any>);
      if (setOnce.size === 0) this.onceListeners.delete(event);
    }
  }

  emit<K extends EventName>(event: K, payload: EventPayload<K>) {
    const nowListeners = this.listeners.get(event);
    if (nowListeners) {
      for (const l of Array.from(nowListeners)) {
        try {
          const res = l(payload as any);
          if (res instanceof Promise) {
            // fire-and-forget to avoid unhandled rejections at callsite
            res.catch(() => {});
          }
        } catch {
          // swallow listener errors to avoid breaking bus
        }
      }
    }

    const onceSet = this.onceListeners.get(event);
    if (onceSet) {
      for (const l of Array.from(onceSet)) {
        try {
          const res = l(payload as any);
          if (res instanceof Promise) {
            res.catch(() => {});
          }
        } catch {
          // ignore
        }
      }
      this.onceListeners.delete(event);
    }
  }

  removeAllListeners() {
    this.listeners.clear();
    this.onceListeners.clear();
  }
}

export type RunControllerHooks = {
  onPause?: () => void;
  onResume?: () => void;
  onCancel?: () => void;
};

export class DefaultRunHandle implements RunHandle {
  public readonly runId: RunId;
  public readonly bus: EventBus;

  private paused = false;
  private cancelled = false;

  private hooks: RunControllerHooks;

  constructor(runId: RunId, bus?: EventBus, hooks?: RunControllerHooks) {
    this.runId = runId;
    this.bus = bus ?? new TypedEventBus();
    this.hooks = hooks ?? {};
  }

  on = this.bus.on.bind(this.bus);
  once = this.bus.once.bind(this.bus);

  pause(): void {
    if (this.cancelled || this.paused) return;
    this.paused = true;
    this.hooks.onPause?.();
  }

  resume(): void {
    if (this.cancelled || !this.paused) return;
    this.paused = false;
    this.hooks.onResume?.();
  }

  cancel(): void {
    if (this.cancelled) return;
    this.cancelled = true;
    this.hooks.onCancel?.();
  }

  // Helpers for agent engines: inspect current state
  get isPaused() {
    return this.paused;
  }
  get isCancelled() {
    return this.cancelled;
  }
}

// Factory to create a run handle and event bus for a new agent run
export function createRunHandle(runId: RunId, hooks?: RunControllerHooks) {
  const bus = new TypedEventBus();
  const handle = new DefaultRunHandle(runId, bus, hooks);
  return { handle, bus } as const;
}
