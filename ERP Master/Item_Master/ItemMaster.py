from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest


class ItemMasterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(
            service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
        )
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    def switch_to_iframe(self, element_id):
        driver = self.driver
        driver.switch_to.default_content()

        for index, iframe in enumerate(driver.find_elements(By.TAG_NAME, "iframe")):
            driver.switch_to.frame(iframe)  # Switch to the iframe
            if driver.find_elements(By.ID, element_id):  # Check if element exists
                print(f"Switched to correct iframe at index {index} for {element_id}")
                return True
            driver.switch_to.default_content()  # Only reset if the element was NOT found

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
        print("Transportation link located successfully")

        menu_items = [
            ("Transportation", "Transportation"),
            ("Transportation Master »", "Transportation Master"),
            ("Common Masters »", "Common Master"),
            ("Item Master", "Item Master"),
        ]

        for link_text, description in menu_items:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, link_text))
            ).click()
            print(f"{description} link clicked successfully")

        if self.switch_to_iframe("btn_NewRecord"):
            driver.find_element(By.ID, "btn_NewRecord").click()
            print("New Record button clicked successfully")
        else:
            print("Failed to switch to iframe for btn_NewRecord")

        if self.switch_to_iframe("TransportProductName"):
            driver.find_element(By.ID, "TransportProductName").send_keys("TEST3")
            print("TransportProductName button clicked successfully")
        else:
            print("Failed to switch to iframe for TransportProductName")

        if self.switch_to_iframe("CommodityTypeId"):
            dropdown = Select(self.driver.find_element(By.ID, "CommodityTypeId"))
            dropdown.select_by_visible_text("FOOD ITEMS")
            print("FOOD ITEMS selected successfully")
        else:
            print("Failed to switch to iframe for CommodityTypeId")

        if self.switch_to_iframe("mysubmit"):
            self.driver.find_element(By.ID, "mysubmit").click()
            print("Form submitted successfully")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
