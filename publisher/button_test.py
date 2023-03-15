import asyncio
import logging
import os
from operator import itemgetter
from typing import Iterable, Union, Generator

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from aiogram_dialog import Dialog, DialogManager, DialogRegistry, StartMode, Window
from aiogram_dialog.manager.protocols import ManagedDialogAdapterProto
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Multiselect,
    Row,
    ScrollingGroup,
    SwitchTo,
    Url,
)
from aiogram_dialog.widgets.text import Const, Format
from config import Config

import publisher.data_source_gateways.collector.collector as collector_gateway
from publisher.publisher_service import publish_news

config = Config()

API_TOKEN = os.environ["TELEGRAM_NEWS_TICKER_DEV_BOT_TOKEN"]

user_data = {
    # "5806566314": {"keywords": set()},
    # "5806566314": {
    #     "keywords": {
    #         "ukraine",
    #     },
    # },
}


class DialogSG(StatesGroup):
    start = State()
    main_menu = State()
    finish = State()
    get_news = State()
    browse = State()
    edit_keywords = State()
    add_keyword = State()


class UserGateway:
    def exists_user_id(user_id: str) -> bool:
        is_user_exists = True
        if user_data.get(user_id) is None:
            is_user_exists = False
        logging.info(f"exists_user_id for {user_id}:  {is_user_exists}")
        return is_user_exists

    def create_user(user_id: str):
        logging.info(f"Create user:  {user_id}")
        if user_data.get("user_id") is None:
            user_data[user_id] = {"keywords": set()}
        else:
            logging.warning(f"User already exists with id:  {user_id}")

    def get_keywords(user_id: str) -> set[str]:  # TODO: SHOULD RATHER RETURN GENERATOR[str, None, None] or List
        return user_data[user_id]["keywords"]

    def create_keywords(
        user_id: str,
        keywords: Union[list[str], set[str], Generator[str, None, None], str, None],
    ) -> None:
        logging.info(f"create_keywords(), user_id:  {user_id}, keywords:  {keywords}")
        if type(keywords) is str:
            user_data[user_id]["keywords"] = {keywords}
        elif keywords is None:
            user_data[user_id]["keywords"] = set()
        else:
            user_data[user_id]["keywords"] = set(keywords)

    def update_keywords(user_id: str, keywords: Union[Iterable[str], str]) -> None:
        logging.info(f"update_keywords(), user_id:  {user_id}, keywords:  {keywords}")
        if type(keywords) is str:
            user_data[user_id]["keywords"].add(keywords)
        else:
            user_data[user_id]["keywords"].update(keywords)


# HELPER
def get_user_id_from_dialog_manager(dialog_manager: DialogManager) -> str:
    logging.info("Get user id from dialog_manager")
    user_id = str(dialog_manager.event["from"]["id"])
    logging.debug(f"Got user_id from dialog_manager:  {user_id}")
    return user_id


# CONTROLLER
async def get_keywords_enumerated(dialog_manager: DialogManager, **kwargs):
    keywords_response = collector_gateway.get_keywords(
        sources=["tagesschau"],
        url=config.collector["url"],
        endpoint=config.collector["endpoints"]["keywords"],
        session_id=config.session_id,
    )

    keywords_enumerated = ((item, i) for i, item in enumerate(keywords_response))
    return {
        "keywords_enumerated": list(keywords_enumerated),
    }


async def get_user_keywords(dialog_manager: DialogManager, **kwargs):
    user_id = get_user_id_from_dialog_manager(dialog_manager)
    user_keywords = UserGateway.get_keywords(user_id)

    return {
        "user_keywords": user_keywords,
    }


async def get_user_keywords_enumerated(dialog_manager: DialogManager, **kwargs):
    user_id = get_user_id_from_dialog_manager(dialog_manager)

    user_keywords = UserGateway.get_keywords(user_id)
    user_keywords_enumerated = [(item, i) for i, item in enumerate(user_keywords)]
    return {
        "user_keywords_enumerated": user_keywords_enumerated,
    }


# EVENT HANDLERS
async def add_keyword_handler(
    m: Message, dialog: ManagedDialogAdapterProto, dialog_manager: DialogManager
):
    if dialog_manager.is_preview():
        await dialog.next()
        return

    user_id = get_user_id_from_dialog_manager(dialog_manager)
    keyword = m.text
    UserGateway.update_keywords(user_id, keyword)

    await m.answer(f"{keyword} has been added to your keywords.")
    await dialog_manager.switch_to(state=DialogSG.main_menu)


