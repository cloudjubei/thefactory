/*
 React hook for Overseer UI: subscribes to run events and exposes a simple state interface.
 Assumes the host app provides a RunHandle-compatible object (from events/runtime) and triggers orchestrator.launch.
*/

import { useEffect, useMemo, useReducer } from "react";
import type { RunHandle } from "../../packages/factory-ts/src/events/types";

export interface UseAgentRunState {
  runId?: string;
  status: "idle" | "running" | "success" | "error" | "rejected";
  progress: string[];
  snapshot?: { tokensUsed?: number; costUsd?: number };
  proposal?: { baseDir: string; changes: any[] } | null;
  error?: string;
}

type Action =
  | { type: "start"; runId: string }
  | { type: "progress"; message: string }
  | { type: "snapshot"; tokensUsed?: number; costUsd?: number }
  | { type: "proposal"; proposal: any }
  | { type: "end"; status: UseAgentRunState["status"] }
  | { type: "error"; message: string };

function reducer(state: UseAgentRunState, action: Action): UseAgentRunState {
  switch (action.type) {
    case "start":
      return { ...state, runId: action.runId, status: "running" };
    case "progress":
      return { ...state, progress: [...state.progress, action.message] };
    case "snapshot":
      return { ...state, snapshot: { tokensUsed: action.tokensUsed, costUsd: action.costUsd } };
    case "proposal":
      return { ...state, proposal: action.proposal };
    case "end":
      return { ...state, status: action.status };
    case "error":
      return { ...state, status: "error", error: action.message };
    default:
      return state;
  }
}

export function useAgentRun(handle: RunHandle | null) {
  const [state, dispatch] = useReducer(reducer, {
    status: "idle",
    progress: [],
    proposal: null,
  } as UseAgentRunState);

  useEffect(() => {
    if (!handle) return;
    const off = [
      handle.on("run/start", (e) => dispatch({ type: "start", runId: e.runId })),
      handle.on("run/progress", (e) => dispatch({ type: "progress", message: e.message })),
      handle.on("run/progress/snapshot", (e) => dispatch({ type: "snapshot", tokensUsed: e.tokensUsed, costUsd: e.costUsd })),
      handle.on("files/proposal", (e) => dispatch({ type: "proposal", proposal: e.proposal })),
      handle.on("run/error", (e) => dispatch({ type: "error", message: e.error?.message || "unknown error" })),
      handle.on("run/end", (e) => dispatch({ type: "end", status: e.status as any })),
    ];
    return () => off.forEach((fn) => fn());
  }, [handle]);

  const actions = useMemo(() => ({
    acceptChanges(proposal: any) {
      if (!handle || !state.runId) return;
      handle.emit("files/accept", { runId: state.runId, accepted: proposal });
    },
    rejectChanges(reason?: string) {
      if (!handle || !state.runId || !state.proposal) return;
      handle.emit("files/reject", { runId: state.runId, rejected: state.proposal, reason: reason || "rejected by user" });
    },
  }), [handle, state.runId, state.proposal]);

  return { state, actions };
}
