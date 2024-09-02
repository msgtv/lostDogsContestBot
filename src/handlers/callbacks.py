import os

from aiogram import F, Router
from aiogram.types import (
    CallbackQuery,
)
from aiogram.fsm.context import FSMContext
import pandas as pd

from src.invite import get_invite_link
from src.settings import DATA_FILENAME, DATA_DIR
from src.utils import load_data, save_data, is_channel_member


router = Router()


@router.callback_query(F.data.startswith('Card_'))
async def select_card_number(callback: CallbackQuery, state: FSMContext):
    global DATA_DF

    card_number = int(callback.data.split('_')[1])

    # здесь нужно
    # сгенерировать ссылку для приглашения друга на канал
    # сохранить:
    #  ид пользователя, firstname, lastname,
    #  login, date, card_number и ссылку-приглашение

    user = callback.from_user

    invite_link = await get_invite_link(callback.message.bot, callback.from_user)
    invite_link = invite_link.invite_link

    data = {
        'date': callback.message.date,
        'user_id': str(user.id),
        'fullname': user.full_name,
        'username': user.username,
        'user_url': user.url,
        'invite_link': invite_link,
        'card_number': str(card_number),
    }

    data_filename = os.path.join(DATA_DIR, DATA_FILENAME)
    data_df = await load_data(data_filename)

    data_df = pd.concat([data_df, pd.DataFrame([data])], ignore_index=True)

    await save_data(data_df, data_filename)

    text = (f'Ты выбрал карту {card_number}!\n\n'
            f'Вот ссылка, с помощью которой ты сможешь пригласить друга '
            f'и участвовать в конкурсе:\n'
            f'{invite_link}\n\n'
            f'Удачи🔥')

    await callback.message.edit_text(text)


@router.callback_query(F.data.startswith('CardWinner_'))
async def get_winner(callback: CallbackQuery):
    # вернуть рандомно выбранного пользователя:
    # фио, ид, username, ссылку-приглашение,
    # выбранную карту, приглашенного друга

    data_filename = os.path.join(DATA_DIR, DATA_FILENAME)
    data_df = await load_data(data_filename)

    if data_df.empty:
        await callback.message.answer('Нет участников!')
    else:
        winner_card_number = int(callback.data.split('_')[1])

        winner_df = data_df[data_df['card_number'] == winner_card_number]

        if winner_df.empty:
            await callback.message.edit_text(
                text='Победителей нет!'
            )
        else:
            while True:
                random_row = winner_df.sample(n=1)
                winner_data = random_row.squeeze().to_dict()
                user_id = winner_data['user_id']

                is_member = await is_channel_member(callback.message.bot, int(user_id), '@odincryptan')

                if is_member:
                    break
                else:
                    winner_df = winner_df[winner_df['user_id'] != user_id]

                if winner_df.empty:
                    winner_data = None
                    break

            if winner_data is None:
                text = (f'Победитель не определен!\n'
                        f'Никто из угадавших не подписан на @odincryptan!')

                await callback.message.edit_text(text)
            else:
                text = (f'Победитель определен!\n\n'
                        f'{winner_data['fullname']} @{winner_data['username']}\n'
                        f'Он выбрал карту №{winner_data['card_number']}\n'
                        f'Его ссылка-приглашение: {winner_data['invite_link']}\n'
                        f'Он пригласил друзей - Х')

                await callback.message.edit_text(text)


@router.callback_query(F.data == 'cancel')
async def cancel_btn(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.edit_text('Возвращайся!')
