import pytest
from unittest.mock import patch, Mock

from data.post import Post
from data.posts_repository import retrieve_posts


@pytest.fixture
def mock_posts():
    return [
        {"userId": 1, "id": 1, "title": "Post 1", "body": "Content of Post 1"},
        {"userId": 1, "id": 2, "title": "Post 2", "body": "Content of Post 2"},
    ]


@patch("requests.get")
def test_retrieve_posts_success(mock_get, mock_posts):
    # Mock the response from requests.get
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_posts
    mock_get.return_value = mock_response

    # Call the function
    posts = retrieve_posts()

    # Validate the results
    assert len(posts) == 2
    assert isinstance(posts[0], Post)
    assert posts[0].title == "Post 1"
    assert posts[1].body == "Content of Post 2"


@patch("requests.get")
def test_retrieve_posts_api_error(mock_get):
    # Mock the response to simulate an API error
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = {"error": "Internal Server Error"}
    mock_get.return_value = mock_response

    # Call the function and expect it to raise RuntimeError
    with pytest.raises(RuntimeError, match="Error retrieving posts"):
        retrieve_posts()
