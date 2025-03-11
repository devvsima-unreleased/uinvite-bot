import html

from app.handlers.message_text import admin_message_text as amt
from app.handlers.message_text import user_message_text as umt
from app.keyboards.default.base import menu_kb
from app.keyboards.inline.report import block_user_ikb
from data.config import MODERATOR_GROUP
from database.models import ProfileModel, UserModel
from database.services import User
from loader import bot
from utils.logging import logger

effect_dict = {
    "🔥": "5104841245755180586",
    "👍": "5107584321108051014",
    "👎": "5104858069142078462",
    "🎉": "5046509860389126442",
    "💩": "5046589136895476101",
}


async def menu(chat_id: int) -> None:
    """Отправляет меню пользователю"""
    await bot.send_message(
        chat_id=chat_id,
        text=umt.MENU,
        reply_markup=menu_kb,
    )


async def complaint_to_profile(user: UserModel, profile: ProfileModel, session) -> None:
    """Отправляет в группу модераторов анкету пользователя
    на которого пришла жалоба"""
    if MODERATOR_GROUP:
        try:
            await send_profile(MODERATOR_GROUP, profile)
            reported_user = await User.get(session, profile.user_id)

            text = umt.REPORT_TO_USER.format(
                user.id, user.username, profile.user_id, reported_user.username
            )

            await bot.send_message(
                chat_id=MODERATOR_GROUP,
                text=text,
                reply_markup=block_user_ikb(
                    user_id=profile.user_id,
                    username=reported_user.username,
                ),
            )
        except:
            logger.error("Сообщение в модераторскую группу не отправленно")


async def send_profile(chat_id: int, profile: ProfileModel) -> None:
    """Отправляет пользователю переданный в функцию профиль"""
    await bot.send_photo(
        chat_id=chat_id,
        photo=profile.photo,
        caption=f"{profile.name}, {profile.age}, {profile.city}\n{profile.description}",
        parse_mode=None,
    )


async def new_user_alert_to_group(user: UserModel) -> None:
    """Отправляет уведомление в модераторскуб группу о новом пользователе"""
    if MODERATOR_GROUP:
        try:
            await bot.send_message(
                chat_id=MODERATOR_GROUP, text=amt.NEW_USER.format(user.id, user.username)
            )
        except:
            logger.error("Сообщение в модераторскую группу не отправленно")


def generate_user_link(user_id: int, username: str = None) -> str:
    """
    Генерирует ссылку на пользователя
    Если указан username, создается ссылка https://t.me/username,
    иначе используется tg://user?id=user_id.
    """
    if username:
        return f"https://t.me/{username}"
    return f"tg://user?id={user_id}"


async def sending_user_contact(chat_id: int, name: str, language: str, user_link: str) -> None:
    """Отправляет сообщение с контактом пользователя"""

    await bot.send_message(
        chat_id=chat_id,
        text=umt.LIKE_ACCEPT(language).format(user_link, html.escape(name)),
        message_effect_id=effect_dict["🎉"],
    )
