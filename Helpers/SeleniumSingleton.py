from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import threading
import time
import json
import atexit

class SeleniumSingleton:
    """
    Singleton class for Selenium WebDriver operations with static methods.
    Ensures only one WebDriver instance exists at a time.
    """
    
    _driver = None
    _lock = threading.Lock()
    _timeout = 10
    _headless = False
    
    @classmethod
    def initialize_driver(cls, browser='chrome', headless=False, timeout=10):
        """Initialize the WebDriver if not already done."""
        if cls._driver is not None:
            return cls._driver
        
        with cls._lock:
            if cls._driver is not None:
                return cls._driver
            
            cls._timeout = timeout
            cls._headless = headless
            
            try:
                if browser.lower() == 'chrome':
                    options = Options()
                    if headless:
                        options.add_argument('--headless')
                    options.add_argument('--no-sandbox')
                    options.add_argument('--disable-dev-shm-usage')
                    options.add_argument('--disable-gpu')
                    options.add_argument("--log-level=3")
                    options.add_experimental_option("excludeSwitches", ["enable-logging"])
                    cls._driver = webdriver.Chrome(options=options)
                elif browser.lower() == 'firefox':
                    from selenium.webdriver.firefox.options import Options as FirefoxOptions
                    options = FirefoxOptions()
                    if headless:
                        options.add_argument('--headless')
                    cls._driver = webdriver.Firefox(options=options)
                else:
                    raise ValueError(f"Unsupported browser: {browser}")
                
                cls._driver.implicitly_wait(cls._timeout)
                
                # Register cleanup on program exit
                atexit.register(cls.quit_driver)
                
                print(f"WebDriver initialized successfully ({browser})")
                return cls._driver
            
            except Exception as e:
                print(f"Error initializing WebDriver: {e}")
                raise
    
    @classmethod
    def get_driver(cls):
        """Get the current WebDriver instance."""
        if cls._driver is None:
            cls.initialize_driver()
        return cls._driver
    
    @staticmethod
    def navigate_to(url):
        """Navigate to a specific URL."""
        driver = SeleniumSingleton.get_driver()
        try:
            driver.get(url)
            print(f"Navigated to: {url}")
            return True
        except Exception as e:
            print(f"Error navigating to {url}: {e}")
            return False
    
    @staticmethod
    def _get_by_locator(selector_type, selector_value):
        """Convert string selector type to Selenium By locator."""
        selector_type = selector_type.lower().strip()
        
        selector_map = {
            'id': By.ID,
            'name': By.NAME,
            'class': By.CLASS_NAME,
            'classname': By.CLASS_NAME,
            'class_name': By.CLASS_NAME,
            'tag': By.TAG_NAME,
            'tagname': By.TAG_NAME,
            'tag_name': By.TAG_NAME,
            'css': By.CSS_SELECTOR,
            'css_selector': By.CSS_SELECTOR,
            'xpath': By.XPATH,
            'link': By.LINK_TEXT,
            'linktext': By.LINK_TEXT,
            'link_text': By.LINK_TEXT,
            'partial_link': By.PARTIAL_LINK_TEXT,
            'partial_link_text': By.PARTIAL_LINK_TEXT,
            'partiallink': By.PARTIAL_LINK_TEXT,
            'partiallinktext': By.PARTIAL_LINK_TEXT
        }
        
        if selector_type not in selector_map:
            raise ValueError(f"Unsupported selector type: '{selector_type}'. "
                           f"Supported types: {list(selector_map.keys())}")
        
        return selector_map[selector_type], selector_value
    
    @staticmethod
    def find_element(selector_type, selector_value, timeout=None):
        """Find a single element with optional explicit wait.
        
        Args:
            selector_type (str): Type of selector ('id', 'css', 'xpath', 'name', etc.)
            selector_value (str): The selector value
            timeout (int): Optional timeout in seconds
        """
        driver = SeleniumSingleton.get_driver()
        wait_time = timeout or SeleniumSingleton._timeout
        
        try:
            by, value = SeleniumSingleton._get_by_locator(selector_type, selector_value)
            wait = WebDriverWait(driver, wait_time)
            element = wait.until(EC.presence_of_element_located((by, value)))
            return element
        except TimeoutException:
            print(f"Element not found: {selector_type}='{selector_value}' within {wait_time} seconds")
            return None
        except ValueError as e:
            print(f"Invalid selector: {e}")
            return None
    
    @staticmethod
    def find_elements(selector_type, selector_value, timeout=None):
        """Find multiple elements with optional explicit wait.
        
        Args:
            selector_type (str): Type of selector ('id', 'css', 'xpath', 'name', etc.)
            selector_value (str): The selector value
            timeout (int): Optional timeout in seconds
        """
        driver = SeleniumSingleton.get_driver()
        wait_time = timeout or SeleniumSingleton._timeout
        
        try:
            by, value = SeleniumSingleton._get_by_locator(selector_type, selector_value)
            wait = WebDriverWait(driver, wait_time)
            wait.until(EC.presence_of_element_located((by, value)))
            elements = driver.find_elements(by, value)
            return elements
        except TimeoutException:
            print(f"Elements not found: {selector_type}='{selector_value}' within {wait_time} seconds")
            return []
        except ValueError as e:
            print(f"Invalid selector: {e}")
            return []
    
    @staticmethod
    def click_element(selector_type, selector_value, timeout=None):
        """Click an element after waiting for it to be clickable.
        
        Args:
            selector_type (str): Type of selector ('id', 'css', 'xpath', 'name', etc.)
            selector_value (str): The selector value
            timeout (int): Optional timeout in seconds
        """
        driver = SeleniumSingleton.get_driver()
        wait_time = timeout or SeleniumSingleton._timeout
        
        try:
            by, value = SeleniumSingleton._get_by_locator(selector_type, selector_value)
            wait = WebDriverWait(driver, wait_time)
            element = wait.until(EC.element_to_be_clickable((by, value)))
            element.click()
            print(f"Clicked element: {selector_type}='{selector_value}'")
            return True
        except TimeoutException:
            print(f"Element not clickable: {selector_type}='{selector_value}' within {wait_time} seconds")
            return False
        except ValueError as e:
            print(f"Invalid selector: {e}")
            return False
    
    @staticmethod
    def send_keys(selector_type, selector_value, text, clear_first=True, timeout=None):
        """Send keys to an input element.
        
        Args:
            selector_type (str): Type of selector ('id', 'css', 'xpath', 'name', etc.)
            selector_value (str): The selector value
            text (str): Text to send to the element
            clear_first (bool): Whether to clear the field first
            timeout (int): Optional timeout in seconds
        """
        element = SeleniumSingleton.find_element(selector_type, selector_value, timeout)
        if element:
            try:
                if clear_first:
                    element.clear()
                element.send_keys(text)
                print(f"Sent keys to element: {selector_type}='{selector_value}'")
                return True
            except Exception as e:
                print(f"Error sending keys: {e}")
                return False
        return False
    
    @staticmethod
    def get_text(selector_type, selector_value, timeout=None):
        """Get text content from an element.
        
        Args:
            selector_type (str): Type of selector ('id', 'css', 'xpath', 'name', etc.)
            selector_value (str): The selector value
            timeout (int): Optional timeout in seconds
        """
        element = SeleniumSingleton.find_element(selector_type, selector_value, timeout)
        if element:
            return element.text
        return None
    
    @staticmethod
    def get_attribute(selector_type, selector_value, attribute, timeout=None):
        """Get attribute value from an element.
        
        Args:
            selector_type (str): Type of selector ('id', 'css', 'xpath', 'name', etc.)
            selector_value (str): The selector value
            attribute (str): The attribute name to get
            timeout (int): Optional timeout in seconds
        """
        element = SeleniumSingleton.find_element(selector_type, selector_value, timeout)
        if element:
            return element.get_attribute(attribute)
        return None
    
    @staticmethod
    def wait_for_element_visible(selector_type, selector_value, timeout=None):
        """Wait for an element to be visible.
        
        Args:
            selector_type (str): Type of selector ('id', 'css', 'xpath', 'name', etc.)
            selector_value (str): The selector value
            timeout (int): Optional timeout in seconds
        """
        driver = SeleniumSingleton.get_driver()
        wait_time = timeout or SeleniumSingleton._timeout
        
        try:
            by, value = SeleniumSingleton._get_by_locator(selector_type, selector_value)
            wait = WebDriverWait(driver, wait_time)
            element = wait.until(EC.visibility_of_element_located((by, value)))
            return element
        except TimeoutException:
            print(f"Element not visible: {selector_type}='{selector_value}' within {wait_time} seconds")
            return None
        except ValueError as e:
            print(f"Invalid selector: {e}")
            return None
    
    @staticmethod
    def wait_for_element_clickable(selector_type, selector_value, timeout=None):
        """Wait for an element to be clickable.
        
        Args:
            selector_type (str): Type of selector ('id', 'css', 'xpath', 'name', etc.)
            selector_value (str): The selector value
            timeout (int): Optional timeout in seconds
        """
        driver = SeleniumSingleton.get_driver()
        wait_time = timeout or SeleniumSingleton._timeout
        
        try:
            by, value = SeleniumSingleton._get_by_locator(selector_type, selector_value)
            wait = WebDriverWait(driver, wait_time)
            element = wait.until(EC.element_to_be_clickable((by, value)))
            return element
        except TimeoutException:
            print(f"Element not clickable: {selector_type}='{selector_value}' within {wait_time} seconds")
            return None
        except ValueError as e:
            print(f"Invalid selector: {e}")
            return None
    
    @staticmethod
    def execute_script(script, *args):
        """Execute JavaScript in the browser."""
        driver = SeleniumSingleton.get_driver()
        try:
            return driver.execute_script(script, *args)
        except Exception as e:
            print(f"Error executing script: {e}")
            return None
    
    @staticmethod
    def take_screenshot(filename=None):
        """Take a screenshot and save it."""
        driver = SeleniumSingleton.get_driver()
        if filename is None:
            filename = f"screenshot_{int(time.time())}.png"
        
        try:
            driver.save_screenshot(filename)
            print(f"Screenshot saved: {filename}")
            return filename
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return None
    
    @staticmethod
    def switch_to_window(window_handle):
        """Switch to a specific browser window."""
        driver = SeleniumSingleton.get_driver()
        try:
            driver.switch_to.window(window_handle)
            print(f"Switched to window: {window_handle}")
            return True
        except Exception as e:
            print(f"Error switching to window: {e}")
            return False
    
    @staticmethod
    def get_current_url():
        """Get the current page URL."""
        driver = SeleniumSingleton.get_driver()
        return driver.current_url
    
    @staticmethod
    def get_page_title():
        """Get the current page title."""
        driver = SeleniumSingleton.get_driver()
        return driver.title
    
    @staticmethod
    def get_window_handles():
        """Get all window handles."""
        driver = SeleniumSingleton.get_driver()
        return driver.window_handles
    
    @staticmethod
    def refresh_page():
        """Refresh the current page."""
        driver = SeleniumSingleton.get_driver()
        driver.refresh()
        print("Page refreshed")
    
    @staticmethod
    def go_back():
        """Navigate back in browser history."""
        driver = SeleniumSingleton.get_driver()
        driver.back()
        print("Navigated back")
    
    @staticmethod
    def go_forward():
        """Navigate forward in browser history."""
        driver = SeleniumSingleton.get_driver()
        driver.forward()
        print("Navigated forward")
    
    @staticmethod
    def close_current_tab():
        """Close the current browser tab."""
        driver = SeleniumSingleton.get_driver()
        driver.close()
        print("Current tab closed")
    
    @staticmethod
    def switch_to_frame(frame_reference):
        """Switch to an iframe or frame."""
        driver = SeleniumSingleton.get_driver()
        try:
            driver.switch_to.frame(frame_reference)
            print(f"Switched to frame: {frame_reference}")
            return True
        except Exception as e:
            print(f"Error switching to frame: {e}")
            return False
    
    @staticmethod
    def switch_to_default_content():
        """Switch back to the main document."""
        driver = SeleniumSingleton.get_driver()
        driver.switch_to.default_content()
        print("Switched to default content")
    
    @staticmethod
    def accept_alert():
        """Accept browser alert."""
        driver = SeleniumSingleton.get_driver()
        try:
            alert = driver.switch_to.alert
            alert.accept()
            print("Alert accepted")
            return True
        except Exception as e:
            print(f"Error accepting alert: {e}")
            return False
    
    @staticmethod
    def dismiss_alert():
        """Dismiss browser alert."""
        driver = SeleniumSingleton.get_driver()
        try:
            alert = driver.switch_to.alert
            alert.dismiss()
            print("Alert dismissed")
            return True
        except Exception as e:
            print(f"Error dismissing alert: {e}")
            return False
    
    @staticmethod
    def get_alert_text():
        """Get text from browser alert."""
        driver = SeleniumSingleton.get_driver()
        try:
            alert = driver.switch_to.alert
            return alert.text
        except Exception as e:
            print(f"Error getting alert text: {e}")
            return None
    
    @classmethod
    def quit_driver(cls):
        """Quit the WebDriver and clean up resources."""
        if cls._driver:
            try:
                cls._driver.quit()
                print("WebDriver quit successfully")
            except Exception as e:
                print(f"Error quitting WebDriver: {e}")
            finally:
                cls._driver = None

    @staticmethod
    def save_cookies(driver, path):
        with open(path, "w") as f:
            json.dump(driver.get_cookies(), f)
            print(f'Cookies saved at path:{path}')

    @staticmethod
    def load_cookies(driver, path):
        with open(path, "r") as f:
            cookies = json.load(f)
        for cookie in cookies:
            # Selenium requires expiry as int, ensure it's int if present
            if isinstance(cookie.get("expiry", None), float):
                cookie["expiry"] = int(cookie["expiry"])
            driver.add_cookie(cookie)

