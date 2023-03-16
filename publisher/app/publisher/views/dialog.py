from aiogram_dialog import Dialog

from publisher.views.browse_keys.browse_keys_view import BrowseKeysView
from publisher.views.edit_keywords.edit_keywords_view import EditKeywordsView
from publisher.views.main_menu.main_menu_view import MainMenuView

dialog = Dialog(
    MainMenuView.main_menu,
    BrowseKeysView.browse_keys,
    EditKeywordsView.edit_keywords,
    EditKeywordsView.add_keywords,
)
