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


class AdvancePay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait=WebDriverWait(cls.driver,15)

    def click_element(self,by,value,retry=2):
        driver=self.driver
        for i in range(retry):
            try:
                self.wait.until(EC.element_to_be_clickable((by,value))).click()
                print(f"[SUCCESS] Clicked element: {value}")
                return True
            except (ex.ElementClickInterceptedException,ex.StaleElementReferenceException,ex.TimeoutException):
                print(f"[WARNING] Attempt {i + 1} failed, retrying...")
                time.sleep(1)
        try:
            element= driver.find_element(by,value)
            driver.execute_script("arguments[0].click();",element)
            print(f"[SUCCESS] Clicked element: {value}")
            return True
        except ex.NoSuchElementException:
            print(f"[ERROR] Element not found: {value}")
            return False

    def send_keys(self,by,value,text):
        try:
            element=self.wait.until(EC.visibility_of_element_located((by,value)))
            element.is_enabled()
            element.clear()
            element.send_keys(text)
            print(f"[SUCCESS] Sent keys: {text}")
            return True
        except ex.NoSuchElementException:
            print(f"[ERROR] Element not found: {value}")
            return False

    def switch_frames(self, element_id):
        driver=self.driver
        driver.switch_to.default_content()
        iframe=driver.find_elements(By.TAG_NAME, "iframe")
        for i in iframe:
            driver.switch_to.frame(i)
            try:
                if driver.find_element(By.ID, element_id):
                    return True
            except ex.NoSuchElementException:
                driver.switch_to.default_content()
        return False

    def dropdown_select(self,by,value,text):
        try:
            e=self.wait.until(EC.element_to_be_clickable((by,value)))
            e.is_enabled()
            e.click()
            print("[SUCCESS] Clicked dropdown")
            self.wait.until(EC.visibility_of_element_located((by,value)))
            element=Select(self.driver.find_element(by,value))
            element.select_by_visible_text(text)
            print(f"[SUCCESS] Selected dropdown option: {text}")
            return True
        except (ex.NoSuchElementException, ex.ElementClickInterceptedException, ex.TimeoutException):
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
                print(f"[SUCCESS] Selected autocomplete suggestion: {text}")
                return True
        ip.send_keys(Keys.DOWN)
        ip.send_keys(Keys.ENTER)
        print("Selected autocomplete option using keyboard:", text)

    def test_DirectDoorDelivery(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/")

        print("Logging in...")
        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")

        for i in ("Transportation",
                  "Transportation Transaction »",
                  "Delivery »",
                  "Direct Door Delivery (POD)",):
            self.click_element(By.LINK_TEXT, i)
            print(f"Navigated to {i}.")

        if self.switch_frames("btn_NewRecord"):
            self.click_element(By.ID, "btn_NewRecord")

        # Document Info
        if self.switch_frames("OrganizationId"):
            self.dropdown_select(By.ID, "OrganizationId", "PUNE")
            # Calendor
            self.click_element(By.CLASS_NAME, "ui-datepicker-trigger")
            self.dropdown_select(By.CLASS_NAME, "ui-datepicker-month", "Jun")
            self.dropdown_select(By.CLASS_NAME, "ui-datepicker-year", "2024")
            self.click_element(By.XPATH, "//a[text()='1']")

        # Booking Detail
        self.autocomplete(By.ID,"VehicleId-select","MHO4ER9009")
        self.dropdown_select(By.ID,"VehicleTripId","AHM-000107-LHC")
        time.sleep(2)
        driver.save_screenshot("Delivery.png")

        # Arrival Detail
        self.click_element(By.XPATH, "(//img[@title='...'])[6]")
        self.dropdown_select(By.XPATH, "(//select[@class='ui-datepicker-month'])[1]", "Jun")
        self.dropdown_select(By.XPATH, "(//select[@class='ui-datepicker-year'])[1]", "2024")
        self.click_element(By.XPATH, "(//a[normalize-space()='1'])[1]")
        self.dropdown_select(By.ID,"ReasonDelayId","TRAFFIC JAAM")

        #Submit form
        self.click_element(By.ID, "mysubmit")
        print("Form submitted successfully.")


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()