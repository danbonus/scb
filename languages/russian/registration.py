from string import Template


class Registration:
    first_entry = {
        "plain": Template("$greeting Ты тут в первый раз. Выбери один из доступных классов: grades"),
        "keyboard": Template("$greeting Ты тут в первый раз. Выбери один из доступных классов.")
    }

    must_register = {
        "plain": "Нужно зарегистрироваться! Отправь цифру 1 или напиши <<Пройти регистрацию>>",
        "keyboard": "Жми на кнопку и регистрируйся!"
    }

    choose_language = {
        "plain": Template("$greeting Выбери удобный тебе язык из списка: \n$languages"),
        "keyboard": Template("$greeting Выбери удобный тебе язык.")
    }

    reg_grade = {
        "plain": Template("Для начала выбери свой класс из списка: \n$grades"),
        "keyboard": Template("Для начала выбери свой класс.")
    }

    wrong_grade = "Такого класса нет. Выбери из списка."

    passed = Template("Регистрация пройдена. \nТвой класс: $grade.\nПодписан на рассылку: $result.")
