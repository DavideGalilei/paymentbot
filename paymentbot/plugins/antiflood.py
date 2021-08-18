import asyncio
from string import Template
from time import time
from typing import Union
from collections import defaultdict

from pyrogram import Client, filters, types

from ..config import shared
from ..utils import ADMINS

shared.BANNED_USERS = BANNED_USERS = filters.user()

MESSAGES, SECONDS, CB_SECONDS = (
    shared.settings.MESSAGES,
    shared.settings.SECONDS,
    shared.settings.CB_SECONDS,
)

_users = defaultdict(list)


async def is_flood(
    user: types.User,
    messages: int = 1,
    seconds: int = 6,
    users: defaultdict = _users,
) -> Union[bool, None]:
    """Checks if a user is flooding"""

    users[user.id].append(time())
    check = list(filter(lambda x: time() - int(x) < seconds, users[user.id]))
    if len(check) > messages:
        users[user.id] = check
        return True


@Client.on_message((filters.private | filters.group) & ~ADMINS, group=-100)
@Client.on_callback_query(~ADMINS, group=-100)
async def anti_flood(_: Client, update: Union[types.Message, types.CallbackQuery]):
    if not update.from_user:
        return
    is_callback = isinstance(update, types.CallbackQuery)
    if await is_flood(
        update.from_user,
        messages=MESSAGES,
        seconds=CB_SECONDS if is_callback else SECONDS,
    ):
        if is_callback:
            return await update.answer(
                Template(shared.translations.FLOOD_BUTTON).substitute(SEC=shared.settings.CB_SECONDS),
                show_alert=True,
            )
        return BANNED_USERS.add(update.from_user.id)
    elif update.from_user.id in BANNED_USERS:
        BANNED_USERS.remove(update.from_user.id)
    await update.continue_propagation()


async def cleaner(
    users: defaultdict,
    sleep: float = 30,
    seconds: int = SECONDS,
):
    while not await asyncio.sleep(sleep):
        for user, messages in users.copy().items():
            check = list(
                filter(lambda x: time() - int(x) < seconds, users[user])
            )
            if not check:
                del users[user]


asyncio.create_task(cleaner(users=_users))
