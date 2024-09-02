import os

from aiogram import Router, Bot
from aiogram.types import (
    Message,
    ChatMember,
)
from aiogram.filters import (
    CommandStart,
    Command
)

from src.keyboards import get_card_select_keyboard, main_kb
from src.cards import cards, QUESTION
from src.settings import DATA_FILENAME, DATA_DIR, OWNER_ID
from src.utils import load_data, is_channel_member

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = str(message.from_user.id)

    if user_id == OWNER_ID:
        await admin_main(message)
    else:
        is_member = await is_channel_member(message.bot, int(user_id), "@odincryptan")

        if is_member:
            await contest_main(message, user_id)
        else:
            await message.answer(
                text='Для участия в конкурсе ты должен '
                     'быть подписан на канал @odincryptan'
            )


async def contest_main(message: Message, user_id: str):
    data_filename = os.path.join(DATA_DIR, DATA_FILENAME)
    data_df = await load_data(data_filename)

    if not data_df.empty:
        data_df['user_id'] = data_df['user_id'].astype(str)

    if data_df.empty or not data_df.empty and not data_df['user_id'].isin([user_id]).any():
        kb = await get_card_select_keyboard(cards)
        text = (
            f'{QUESTION}\n\n'
            'Выбери карту.\n'
            'После выбора карты ты '
            'получишь ссылку для приглашения друга!\n'
            'Если передумал - нажми "Отмена"'
        )

        await message.answer(
            text,
            reply_markup=kb
        )

    else:
        await message.answer('Ты уже выбрал карту!')


async def admin_main(message: Message):
    await message.answer(
        text='Админ меню',
        reply_markup=main_kb,
    )


