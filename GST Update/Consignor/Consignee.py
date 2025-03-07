import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
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
        cls.driver.implicitly_wait(5)
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
        driver.get("http://r-logic9.com/RlogicDemoFtl/")

        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "OMSGN9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful")

        menus = [
            "Transportation",
            "Transportation Master »",
            "Consignor/Consignee »",
            "Consignor / Consignee",
        ]

        for link_test in menus:
            self.click_element(By.LINK_TEXT, link_test)
            print(f"{link_test} link clicked successfully")

        df = pd.read_excel("UID.xlsx")
        for _, row in df.iterrows():

            if self.switch_frames("txt_Extrasearch"):
                self.send_keys(By.ID, "txt_Extrasearch",str(row["UID"]))
                self.click_element(By.ID, "btn_Seach")
                time.sleep(2)
                driver.save_screenshot("Search Results.png")

                self.click_element(By.ID,(row["DD"]))
            edit_button = driver.find_element(By.PARTIAL_LINK_TEXT, "Edit")
            edit_button.click()

            if self.switch_frames("acaretdowndivGstEkyc"):
                self.click_element(By.ID, "acaretdowndivGstEkyc")
                self.click_element(By.ID, "btn_SearchGSTNo")

            if self.switch_frames("mysubmit"):
                self.click_element(By.ID, "mysubmit")
                print("Customer record created successfully")
                time.sleep(2)
                driver.save_screenshot("Customer Record Created.png")


    @classmethod
    def tearDownClass(cls):
        """Closes the browser after tests are complete."""
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
