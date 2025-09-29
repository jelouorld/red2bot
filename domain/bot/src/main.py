import router
import typing as tp

import dataaccess
import responses
import ai
import exceptions as ex

@router.route("/init", method="POST")
def init():
    try:
        session_id: dataaccess.UUID4 = dataaccess.chats.init_conversation()
        return responses.success_created(session_id)
    except Exception as e:
        # if os environ.debug:
        return responses.error("Error initializing conversation: " + str(e))


@router.route("/chat/{session_id}", method="POST")
def chat(session_id: str, *, text=""):

    # validate session_id


    conversation = dataaccess.chats.add_message(session_id, role="user", content=text)

    return {"session_id": session_id, "text": text}


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
        return responses.error("Error routing request: " + str(e))