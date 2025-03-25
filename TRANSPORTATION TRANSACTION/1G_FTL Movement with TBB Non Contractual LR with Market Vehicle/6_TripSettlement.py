from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
import selenium.common.exceptions as ex
from webdriver_manager.chrome import ChromeDriverManager


class TripSettlement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait=WebDriverWait(cls.driver,15)

    def click_element(self,by,value,retry=2):
        for i in range(retry):
            try:
                self.wait.until(EC.element_to_be_clickable((by,value))).click()
                print("Clicked on element",value)
                return True
            except(ex.ElementClickInterceptedException,ex.StaleElementReferenceException,ex.TimeoutException):
                print("Element not clickable. Retrying...")
                time.sleep(1)
        try:
            element=self.driver.find_element(by,value)
            self.driver.execute_script("arguments[0].click();",element)
            print("Clicked on element",value)
            return True
        except ex.NoSuchElementException:
            print("Element not found. Unable to click.")
            return False

    def send_keys(self,by,value,text):
        try:
            element=self.wait.until(EC.visibility_of_element_located((by,value)))
            element.is_enabled()
            element.clear()
            element.send_keys(text)
            print("Sent keys",text,"to element",value)
            return True
        except ex.NoSuchElementException:
            print("Element not found. Unable to send keys.")
            return False

    def switch_frames(self,element_id):
        driver=self.driver
        driver.switch_to.default_content()
        i=driver.find_elements(By.TAG_NAME,"iframe")
        for iframe in i:
            driver.switch_to.frame(iframe)
            try:
                if driver.find_element(By.ID,element_id):
                    return True
            except ex.NoSuchElementException:
                driver.switch_to.default_content()
        return False

    def dropdown(self,by,value,text):
        try:
            E=self.wait.until(EC.element_to_be_clickable((by,value)))
            E.click()
            print("Clicked dropdown")
            element=Select(self.wait.until(EC.visibility_of_element_located((by,value))))
            element.select_by_visible_text(text)
            print("Selected dropdown option:",text)
            return True
        except (ex.NoSuchElementException,ex.ElementClickInterceptedException,ex.TimeoutException):
            return False

    def autocomplete(self,by,value,text):
        ip=self.wait.until(EC.visibility_of_element_located((by,value)))
        ip.clear()
        ip.send_keys(text)
        time.sleep(1)

        suggest = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-menu-item")))
        for i in suggest:
            if text.upper() in i.text.upper():
                i.click()
                return
        ip.send_keys(Keys.DOWN)
        ip.send_keys(Keys.ENTER)
        print("Selected autocomplete using Keyboard option:",text)

    def test_trip(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/")

        print("Logging in...")
        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")

        for i in ("Transportation",
                  "Transportation Transaction »",
                  "Trip Management »",
                  "Trip Settlement",):
            self.click_element(By.LINK_TEXT, i)
            print(f"Navigated to {i}.")

        if self.switch_frames("btn_NewRecord"):
            self.click_element(By.ID, "btn_NewRecord")

            # Document Details
            if self.switch_frames("OrganizationId"):
                self.dropdown(By.ID, "OrganizationId", "AHMEDABAD")
                # Calendor
                self.click_element(By.CLASS_NAME, "ui-datepicker-trigger")
                self.dropdown(By.CLASS_NAME, "ui-datepicker-month", "Jun")
                self.dropdown(By.CLASS_NAME, "ui-datepicker-year", "2024")
                self.click_element(By.XPATH, "//a[text()='1']")

            #General
            self.autocomplete(By.ID,"VehicleId-select","MHO4ER9009")
            self.dropdown(By.ID, "VehicleTripId", "AHM-000107-LHC")

            #Balance / Payment Slip Details
            self.autocomplete(By.ID,"OrganizationalLocationId-select","AHMEDABAD")
            self.send_keys(By.ID, "AdvanceAmount", "5000")
            self.click_element(By.ID, "btnSave-VehicleTripAdvanceVehicleTripSessionName658")

            #Submit Trip
            self.click_element(By.ID, "mysubmit")
            print("Trip submitted successfully.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()