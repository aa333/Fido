
from telegram import ParseMode
from functools import wraps
from config import admins, authorId

from api import get_admin_ids

# Access control wrappers. Test that user belongs to certain group before running a handler


def botAdminsRestricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in admins:
            context.bot.send_message(authorId, "Unauthorized admin func {} access denied for {}.".format(
                func.__name__, user_id), parse_mode=ParseMode.HTML)
            return
        return func(update, context, *args, **kwargs)
    return wrapped


def botOwnerRestricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id != authorId:
            context.bot.send_message(authorId, "Unauthorized owner func {} access denied for {}.".format(
                func.__name__, user_id), parse_mode=ParseMode.HTML)
            return
        return func(update, context, *args, **kwargs)
    return wrapped


def groupAdminsRestricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if update.effective_user.id in get_admin_ids(context.bot, update.message.chat_id):
            context.bot.send_message(authorId, "Unauthorized owner func {} access denied for {}.".format(
                func.__name__, user_id), parse_mode=ParseMode.HTML)
            return
        return func(update, context, *args, **kwargs)
    return wrapped
