

from accessControls import botAdminsRestricted, botOwnerRestricted
from telegram.ext import CommandHandler

from config import admins

def help(update, context):
    u_str = """
    Fido can do: 
    
    /help - this message
    /setWelcomeMessage - set welcome message for new users of the group chat. Reply "none" to disable.
    """
    adm_str = ""
    if(update.effective_user.id in admins):
        adm_str = """
        Administrative tools:
        /testQueue - test queue sending capabilities
        """
    update.message.reply_markdown(u_str+adm_str)


def init_help(dp):
    dp.add_handler(CommandHandler("help", help))
