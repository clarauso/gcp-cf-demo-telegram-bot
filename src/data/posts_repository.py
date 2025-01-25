import logging

import requests
from typing import List

from pydantic import TypeAdapter

from .post import Post

base_url = "https://jsonplaceholder.typicode.com/posts"


def retrieve_posts() -> List[Post]:
    """ Get posts from the remote server, then return them as a list. """

    raw_response = requests.get(base_url)
    json = raw_response.json()
    if raw_response.status_code != 200:
        logging.error(f"API error statusCode={raw_response.status_code} json={json}")
        raise RuntimeError("Error retrieving posts")

    ta = TypeAdapter(List[Post])

    return ta.validate_python(json)
