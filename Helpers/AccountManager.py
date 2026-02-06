from Config.settings import ACCOUNTS_FILE
from Helpers.UrlManager import URLManager
import json

class AccountManager:
    _accounts = None  # cache

    @classmethod
    def _load_accounts(cls):
        if cls._accounts is None:
            try:
                with open(ACCOUNTS_FILE, "r") as f:
                    cls._accounts = json.load(f)
            except FileNotFoundError as e:
                print(f"Accounts file not found: {e}")
                cls._accounts = {}
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from accounts file: {e}")
                cls._accounts = {}
        return cls._accounts

    @classmethod
    def get_account(cls, account_name):
        accounts = cls._load_accounts()

        if not accounts:
            raise ValueError("Accounts data is empty or could not be loaded.")

        if account_name not in accounts:
            raise ValueError(f"Account '{account_name}' not found in accounts.json")

        account = accounts[account_name]
        url = None

        if account.get('has_cookies'):
            url = URLManager.get_url(category='login', key='login')
        else:
            url = URLManager.get_url(category='login', key='first_login')

        return account, url

    @classmethod
    def update_has_cookies(cls, account_name, value: bool):
        accounts = cls._load_accounts()

        if account_name not in accounts:
            raise ValueError(f"Account '{account_name}' not found.")

        accounts[account_name]['has_cookies'] = value

        with open(ACCOUNTS_FILE, "w") as f:
            json.dump(accounts, f, indent=4)

        cls._accounts = accounts  # update cache
