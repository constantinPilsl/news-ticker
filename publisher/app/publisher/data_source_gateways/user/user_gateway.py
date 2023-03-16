import logging
from typing import Generator, Iterable, Union


user_data = {
    # "5806566314": {"keywords": set()},
    # "5806566314": {
    #     "keywords": {
    #         "ukraine",
    #     },
    # },
}


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

    def get_keywords(
        user_id: str,
    ) -> set[str]:  # TODO: SHOULD RATHER RETURN GENERATOR[str, None, None] or List
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
