from vkbottle_overrides.bot import Blueprint

bp = Blueprint()
bp.name = "Users Control"
#  phrases.load(Menu)


'''@bp.on.private_message()
async def menu(message: Message, scb: SCB):
    await message.answer(scb.phrases.menu.user_menu,keyboard=MENU_KEYBOARD)


@bp.on.private_message(IsWriter=True)
async def writer_menu(message: Message, scb: SCB):
    await message.answer(scb.phrases.menu.user_menu, keyboard=MENU_KEYBOARD)'''
