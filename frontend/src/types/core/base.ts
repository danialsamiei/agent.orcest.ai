export type MaestristEventType =
  | "message"
  | "system"
  | "agent_state_changed"
  | "change_agent_state"
  | "run"
  | "read"
  | "write"
  | "edit"
  | "run_ipython"
  | "delegate"
  | "browse"
  | "browse_interactive"
  | "reject"
  | "think"
  | "finish"
  | "error"
  | "recall"
  | "mcp"
  | "call_tool_mcp"
  | "task_tracking"
  | "user_rejected";

export type MaestristSourceType = "agent" | "user" | "environment";

interface MaestristBaseEvent {
  id: number;
  source: MaestristSourceType;
  message: string;
  timestamp: string; // ISO 8601
}

export interface MaestristActionEvent<
  T extends MaestristEventType,
> extends MaestristBaseEvent {
  action: T;
  args: Record<string, unknown>;
}

export interface MaestristObservationEvent<
  T extends MaestristEventType,
> extends MaestristBaseEvent {
  cause: number;
  observation: T;
  content: string;
  extras: Record<string, unknown>;
}
