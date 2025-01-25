import asyncio

import telegram
from typing import List, Optional
import os

from telegram.constants import ParseMode

# no Telegram token found
ERR_SERVER_TOKEN = 'TG_MISCONF_TK'
# no Telegram chat found
ERR_SERVER_CHAT = 'TG_MISCONF_CHAT'


def check_telegram_config() -> Optional[str]:
    """Check if Telegram config is properly set, otherwise return an error code"""
    token = os.environ.get('TG_TOKEN')
    if token is None:
        return ERR_SERVER_TOKEN

    chat_ids_str = os.environ.get('TG_CHAT_IDS')
    if chat_ids_str is None:
        return ERR_SERVER_TOKEN

    return None


async def send_telegram_message(msg: str, chat_ids: List[str]=None) -> bool:
    """Send the input message to a list of chats, or to the default chats if the input list is None"""
    if chat_ids is None:
        chat_ids = __get_telegram_chat_ids()

    token = os.environ.get('TG_TOKEN')
    chatbot = telegram.Bot(token=token)
    async with asyncio.TaskGroup() as tg:
        for chat_id in chat_ids:
            tg.create_task(chatbot.send_message(chat_id=chat_id, text=msg, parse_mode=ParseMode.HTML))

    return True


def __get_telegram_chat_ids() -> List[str]:
    """Return the chat ids to send messages to"""
    chat_ids_str = os.environ.get('TG_CHAT_IDS')
    return chat_ids_str.split(',')
