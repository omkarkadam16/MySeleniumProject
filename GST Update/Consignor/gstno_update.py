import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
import selenium.common.exceptions as ex
from selenium_helper import SeleniumHelper


class CustomerMaster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize WebDriver"""
        cls.driver = webdriver.Chrome(
            service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe"),
        )
        cls.driver.maximize_window()
        cls.Helper = SeleniumHelper(cls.driver)


    def test_customer(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9UataScript/Login")


        # Login
        self.Helper.send_keys(By.ID, "Login", "admin")
        self.Helper.send_keys(By.ID, "Password", "omsgn9")
        self.Helper.click_element(By.ID, "btnLogin")
        print("Login successful")

        # Navigate to required page
        for link_text in [
            "Transportation",
            "Transportation Master »",
            "Consignor/Consignee »",
            "Consignor / Consignee",
        ]:
            self.Helper.click_element(By.LINK_TEXT, link_text)

        # Read Excel data
        df = pd.read_excel("UID.xlsx", engine="openpyxl")

        for index, row in df.iterrows():
            try:
                print(f"Processing UID: {row['UID']}")
                #self.close_popups()  # Close popups before proceeding

                if self.Helper.switch_frames("txt_Extrasearch"):
                    self.Helper.send_keys(By.ID, "txt_Extrasearch", str(row["UID"]))
                    self.Helper.click_element(By.ID, "btn_Seach")
                    #time.sleep(1)

                    self.Helper.click_element(By.ID, row["DD"])

                self.click_element(By.PARTIAL_LINK_TEXT, "Edit")


                if self.switch_frames("mysubmit"):
                    self.click_element(By.ID, "mysubmit")
                    print(f"Customer UID {row['UID']} KYC Updated successfully")
                    df.at[index, "Status"] = "Passed"

            except Exception as e:
                print(f"Failed to process UID {row['UID']}: {str(e)}")
                df.at[index, "Status"] = "Failed"

        # Save after each entry
            df.to_excel("UID.xlsx", index=False, engine="openpyxl")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
