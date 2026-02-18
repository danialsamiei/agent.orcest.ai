import { MaestristAction } from "./actions";
import { MaestristObservation } from "./observations";
import { MaestristVariance } from "./variances";

/**
 * @deprecated Will be removed once we fully transition to v1 events
 */
export type MaestristParsedEvent =
  | MaestristAction
  | MaestristObservation
  | MaestristVariance;
