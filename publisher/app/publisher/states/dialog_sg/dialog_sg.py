from aiogram.dispatcher.filters.state import State, StatesGroup


class DialogSG(StatesGroup):
    start = State()
    main_menu = State()
    finish = State()
    get_news = State()
    browse = State()
    edit_keywords = State()
    add_keyword = State()
