import asyncio

import functions_framework
import logging

from data.post import Post
from data.posts_repository import retrieve_posts
from string import Template
from tg_utils import send_telegram_message, check_telegram_config

# template for error response
ERR_JSON = '{"error_code": "$code"}'

logging.basicConfig(level=logging.INFO)


@functions_framework.http
def send_message(request):
    # first check if the CF is properly configured, otherwise return server error
    config_telegram_error: str = check_telegram_config()
    if config_telegram_error is not None:
        return Template(ERR_JSON).safe_substitute(code=config_telegram_error), 500

    # retrieve post list and send Telegram message
    posts = retrieve_posts()
    latest_post: Post = posts.pop()
    msg: str = f"Latest post title is\n<b>{latest_post.title}</b>"
    message_sent = asyncio.run(send_telegram_message(msg))

    json_outcome: str
    if message_sent:
        json_outcome = '{"outcome":"SENT"}'
    else:
        json_outcome = '{"outcome":"NOT_SENT"}'

    return json_outcome, 202
