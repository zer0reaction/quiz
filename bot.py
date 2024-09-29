import telebot, database, creds

bot = telebot.TeleBot(token=creds.token)


def welcome():
    ...


@bot.message_handler()
def message_handler(message):
    if message.text == "/start":
        database.init_user(message.from_user.id)
        welcome()


bot.polling(non_stop=True)
