from vkbottle_overrides.bot import Blueprint
from utils.args_object import SCB
from constants.states import GradeCreationStatesList, GradeCreationStates
from vkbottle_overrides.bot import Message
from vkbottle.tools.dev_tools import message_min
from logger import logger

bp = Blueprint()
bp.name = "Back Handler"


async def get_requests(requests, state_handlers, scb, step):
    logger.info("Get Requests Function Called")
    #logger.info(requests)
    for request in requests:
        #logger.debug("Request: %s" % request)

        if request["handler"] in state_handlers:
            #logger.warning("Request handler in state_handlers")
            handler = request["handler"]
            last_event = request["event"]
            #logger.critical("RETURNING")
            return handler, last_event

    logger.error("NEW ITERATION!")
    new_requests = await scb.requests.get_last_requests_by_count(step, 10)
    return await get_requests(new_requests, state_handlers, scb, step + 10)


@bp.on.message(text="Вернуться", state=GradeCreationStatesList)
async def back_handler(message: Message, scb: SCB):
    await scb.requests.update(return_command=True)
    logger.debug("Current state: %s" % message.state_peer.state)
    state_revert = message.state_peer.state - 2

    if state_revert < GradeCreationStates.CMD_CHOICE:
        state = "NO_STATE"
        await bp.state_dispenser.delete(message.peer_id)
        logger.warning("State deleted")
        requests = await scb.requests.get_stateless_requests_by_count(0, 10)

    else:
        state = GradeCreationStates(state_revert)
        await bp.state_dispenser.set(message.peer_id, state)
        logger.warning("New state: %s" % GradeCreationStates(state_revert))
        requests = await scb.requests.get_last_requests_by_count(0, 10)
        logger.info("Requests fetched")

    state_handlers = scb.context["states"][state]
    # new_state = (await bp.state_dispenser.get(message.peer_id)).state
    #logger.debug("New state: %s" % new_state)

    handler, last_event = await get_requests(requests, state_handlers, scb, 10)

    for i in scb.context["handlers"]:
        if i.handler.__name__ != "back_handler":
            event = message_min(last_event, message.ctx_api)
            event.state_peer = await bp.state_dispenser.cast(message.peer_id)
            result = await i.filter(event, scb)
            if result == {} or result:
                logger.info("Back-handling: %s" % i)
                await i.handle(event, scb)
                return

    logger.error("ANSWERED")
