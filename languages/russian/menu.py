from string import Template


class Menu:
    user = {
        "plain": Template("$greeting Список доступных команд (можно просто написать цифру): "),
        "keyboard": Template("$greeting Выбери команду из панели кнопок.")
    }

    writer = {
        "plain": Template("$greeting Список доступных команд: "),
        "keyboard": Template("$greeting Выбери команду из панели кнопок.")
    }

    admins = {
        "plain": Template("$greeting Список доступных команд: "),
        "keyboard": Template("$greeting Выбери команду из панели кнопок. ")
    }

    grades = {
        "plain": """Управление классами. Команды: 
            1) Создать класс
            2) Редактировать класс
            3) Удалить класс
            4) Список классов
            Напиши цифру нужной команды, либо <<назад>>, чтобы выйти из управления классами.""",
        "keyboard": "Анальное админ-меню. Я слушаю!"
    }