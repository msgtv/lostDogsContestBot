import os
from datetime import datetime

from aiogram import F, Router
from aiogram.types import (
    FSInputFile,
    Message, InlineKeyboardMarkup,
)
from aiogram.fsm.context import FSMContext

from src.utils import load_data
from src.settings import DATA_DF, DATA_DIR, DATA_FILENAME
from src.keyboards import get_card_select_keyboard
from src.cards import cards
from src.btn_names import (
    GET_WINNER,
    GET_RESULTS,
    GET_STATISTICS,
)

router = Router()


@router.message(F.text == GET_RESULTS)
async def get_results_file(message: Message):
    data_filename = os.path.join(DATA_DIR, DATA_FILENAME)

    if os.path.isfile(data_filename):
        await message.bot.send_document(
            chat_id=message.chat.id,
            document=FSInputFile(data_filename),
        )
    else:
        await message.answer('Нет участников!')


@router.message(F.text == GET_WINNER)
async def get_winner_card(message: Message):
    # вернуть рандомно выбранного пользователя:
    # фио, ид, username, ссылку-приглашение,
    # выбранную карту, приглашенного друга

    # выбрать карту-победитель
    kb = await get_card_select_keyboard(cards=cards, callback_title='CardWinner')

    await message.answer(text='Какая карта выиграла?', reply_markup=kb)


@router.message(F.text == GET_STATISTICS)
async def get_statistics(message: Message):
    data_filename = os.path.join(DATA_DIR, DATA_FILENAME)
    data_df = await load_data(data_filename)

    if data_df.empty:
        await message.answer(text='Нет участников!')
    else:
        # Общее количество строк
        total_count = len(data_df)

        # Вычисляем количество каждого уникального значения в 'card_number'
        value_counts = data_df['card_number'].value_counts()

        # Рассчитываем процентное соотношение
        percentage = (value_counts / total_count) * 100

        text = 'Статистика:\n'
        # Форматируем и выводим результаты
        for card_number, count in value_counts.items():
            perc = percentage[card_number]

            text += f"Карта №{card_number} - {perc:.2f}% (голосов: {count})\n"

        await message.answer(text)
