from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time


class CustomerMaster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(
            service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
        )
        cls.driver.implicitly_wait(10)
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

    def dropdown_option(self, by, value, option_text, timeout=5):
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
        dropdown = Select(self.driver.find_element(by, value))
        dropdown.select_by_visible_text(option_text)
        print(f"{value} updated to {option_text}")

    def autocomplete_select(self, by, value, text, timeout=10):
        """Selects an option from an autocomplete dropdown by typing and choosing the first suggestion."""
        input_field = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
        input_field.send_keys(text)  # Step 1: Enter text
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ui-menu-item"))
        ).click()  # Step 2: Wait for suggestions and click
        print(f"{value} updated with {text}")

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

        # Basic Information
        if self.switch_frames("Party_PartyName"):
            self.send_keys(By.ID, "Party_PartyName", "Ducati Motorsport")

            self.dropdown_option(By.ID, "Party_PartyCategoryId", "GENERAL")

            self.dropdown_option(By.ID, "Party_PartyIndustryTypeId", "GENERAL")

            self.dropdown_option(By.ID, "Party_PartyGradeId", "A Class")

            self.dropdown_option(By.ID, "Party_PartyGroupId", "GENERAL")

            self.send_keys(By.ID, "EffectiveFromDate", "27-01-2025")

            self.send_keys(By.ID, "PANNo", "ABCCK4599D")

            driver.save_screenshot("Basic Details.png")

        # Address Details

        if self.switch_frames("AddressTypeId"):
            self.dropdown_option(By.ID, "AddressTypeId", "Office")

            self.send_keys(By.ID, "AddressLine", "123 Main St Mumbai")

            self.autocomplete_select(By.ID, "CityId-select", "MUMBAI")

            self.send_keys(By.ID, "PinCode", "400001")

            self.send_keys(By.ID, "ContactNo", "1234567890")

            self.send_keys(By.ID, "Mob", "5564567890")

            self.click_element(By.ID, "btnSave-AddressSession77")

            driver.save_screenshot("Address Details.png")

        # Registation Number Details

        if self.switch_frames("RegistrationHeadId"):
            self.dropdown_option(By.ID, "RegistrationHeadId", "PAN No.")

            self.send_keys(By.ID, "Number", "ABCCK4599D")

            self.click_element(By.ID, "btnSave-RegistrationSession77")

            driver.save_screenshot("Registration Number Details.png")

        # Account Information

        time.sleep(2)  # Add a small delay before clicking
        if self.switch_frames("liTab2"):
            self.click_element(By.ID, "liTab2")

            # Applicable Payment Types
        if self.switch_frames("PaymentTypeId"):
            self.dropdown_option(By.ID, "PaymentTypeId", "Paid")
            self.click_element(By.ID, "btnSave-PaymentTypeConfigSession77")
            self.dropdown_option(By.ID, "PaymentTypeId", "To Pay")
            self.click_element(By.ID, "btnSave-PaymentTypeConfigSession77")
            self.dropdown_option(By.ID, "PaymentTypeId", "To Be Billed")
            self.click_element(By.ID, "btnSave-PaymentTypeConfigSession77")

            # Billing Details
        if self.switch_frames("BillingOn"):
            self.dropdown_option(By.ID, "BillingLocationTypeId", "Booking Branch")
            self.autocomplete_select(By.ID, "CollectionLocationId-select", "AHMEDABAD")
        if self.switch_frames("SubmissionLocationId-select"):
            self.autocomplete_select(
                By.ID, "SubmissionLocationId-select", "MUMBAI", timeout=10
            )
            self.send_keys(By.ID, "CreditDays", "20")
            self.send_keys(By.ID, "Party_CreditLimit", "20000")
            driver.save_screenshot("Account Information.png")

            # GST Registration

        time.sleep(2)  # Add a small delay before clicking
        if self.switch_frames("liTab5"):
            self.click_element(By.ID, "liTab5")

        if self.switch_frames("StateId"):
            self.dropdown_option(By.ID, "StateId", "MAHARASHTRA")
            self.dropdown_option(By.ID, "BusinessVerticalId", "TRANSPORTATION")
            self.send_keys(By.ID, "GSTNumber", "27ABCCK4599DSZA")
            self.click_element(By.ID, "btnSave-CustGSTRegistrationSession77")
            driver.save_screenshot("GST Registration.png")

        if self.switch_frames("mysubmit"):
            self.click_element(By.ID, "mysubmit")
            print("Customer record created successfully")
            driver.save_screenshot("Customer Record Created.png")

    @classmethod
    def tearDownClass(cls):
        """Closes the browser after tests are complete."""
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
