import { MaestristAction } from "#/types/core/actions";
import { MaestristEventType } from "#/types/core/base";
import {
  isCommandAction,
  isCommandObservation,
  isMaestristAction,
  isMaestristObservation,
} from "#/types/core/guards";
import { MaestristObservation } from "#/types/core/observations";

const COMMON_NO_RENDER_LIST: MaestristEventType[] = [
  "system",
  "agent_state_changed",
  "change_agent_state",
];

const ACTION_NO_RENDER_LIST: MaestristEventType[] = ["recall"];

const OBSERVATION_NO_RENDER_LIST: MaestristEventType[] = ["think"];

export const shouldRenderEvent = (
  event: MaestristAction | MaestristObservation,
) => {
  if (isMaestristAction(event)) {
    if (isCommandAction(event) && event.source === "user") {
      // For user commands, we always hide them from the chat interface
      return false;
    }

    const noRenderList = COMMON_NO_RENDER_LIST.concat(ACTION_NO_RENDER_LIST);
    return !noRenderList.includes(event.action);
  }

  if (isMaestristObservation(event)) {
    if (isCommandObservation(event) && event.source === "user") {
      // For user commands, we always hide them from the chat interface
      return false;
    }

    const noRenderList = COMMON_NO_RENDER_LIST.concat(
      OBSERVATION_NO_RENDER_LIST,
    );
    return !noRenderList.includes(event.observation);
  }

  return true;
};

export const hasUserEvent = (
  events: (MaestristAction | MaestristObservation)[],
) =>
  events.some((event) => isMaestristAction(event) && event.source === "user");
