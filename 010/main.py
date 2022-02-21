from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, ConversationHandler
from time import sleep
from random import randint

def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')


COUNT_CANDY, MAX_CANDY, EAT_CANDY, BOT_CANDY = range(4)

count_candies = 2022
eat_candies = 8
max_candy = 5

def start_talk(update: Update, _):
    update.message.reply_text(
        'Привет! Давай сыграем в игру конфеты. \
        Задай количество конфет в игре')
    return COUNT_CANDY

def max_count_candy(update: Update, _):
    global max_candy
    max_candy = int(update.message.text)
    update.message.reply_text(
        'Сколько возьмем конфет?')
    return EAT_CANDY

def count_candy(update: Update, _):             # За ход берет
    global count_candies
    count_candies = int(update.message.text)
    update.message.reply_text(
         'А еще давай проговорим какое количество конфет можно брать за ход?')
    return MAX_CANDY

def eat_candy(update: Update, context: CallbackContext):
    global count_candies
    global eat_candies
    global max_candy
    eat_candies = int(update.message.text)
    if eat_candies > max_candy:
        return update.message.reply_text(
        'Хватайте его, он не честно ведет игру!!!')


    count_candies -= eat_candies
    update.message.reply_text(
        f'Вы взяли {eat_candies}, осталось {count_candies}')
    if count_candies >= max_candy:
        count_candies, eat_candies = bot_candy(count_candies, max_candy)
        sleep(1)
        update.message.reply_text(
            f'Я взял {eat_candies}, осталось {count_candies}')
    if count_candies < max_candy:
        update.message.reply_text(
        'Игра окончена, кто последний взял тот и крут!')
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Введите сколько вы хотите конфет взять')
        return EAT_CANDY

def goodbye(update: Update, _): 
    update.message.reply_text(
        'Хватайте его, он не честно ведет игру!!!')
    return ConversationHandler.END
    
def bot_candy(candies, max_candy):
    eat = candies %(max_candy + 1)
    if eat == 0:
        eat = randint(1, max_candy + 1)
    candies -= eat 
    return (candies, eat)

conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('talk', start_talk)],
    states={
        COUNT_CANDY: [MessageHandler(Filters.text, count_candy)],
        MAX_CANDY: [MessageHandler(Filters.text, max_count_candy)],
        EAT_CANDY: [MessageHandler(Filters.text, eat_candy)],
        BOT_CANDY: [MessageHandler(Filters.text, bot_candy)]
        # GOODBYE: [MessageHandler(Filters.text, goodbye)]
    },
    fallbacks=[CommandHandler('bye', goodbye)]
)

updater = Updater('5176377813:AAFN_TYTB7-5fsD5qOhEt9OJQlWHiTsnErE')
updater.dispatcher.add_handler(CommandHandler('hello', hello))
# updater.dispatcher.add_handler(CommandHandler('talk', bot_conversation))
# updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo_message))
updater.dispatcher.add_handler(conversation_handler)


updater.start_polling()
updater.idle()


