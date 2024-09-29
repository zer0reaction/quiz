import telebot, database, creds
from telebot.types import InlineKeyboardButton, ReplyKeyboardMarkup

bot = telebot.TeleBot(token=creds.token)


def welcome(message):
    text = "Ответы вводятся согласно нормам русского языка.\n\nВыберите вопрос:"
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    labels = database.get_question_labels()

    for label in labels:
        markup.add(InlineKeyboardButton(label))

    bot.send_message(message.chat.id, text, reply_markup=markup)
    database.change_user_state(message.from_user.id, "welcome")


def display_question(message, question_number: int):
    data = database.get_question_qha(question_number)

    text = data[0]
    photo = database.get_question_photo(question_number)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    answer_button = InlineKeyboardButton("Ответить на вопрос")
    back_button = InlineKeyboardButton("Назад")

    markup.add(answer_button)
    markup.add(back_button)

    bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup)
    database.change_user_state(message.from_user.id, "viewing_question_" + str(question_number))


@bot.message_handler()
def message_handler(message):
    text = message.text
    state = database.get_user_state(message.from_user.id)
    labels = database.get_question_labels()

    if message.text == "/start":
        database.init_user(message.from_user.id)
        welcome(message)
    elif message.text == "Назад" and ("viewing_question_" in str(state)):
        welcome(message)
    elif text in labels and state == "welcome":
        display_question(message, labels.index(text) + 1)


bot.polling(non_stop=True)
