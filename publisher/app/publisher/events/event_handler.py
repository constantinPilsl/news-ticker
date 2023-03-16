import logging

from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.manager.protocols import ManagedDialogAdapterProto
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Multiselect,
    Row,
    ScrollingGroup,
    SwitchTo,
    Url,
)

from publisher.config.config import Config
from publisher.controller.controller import Controller

# TODO:  Gateways should handled via controller!
from publisher.data_source_gateways.collector.collector_gateway import CollectorGateway
from publisher.data_source_gateways.user.user_gateway import UserGateway
from publisher.states.dialog_sg.dialog_sg import DialogSG

config = Config()


class EventHandler:
    async def add_keyword_handler(
        m: Message, dialog: ManagedDialogAdapterProto, dialog_manager: DialogManager
    ):
        if dialog_manager.is_preview():
            await dialog.next()
            return

        user_id = Controller.get_user_id_from_dialog_manager(dialog_manager)
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

        user_id = Controller.get_user_id_from_dialog_manager(dialog_manager)

        # TODO: This should not be a separate request and it does not work for editing keywords
        keywords_response = CollectorGateway.get_keywords(
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

        user_id = Controller.get_user_id_from_dialog_manager(dialog_manager)
        mselect = dialog_manager.current_context().widget_data["mselect"]

        keywords = keywords = UserGateway.get_keywords(user_id)
        selected_ids = [int(id) for id in mselect]
        keyword_id_mapping = ((i, item) for i, item in enumerate(keywords))
        keywords = (i[1] for i in keyword_id_mapping if i[0] in selected_ids)

        UserGateway.create_keywords(user_id, keywords)
        updated_keywords = UserGateway.get_keywords(user_id)

        keyword_id_str = ", ".join(updated_keywords)
        logging.info(f"Keyword ids set to:  {keyword_id_str}")

        await c.message.answer(f"Your keywords have been set to: {keyword_id_str}")
        await dialog_manager.switch_to(state=DialogSG.main_menu)

    async def on_get_news(
        c: CallbackQuery, button: Button, dialog_manager: DialogManager
    ):
        if dialog_manager.is_preview():
            await dialog_manager.done()
            return

        user_id = Controller.get_user_id_from_dialog_manager(dialog_manager)

        logging.info("Getting news...")
        user_keywords = UserGateway.get_keywords(user_id)
        logging.info(f"For following keywords:  {user_keywords}")

        news_response = CollectorGateway.get_news(
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

    async def on_finish(
        c: CallbackQuery, button: Button, dialog_manager: DialogManager
    ):
        if dialog_manager.is_preview():
            await dialog_manager.done()
            return
        await dialog_manager.done()

    async def start(m: Message, dialog_manager: DialogManager):
        # it is important to reset stack because user wants to restart everything
        await dialog_manager.start(DialogSG.main_menu, mode=StartMode.RESET_STACK)

        user_id = Controller.get_user_id_from_dialog_manager(dialog_manager)

        if not UserGateway.exists_user_id(user_id):
            UserGateway.create_user(user_id)
