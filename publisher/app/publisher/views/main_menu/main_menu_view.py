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
from publisher.states.dialog_sg.dialog_sg import DialogSG


class MainMenuView:
    main_menu = Window(
            Const("~ NEWS TICKER ~"),
            Row(
                Button(
                    Const("Get News"), id="get_news", on_click=EventHandler.on_get_news
                ),  # TODO:  SwitchTo ones it is implemented
                SwitchTo(
                    Const("Browse"),
                    id="browse",
                    state=DialogSG.browse,
                ),
                SwitchTo(
                    Const("Edit Keywords"),
                    id="edit_keywords",
                    state=DialogSG.edit_keywords,
                ),
            ),
            Row(
                Button(Const("End"), on_click=EventHandler.on_finish, id="finish"),
                SwitchTo(Const("Home"), id="start", state=DialogSG.main_menu),
            ),
            state=DialogSG.main_menu,
        )
