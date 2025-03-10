from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
import selenium.common.exceptions as ex


class CustomerMaster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize WebDriver"""
        cls.driver = webdriver.Chrome(
            service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe"),
        )
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 5)  # Reduce timeout for faster execution

    def click_element(self, by, value, max_attempts=3):
        attempt = 0
        element = None
        """Click an element with retry logic and JS fallback."""
        while attempt < max_attempts:
            try:
                element = self.wait.until(EC.element_to_be_clickable((by, value)))
                element.click()
                print(f"Successfully clicked element: {value}")
                return True
            except (ex.ElementClickInterceptedException, ex.StaleElementReferenceException, ex.TimeoutException) as e:
                print(f"Attempt {attempt + 1}: Failed to click element {value} due to {type(e).__name__}. Retrying...")
                time.sleep(1)

            # JavaScript Click Fallback
            try:
                if element:
                    self.driver.execute_script("arguments[0].click();", element)
                    print(f"Successfully clicked element using JavaScript: {value}")
                    return True
            except ex.JavascriptException as js_error:
                print(f"Attempt {attempt + 1}: JavaScript click failed due to {type(js_error).__name__}")

            attempt += 1

        print(f"Failed to click element {value} after {max_attempts} attempts.")
        return False

    def send_keys(self, by, value, text):
        """Enter text after ensuring element visibility"""
        element = self.wait.until(EC.visibility_of_element_located((by, value)))
        element.clear()
        element.send_keys(text)

    def switch_frames(self, element_id):
        """Switch to an iframe that contains a specific element"""
        self.driver.switch_to.default_content()
        for iframe in self.driver.find_elements(By.TAG_NAME, "iframe"):
            self.driver.switch_to.frame(iframe)
            try:
                if self.driver.find_element(By.ID, element_id):
                    return True
            except:
                self.driver.switch_to.default_content()
        return False

    def close_popups(self):
        try:
            close_button = self.driver.find_element(By.CLASS_NAME, "close")
            close_button.click()
            print("Closed blocking popup")
        except:
            pass

    def test_customer(self):
        driver = self.driver
        driver.get("http://r-logic9.com/RlogicDemoFtl/")

        # Login
        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "OMSGN9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful")

        # Navigate to required page
        for link_text in [
            "Transportation",
            "Transportation Master »",
            "Consignor/Consignee »",
            "Consignor / Consignee",
        ]:
            self.click_element(By.LINK_TEXT, link_text)

        # Read Excel data
        df = pd.read_excel("UID.xlsx", engine="openpyxl")

        for index, row in df.iterrows():
            try:
                print(f"Processing UID: {row['UID']}")
                self.close_popups()  # Close popups before proceeding

                if self.switch_frames("txt_Extrasearch"):
                    self.send_keys(By.ID, "txt_Extrasearch", str(row["UID"]))
                    self.click_element(By.ID, "btn_Seach")
                    #time.sleep(1)

                    self.click_element(By.ID, row["DD"])

                self.click_element(By.PARTIAL_LINK_TEXT, "Edit")

                if self.switch_frames("acaretdowndivGstEkyc"):
                    self.click_element(By.ID, "acaretdowndivGstEkyc")
                    self.click_element(By.ID, "btn_SearchGSTNo")
                    #time.sleep(1)
                    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    driver.execute_script("window.scrollTo(0, 1000);")#Scroll to bottom

                if self.switch_frames("mysubmit"):
                    self.click_element(By.ID, "mysubmit")
                    print(f"Customer UID {row['UID']} KYC Updated successfully")
                    df.at[index, "Status"] = "Passed"
                    df.at[index, "Execution Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                else:
                    print(f"Customer UID {row['UID']} KYC update failed")
                    df.at[index, "Status"] = "Failed"

            except Exception as e:
                print(f"Failed to process UID {row['UID']}: {str(e)}")
                df.at[index, "Status"] = "Failed"
                df.at[index, "Execution Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save after each entry
            df.to_excel("UID.xlsx", index=False, engine="openpyxl")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
