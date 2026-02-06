import json
from Config.settings import URLS_FILE

class URLManager:
    _data = None  # Cache variable

    @classmethod
    def __load_data(cls):
        if cls._data is None:
            with open(URLS_FILE, "r") as f:
                cls._data = json.load(f)
        return cls._data

    @classmethod
    def get_url(cls, category, platform='twitter', key=None):
        """
        Generic URL getter.

        Args:
            platform (str): Name of the platform, e.g., 'twitter'.
            category (str): Category in the JSON, e.g., 'login', 'posts', 'api_urls'.
            key (str or None): Optional subkey inside the category.

        Returns:
            The requested URL, list, or None if not found.
        """
        data = cls.__load_data()
        cat_data = data.get(platform, {}).get(category)

        if key is not None and cat_data is not None:
            return cat_data.get(key)
        
        return cat_data
