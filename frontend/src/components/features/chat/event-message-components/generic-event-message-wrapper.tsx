import React from "react";
import { MaestristAction } from "#/types/core/actions";
import { MaestristObservation } from "#/types/core/observations";
import { isMaestristAction, isMaestristObservation } from "#/types/core/guards";
import { ChatMessage } from "../chat-message";
import { GenericEventMessage } from "../generic-event-message";
import { ConfirmationButtons } from "#/components/shared/buttons/confirmation-buttons";
import { getEventContent } from "../event-content-helpers/get-event-content";
import { getObservationResult } from "../event-content-helpers/get-observation-result";

const hasThoughtProperty = (
  obj: Record<string, unknown>,
): obj is { thought: string } => "thought" in obj && !!obj.thought;

interface GenericEventMessageWrapperProps {
  event: MaestristAction | MaestristObservation;
  shouldShowConfirmationButtons: boolean;
}

export function GenericEventMessageWrapper({
  event,
  shouldShowConfirmationButtons,
}: GenericEventMessageWrapperProps) {
  return (
    <div>
      {isMaestristAction(event) &&
        hasThoughtProperty(event.args) &&
        event.action !== "think" && (
          <ChatMessage type="agent" message={event.args.thought} />
        )}

      <GenericEventMessage
        title={getEventContent(event).title}
        details={getEventContent(event).details}
        success={
          isMaestristObservation(event)
            ? getObservationResult(event)
            : undefined
        }
      />

      {shouldShowConfirmationButtons && <ConfirmationButtons />}
    </div>
  );
}
