from operator import itemgetter

from aiogram_dialog import Dialog, DialogManager, StartMode, Window
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

from publisher.controller.controller import Controller
from publisher.events.event_handler import EventHandler
from publisher.states.dialog_sg.dialog_sg import DialogSG


class EditKeywordsView:
    edit_keywords = Window(
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
                on_click=EventHandler.on_submit_edit_keywords,
                id="submit",
            ),
        ),
        getter=Controller.get_user_keywords_enumerated,
        state=DialogSG.edit_keywords,
    )

    add_keywords = Window(
        Const("Add keyword:"),
        MessageInput(EventHandler.add_keyword_handler),
        state=DialogSG.add_keyword,
    )
