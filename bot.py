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


@bot.message_handler()
def message_handler(message):
    if message.text == "/start":
        database.init_user(message.from_user.id)
        welcome(message)


bot.polling(non_stop=True)
