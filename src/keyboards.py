from typing import List
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.cards import LostDogsCard
from src.btn_names import CANCEL_BTN_NAME, GET_WINNER, GET_RESULTS, GET_STATISTICS


cancel_btn = InlineKeyboardButton(
    text=CANCEL_BTN_NAME,
    callback_data='cancel',
)

main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=GET_WINNER)],
    [KeyboardButton(text=GET_RESULTS),
     KeyboardButton(text=GET_STATISTICS)],
], resize_keyboard=True)

# start_game_kb = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text=START_GAME, url='https://t.me/lost_dogs_bot/lodoapp')]
# ])

cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [cancel_btn]
])

# intermediate_times_adding = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Ввести время', callback_data='add_intermediate_times'),
#      InlineKeyboardButton(text='Старт', callback_data='start_analyze')],
#     [cancel_btn],
# ])


async def get_card_select_keyboard(
        cards: [LostDogsCard],
        callback_title: str = 'Card'
):
    kb = InlineKeyboardBuilder()

    for card in cards:
        title = f'{card.number}. {card.title}'
        callback = f'{callback_title}_{card.number}'

        kb.add(
            InlineKeyboardButton(
                text=title,
                callback_data=callback,
            )
        )

    kb.add(cancel_btn)

    return kb.adjust(1).as_markup()


# async def get_keyboard(
#         chat_list,
#         selected_nums: List[int] = None
# ) -> InlineKeyboardMarkup:
#     if selected_nums is None:
#         selected_nums = []
#
#     kb = InlineKeyboardBuilder()
#     for i, chat in enumerate(chat_list):
#         title = chat.title
#         if i in selected_nums:
#             title = "✅ " + title
#         kb.add(
#             InlineKeyboardButton(
#                 text=title,
#                 callback_data=f"Chat_{i}"
#             )
#         )
#     if selected_nums:
#         kb.add(
#             InlineKeyboardButton(
#                 text='🔥 Дальше 🔥',
#                 callback_data="Day"
#             )
#         )
#     kb.add(cancel_btn)
#
#     return kb.adjust(2).as_markup()
#
#
# async def select_day_num_keyboard(
#         selected: list[int] = None,
#         data_type: str = 'messages'
# ):
#     if selected is None:
#         selected = []
#
#     day_count = days_difference(START_DAY)
#     kb = InlineKeyboardBuilder()
#
#     for num in range(1, day_count + 1):
#         text = str(num)
#         if data_type and selected and selected[0] == num or num in selected:
#             text = "✅ " + text
#
#         kb.add(
#             InlineKeyboardButton(
#                 text=text,
#                 callback_data=f"Day_{num}"
#             )
#         )
#
#     if data_type == 'polls':
#         kb.add(
#             InlineKeyboardButton(
#                 text='Далее',
#                 callback_data=f'intermediate_times',
#             )
#             # InlineKeyboardButton(
#             #     text='Начать',
#             #     callback_data="start_analyze"
#             # )
#         )
#     elif data_type in ['messages', 'reactions']:
#         if len(selected) > 0:
#             kb.add(
#                 InlineKeyboardButton(
#                     text='🔥 Дальше 🔥',
#                     callback_data="usersfilter"
#                 )
#             )
#     elif data_type == 'advice_adding':
#         kb.add(
#             InlineKeyboardButton(
#                 text='Ввести время',
#                 callback_data="adding_advice_callback",
#             )
#         )
#     kb.add(cancel_btn)
#
#     return kb.adjust(7).as_markup()
#
#
# async def usersfilter_keyboard(
#         is_filter: bool = False,
# ):
#     if is_filter:
#         yes = '✅ Да'
#         no = 'Нет'
#     else:
#         yes = 'Да'
#         no = '✅ Нет'
#
#     kb = InlineKeyboardBuilder()
#
#     kb.add(
#         InlineKeyboardButton(
#             text=yes,
#             callback_data='usersfilter_1'
#         ),
#     )
#     kb.add(
#         InlineKeyboardButton(
#             text=no,
#             callback_data='usersfilter_0'
#         ),
#     )
#     kb.add(cancel_btn)
#     kb.add(
#         InlineKeyboardButton(
#             text='🚀 Поехали 👨‍🚀',
#             callback_data="start_analyze"
#         )
#     )
#
#     return kb.adjust(2).as_markup()
