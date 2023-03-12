import asyncio
import logging
import os
from operator import itemgetter
from typing import Any, Union

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
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Group,
    Multiselect,
    Row,
    Select,
    ScrollingGroup,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const, Format, Multi


API_TOKEN = os.environ["TELEGRAM_NEWS_TICKER_DEV_BOT_TOKEN"]

application_data = {
    "items": [
        "Ukraine",
        "USA",
        "Deutschland",
        "Technologie",
        "Silion Valley",
        "Hard Rock Cafe",
    ],
}

user_data = {
    "keywords": None,
}


class DialogSG(StatesGroup):
    start = State()
    main_menu = State()
    finish = State()
    get_news = State()
    add_keywords = State()
    edit_keywords = State()



# CONTROLLER
async def get_keywords_enumerated(dialog_manager: DialogManager, **kwargs):
    enumerated_keywords = [(item, i) for i, item in enumerate(application_data["items"])]
    return {
        "enumerated_keywords": enumerated_keywords,
    }


async def get_user_keywords(dialog_manager: DialogManager, **kwargs):
    return {
        "user_keywords": user_data["keywords"],
    }


async def get_user_keywords_enumerated(dialog_manager: DialogManager, **kwargs):
    user_keywords_enumerated = [(item, i) for i, item in enumerate(user_data["keywords"])]
    return {
        "user_keywords_enumerated": user_keywords_enumerated,
    }


# EVENT HANDLERS
async def on_submit(c: CallbackQuery, button: Button, manager: DialogManager):
    if manager.is_preview():
        await manager.done()
        return

    mselect = manager.current_context().widget_data["mselect"]
    selected_ids = [int(id) for id in mselect]

    item_id_mapping = ((i, item) for i, item in enumerate(application_data["items"]))
    user_data["keywords"] = [i[1] for i in item_id_mapping if i[0] in selected_ids]

    item_id_str = ", ".join([i for i in user_data.get("keywords")])
    logging.info(f"Keyword ids set to:  {item_id_str}")

    await c.message.answer(f"Your keywords have been set to: {item_id_str}")
    await manager.done()


async def on_finish(c: CallbackQuery, button: Button, manager: DialogManager):
    if manager.is_preview():
        await manager.done()
        return
    # await c.message.answer("Fuck you!")
    await manager.done()


# VIEWS
dialog = Dialog(
    Window(
        Const("Start >"),
        Row(
            Button(
                Const("Get News"), id="get_news"
            ),  # TODO:  SwitchTo ones it is implemented
            SwitchTo(
                Const("Add Keywords"), id="add_keywords", state=DialogSG.add_keywords
            ),
            SwitchTo(
                Const("Edit Keywords"), id="edit_keywords", state=DialogSG.edit_keywords
            ),
        ),
        Row(
            Back(),
            SwitchTo(Const("Home"), id="start", state=DialogSG.main_menu),
            Button(Const("End"), on_click=on_finish, id="finish"),
        ),
        state=DialogSG.main_menu,
    ),
    Window(
        Const("Please select your keywords:"),
        ScrollingGroup(
            Multiselect(
                checked_text=Format("✓ {item[0]}"),
                unchecked_text=Format("{item[0]}"),
                id="mselect",
                item_id_getter=itemgetter(1),
                items="enumerated_keywords",
            ),
            width=2,
            height=4,
            id="add_keywords",
        ),
        Row(
            Back(),
            Button(Const("✓ Submit"), on_click=on_submit, id="submit"),
            Button(Const("x Discard"), on_click=on_finish, id="finish"),
        ),
        getter=get_keywords_enumerated,
        state=DialogSG.add_keywords,
    ),
    Window(
        # TODO:  EDIT KEYWORDS SHOULD HAVE SELECTED KEYWORDS ALREADY CHECKED
        Const("Your keywords are:"),
        ScrollingGroup(
            Multiselect(
                checked_text=Format("✓ {item[0]}"),
                unchecked_text=Format("{item[0]}"),
                id="mselect",
                item_id_getter=itemgetter(1),
                items="user_keywords_enumerated",
            ),
            width=2,
            height=4,
            id="add_keywords",
        ),
        Row(
            Back(),
            Button(Const("✓ Submit"), on_click=on_submit, id="submit"),
            Button(Const("x Discard"), on_click=on_finish, id="finish"),
        ),
        getter=get_user_keywords_enumerated,
        state=DialogSG.edit_keywords,
    ),
)


async def start(m: Message, dialog_manager: DialogManager):
    # it is important to reset stack because user wants to restart everything
    await dialog_manager.start(DialogSG.main_menu, mode=StartMode.RESET_STACK)


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
