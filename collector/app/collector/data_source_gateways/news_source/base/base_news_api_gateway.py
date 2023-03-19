

class BaseNewsApiGateway:
    source: str
    base_url: str

    def get_news():
        raise NotImplementedError
