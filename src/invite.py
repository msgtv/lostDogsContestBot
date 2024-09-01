from aiogram import Bot
from aiogram.types import ChatInviteLink, User
from aiogram.methods import CreateChatInviteLink


async def get_invite_link(
        bot: Bot,
        user: User
) -> ChatInviteLink | None:
    try:
        username = user.username and f'@{user.username}' or user.id

        description = f'{user.full_name} {username}'
        # Создание ссылки приглашения
        invite_link: ChatInviteLink = await bot(CreateChatInviteLink(
            chat_id='@odincryptan',  # ID или username вашего канала
            expire_date=None,  # Установите время истечения действия ссылки, если нужно
            member_limit=None,  # Установите лимит участников, если нужно
            name=description  # Название ссылки
        ))

        return invite_link

    except Exception as e:
        return None
