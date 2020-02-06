#!/usr/bin/env python

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from errorHandler import onError

# TODO
# detect conversation
# custom greeting module
# mqueue for overflow
# 

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

with open('token.txt', 'r') as file:
    token = file.read().replace('\n', '')

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello there.')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('/set-greeting') #todo move to text resources

def setHelloMessage(update, context): #todo separate module
    update.message.reply_text('Woof!')

def reply(update, context):
    update.message.reply_text('Woof!')


def main():
    """Start the bot."""

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("test-error", help))

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
