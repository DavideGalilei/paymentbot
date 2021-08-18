from typing import Dict, List

from pyrogram import Client, ContinuePropagation
from pyrogram.types import Update, User, Chat
from pyrogram.raw.types import UpdateBotShippingQuery, UpdateBotPrecheckoutQuery

_on_shipping_query_handlers: List[callable] = []
_on_checkout_query_handlers: List[callable] = []


def on_shipping_query(func: callable):
    _on_shipping_query_handlers.append(func)
    return func


def on_checkout_query(func: callable):
    _on_checkout_query_handlers.append(func)
    return func


@Client.on_raw_update()
async def _raw(bot: Client, update: Update, users: Dict[int, User], chats: Dict[int, Chat]):
    # print(type(x) for x in (update, users, chats))
    # print(update, users, chats)
    if isinstance(update, UpdateBotShippingQuery):
        for handler in _on_shipping_query_handlers:
            await handler(bot, update, users, chats)
    elif isinstance(update, UpdateBotPrecheckoutQuery):
        for handler in _on_checkout_query_handlers:
            await handler(bot, update, users, chats)
    else:
        raise ContinuePropagation()


"""
{
    "_": "types.UpdateBotShippingQuery",
    "query_id": 1028888578233737147,
    "user_id": 239556789,
    "payload": "b'239556789_bought'",
    "shipping_address": {
        "_": "types.PostAddress",
        "street_line1": "a",
        "street_line2": "a",
        "city": "Rome",
        "state": "a",
        "country_iso2": "IT",
        "post_code": "1010"
    }
}

{
    "_": "types.UpdateBotPrecheckoutQuery",
    "query_id": 1028888575142874651,
    "user_id": 239556789,
    "payload": "b'239556789_bought'",
    "currency": "EUR",
    "total_amount": 42000,
    "info": {
        "_": "types.PaymentRequestedInfo",
        "name": "asddsadsa",
        "phone": "393331341834",
        "email": "dsadsaads@gmail.com",
        "shipping_address": {
            "_": "types.PostAddress",
            "street_line1": "a",
            "street_line2": "a",
            "city": "Rome",
            "state": "a",
            "country_iso2": "IT",
            "post_code": "1010"
        }
    },
    "shipping_option_id": "asd"
}
"""
