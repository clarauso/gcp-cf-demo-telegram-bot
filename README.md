# Cloud Run Function for a Telegram bot

This repository contains an example of Python code that retrieves data from a public API endpoint and sends a Telegram message using the retrieved info.

## Local testing

```
export TG_CHAT_IDS=<REPLACE THIS WITH THE IDS OF THE TARGET CHATS>
export TG_TOKEN=<REPLACE THIS WITH YOUR BOT'S TOKEN>

functions-framework --target=send_message --source=src/main.py --debug
```