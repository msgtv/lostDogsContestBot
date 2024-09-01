import traceback
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import (
    TelegramObject,
    Message,
)
from more_itertools import chunked

from src.settings import OWNER_ID
from src.cards import EXPIRE_DATE


class AuthMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        chat_id = str(event.chat.id)
        if chat_id != OWNER_ID and isinstance(event, Message) and event.date > EXPIRE_DATE:
            await event.answer('Конкурс завершен!')
        else:
            try:
                result = await handler(event, data)

                return result
            except Exception as err:

                err_string = (
                    f"Что-то пошло не так: {err.__class__.__name__} - {err}"
                    f"Traceback: {traceback.format_exc()}")

                if isinstance(event, Message):
                    username = event.from_user.username and f'@{event.from_user.username}' or event.from_user.id

                    text = ('Произошла ошибка!\n'
                            f'Время ошибки: {event.date}\n'
                            f'Пользователь: {event.from_user.full_name} {username}\n'
                            f'Текст в сообщении ниже')

                    if chat_id != OWNER_ID:
                        await event.answer(f'Что-то пошло не так!\n'
                                           f'Время ошибки: {event.date}\n'
                                           f'Обратитесь к создателю @odincryptan_manager!')

                    await event.bot.send_message(
                        chat_id=OWNER_ID,
                        text=text,
                    )

                    for substring in chunked(err_string, 1000):
                        await event.bot.send_message(
                            chat_id=OWNER_ID,
                            text=''.join(substring)
                        )

                print(
                    err_string
                )
