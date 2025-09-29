import router
import typing as tp

import responses
import exceptions as ex

import service

chatservice = service.ChatService()

@router.route("/init", method="POST")
def init():
    try:
        session_id: str= chatservice.init_conversation()
        return responses.success_conver_created(session_id)
    except ValueError as e:
        return responses.internal_error("Error initializing conversation: " + str(e))
    
@router.route("/chat/{session_id}", method="POST")
def chat(session_id: str, *, text=""):
    # validate stuff
    try:
        return responses.ok(chatservice.send_message(session_id, text))
    except ValueError as e:
        return responses.bad_request("Error sending message: " + str(e))
    except Exception as e:
        return responses.internal_error("Error processing request: " + str(e))


@router.route("/event", method="GET")
def event(event: tp.Dict[str, tp.Any]) -> tp.Dict[str, tp.Any]:
    return event


def lambda_entrypoint(event: dict, _):  # context unused
    # cli invocation
    if not event:
        return {"cli_invocation": True}

    try:
        return router.dispatch(event)
    except ex.RoutingError as e:
        return responses.bad_request("Error routing request: " + str(e))
    except Exception as e:
        return responses.internal_error("Error processing request: " + str(e))
