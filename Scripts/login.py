import json
import time
from Config.settings import TWITTER_COOKIES_DIR, ACCOUNTS_FILE
from Helpers.AccountManager import AccountManager
from selenium.webdriver.common.keys import Keys
from Helpers.SeleniumSingleton import SeleniumSingleton

accounts_file=ACCOUNTS_FILE

def login(account_name):
    # Load credentials from accounts.json

    account_data, url = AccountManager.get_account(account_name)

    username = account_data["username"]
    password = account_data["password"]

    cookie_file_path = TWITTER_COOKIES_DIR / f"{username}.json"

    # Start driver
    driver = SeleniumSingleton.initialize_driver(timeout=15)

    # Go to Twitter login page
    SeleniumSingleton.navigate_to(url)
    time.sleep(3)

    # Load cookies if available
    if cookie_file_path.exists():
        AccountManager.update_has_cookies(account_name, True)
        SeleniumSingleton.load_cookies(driver, cookie_file_path)
        driver.refresh()
        time.sleep(3)

        if "home" in driver.current_url:
            print("✅ Logged in using cookies.")
            AccountManager.update_has_cookies(account_name, True)
            return True
        else:
            print("⚠️ Cookies invalid or expired, proceeding with manual login.")

    else:
        AccountManager.update_has_cookies(account_name, False)


    # Manual login flow
    try:
        SeleniumSingleton.click_element("tag", "input")
        time.sleep(1)
        SeleniumSingleton.send_keys("tag", "input", username)
        SeleniumSingleton.send_keys("tag", "input", Keys.ENTER, clear_first=False)
        time.sleep(3)

        inputs = SeleniumSingleton.find_elements("tag", "input")
        if len(inputs) > 1:
            SeleniumSingleton.send_keys("tag", "input", username)
            SeleniumSingleton.send_keys("tag", "input", Keys.ENTER, clear_first=False)
            time.sleep(2)

        SeleniumSingleton.send_keys("name", "password", password)
        SeleniumSingleton.send_keys("name", "password", Keys.ENTER, clear_first=False)
        time.sleep(5)

        if "home" in driver.current_url:
            print("✅ Logged in successfully. Saving cookies...")
            SeleniumSingleton.save_cookies(driver, cookie_file_path)
            AccountManager.update_has_cookies(account_name, True)

            return True
        else:
            print("❌ Login may have failed.")
            return False

    except Exception as e:
        print(f"❌ Exception during login: {e}")
        return False
