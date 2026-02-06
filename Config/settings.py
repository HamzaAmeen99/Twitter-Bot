from pathlib import Path
from typing import Final

BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent
DATA_DIR: Final[Path] = BASE_DIR / "data"
COOKIES_DIR: Final[Path] = DATA_DIR / "cookies"
TWITTER_COOKIES_DIR: Final[Path] = COOKIES_DIR / "twitter"
PROMPT_DIR = BASE_DIR / "Prompts"

ACCOUNTS_FILE: Final[Path] = DATA_DIR / "accounts.json"
URLS_FILE: Final[Path] = DATA_DIR / "urls.json"
KEYWORDS_FILE: Final[Path] = DATA_DIR / "keywords.txt"
XPATH_FILE: Final[Path] = DATA_DIR / "xpaths.json"
PROMPT_FILE: Final[Path] = PROMPT_DIR / "summerize.poml"

TWITTER_COOKIES_DIR.mkdir(parents=True, exist_ok=True)
