import { MaestristObservation } from "./types/core/observations";
import { MaestristAction } from "./types/core/actions";

export type Message = {
  sender: "user" | "assistant";
  content: string;
  timestamp: string;
  imageUrls?: string[];
  type?: "thought" | "error" | "action";
  success?: boolean;
  pending?: boolean;
  translationID?: string;
  eventID?: number;
  observation?: { payload: MaestristObservation };
  action?: { payload: MaestristAction };
};
