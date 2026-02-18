import { MaestristParsedEvent } from ".";
import {
  UserMessageAction,
  AssistantMessageAction,
  MaestristAction,
  SystemMessageAction,
  CommandAction,
  FinishAction,
  TaskTrackingAction,
} from "./actions";
import {
  AgentStateChangeObservation,
  CommandObservation,
  ErrorObservation,
  MCPObservation,
  MaestristObservation,
  TaskTrackingObservation,
} from "./observations";
import { StatusUpdate } from "./variances";

export const isMaestristEvent = (
  event: unknown,
): event is MaestristParsedEvent =>
  typeof event === "object" &&
  event !== null &&
  "id" in event &&
  "source" in event &&
  "message" in event &&
  "timestamp" in event;

export const isMaestristAction = (
  event: MaestristParsedEvent,
): event is MaestristAction => "action" in event;

export const isMaestristObservation = (
  event: MaestristParsedEvent,
): event is MaestristObservation => "observation" in event;

export const isUserMessage = (
  event: MaestristParsedEvent,
): event is UserMessageAction =>
  isMaestristAction(event) &&
  event.source === "user" &&
  event.action === "message";

export const isAssistantMessage = (
  event: MaestristParsedEvent,
): event is AssistantMessageAction =>
  isMaestristAction(event) &&
  event.source === "agent" &&
  (event.action === "message" || event.action === "finish");

export const isErrorObservation = (
  event: MaestristParsedEvent,
): event is ErrorObservation =>
  isMaestristObservation(event) && event.observation === "error";

export const isCommandAction = (
  event: MaestristParsedEvent,
): event is CommandAction => isMaestristAction(event) && event.action === "run";

export const isAgentStateChangeObservation = (
  event: MaestristParsedEvent,
): event is AgentStateChangeObservation =>
  isMaestristObservation(event) && event.observation === "agent_state_changed";

export const isCommandObservation = (
  event: MaestristParsedEvent,
): event is CommandObservation =>
  isMaestristObservation(event) && event.observation === "run";

export const isFinishAction = (
  event: MaestristParsedEvent,
): event is FinishAction =>
  isMaestristAction(event) && event.action === "finish";

export const isSystemMessage = (
  event: MaestristParsedEvent,
): event is SystemMessageAction =>
  isMaestristAction(event) && event.action === "system";

export const isRejectObservation = (
  event: MaestristParsedEvent,
): event is MaestristObservation =>
  isMaestristObservation(event) && event.observation === "user_rejected";

export const isMcpObservation = (
  event: MaestristParsedEvent,
): event is MCPObservation =>
  isMaestristObservation(event) && event.observation === "mcp";

export const isTaskTrackingAction = (
  event: MaestristParsedEvent,
): event is TaskTrackingAction =>
  isMaestristAction(event) && event.action === "task_tracking";

export const isTaskTrackingObservation = (
  event: MaestristParsedEvent,
): event is TaskTrackingObservation =>
  isMaestristObservation(event) && event.observation === "task_tracking";

export const isStatusUpdate = (event: unknown): event is StatusUpdate =>
  typeof event === "object" &&
  event !== null &&
  "status_update" in event &&
  "type" in event &&
  "id" in event;

export const isActionOrObservation = (
  event: MaestristParsedEvent,
): event is MaestristAction | MaestristObservation =>
  isMaestristAction(event) || isMaestristObservation(event);
