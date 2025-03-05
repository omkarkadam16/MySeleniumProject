from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest


class CustomerMaster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(
            service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
        )
        cls.driver.implicitly_wait(5)
        cls.driver.maximize_window()

    def click_element(self, by, value, timeout=5):
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        ).click()
        print(f"{value} clicked successfully")

    def send_keys(self, by, value, text, timeout=5):
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        ).send_keys(text)
        print(f"{value} updated with {text}")

    def dropdown_option(self, by, value, option_text, timeout=2):
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
        dropdown = Select(self.driver.find_element(by, value))
        dropdown.select_by_visible_text(option_text)
        print(f"{value} updated to {option_text}")

    def switch_frames(self, element_id):
        driver = self.driver
        driver.switch_to.default_content()

        for iframe in driver.find_elements(By.TAG_NAME, "iframe"):
            driver.switch_to.frame(iframe)

            if driver.find_elements(By.ID, element_id):
                return True
            print(f"Switched to correct iframe for {element_id}")

            driver.switch_to.default_content()
        print(f"Unable to locate {element_id} in any iframe!")
        return False

    def test_customer(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/Login")

        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "OMSGN9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful")

        menus = [
            "Transportation",
            "Transportation Master »",
            "Customer »",
            "Customer",
        ]

        for link_test in menus:
            self.click_element(By.LINK_TEXT, link_test)
            print(f"{link_test} link clicked successfully")

        if self.switch_frames("btn_NewRecord"):
            self.click_element(By.ID, "btn_NewRecord")

        if self.switch_frames("Party_PartyName"):
            self.send_keys(By.ID, "Party_PartyName", "Ducati Motorsport")

        if self.switch_frames("Party_PartyCategoryId"):
            self.dropdown_option(By.ID, "Party_PartyCategoryId", "GENERAL")

        if self.switch_frames("Party_PartyIndustryTypeId"):
            self.dropdown_option(By.ID, "Party_PartyIndustryTypeId", "GENERAL")

        if self.switch_frames("Party_PartyGradeId"):
            self.dropdown_option(By.ID, "Party_PartyGradeId", "A Class")

        if self.switch_frames("Party_PartyGroupId"):
            self.dropdown_option(By.ID, "Party_PartyGroupId", "GENERAL ")

        if self.switch_frames("EffectiveFromDate"):
            self.send_keys(By.ID, "EffectiveFromDate", "27-01-2025")

    @classmethod
    def tearDownClass(cls):
        """Closes the browser after tests are complete."""
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
