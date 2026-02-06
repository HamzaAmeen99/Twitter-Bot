import time
import sys
from Scripts.login import login
from Helpers.UrlManager import URLManager
from Scripts.TweetOperations import Tweet
from Helpers.SeleniumSingleton import SeleniumSingleton as SS


first_tweet = Tweet()

posts = URLManager.get_url(category='posts')
username = "globalnews2183"


def run_script():

    login(username)
    time.sleep(5)

    for post in posts:
        SS.navigate_to(post)
        time.sleep(5)
                
        first_tweet.click_first_tweet()

        time.sleep(5)

        first_tweet.comment_this_post(do_summerize=True)

        time.sleep(10)



if __name__ == '__main__':
    try:
        run_script()

        
    except KeyboardInterrupt as e:
        print()  # start on a new line
        dots = ""
        try:
            while True:
                dots = "." * ((len(dots) % 3) + 1)  # 1 → 2 → 3 → 1 ...
                sys.stdout.write(f"\rclosing{dots}   ")  # spaces clear leftovers
                sys.stdout.flush()
                time.sleep(0.5)

        except KeyboardInterrupt:
            # Allow the user to break out of the animation
            print("\nForce closed.")