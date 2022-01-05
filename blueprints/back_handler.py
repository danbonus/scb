from logger import logger
from utils.args_object import SCB
from vkbottle_overrides.bot import Blueprint
# from constants.states import GradeCreationStatesList, GradeCreationStates
from vkbottle_overrides.bot import Message

bp = Blueprint()
bp.name = "Back Handler"

"""ГОВНОДИЩЕ ! ПРОСТО ПИЗДЕЦ ! НЕ СМОТРЕТЬ"""


'''@bp.on.private_message(text=["Вернуться", "Back", "Бэк"])
async def back_handler(message: Message, scb: SCB):
    await scb.requests.update(return_command=True)

    if message.state_peer and not len(message.state_peer.tree) == 1 and message.state_peer.tree[0]["handler"]:
        logger.debug("Current state: %s" % message.state_peer.state)
        current_state = message.state_peer
        state_tree = current_state.tree
        logger.debug("Current tree: %s" % [i for i in state_tree])

        state_index = list(state_tree).index(current_state.state)
        logger.debug("State index: %s" % state_index)
        if state_index == 1:
            previous_state = list(state_tree)[state_index - 1]
            #last_event = await get_requests(requests, handler_name, scb, 10)
        else:
            previous_state = list(state_tree)[state_index - 1]

        handler = state_tree[previous_state]["handler"]
        previous_message = state_tree[previous_state]["message"]
        print(handler)
        print(state_tree)
        await message.answer("💥 | Возвращаю на шаг назад!")
        handler_name = handler.handler.__name__

    else:
        if message.state_peer and message.state_peer.tree[0]["handler"]:
            return "а куда возвращаться то"
        print("BACK TO MENU")
        await message.answer("💥 | Возвращаю в меню!")
        handler = scb.context["handlers"]["menu"]
        handler_name = "menu"
        message.text = 'меню'
        previous_message = message

    logger.info("Back-handling: %s" % handler_name)
    await bp.state_dispenser.set_tree(message.peer_id, handler, previous_message)
    await handler.handle(previous_message, scb)
    return'''''