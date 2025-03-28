from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def enter_username(self, username):
        user=self.wait.until(EC.visibility_of_element_located((By.ID, "Login")))
        user.clear()  # Clear previous input if any
        user.send_keys(username)

    def enter_password(self, password):
        pas = self.wait.until(EC.visibility_of_element_located((By.ID, "Password")))
        pas.clear()  # Clear previous input if any
        pas.send_keys(password)

    def click_login(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "btnLogin"))).click()

    def login(self, username, password):
        """Combines all steps to perform login."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
