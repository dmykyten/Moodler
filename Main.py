from telegram.ext import CommandHandler, Dispatcher, Updater, MessageHandler, Filters
from time import sleep, time
from MoodleNotifier import Credentials

TOKEN = "TOKEN"
credentials = {"login": "john.dou",
               "password": "password",
               "url": "https://cms.ucu.edu.ua"}
start_time = time()

notifier = Credentials(credentials)

def reauth():
    if time() - start_time >= 3600:
        notifier.auth_moodle()

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Greetings! I'm MoodlerBot!")


def tasks(update, context):
    sleep(0.100)
    reauth()
    answer = notifier.get_tasks()
    context.bot.send_message(chat_id=update.effective_chat.id, text=answer)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
start_handler = CommandHandler('start', start)
tasks_handler = CommandHandler('tasks', tasks)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(tasks_handler)
updater.start_polling(poll_interval=0.3)


















"""
bot = telegram.Bot(TOKEN)
updates = bot.get_updates()
start_handler = CommandHandler('start', start(updates, ))
dispatcher = updater.dispatcher
dispatcher.add_handler(handler=start_handler)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def tasks(update, context):
    pass

def return_tasks(message, text):
    user_id = message.from_user.id
    bot.send_chat_action(chat_id=user_id, action=telegram.ChatAction.TYPING)
    sleep(1)
    bot.send_message(chat_id=user_id, text=text)

print(bot.getMe())
dispatcher.start()
while True:
    if not(updates is None or updates == []) and updates != bot.get_updates():

    updates = bot.get_updates()
    sleep(2)
    print(bot.getMe())
"""
