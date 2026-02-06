import time
from APIs.OpenAi import summerize_api
from Helpers.XpathManager import XpathManager
from Helpers.SeleniumSingleton import SeleniumSingleton as SS



class Tweet:

    def click_first_tweet(self):

        try:
            self.tweet_xpath = XpathManager.get_xpath('tweet_page', 'first_tweet_xpath')
            self.tweet = SS.find_element("xpath", self.tweet_xpath)

            if self.tweet:
                # Scroll and bring the tweet into view (with offset to avoid headers)
                self.scroll(self.tweet)
                time.sleep(1)

                # Wait for tweet to be clickable, then click
                SS.execute_script("arguments[0].click();", self.tweet)
                print("🖱️ Opened first tweet.")
                time.sleep(4)

            else:
                print("❌ Could not find the first tweet.")

        except Exception as e:
            print(f"❌ Error interacting with first post: {e}")


    def scroll(self, tweet):

        try:
            SS.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'}); window.scrollBy(0, -80);",
                    tweet
                )
            
        except Exception as e:
            print(f"❌ Error scrolling with post page: {e}")


    def comment_this_post(self, comment_text="Great post!", do_summerize=False):
        comment_box_css = XpathManager.get_xpath('detailed_tweet_page', 'comment_box_css')
        reply_button_css = XpathManager.get_xpath('detailed_tweet_page', 'reply_button_css')

        # ✅ Step 1: If summarization is requested, get summary instead of using comment_text
        if do_summerize:
            summary = self.summarize()
            if summary:
                comment_text = summary
            else:
                print("⚠️ Could not generate summary, using default comment instead.")

        # ✅ Step 2: Comment on the tweet
        comment_box = SS.find_element("css", comment_box_css)
        if comment_box:
            time.sleep(1)
            SS.send_keys("css", comment_box_css, comment_text)
            time.sleep(1)

            reply_button = SS.find_element("css", reply_button_css)
            if reply_button:
                SS.execute_script("arguments[0].click();", reply_button)
                print(f"💬 Commented on the post: {comment_text}")
            else:
                print("⚠️ Reply button not found.")
        else:
            print("⚠️ Comment box not found.")

    def summarize(self):
        """Extracts tweet text and summarizes it via API"""
        tweet_text_css = XpathManager.get_xpath('detailed_tweet_page', 'tweet_content_css')
        tweet_element = SS.find_element('css', tweet_text_css)

        if tweet_element:
            time.sleep(1)
            tweet_text = tweet_element.text.strip()
            try:
                return summerize_api(tweet_text)
            except Exception as e:
                print(f"⚠️ Summarization API failed: {e}")
                return None
        else:
            print("⚠️ Failed to get tweet text for summarization.")
            return None