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

#
# @router.message(F.text == START_GAME)
# async def start_game(message: Message):
#     await message.answer(text='Играть', reply_markup=start_game_kb)
#
#
# @router.message(F.text == ANALYZE_MSG_BTN_NAME)
# async def analyze_messages(message: Message, state: FSMContext):
#     await state.update_data(data_type='messages')
#
#     await analyze(message, state)
#
#
# @router.message(F.text == ANALYZE_REACTIONS_BTN_NAME)
# async def analyze_reactions(message: Message, state: FSMContext):
#     await state.update_data(data_type='reactions')
#
#     await analyze(message, state)
#
#
# @router.message(F.text == COLLECT_POLLS_BTN_NAME)
# async def analyze_polls(message: Message, state: FSMContext):
#     await state.update_data(data_type='polls')
#
#     await analyze(message, state)
#
#
# @router.message(F.text == ADD_ADVICE_BTN_NAME)
# async def add_advice_datetime(message: Message, state: FSMContext):
#     await state.set_state(AnalyzeParamsState.advice_time)
#
#     kb = await select_day_num_keyboard([], 'advice_adding')
#
#     await message.answer(
#         text='Выбери день',
#         reply_markup=kb,
#     )
#
#
# async def analyze(message: Message, state: FSMContext):
#     data = await state.get_data()
#
#     data_type = data['data_type']
#     if data_type == 'polls':
#         kb = await select_day_num_keyboard()
#
#         await message.answer(
#             text='Выбери день',
#             reply_markup=kb,
#         )
#
#     else:
#         chat_list = await get_chat_for_select()
#
#         kb = await get_keyboard(chat_list)
#
#         await state.update_data(chat_list=chat_list)
#
#         await message.answer(text='Выбери чаты', reply_markup=kb)
#
#
# @router.message(AnalyzeParamsState.chat_list)
# async def select_target_chats(
#         message: Message,
#         state: FSMContext,
# ):
#     selected_chats = [int(num) - 1 for num in message.text.split(' ')]
#
#     data = await state.get_data()
#
#     chat_list = data['chat_list']
#
#     chat_list = [chat_list[i] for i in selected_chats]
#
#     await state.update_data(chat_list=chat_list)
#
#     await state.set_state(AnalyzeParamsState.day_number)
#
#     await message.answer('Введи номер дня (1 - 42)')
#
#
# @router.message(AnalyzeParamsState.day_number)
# async def select_day_number(
#         message: Message,
#         state: FSMContext,
# ):
#     day_number = int(message.text)
#
#     await state.update_data(day_number=day_number)
#
#     await message.answer('Начинаю анализ...')
#
#     data = await state.get_data()
#
#     day_number = data['day_number']
#     chat_list = data['chat_list']
#
#     params = await get_analyze_params(day_number)
#     params.update({
#         'day_number': day_number,
#         'chat_list': chat_list,
#     })
#
#     async for analyze_image in start_analyze(**params):
#         if os.path.isfile(analyze_image):
#             img = FSInputFile(analyze_image)
#             await message.answer_photo(img)
#         else:
#             await message.answer(f'Фото по такому пути не существует: {analyze_image}')
#
#     await state.clear()
#
#
# @router.message(AnalyzeParamsState.advice_time)
# async def get_date_advice_and_go(
#         message: Message,
#         state: FSMContext,
# ):
#     try:
#         # Парсим время пользователя
#         user_time = datetime.strptime(message.text, "%H:%M").time()
#
#         data = await state.get_data()
#
#         await state.update_data(advice_time=user_time)
#
#         old_time = data.get('advice_time', None)
#         # is_filter = data.get('usersfilter', False)
#         day_numbers = data.get('day_numbers', None)
#
#         resp_str = 'Принято!'
#         if old_time:
#             old_time = old_time.strftime('%H:%M')
#             resp_str += f'\nНовое время подсказки - {user_time}. Было - {old_time}'
#         else:
#             resp_str += f'\nУстановлено время подсказки - {user_time}'
#
#         if day_number := day_numbers and day_numbers[0]:
#             await update_params(day_number, date_advice=time_to_str(user_time))
#
#         await message.answer(
#             text=resp_str,
#         )
#
#         await state.clear()
#
#     except ValueError:
#         await message.edit_text("Неверный формат времени. Пожалуйста, используйте формат ЧЧ:ММ.")
#
#
# @router.message(AnalyzeParamsState.intermediate_times)
# async def get_intermediate_times(message: Message, state: FSMContext):
#     data = await state.get_data()
#     intermediate_times = data.get('intermediate_times', [])
#     for t in message.text.split(' '):
#         try:
#             dt = str_time_to_datetime(t)
#             intermediate_times.append(dt)
#         except Exception:
#             continue
#
#     if intermediate_times:
#         str_int_times = [time_to_str(dt) for dt in intermediate_times]
#         text = (f'Установлено, промежуточное время: {', '.join(str_int_times)}')
#
#         await state.update_data(intermediate_times=intermediate_times)
#
#         await message.answer(
#             text,
#             reply_markup=intermediate_times_adding,
#         )
#     else:
#         await message.answer('Неизвестный ввод')
