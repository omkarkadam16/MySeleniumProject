from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import unittest


class LoginTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up Chrome WebDriver service
        service = Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
        cls.driver = webdriver.Chrome(service=service)
        cls.driver.implicitly_wait(30)  # Implicit wait to handle minor delays

    def test_commodity_master(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/Login")  # Open the login page

        # Login Process
        driver.find_element(
            By.ID, "Login"
        ).clear()  # Clear the input field before entering text
        driver.find_element(By.ID, "Login").send_keys("Riddhi")  # Enter username
        driver.find_element(By.ID, "Password").clear()  # Clear the password field
        driver.find_element(By.ID, "Password").send_keys("OMSGN9")  # Enter password
        driver.find_element(By.ID, "btnLogin").click()  # Click login button

        # Wait for page to load after login
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Transportation"))
        )
        print("Login successful!")
