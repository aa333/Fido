from mwt import MWT

@MWT(timeout=60*5)
def get_admin_ids(bot, chat_id):
    """Returns a list of admin IDs for a given chat. Results are cached for 5 min."""
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]
