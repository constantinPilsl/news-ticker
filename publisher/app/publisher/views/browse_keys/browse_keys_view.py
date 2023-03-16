from operator import itemgetter

from aiogram_dialog import Dialog, DialogManager, StartMode, Window
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

from publisher.events.event_handler import EventHandler
from publisher.controller.controller import Controller
from publisher.states.dialog_sg.dialog_sg import DialogSG


class BrowseKeysView:
    browse_keys = Window(
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
                Button(
                    Const("✓ Submit"),
                    on_click=EventHandler.on_submit_browse_keywords,
                    id="submit",
                ),
            ),
            getter=Controller.get_keywords_enumerated,
            state=DialogSG.browse,
        )
