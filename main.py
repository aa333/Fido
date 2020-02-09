#!/usr/bin/env python

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.utils.request import Request
from MQBot import MQBot

from accessControls import botAdminsRestricted, botOwnerRestricted

from mod_errorHandler import onError
from mod_tests import init_tests
from mod_help import init_help


# TODO MVC
# basic help
# 
# custom greeting module 
#   - work in groups (replies, mentions)
#   - command chains

# TODO NTH
# restarting

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

with open('token.txt', 'r') as file:
    token = file.read().replace('\n', '')

def start(update, context):
    """Send a message when the command /start is issued."""
    if (update.message.chat_id != 0):
        update.message.reply_text('Hello there. Ask /help if you need it')


def reply(update, context):
    update.message.reply_text('Woof!')


def main():
    """Start the bot."""

    # set connection pool size for bot
    request = Request(con_pool_size=8)
    throttledBot = MQBot(token, request=request)
    updater = Updater(bot=throttledBot, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    
    init_tests(dp)
    init_help(dp)

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, reply))

    # log all errors
    dp.add_error_handler(onError)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
