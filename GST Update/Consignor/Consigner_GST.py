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
        cls.wait = WebDriverWait(cls.driver, 2)  # Reduced timeout

    # noinspection PyBroadException
    def click_element(self, by, value, retries=1):
        """Click an element with retry logic and JS fallback."""
        for attempt in range(retries):
            try:
                element = self.wait.until(EC.element_to_be_clickable((by, value)))
                element.click()
                return True
            except (ex.ElementClickInterceptedException, ex.StaleElementReferenceException, ex.TimeoutException):
                print(f"⚠️ Retrying click for {value}... ({attempt + 1}/{retries})")

        # noinspection PyBroadException
        try:
            element = self.driver.find_element(by, value)
            self.driver.execute_script("arguments[0].click();", element)
            return True
        except:
            print(f"❌ Failed click for {value}")
            return False

    def send_keys(self, by, value, text):
        """Enter text after ensuring element visibility"""
        element = self.wait.until(EC.visibility_of_element_located((by, value)))
        element.clear()
        element.send_keys(text)

    # noinspection PyBroadException
    def switch_frames(self, element_id):
        """Switch to an iframe only if necessary"""
        self.driver.switch_to.default_content()
        frames = self.driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in frames:
            self.driver.switch_to.frame(iframe)
            # noinspection PyBroadException
            try:
                if self.driver.find_element(By.ID, element_id):
                    return True
            except:
                self.driver.switch_to.default_content()
        return False

    # noinspection PyBroadException
    def close_popups(self):
        """Close popups if they exist"""
        # noinspection PyBroadException
        try:
            close_button = self.driver.find_element(By.CLASS_NAME, "close")
            close_button.click()
        except:
            pass

    def test_customer(self):
        driver = self.driver
        driver.get("http://r-logic9.com/RlogicDemoFtl/")

        # Login
        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "OMSGN9")
        self.click_element(By.ID, "btnLogin")

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

                    self.click_element(By.ID, row["DD"])

                self.click_element(By.PARTIAL_LINK_TEXT, "Edit")

                if self.switch_frames("acaretdowndivGstEkyc"):
                    self.click_element(By.ID, "acaretdowndivGstEkyc")
                    self.click_element(By.ID, "btn_SearchGSTNo")
                    driver.execute_script("window.scrollTo(0, 1000);")

                if self.switch_frames("mysubmit"):
                    self.click_element(By.ID, "mysubmit")
                    print(f"Customer UID {row['UID']} KYC Updated successfully")
                    df.at[index, "Status"] = "Passed"

            except Exception as e:
                print(f"Failed to process UID {row['UID']}: {str(e)}")
                df.at[index, "Status"] = "Failed"

            df.to_excel("UID.xlsx", index=False, engine="openpyxl")  # Save only once at the end

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
