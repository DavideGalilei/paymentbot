import html
from typing import Dict
from uuid import uuid4

from pyrogram import Client, filters
from pyrogram.types import Message, User, Chat, InlineQuery
from pyrogram.raw.types import (
    InputMediaInvoice,
    DataJSON,
    Invoice,
    LabeledPrice,
    UpdateBotShippingQuery,
    ShippingOption,
    UpdateBotPrecheckoutQuery,
    InputBotInlineResult,
    InputBotInlineMessageMediaInvoice,
)
from pyrogram.raw.functions.messages import (
    SendMedia,
    SetBotPrecheckoutResults,
    SetBotShippingResults,
    SetInlineBotResults,
)

from paymentbot.config import shared
from paymentbot.utils import ADMINS

from .handlers import on_shipping_query, on_checkout_query


invoice = Invoice(
    currency="EUR",
    prices=[
        LabeledPrice(amount=2000, label="asd"),
        LabeledPrice(amount=20000, label="asd"),
    ],
    test=True,
    name_requested=True,
    phone_requested=True,
    email_requested=True,
    shipping_address_requested=True,
    flexible=True,
    phone_to_provider=True,
    email_to_provider=True,
)


@Client.on_message(filters.group & filters.command("invoice") & ADMINS)
async def send_invoice(bot: Client, msg: Message):
    r = await bot.send(
        SendMedia(
            peer=await bot.resolve_peer(msg.chat.id),
            media=InputMediaInvoice(
                title="title",
                description="description",
                # photo=InputWebDocument(
                #     url=photo,
                #     file_size=file_size,
                #     mime_type=mime_type,
                #     attributes=[DocumentAttributeImageSize(
                #         w=width, h=height
                #     )]
                # ) if photo else None,
                invoice=invoice,
                payload=f"{msg.from_user.id}_bought".encode(),
                provider=shared.settings.PROVIDER_TOKEN,
                provider_data=DataJSON(data="{}"),
                start_param="start_param",
            ),
            message="",
            random_id=bot.rnd_id(),
        )
    )


@on_shipping_query
async def process_shipping_query(
    bot: Client,
    query: UpdateBotShippingQuery,
    users: Dict[int, User],
    chats: Dict[int, Chat],
):
    await bot.send_message(
        chat_id=query.user_id,
        text=f"You've chosen an option.\n\n<b>Payload</b>:\n<code>{html.escape(str(query))}</code>",
    )
    return await bot.send(
        SetBotShippingResults(
            query_id=query.query_id,
            shipping_options=[
                ShippingOption(
                    id="asd",
                    title="Test Shipping Option",
                    prices=[
                        LabeledPrice(amount=20000, label="asd"),
                    ],
                )
            ],
            error=None,
        )
    )


@on_checkout_query
async def process_checkout_query(
    bot: Client,
    query: UpdateBotPrecheckoutQuery,
    users: Dict[int, User],
    chats: Dict[int, Chat],
):
    await bot.send_message(
        chat_id=query.user_id,
        text=f"You successfully bought something.\n\n<b>Payload</b>:\n<code>{html.escape(str(query))}</code>",
    )
    return await bot.send(
        SetBotPrecheckoutResults(
            query_id=query.query_id,
            success=True,
            error=None,
        )
    )


@Client.on_inline_query()
async def inline_invoice(bot: Client, query: InlineQuery):
    return await bot.send(
        SetInlineBotResults(
            query_id=int(query.id),
            results=[
                InputBotInlineResult(
                    id=uuid4().hex,
                    type="article",
                    send_message=InputBotInlineMessageMediaInvoice(
                        title="Inline Title",
                        description="Inline Description",
                        invoice=invoice,
                        payload=f"{query.from_user.id}_bought".encode(),
                        provider=shared.settings.PROVIDER_TOKEN,
                        provider_data=DataJSON(data="{}"),
                        photo=None,
                        reply_markup=None,
                    ),
                    title="Title",
                    description="Description",
                )
            ],
            cache_time=0,
            private=True,
        )
    )