# Usage Example
# if __name__ == "__main__":
#     try:
#         # Initialize driver (only needs to be called once)
#         SeleniumSingleton.initialize_driver('chrome', headless=False, timeout=15)
        
#         # All operations now use string selectors - NO SELENIUM IMPORTS NEEDED!
#         SeleniumSingleton.navigate_to("https://www.example.com")
        
#         # Get page information
#         title = SeleniumSingleton.get_page_title()
#         url = SeleniumSingleton.get_current_url()
#         print(f"Page title: {title}")
#         print(f"Current URL: {url}")
        
#         # Find and interact with elements using string selectors
#         # SeleniumSingleton.click_element("id", "some-button")
#         # SeleniumSingleton.send_keys("name", "search", "Hello World")
#         # text = SeleniumSingleton.get_text("tag", "h1")
#         # SeleniumSingleton.click_element("css", ".submit-btn")
#         # SeleniumSingleton.click_element("xpath", "//button[text()='Submit']")
        
#         # Take a screenshot
#         SeleniumSingleton.take_screenshot("example_page.png")
        
#         # Wait a bit to see the page
#         time.sleep(3)
        
#     finally:
#         # Clean up
#         SeleniumSingleton.quit_driver()

# Example usage in different modules - NO SELENIUM IMPORTS NEEDED:
# from selenium_singleton import SeleniumSingleton
# 
# # Clean string-based selectors
# SeleniumSingleton.navigate_to("https://google.com")
# SeleniumSingleton.send_keys("name", "q", "Python Selenium")
# SeleniumSingleton.click_element("name", "btnK")
# 
# # Case insensitive selector types work too:
# SeleniumSingleton.click_element("ID", "submit")           # works
# SeleniumSingleton.click_element("css", ".button")        # works  
# SeleniumSingleton.click_element("XPath", "//div[@id='x']") # works
# SeleniumSingleton.click_element("class_name", "btn")     # works
# SeleniumSingleton.click_element("LINK_TEXT", "Click Me") # works