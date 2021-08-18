from pyrogram import Client, filters
from pyrogram.types import Message

from .antiflood import BANNED_USERS


@Client.on_message(
    filters.private & filters.text & filters.command("start") & ~BANNED_USERS
)
async def start(_: Client, msg: Message):
    return await msg.reply_text("t")
