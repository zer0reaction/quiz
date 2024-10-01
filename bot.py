import telebot, users_database, quiz_database, creds, re
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

bot = telebot.TeleBot(token=creds.token, parse_mode="HTML")


def welcome(message):
    print("Welcoming user " + str(message.from_user.id))

    users_database.change_user_state(message.from_user.id, "welcome")

    text = "Привет! Поучаствуй в нашей викторине!\n\n<b>Выбери вопрос:</b>"
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    labels = quiz_database.get_question_labels()
    question_statuses = users_database.get_question_statuses(message.from_user.id)

    for i in range(len(labels)):
        label = labels[i]
        question_status = question_statuses[i]

        if question_status == "right":
            label += "✅"
        elif question_status == "wrong":
            label += "❌"

        markup.add(InlineKeyboardButton(label))

    bot.send_message(message.chat.id, text, reply_markup=markup)


def display_question(message, question_number: int):
    print("Displaying question for user " + str(message.from_user.id))

    users_database.change_user_state(message.from_user.id, "viewing_question_" + str(question_number))

    data = quiz_database.get_question_qa(question_number)

    text = data[0]
    photo = quiz_database.get_question_photo(question_number)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    answer_button = InlineKeyboardButton("Ответить на вопрос")
    hint_button = InlineKeyboardButton("Хочешь подсказку?")
    back_button = InlineKeyboardButton("Назад")

    markup.add(answer_button)
    markup.add(hint_button)
    markup.add(back_button)

    bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup)


def answer_question(message, question_number: int):
    print("User " + str(message.from_user.id) + " is answering question")

    users_database.change_user_state(message.from_user.id, "answering_question_" + str(question_number))

    text = "Отправьте Ваш ответ на вопрос:"
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    back_button = InlineKeyboardButton("Назад")

    markup.add(back_button)

    bot.send_message(message.from_user.id, text, reply_markup=markup)


def check_answer(message, question_number: int):
    print("Checking answer for user " + str(message.from_user.id))
    data = quiz_database.get_question_qa(question_number)

    answers = data[1]
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    if message.text in answers.split(", "):
        text = "Поздравляем! Ваш ответ верный"

        users_database.change_question_status(question_number, message.from_user.id, "right")
        users_database.change_user_state(message.from_user.id, "answered_right_" + str(question_number))

        markup.add(InlineKeyboardButton("Назад"))

        bot.send_message(message.chat.id, text, reply_markup=markup)

    else:
        text = "Ваш ответ неверный. Попробуйте еще раз или воспользуйтесь подсказкой"

        users_database.change_question_status(question_number, message.from_user.id, "wrong")
        users_database.change_user_state(message.from_user.id, "answered_wrong_" + str(question_number))

        markup.add(InlineKeyboardButton("Хочешь подсказку?"))
        markup.add(InlineKeyboardButton("Назад"))

        bot.send_message(message.chat.id, text, reply_markup=markup)


def show_hints(message, question_number):
    print("Showing hints for user " + str(message.from_user.id))

    state = users_database.get_user_state(message.from_user.id)

    if "answered_wrong_" in str(state):
        users_database.change_user_state(message.from_user.id, "viewing_hints_for_question_after_answering_wrong_" + str(question_number))
    else:
        users_database.change_user_state(message.from_user.id, "viewing_hints_for_question_" + str(question_number))

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    
    hints_amount = quiz_database.get_hints_amount(question_number)
    for i in range(1, hints_amount + 1):
        markup.add(InlineKeyboardButton("Подсказка " + str(i)))

    markup.add(InlineKeyboardButton("Назад"))

    bot.send_message(message.chat.id, "Выбери подсказку:", reply_markup=markup)


