import os

import aiofiles
import pandas as pd
from io import StringIO

from aiogram import Bot
from aiogram.enums import ChatMemberStatus


def create_dir_if_not_exists(path):
    if not os.path.isdir(path):
        os.makedirs(path)


async def load_data(filename):
    data_file = os.path.join(filename)

    try:
        async with aiofiles.open(data_file, 'r', encoding='utf-8') as f:
            data = await f.read()

        df = pd.read_csv(StringIO(data))
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df = pd.DataFrame()

    return df


async def save_data(df: pd.DataFrame, data_file: str):
    # Преобразование DataFrame в строку CSV
    output = StringIO()
    df.to_csv(output, index=False, encoding='utf-8')

    # Получение содержимого строки CSV
    csv_data = output.getvalue()

    # Асинхронная запись содержимого в файл
    async with aiofiles.open(data_file, 'w', encoding='utf-8', newline='') as f:
        await f.write(csv_data)


async def is_channel_member(bot: Bot, user_id: int, channel: str) -> bool:
    chat = await bot.get_chat(channel)
    member = await bot.get_chat_member(chat.id, user_id)

    if member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        return True
    else:
        return False

