import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginTest(unittest.TestCase):

    def setUp(self):
        # Set up ChromeOptions
        chrome_options = Options()
        chrome_options.binary_location = r"C:\Users\user\Downloads\chrome-win64\chrome-win64\chrome.exe"  # Path to Chrome Beta

        # Set up ChromeDriver path
        chrome_driver_path = r"C:\Users\user\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"  # Path to ChromeDriver

        # Set up Chrome WebDriver with the specified options
        service = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)

    def test_login(self):
        driver = self.driver
        driver.get("http://r-logic9.com/RlogicDemoFtl/Login")

        # Enter username
        username = driver.find_element(By.ID, "Login")
        username.send_keys("Admin")

        # Enter password
        password = driver.find_element(By.ID, "Password")
        password.send_keys("omsgn9")

        # Click login button
        login_button = driver.find_element(By.ID, "btnLogin")  # Ensure this ID is correct
        login_button.click()

        try:
            # Wait for success message
            success_message = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Dashboard') or contains(text(), 'Welcome')]"))
            )
            print("Login Successful:", success_message.text)
            self.assertIn("Dashboard", success_message.text)

        except:
            # Check if login failed
            try:
                error_message = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "error-message"))  # Update the class name
                )
                print("Login Failed:", error_message.text)
            except:
                print("Login failed, but no error message found.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