def show_hint(message, question_number: int, hint_number: int):
    print("Showing hint for user " + str(message.from_user.id))

    state = users_database.get_user_state(message.from_user.id)

    if "viewing_hints_for_question_after_answering_wrong_" in str(state): 
        users_database.change_user_state(message.from_user.id, "viewing_hint_for_question_after_answering_wrong_" + str(hint_number) + "_" + str(question_number))

    elif "viewing_hints_for_question_" in str(state): 
        users_database.change_user_state(message.from_user.id, "viewing_hint_for_question_" + str(hint_number) + "_" + str(question_number))

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(InlineKeyboardButton("Назад"))

    photo = quiz_database.get_hint_photo(question_number, hint_number)
    text = quiz_database.get_hint_text(question_number, hint_number)

    bot.send_photo(message.chat.id, photo=photo, caption=text, reply_markup=markup)


@bot.message_handler(commands=["start", "reset"])
def start(message):
    text = message.text

    if text == "/start":
        users_database.init_user(message.from_user.id)
        welcome(message)

    elif text == "/reset":
        users_database.reset_user(message.from_user.id)
        welcome(message)


@bot.message_handler()
def message_handler(message):
    text = message.text
    state = users_database.get_user_state(message.from_user.id)
    labels = quiz_database.get_question_labels()

    # Checking back buttons
    if text == "Назад":
        if "viewing_question_" in str(state):
            welcome(message)

        elif "answering_question_" in str(state):
            question_number = int(re.findall(r"\d+", str(state))[0])
            display_question(message, question_number)

        elif "answered_right_" in str(state):
            welcome(message)

        elif "answered_wrong_" in str(state):
            welcome(message)

        elif "viewing_hints_for_question_after_answering_wrong_" in str(state):
            question_number = int(re.findall(r"\d+", str(state))[0])
            answer_question(message, question_number)

        elif "viewing_hints_for_question_" in str(state):
            question_number = int(re.findall(r"\d+", str(state))[0])
            display_question(message, question_number)

        elif "viewing_hint_for_question_after_answering_wrong_" in str(state):
            r = re.findall(r"\d+", str(state))
            hint_number = int(r[0])
            question_number = int(r[1])

            users_database.change_user_state(message.from_user.id, "answered_wrong_" + str(question_number))
            show_hints(message, question_number)

        elif "viewing_hint_for_question_" in str(state):
            r = re.findall(r"\d+", str(state))
            hint_number = int(r[0])
            question_number = int(r[1])

            show_hints(message, question_number)

    # Checking going to questions
    elif state == "welcome":
        # When the text is with mark
        if text[:-1] in labels:
            question_number = labels.index(text[:-1]) + 1
            display_question(message, question_number)

        elif text in labels:
            question_number = labels.index(text) + 1
            display_question(message, question_number)

    # Checking question buttons
    elif text == "Ответить на вопрос" and ("viewing_question_" in str(state)):
        question_number = int(re.findall(r"\d+", str(state))[0])
        answer_question(message, question_number)

    elif text == "Хочешь подсказку?" and "answered_wrong_" in str(state):
        question_number = int(re.findall(r"\d+", str(state))[0])
        show_hints(message, question_number)

    elif text == "Хочешь подсказку?" and "viewing_question_" in str(state):
        question_number = int(re.findall(r"\d+", str(state))[0])
        show_hints(message, question_number)

    # Checking hint buttons
    elif "viewing_hints_for_question_after_answering_wrong_" in str(state):
        question_number = int(re.findall(r"\d+", str(state))[0])
        hint_number = int(re.findall(r"\d+", str(text))[0])

        show_hint(message, question_number, hint_number)

    elif "viewing_hints_for_question_" in str(state):
        question_number = int(re.findall(r"\d+", str(state))[0])
        hint_number = int(re.findall(r"\d+", str(text))[0])

        show_hint(message, question_number, hint_number)

    # Checking answers
    elif "answering_question_" in str(state):
        question_number = int(re.findall(r"\d+", str(state))[0])
        check_answer(message, question_number)

    elif "answered_wrong_" in str(state):
        question_number = int(re.findall(r"\d+", str(state))[0])
        check_answer(message, question_number)


bot.polling(non_stop=True)
