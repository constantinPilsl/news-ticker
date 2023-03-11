import asyncio
import logging
import os.path
from operator import itemgetter
from typing import Any

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import (
    ChatEvent,
    Dialog,
    DialogManager,
    DialogRegistry,
    StartMode,
    Window,
)
from aiogram_dialog.manager.protocols import ManagedDialogAdapterProto
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Button, Multiselect, Row, Select, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Multi

src_dir = os.path.normpath(os.path.join(__file__, os.path.pardir))

API_TOKEN = os.environ["TELEGRAM_NEWS_TICKER_DEV_BOT_TOKEN"]


class DialogSG(StatesGroup):
    greeting = State()
    finish = State()
    select_keywords = State()


async def get_data(dialog_manager: DialogManager, **kwargs):
    keywords = dialog_manager.current_context().dialog_data.get("keywords", None)
    return {
        "keywords": keywords,
    }


async def start_handler(
    m: Message, dialog: ManagedDialogAdapterProto, manager: DialogManager
):
    if manager.is_preview():
        await dialog.next()
        return
    await dialog.next()


async def on_submit(c: CallbackQuery, button: Button, manager: DialogManager):
    if manager.is_preview():
        await manager.done()
        return

    mselect = manager.current_context().widget_data["mselect"]

    print(mselect)
    item_ids = [item for item in mselect]
    item_id_str = ",".join(str(i) for i in item_ids)

    manager.current_context().dialog_data["keywords"] = item_id_str
    await c.message.answer(f"Your keywords have been set to: {item_id_str}")
    await manager.dialog().next()


async def on_finish(c: CallbackQuery, button: Button, manager: DialogManager):
    if manager.is_preview():
        await manager.done()
        return
    await c.message.answer("Thank you. To start again click /start")
    await manager.done()


items = [("Ukraine", 1), ("USA", 2), ("Deutschland", 3), ("Technologie", 4)]

multiselect = Multiselect(
    checked_text=Format("✓ {item[0]}"),
    unchecked_text=Format("{item[0]}"),
    id="mselect",
    # item_id_getter=itemgetter(0),
    item_id_getter=itemgetter(1),
    items=items,
)

dialog = Dialog(
    Window(
        Const("Please select your keywords:"),
        multiselect,
        Row(
            Back(),
            SwitchTo(Const("Restart"), id="restart", state=DialogSG.select_keywords),
            Button(Const("Submit"), on_click=on_submit, id="submit"),
        ),
        getter=get_data,
        state=DialogSG.select_keywords,
    ),
    Window(
        Multi(
            Format("Your keywords have been set"),
            sep="\n\n",
        ),
        Row(
            Back(),
            SwitchTo(Const("Restart"), id="restart", state=DialogSG.select_keywords),
            Button(Const("Finish"), on_click=on_finish, id="finish"),
        ),
        getter=get_data,
        state=DialogSG.finish,
    ),
)


async def start(m: Message, dialog_manager: DialogManager):
    # it is important to reset stack because user wants to restart everything
    await dialog_manager.start(DialogSG.select_keywords, mode=StartMode.RESET_STACK)


async def main():
    # real main
    logging.basicConfig(level=logging.INFO)
    storage = MemoryStorage()
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot, storage=storage)
    dp.register_message_handler(start, text="/start", state="*")
    registry = DialogRegistry(dp)
    registry.register(dialog)

    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
