from telethon.sync import TelegramClient
import asyncio
from dotenv import dotenv_values


ENV_VALUES = dotenv_values(".env")


async def helper(message_text: str) -> None:
    api_id = ENV_VALUES["API_ID"]
    api_hash = ENV_VALUES["API_HASH"]
    bot_token = ENV_VALUES["BOT_TOKEN"]
    group_id = int(ENV_VALUES["GROUP_ID"])

    async with TelegramClient("bot_session", api_id, api_hash) as client:
        await client.start(bot_token=bot_token)

        await client.send_message(group_id, message_text)


async def notification(message_text: str) -> None:
    await asyncio.sleep(0.1)
    await helper(message_text)
