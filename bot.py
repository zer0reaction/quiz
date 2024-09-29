import telebot, database, creds, re
from telebot.types import InlineKeyboardButton, ReplyKeyboardMarkup

bot = telebot.TeleBot(token=creds.token)


def welcome(message):
    print("Welcoming user " + str(message.from_user.id))

    database.change_user_state(message.from_user.id, "welcome")

    text = "Ответы вводятся согласно нормам русского языка.\n\nВыберите вопрос:"
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    labels = database.get_question_labels()
    question_statuses = database.get_question_statuses(message.from_user.id)

    for i in range(len(labels)):
        label = labels[i]

        if str(question_statuses[i]) == "right":
            label += "✅"
        elif question_statuses[i] == "wrong":
            label += "❌"

        markup.add(InlineKeyboardButton(label))

    bot.send_message(message.chat.id, text, reply_markup=markup)


def display_question(message, question_number: int):
    print("Displaying question for user " + str(message.from_user.id))

    database.change_user_state(message.from_user.id, "viewing_question_" + str(question_number))

    data = database.get_question_qha(question_number)

    text = data[0]
    photo = database.get_question_photo(question_number)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    answer_button = InlineKeyboardButton("Ответить на вопрос")
    back_button = InlineKeyboardButton("Назад")

    markup.add(answer_button)
    markup.add(back_button)

    bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup)


def answer_question(message, question_number: int):
    print("User " + str(message.from_user.id) + " is answering question")

    database.change_user_state(message.from_user.id, "answering_question_" + str(question_number))

    text = "Отправьте Ваш ответ на вопрос:"
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    back_button = InlineKeyboardButton("Назад")

    markup.add(back_button)

    bot.send_message(message.from_user.id, text, reply_markup=markup)


def check_answer(message, question_number: int):
    print("Checking answer for user " + str(message.from_user.id))
    data = database.get_question_qha(question_number)

    answers = data[2]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    if message.text in answers.split(", "):
        text = "Поздравляем! Ваш ответ верный"

        database.change_question_status(question_number, message.from_user.id, "right")
        database.change_user_state(message.from_user.id, "answered_right_" + str(question_number))

        markup.add(InlineKeyboardButton("Назад"))

        bot.send_message(message.chat.id, text, reply_markup=markup)
    else:
        text = "Ваш ответ неверный. Попробуйте еще раз или воспользуйтесь подсказкой"

        database.change_question_status(question_number, message.from_user.id, "wrong")
        database.change_user_state(message.from_user.id, "answered_wrong_" + str(question_number))

        markup.add(InlineKeyboardButton("Подсказка"))
        markup.add(InlineKeyboardButton("Назад"))

        bot.send_message(message.chat.id, text, reply_markup=markup)


def show_hint(message, question_number):
    print("Showing hint for user " + str(message.from_user.id))

    data = database.get_question_qha(question_number)
    hint = data[1]

    bot.send_message(message.chat.id, "Подсказка: " + str(hint))
    answer_question(message, question_number)


@bot.message_handler()
def message_handler(message):
    text = message.text
    state = database.get_user_state(message.from_user.id)
    labels = database.get_question_labels()

    if text == "/start":
        database.init_user(message.from_user.id)
        welcome(message)

    elif text == "Назад" and ("viewing_question_" in str(state)):
        welcome(message)

    elif text == "Назад" and ("answering_question_" in str(state)):
        question_number = int(re.findall(r"\d+", str(state))[0])
        display_question(message, question_number)

    elif text == "Назад" and ("answered_right_" in str(state)):
        welcome(message)

    elif text == "Назад" and ("answered_wrong_" in str(state)):
        welcome(message)

    elif text[:-1] in labels and state == "welcome":
        question_number = labels.index(text[:-1]) + 1
        display_question(message, question_number)

    elif text in labels and state == "welcome":
        question_number = labels.index(text) + 1
        display_question(message, question_number)

    elif text == "Ответить на вопрос" and ("viewing_question_" in str(state)):
        question_number = int(re.findall(r"\d+", str(state))[0])
        answer_question(message, question_number)

    elif text == "Подсказка" and "answered_wrong_" in str(state):
        question_number = int(re.findall(r"\d+", str(state))[0])
        show_hint(message, question_number)

    elif "answering_question_" in str(state):
        question_number = int(re.findall(r"\d+", str(state))[0])
        check_answer(message, question_number)

    elif "answered_wrong_" in str(state):
        question_number = int(re.findall(r"\d+", str(state))[0])
        check_answer(message, question_number)


bot.polling(non_stop=True)
