

from access_controls import botAdminsRestricted, botOwnerRestricted
from telegram.ext import CommandHandler

@botOwnerRestricted
def test_queue(update, context):
    for ix in range(10):
        context.bot.send_message(chat_id=update.message.chat_id, text='%s) %s' % (ix + 1, update.message.text))

def init_tests(dp):
    dp.add_handler(CommandHandler("testQueue", test_queue))