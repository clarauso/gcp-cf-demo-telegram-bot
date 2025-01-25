import pytest
from unittest.mock import patch, AsyncMock
from tg_utils import check_telegram_config, send_telegram_message, __get_telegram_chat_ids

# Replace 'your_module' with the actual module name.

@pytest.fixture
def mock_env_vars():
    """Fixture to mock environment variables."""
    with patch.dict("os.environ", {"TG_TOKEN": "test_token", "TG_CHAT_IDS": "12345,67890"}):
        yield


def test_check_telegram_config_no_token():
    """Test that check_telegram_config returns an error if TG_TOKEN is missing."""
    with patch.dict("os.environ", {}, clear=True):
        assert check_telegram_config() == "TG_MISCONF_TK"


def test_check_telegram_config_no_chat_ids():
    """Test that check_telegram_config returns an error if TG_CHAT_IDS is missing."""
    with patch.dict("os.environ", {"TG_TOKEN": "test_token"}, clear=True):
        assert check_telegram_config() == "TG_MISCONF_TK"


def test_check_telegram_config_success(mock_env_vars):
    """Test that check_telegram_config returns None if the configuration is valid."""
    assert check_telegram_config() is None


def test_get_telegram_chat_ids(mock_env_vars):
    """Test __get_telegram_chat_ids returns the correct list of chat IDs."""
    assert __get_telegram_chat_ids() == ["12345", "67890"]


@pytest.mark.asyncio()
@patch("telegram.Bot")
async def test_send_telegram_message(mock_bot, mock_env_vars):
    """Test send_telegram_message sends messages to the correct chats."""
    # Mock the bot's send_message method
    mock_send_message = AsyncMock()
    mock_bot.return_value.send_message = mock_send_message

    message = "Test message"
    chat_ids = ["12345", "67890"]

    # Call the function
    result = await send_telegram_message(message, chat_ids)

    # Assertions
    assert result is True
    assert mock_send_message.call_count == len(chat_ids)
    mock_send_message.assert_any_call(chat_id="12345", text=message, parse_mode="HTML")
    mock_send_message.assert_any_call(chat_id="67890", text=message, parse_mode="HTML")
