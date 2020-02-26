#!/usr/bin/env python

import logging
import os
import sys
from threading import Thread

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, PicklePersistence
from telegram.utils.request import Request
from MQBot import MQBot

from access_controls import botAdminsRestricted, botOwnerRestricted
from config import ownerId

from modules.errorHandler import onError
from modules.tests import init_tests
from modules.help import init_help

# TODO MVC
# 
# custom greeting module - ConversationHandler, 
# if in private, ask which group (from all joined), save reply to chat_data.
# restrict access to groups by asking owner.
# group admins handling. everyone_is_admin case.

# TODO NTH
#
# module bus - register, auto-gather descriptions and help, permission management


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

    persistence = PicklePersistence(filename='bot_state')
    # set connection pool size for bot
    request = Request(con_pool_size=8)
    throttledBot = MQBot(token, request=request)
    updater = Updater(bot=throttledBot, use_context=True, persistence=persistence)
    updater.bot.send_message(ownerId, "Woof! Woof!", timeout=10)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    def stop_and_restart():
       updater.stop()
       os.execl(sys.executable, sys.executable, *sys.argv)

    @botAdminsRestricted
    def restart(update, context):
        update.message.reply_text('Bot is restarting...')
        Thread(target=stop_and_restart).start()

    dp.add_handler(CommandHandler('restart', restart))

    
    # Setup command handlers
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
