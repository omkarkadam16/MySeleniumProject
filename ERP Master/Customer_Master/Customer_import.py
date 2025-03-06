import pandas as pd
from selenium import webdriver
from selenium.webdriver import Keys
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
        CE = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
        CE.clear()
        CE.send_keys(text)
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
        input_field.clear()
        input_field.send_keys(text)  # Step 1: Enter text

        time.sleep(3)  # Increase time for dropdown to load

        # Wait until at least one suggestion appears
        suggestions = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-menu-item"))
        )

        for suggestion in suggestions:
            print(f"Suggestion found: {suggestion.text}")  # Debugging
            if text.upper() in suggestion.text.upper():
                suggestion.click()
                print(f"Selected {text} from autocomplete")
                return

        # If no exact match, try arrow key + Enter
        input_field.send_keys(Keys.DOWN)
        input_field.send_keys(Keys.ENTER)
        print(f"{value} updated with {text} using keyboard")

    def switch_frames(self, element_id):
        """Switches to the correct iframe containing the desired element."""
        driver = self.driver
        driver.switch_to.default_content()

        for iframe in driver.find_elements(By.TAG_NAME, "iframe"):
            driver.switch_to.frame(iframe)

            try:
                if driver.find_element(By.ID, element_id):
                    print(f"Switched to iframe containing {element_id}")
                    return True
            except:
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

        df = pd.read_excel("customer_data.xlsx")
        for _, row in df.iterrows():

            # Basic Information
            if self.switch_frames("Party_PartyName"):
                self.send_keys(By.ID, "Party_PartyName", row["PartyName"])

                self.dropdown_option(
                    By.ID, "Party_PartyCategoryId", row["PartyCategory"]
                )

                self.dropdown_option(
                    By.ID, "Party_PartyIndustryTypeId", row["PartyIndustryType"]
                )

                self.dropdown_option(By.ID, "Party_PartyGradeId", row["PartyGrade"])

                self.dropdown_option(By.ID, "Party_PartyGroupId", row["PartyGroup"])
            if self.switch_frames("EffectiveFromDate"):
                self.send_keys(By.ID, "EffectiveFromDate", row["EffectiveFromDate"])

                self.send_keys(By.ID, "PANNo", row["PANNo"])

                driver.save_screenshot("Basic Details.png")

            # Address Details
            if self.switch_frames("AddressTypeId"):
                self.dropdown_option(By.ID, "AddressTypeId", row["AddressType"])
                self.send_keys(By.ID, "AddressLine", row["AddressLine"])
                self.autocomplete_select(By.ID, "CityId-select", row["City"])
                self.send_keys(By.ID, "PinCode", str(row["PinCode"]))
                self.send_keys(By.ID, "ContactNo", str(row["ContactNo"]))
                self.send_keys(By.ID, "Mob", str(row["Mob"]))
                self.click_element(By.ID, "btnSave-AddressSession77")

                driver.save_screenshot("Address Details.png")

            # Registation Number Details

            if self.switch_frames("RegistrationHeadId"):
                self.dropdown_option(
                    By.ID, "RegistrationHeadId", row["RegistrationHead"]
                )

                self.send_keys(By.ID, "Number", str(row["RegistrationNumber"]))

                self.click_element(By.ID, "btnSave-RegistrationSession77")

                driver.save_screenshot("Registration Number Details.png")

            # Account Information
            driver.execute_script(
                "window.scrollTo(0, 0);"
            )  # Scroll up before switching to "liTab2"
            time.sleep(3)  # Add a small delay before clicking
            if self.switch_frames("liTab2"):
                self.click_element(By.ID, "liTab2")

            # Payment Types (No Loop, Three Columns)
            if self.switch_frames("PaymentTypeId"):
                self.dropdown_option(By.ID, "PaymentTypeId", row["PaymentType1"])
                self.click_element(By.ID, "btnSave-PaymentTypeConfigSession77")
                time.sleep(2)

                self.dropdown_option(By.ID, "PaymentTypeId", row["PaymentType2"])
                self.click_element(By.ID, "btnSave-PaymentTypeConfigSession77")
                time.sleep(2)

                self.dropdown_option(By.ID, "PaymentTypeId", row["PaymentType3"])
                self.click_element(By.ID, "btnSave-PaymentTypeConfigSession77")

            # Billing Details
            if self.switch_frames("BillingOn"):
                self.dropdown_option(By.ID, "BillingOn", "Booking")
                self.dropdown_option(By.ID, "BillingLocationTypeId", "Booking Branch")
                self.autocomplete_select(
                    By.ID, "CollectionLocationId-select", "AHMEDABAD"
                )
            if self.switch_frames("SubmissionLocationId-select"):
                self.autocomplete_select(By.ID, "SubmissionLocationId-select", "MUMBAI")
                self.send_keys(By.ID, "CreditDays", "20")
                self.send_keys(By.ID, "Party_CreditLimit", "20000")
                driver.save_screenshot("Account Information.png")

            # GST Registration
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)  # Add a small delay before clicking
            if self.switch_frames("liTab5"):
                self.click_element(By.ID, "liTab5")

            if self.switch_frames("StateId"):
                self.dropdown_option(By.ID, "StateId", row["State"])
                self.dropdown_option(
                    By.ID, "BusinessVerticalId", row["BusinessVertical"]
                )
                self.send_keys(By.ID, "GSTNumber", str(row["GSTNumber"]))
                self.click_element(By.ID, "btnSave-CustGSTRegistrationSession77")
                driver.save_screenshot("GST Registration.png")

            # Submit Form
            if self.switch_frames("mysubmitNew"):
                self.click_element(By.ID, "mysubmitNew")
                print(f"Customer {row['PartyName']} record created successfully")
                time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        """Closes the browser after tests are complete."""
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
