import json
from Config.settings import XPATH_FILE


class XpathManager:

    _xpaths = None  # cache

    @classmethod
    def _load_xpaths(self):
        if self._xpaths is None:
            try:
                with open(XPATH_FILE, "r") as f:
                    self._xpaths = json.load(f)
            except FileNotFoundError as e:
                print(f"Accounts file not found: {e}")
                self._xpaths = {}
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from Xpath file: {e}")
                self._xpaths = {}
        return self._xpaths
    
    @classmethod
    def get_xpath(cls, page, element):
        data = cls._load_xpaths()
        return data.get(page, {}).get(element, {})
        

