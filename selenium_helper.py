
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions as ex
import time

class SeleniumHelper:
    def __init__(self, driver):
        """
        Initialize the SeleniumHelper class with a WebDriver instance.
        :param driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def normal_click(self, by, value):
        """
        Click an element when it becomes clickable.
        :param by: Locator strategy (By.ID, By.NAME, etc.)
        :param value: Locator value
        """
        self.wait.until(EC.element_to_be_clickable((by, value))).click()

    def send_keys(self, by, value, text):
        """
        Send text to an input field when it becomes visible.
        :param by: Locator strategy
        :param value: Locator value
        :param text: Text to be entered
        """
        element=self.wait.until(EC.visibility_of_element_located((by, value)))
        if element.is_enabled():
            element.clear()
            element.send_keys(text)
        else:
            raise Exception(f"Element located by ({by}, {value}) is not enabled.")


    def select_dropdown(self, by, value, option_text):
        """
        Select an option from a dropdown by visible text.
        :param by: Locator strategy
        :param value: Locator value
        :param option_text: Option text to select
        """
        self.wait.until(EC.visibility_of_element_located((by, value)))
        dropdown = Select(self.driver.find_element(by, value))
        dropdown.select_by_visible_text(option_text)
    def autocomplete_select(self, by, value, text):
        """
        Select an autocomplete suggestion based on input text.
        :param by: Locator strategy
        :param value: Locator value
        :param text: Text to input and search in suggestions
        """
        input_field = self.wait.until(EC.visibility_of_element_located((by, value)))
        input_field.clear()
        input_field.send_keys(text)
        time.sleep(2)  # Allow time for suggestions to appear
        suggestions = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-menu-item")))
        for suggestion in suggestions:
            if text.upper() in suggestion.text.upper():
                suggestion.click()
                return
        input_field.send_keys(Keys.DOWN)
        input_field.send_keys(Keys.ENTER)
    def click_element_while_loop(self, by, value, max_attempts=3):
        """
        Click an element with retry logic and JavaScript fallback.
        :param by: Locator strategy
        :param value: Locator value
        :param max_attempts: Maximum retry attempts before failing
        """
        attempt = 0
        element = None
        while attempt < max_attempts:
            try:
                element = self.wait.until(EC.element_to_be_clickable((by, value)))
                element.click()
                return True
            except (ex.ElementClickInterceptedException, ex.StaleElementReferenceException, ex.TimeoutException) as e:
                print(f"Attempt {attempt + 1}: Failed to click element {value} due to {type(e).__name__}. Retrying...")
                time.sleep(1)

            # JavaScript Click Fallback
            try:
                if element:
                    self.driver.execute_script("arguments[0].click();", element)
                    return True
            except ex.JavascriptException as js_error:
                print(f"Attempt {attempt + 1}: JavaScript click failed due to {type(js_error).__name__}")

            attempt += 1

        print(f"Failed to click element {value} after {max_attempts} attempts.")
        return False

    def click_element(self, by, value, retries=2):
        for attempt in range(retries):
            try:
                element = self.wait.until(EC.element_to_be_clickable((by, value)))
                element.click()
                return True
            except (ex.ElementClickInterceptedException, ex.StaleElementReferenceException, ex.TimeoutException):
                print(f"[WARNING] Attempt {attempt + 1} failed, retrying...")
        try:
            element = self.driver.find_element(by, value)
            self.driver.execute_script("arguments[0].click();", element)
            return True
        except:
            return False

    def close_popups(self):
        """
        Close unexpected popups dynamically.
        """
        try:
            close_button = self.driver.find_element(By.CLASS_NAME, "close")
            close_button.click()
        except:
            pass  # No popup found

    def switch_frames(self, element_id):
        """Switch to an iframe that contains a specific element"""
        self.driver.switch_to.default_content()
        for iframe in self.driver.find_elements(By.TAG_NAME, "iframe"):
            self.driver.switch_to.frame(iframe)
            try:
                if self.driver.find_element(By.ID, element_id):
                    return True
            except:
                self.driver.switch_to.default_content()
        return False

    def copy_paste_text(self, source_by, source_value, target_by, target_value):
        """
        Copy text from one input field and paste it into another.
        :param source_by: Locator strategy for source element
        :param source_value: Locator value for source element
        :param target_by: Locator strategy for target element
        :param target_value: Locator value for target element
        """
        source_element = self.wait.until(EC.visibility_of_element_located((source_by, source_value)))
        text_to_copy = source_element.get_attribute("value")  # Get text from source field

        target_element = self.wait.until(EC.visibility_of_element_located((target_by, target_value)))
        target_element.clear()  # Clear the field before pasting
        target_element.send_keys(text_to_copy)  # Paste the copied text


    def copy_paste_text_with_click(self, source_by, source_value, click_by, click_value, target_by, target_value):
        """
        Click an element to reveal a field, then copy text from one field and paste it into another.
        :param source_by: Locator strategy for source element (GSTNumber)
        :param source_value: Locator value for source element
        :param click_by: Locator strategy for the element to click before pasting
        :param click_value: Locator value for the element to click (acaretUpdivGstEkyc)
        :param target_by: Locator strategy for target element (ekycGSTNo)
        :param target_value: Locator value for target element
        """
        # Click the element to reveal the ekycGSTNo field
        self.normal_click(click_by, click_value)

        # Copy text from GSTNumber field
        source_element = self.wait.until(EC.visibility_of_element_located((source_by, source_value)))
        text_to_copy = source_element.get_attribute("value")

        # Paste text into ekycGSTNo field
        target_element = self.wait.until(EC.visibility_of_element_located((target_by, target_value)))
        target_element.clear()
        target_element.send_keys(text_to_copy)

    def get_text(self, by_type, element_id):
        """Extracts text from an element"""
        try:
            element = self.wait.until(EC.presence_of_element_located((by_type, element_id)))
            return element.text.strip() if element.text else None
        except Exception as e:
            print(f"[ERROR] Could not extract text from {element_id}: {str(e)}")
            return None

