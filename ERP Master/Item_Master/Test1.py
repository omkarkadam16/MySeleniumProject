from operator import truediv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import unittest


class ItemMasterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(
            service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
        )
        cls.driver.implicitly_wait(10)  # Implicit wait
        cls.driver.maximize_window()

    def switch_to_iframe(self, element_id):
        driver = self.driver
        driver.switch_to.default_content()

        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for index, iframe in enumerate(iframes):
            driver.switch_to.frame(index)
            try:
                if driver.find_elements(By.ID, element_id):
                    print(
                        f"Switched to correct iframe at index {index} for {element_id}"
                    )
                    return True
            except:
                print(f"No iframe found for {element_id}")
        return False

    def test_item_master(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/Login")

        driver.find_element(By.ID, "Login").send_keys("Riddhi")
        driver.find_element(By.ID, "Password").send_keys("OMSGN9")
        driver.find_element(By.ID, "btnLogin").click()
        print("Login successful")

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Transportation"))
        )
        print("LinkTest Located successfully")

        menu_items = [
            ("Transportation", "Transportation"),
            ("Transportation Master »", "Transportation Master"),
            ("Common Masters »", "Common "),
            ("Item Master", "Item "),
        ]

        for link_text, description in menu_items:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, link_text))
            ).click()
            print(f"{description} link clicked successfully")

        # Switch to iframe dynamically for New Record button
        if self.switch_to_iframe("btn_NewRecord"):
            driver.find_element(By.ID, "btn_NewRecord").click()
            print("New Record button clicked successfully")

        if self.switch_to_iframe("TransportProductName"):
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "TransportProductName"))
            ).send_keys("TEST8")
            print("✅ TransportProductName field filled")
        else:
            print("No iframe found for TransportProductName")
