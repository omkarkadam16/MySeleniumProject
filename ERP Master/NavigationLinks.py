from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest


class LoginTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Provide the path to your ChromeDriver
        cls.driver = webdriver.Chrome(
            service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
        )
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    def test_commodity(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/Login")

        driver.find_element(By.ID, "Login")
        driver.find_element(By.ID, "Login").send_keys("Riddhi")
        driver.find_element(By.ID, "Password").send_keys("OMSGN9")
        driver.find_element(By.ID, "btnLogin").click()

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Transportation"))
        ).click()
        print("Transportation link clicked successfully")

        menu_items = [
            ("Transportation Master »", "Transportation Master"),
            ("Common Masters »", "Common Masters"),
            ("Item Master", "Item Master"),
        ]

        for link_text, description in menu_items:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.LINK_TEXT, link_text))
            ).click()
            print(f"{description} link clicked successfully")
