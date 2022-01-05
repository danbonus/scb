from vkbottle_overrides.bot import Blueprint

#from constants.keyboards import GRADES_KEYBOARD

bp = Blueprint()
bp.name = "Grades Menu"


'''@bp.on.private_message(text="Классы", IsAdmin=True)
async def grades_menu(message: Message, scb: SCB):
    await message.answer(scb.phrases.menu.grades, keyboard=GRADES_KEYBOARD)
    await bp.state_dispenser.set(message.peer_id, GradesMenuStates.CMD_CHOICE)'''
