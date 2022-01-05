from vkbottle import Text, KeyboardButtonColor

from vkbottle_overrides import Keyboard


def subjects_iteration(subjects_list, row=3):
    smth_plain_list = ""
    keyboard = Keyboard()
    #  LANGUAGES_KEYBOARD.buttons = []

    for subject in subjects_list:
        nomn = subject.nomn
        color = KeyboardButtonColor.PRIMARY
        if subject.lang_group or subject.exam_group:
            color = KeyboardButtonColor.SECONDARY
            nomn = f"{subject.nomn} {subject.name}"
        if subject.label.endswith("-el"):
            color = KeyboardButtonColor.SECONDARY
        keyboard.add(Text(nomn, {"subject": subject.label}), color=color, row=row)
        smth_plain_list += f"-- {nomn}\n"

    return smth_plain_list, keyboard


def subjects_to_delete_iteration(homework_list, row=3):
    smth_plain_list = ""
    keyboard = Keyboard()
    #  LANGUAGES_KEYBOARD.buttons = []

    for homework in homework_list:
        nomn = homework.subject.nomn
        color = KeyboardButtonColor.PRIMARY
        if homework.subject.lang_group or homework.subject.exam_group:
            color = KeyboardButtonColor.SECONDARY
            nomn = f"{homework.subject.nomn} {homework.subject.name}"
        if homework.subject.label.endswith("-el"):
            color = KeyboardButtonColor.SECONDARY
        keyboard.add(Text(f"[{homework.homework_id}] {nomn} ({homework.homework}"[:37] + "..)", {"homework_id": homework.homework_id}), color=color, row=row)
        print("adding button")
        smth_plain_list += f"-- {nomn}\n"

    return smth_plain_list, keyboard
