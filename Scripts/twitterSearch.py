import time
import json
from Scripts.login import login
from main import username
from Helpers.SeleniumSingleton import SeleniumSingleton

def load_selectors(json_path="xpaths.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Loading Selector Paths
selectors = load_selectors()

def read_keywords(file_path="keywords.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return []


def search_keyword(keyword):
    search_url = f"https://twitter.com/search?q={keyword}&src=typed_query"
    SeleniumSingleton.navigate_to(search_url)
    print(f"🔍 Searching: {keyword}")
    time.sleep(3)


def go_to_latest_tab():
    try:
        latest_tab_xpath = selectors['search_page']['latest_tab_xpath']

        # "Latest" tab has 'Latest' text, it's a nav item
        SeleniumSingleton.click_element("xpath", "//span[text()='Latest']/ancestor::a")
        print("🕒 Switched to 'Latest' tab.")
        time.sleep(3)
    except Exception as e:
        print(f"❌ Could not switch to 'Latest': {e}")


def interact_with_first_post(comment_text="Great post!"):
    try:
        tweet_xpath = selectors['tweet']['first_tweet_xpath']
        tweet = SeleniumSingleton.find_element("xpath", tweet_xpath)

        if tweet:
            # Scroll and bring the tweet into view (with offset to avoid headers)
            SeleniumSingleton.execute_script(
                "arguments[0].scrollIntoView({block: 'center'}); window.scrollBy(0, -80);",
                tweet
            )
            time.sleep(1)

            # Wait for tweet to be clickable, then click
            SeleniumSingleton.execute_script("arguments[0].click();", tweet)
            print("🖱️ Opened first tweet.")
            time.sleep(4)

            # Step 1: Locate the like button in the detailed tweet view
            like_button_css = selectors['detailed_tweet']['like_button_css']
            like_button = SeleniumSingleton.find_element("css", like_button_css)

            # Step 2: Click it if found
            if like_button:
                SeleniumSingleton.execute_script("arguments[0].scrollIntoView(true);", like_button)
                time.sleep(1)
                SeleniumSingleton.execute_script("arguments[0].click();", like_button)
                print("❤️ Liked the detailed tweet.")
            else:
                print("⚠️ Like button not found in detailed view.")

            time.sleep(2)

            # ✅ Step 2: Comment on the tweet
            comment_box_css = selectors['detailed_tweet']['comment_box_css']
            comment_box = SeleniumSingleton.find_element("css", comment_box_css)
            if comment_box:
                # SeleniumSingleton.execute_script("arguments[0].scrollIntoView(true);", comment_box)
                time.sleep(1)
                SeleniumSingleton.send_keys("css", comment_box_css, comment_text)
                time.sleep(1)

                reply_button_css = selectors['detailed_tweet']['reply_button_css']
                reply_button = SeleniumSingleton.find_element("css", reply_button_css)
                if reply_button:
                    SeleniumSingleton.execute_script("arguments[0].click();", reply_button)
                    print("💬 Commented on the post.")
                else:
                    print("⚠️ Reply button not found.")
            else:
                print("⚠️ Comment box not found.")
            
            time.sleep(3)
            SeleniumSingleton.go_back()
            print("🔙 Navigated back.")
            time.sleep(2)

        else:
            print("❌ Could not find the first tweet.")

    except Exception as e:
        print(f"❌ Error interacting with first post: {e}")


def process_keywords(comment_text="Nice one!"):
    keywords = read_keywords()
    if not keywords:
        return

    for keyword in keywords:
        try:
            search_keyword(keyword)
            go_to_latest_tab()
            interact_with_first_post(comment_text)
        except Exception as e:
            print(f"❌ Error processing keyword '{keyword}': {e}")

    print("✅ Done with all keywords.")


if __name__ == "__main__":
    SeleniumSingleton.initialize_driver(timeout=15)

    time.sleep(3)
    
    SeleniumSingleton.navigate_to('https://x.com/Josephine0u/status/1954113623187390588')
    # process_keywords(comment_text="🔥 Amazing insight!")
