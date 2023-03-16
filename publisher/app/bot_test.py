import asyncio
import logging
import os
from typing import Any

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Data, Dialog, DialogManager, DialogRegistry, Window
# from aiogram_dialog.tools import render_preview, render_transitions
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, Group, Next, Row, Start
from aiogram_dialog.widgets.text import Const, Format, Multi

API_TOKEN = os.environ["TELEGRAM_NEWS_TICKER_DEV_BOT_TOKEN"]


# name input dialog


class NameSG(StatesGroup):
    input = State()
    confirm = State()


async def name_handler(m: Message, dialog: Dialog, manager: DialogManager):
    manager.current_context().dialog_data["name"] = m.text
    await dialog.next(manager)


async def get_name_data(dialog_manager: DialogManager, **kwargs):
    return {"name": dialog_manager.current_context().dialog_data.get("name")}


async def on_finish(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.done({"name": manager.current_context().dialog_data["name"]})


name_dialog = Dialog(
    Window(
        Const("What is your name?"),
        Cancel(),
        MessageInput(name_handler),
        state=NameSG.input,
        preview_add_transitions=[Next()],  # hint for graph rendering
    ),
    Window(
        Format("Your name is `{name}`, it is correct?"),
        Row(Back(Const("No")), Button(Const("Yes"), id="yes", on_click=on_finish)),
        state=NameSG.confirm,
        getter=get_name_data,
        preview_add_transitions=[Cancel()],  # hint for graph rendering
    ),
)


# main dialog
class MainSG(StatesGroup):
    main = State()


async def process_result(start_data: Data, result: Any, manager: DialogManager):
    if result:
        manager.current_context().dialog_data["name"] = result["name"]


async def get_main_data(dialog_manager: DialogManager, **kwargs):
    return {
        "name": dialog_manager.current_context().dialog_data.get("name"),
    }


async def on_reset_name(c: CallbackQuery, button: Button, manager: DialogManager):
    del manager.current_context().dialog_data["name"]


main_menu = Dialog(
    Window(
        Multi(
            Format("Hello, {name}", when="name"),
            Const(
                "Hello, unknown person",
                when=lambda data, whenable, manager: not data.get("name"),
            ),
        ),
        Group(
            Start(Const("Enter name"), id="set", state=NameSG.input),
            Button(
                Const("Reset name"), id="reset", on_click=on_reset_name, when="name"
            ),
        ),
        state=MainSG.main,
        getter=get_main_data,
    ),
    on_process_result=process_result,
)


async def main():
    # real main
    logging.basicConfig(level=logging.INFO)
    storage = MemoryStorage()
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot, storage=storage)
    registry = DialogRegistry(dp)
    registry.register_start_handler(
        MainSG.main
    )  # resets stack and start dialogs on /start command
    registry.register(name_dialog)
    registry.register(main_menu)
    # render_transitions(registry)  # render graph with current transtions

    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