async def on_submit_browse_keywords(
    c: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    if dialog_manager.is_preview():
        await dialog_manager.done()
        return

    user_id = get_user_id_from_dialog_manager(dialog_manager)

    # TODO: This should not be a separate request and it does not work for editing keywords
    keywords_response = collector_gateway.get_keywords(
        sources=["tagesschau"],
        url=config.collector["url"],
        endpoint=config.collector["endpoints"]["keywords"],
        session_id=config.session_id,
    )

    mselect = dialog_manager.current_context().widget_data["mselect"]
    selected_ids = [int(id) for id in mselect]
    item_id_mapping = ((i, item) for i, item in enumerate(keywords_response))
    new_keywords = (i[1] for i in item_id_mapping if i[0] in selected_ids)

    UserGateway.update_keywords(user_id, new_keywords)
    updated_keywords = UserGateway.get_keywords(user_id)

    keyword_id_str = ", ".join(updated_keywords)
    logging.info(f"Keyword ids set to:  {keyword_id_str}")

    await c.message.answer(f"Your keywords have been set to: {keyword_id_str}")
    await dialog_manager.switch_to(state=DialogSG.main_menu)


async def on_submit_edit_keywords(
    c: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    if dialog_manager.is_preview():
        await dialog_manager.done()
        return

    user_id = get_user_id_from_dialog_manager(dialog_manager)
    mselect = dialog_manager.current_context().widget_data["mselect"]

    keywords = keywords = UserGateway.get_keywords(user_id)
    selected_ids = [int(id) for id in mselect]
    keyword_id_mapping = (
        (i, item) for i, item in enumerate(keywords)
    )
    keywords = (i[1] for i in keyword_id_mapping if i[0] in selected_ids)

    UserGateway.create_keywords(user_id, keywords)
    updated_keywords = UserGateway.get_keywords(user_id)

    keyword_id_str = ", ".join(updated_keywords)
    logging.info(f"Keyword ids set to:  {keyword_id_str}")

    await c.message.answer(f"Your keywords have been set to: {keyword_id_str}")
    await dialog_manager.switch_to(state=DialogSG.main_menu)


async def on_get_news(c: CallbackQuery, button: Button, dialog_manager: DialogManager):
    if dialog_manager.is_preview():
        await dialog_manager.done()
        return

    user_id = get_user_id_from_dialog_manager(dialog_manager)

    logging.info("Getting news...")
    user_keywords = UserGateway.get_keywords(user_id)
    logging.info(f"For following keywords:  {user_keywords}")

    news_response = collector_gateway.get_news(
        keywords=user_keywords,
        sources=["tagesschau"],
        url=config.collector["url"],
        endpoint=config.collector["endpoints"]["news"],
        session_id=config.session_id,
    )

    for news in news_response:
        title = news.title
        url = news.url
        logging.info(f"Send news for {title} with {url}")
        url_button = InlineKeyboardButton(text=title, url=url)
        reply_markup = InlineKeyboardMarkup().add(url_button)

        await c.message.answer(
            text="———", disable_notification=True, reply_markup=reply_markup
        )

    await dialog_manager.switch_to(state=DialogSG.main_menu)


async def on_finish(c: CallbackQuery, button: Button, dialog_manager: DialogManager):
    if dialog_manager.is_preview():
        await dialog_manager.done()
        return
    await dialog_manager.done()


# VIEWS
dialog = Dialog(
    # MAIN MENU
    Window(
        Const("~ NEWS TICKER ~"),
        Row(
            Button(
                Const("Get News"), id="get_news", on_click=on_get_news
            ),  # TODO:  SwitchTo ones it is implemented
            SwitchTo(
                Const("Browse"),
                id="browse",
                state=DialogSG.browse,
            ),
            SwitchTo(
                Const("Edit Keywords"), id="edit_keywords", state=DialogSG.edit_keywords
            ),
        ),
        Row(
            Button(Const("End"), on_click=on_finish, id="finish"),
            SwitchTo(Const("Home"), id="start", state=DialogSG.main_menu),
        ),
        state=DialogSG.main_menu,
    ),
    # BROWSE KEYWORDS
    Window(
        Const("Please select your keywords:"),
        ScrollingGroup(
            Multiselect(
                checked_text=Format("✓ {item[0]}"),
                unchecked_text=Format("{item[0]}"),
                id="mselect",
                item_id_getter=itemgetter(1),
                items="keywords_enumerated",
            ),
            width=2,
            height=4,
            id="browse",
        ),
        Row(
            SwitchTo(
                Const("x Discard"),
                state=DialogSG.main_menu,
                id="discard",
            ),
            Button(Const("✓ Submit"), on_click=on_submit_browse_keywords, id="submit"),
        ),
        getter=get_keywords_enumerated,
        state=DialogSG.browse,
    ),
    # EDIT KEYWORDS
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
            id="edit_kewords",
        ),
        Row(
            SwitchTo(
                Const("Add Keyword"), id="add_keyword", state=DialogSG.add_keyword
            ),
        ),
        Row(
            SwitchTo(
                Const("x Discard"),
                state=DialogSG.main_menu,
                id="discard",
            ),
            Button(
                Const("✓ Submit"),
                on_click=on_submit_edit_keywords,
                id="submit",
            ),
        ),
        getter=get_user_keywords_enumerated,
        state=DialogSG.edit_keywords,
    ),
    Window(
        Const("Add keyword:"),
        MessageInput(add_keyword_handler),
        state=DialogSG.add_keyword,
    ),
)


async def start(m: Message, dialog_manager: DialogManager):
    # it is important to reset stack because user wants to restart everything
    await dialog_manager.start(DialogSG.main_menu, mode=StartMode.RESET_STACK)

    user_id = get_user_id_from_dialog_manager(dialog_manager)

    if not UserGateway.exists_user_id(user_id):
        UserGateway.create_user(user_id)


async def main():
    # real main
    storage = MemoryStorage()
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot, storage=storage)
    dp.register_message_handler(start, text="/start", state="*")
    registry = DialogRegistry(dp)
    registry.register(dialog)

    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
