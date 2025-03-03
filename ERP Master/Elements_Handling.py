from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


def click_element(self, by, value, timeout=5):
    """Waits for an element to be clickable and clicks it."""
    WebDriverWait(self.driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    ).click()
    print(f"Clicked element {value}")


def send_keys(self, by, value, text, timeout=5):
    """Waits for an element to be present and sends text to it."""
    WebDriverWait(self.driver, timeout).until(
        EC.presence_of_element_located((by, value))
    ).send_keys(text)
    print(f"Entered '{text}' in element {value}")


def select_dropdown(self, by, value, option_text, timeout=5):
    """Waits for a dropdown to be present and selects an option by visible text."""
    WebDriverWait(self.driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )
    dropdown = Select(self.driver.find_element(by, value))
    dropdown.select_by_visible_text(option_text)
    print(f"Selected '{option_text}' from dropdown {value}")
