import logging

from aiogram_dialog import DialogManager

from publisher.config.config import Config
from publisher.data_source_gateways.collector.collector_gateway import CollectorGateway
from publisher.data_source_gateways.user.user_gateway import UserGateway

config = Config()


class Controller:
    @staticmethod
    def get_user_id_from_dialog_manager(dialog_manager: DialogManager) -> str:
        logging.info("Get user id from dialog_manager")
        user_id = str(dialog_manager.event["from"]["id"])
        logging.debug(f"Got user_id from dialog_manager:  {user_id}")
        return user_id

    @staticmethod
    async def get_keywords_enumerated(dialog_manager: DialogManager, **kwargs):
        keywords_response = CollectorGateway.get_keywords(
            sources=["tagesschau"],
            url=config.collector["url"],
            endpoint=config.collector["endpoints"]["keywords"],
            session_id=config.session_id,
        )

        keywords_enumerated = ((item, i) for i, item in enumerate(keywords_response))
        return {
            "keywords_enumerated": list(keywords_enumerated),
        }

    @staticmethod
    async def get_user_keywords(dialog_manager: DialogManager, **kwargs):
        user_id = Controller.get_user_id_from_dialog_manager(dialog_manager)
        user_keywords = UserGateway.get_keywords(user_id)

        return {
            "user_keywords": user_keywords,
        }

    @staticmethod
    async def get_user_keywords_enumerated(dialog_manager: DialogManager, **kwargs):
        user_id = Controller.get_user_id_from_dialog_manager(dialog_manager)

        user_keywords = UserGateway.get_keywords(user_id)
        user_keywords_enumerated = [(item, i) for i, item in enumerate(user_keywords)]
        return {
            "user_keywords_enumerated": user_keywords_enumerated,
        }
