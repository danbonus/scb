from vkbottle_overrides.bot import Blueprint

bp = Blueprint()
bp.name = "Registration: choose language"

'''
@bp.on.private_message(state=RegistrationStates.LANGUAGE_STATE)
async def language_handler(message: Message, scb: SCB):
    print(scb.phrases.languages)
    payload = json.loads(message.payload)
    if payload:
        language = payload["language"]
    else:
        if not message.text.lower() in scb.phrases.languages:
            return scb.phrases.grade_creation.wrong_language
        language = scb.phrases.languages[message.text.lower()]

    answer = scb.phrases.registration.reg_grade
    grades_list = await scb.grades.list

    if not grades_list:
        await message.answer(scb.phrases.grade_creation.no_grades, keyboard=EMPTY_KEYBOARD)
        await bp.state_dispenser.set(message.peer_id, GradeCreationStates.LABEL)
        return

    grades, keyboard = grades_iteration(grades_list)

    await message.answer(answer.safe_substitute(grades=grades), keyboard=keyboard)
    await bp.state_dispenser.set(message.peer_id, RegistrationStates.GRADE_CHECK)
'''