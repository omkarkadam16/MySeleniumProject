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

class LHC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait=WebDriverWait(cls.driver, 10)

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
            return True
        except:
            return False

    def send_keys(self,by,value,text):
        element=self.driver.find_element(by,value)
        element.clear()
        element.send_keys(text)
        print("Sent keys:",text)

    def switch_frames(self, element_id):
        driver = self.driver
        driver.switch_to.default_content()
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            driver.switch_to.frame(iframe)
            try:
                if driver.find_element(By.ID, element_id):
                    return True
            except ex.NoSuchElementException:
                driver.switch_to.default_content()
        return False

    def select_dropdown(self,by,value,text):
        try:
            self.wait.until(EC.element_to_be_clickable((by,value)))
            self.wait.until(EC.visibility_of_element_located((by,value)))
            dropdown=Select(self.driver.find_element(by, value))
            dropdown.select_by_visible_text(text)
            return True
        except ex.NoSuchElementException:
            return False

    def auto_select(self,by,value,text):
        element=self.wait.until(EC.visibility_of_element_located((by,value)))
        element.clear()
        element.send_keys(text)
        time.sleep(2)
        suggest = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-menu-item")))
        for i in suggest:
            if text.upper() in i.text.upper():
                i.click()
                time.sleep(1)
                print("Selected autocomplete option:", text)
                return
        element.send_keys(Keys.DOWN)
        element.send_keys(Keys.ENTER)

    def test_LHC(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/")

        print("Logging in...")
        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "omsgn9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful.")

        for i in ("Transportation",
                  "Transportation Transaction »",
                  "Outward »",
                  "Lorry Hire Challan",):
            self.click_element(By.LINK_TEXT, i)
            print(f"Navigated to {i}.")

        if self.switch_frames("btn_NewRecord"):
            self.click_element(By.ID, "btn_NewRecord")

        # Document Details
        if self.switch_frames("OrganizationId"):
            self.select_dropdown(By.ID, "OrganizationId", "AHMEDABAD")
            self.select_dropdown(By.ID,"SeriesId","AHM - 101 To 500 - LHC")
            # Calendar
            self.click_element(By.CLASS_NAME, "ui-datepicker-trigger")
            self.select_dropdown(By.CLASS_NAME, "ui-datepicker-month", "Jun")
            self.select_dropdown(By.CLASS_NAME, "ui-datepicker-year", "2024")
            self.click_element(By.XPATH, "//a[text()='1']")
            time.sleep(1)

        #General Details
        self.click_element(By.ID,"btn_modify")
        time.sleep(1)
        self.send_keys(By.ID, "SearchValue", "AHM-000007-MEMO")
        self.click_element(By.ID, "btn-searchcriteria")
        self.auto_select(By.ID, "VehicleId-select","MHO4ER9009")
        time.sleep(1)

        #Hire Details
        self.select_dropdown(By.ID, "PurchaseBookedOnId","Owner")
        self.send_keys(By.ID, "DriverName", "Shailesh Gothal")
        self.send_keys(By.ID, "LicenseExpDate","31-12-2025")
        self.auto_select(By.ID, "BalanceLocationId-select","Pune")
        self.send_keys(By.ID, "LicenseNo", "98765")
        self.send_keys(By.ID, "ContactNo", "9863575754")
        #Booking movement
        self.click_element(By.ID, "IsSelectMemoSearchSessionName6611")

        #Hire Charges Details
        self.select_dropdown(By.ID, "FreightUnitId","Fixed")
        self.send_keys(By.ID, "FreightRate","15000")
        time.sleep(1)

        #Advance Payable Details
        self.auto_select(By.ID, "OrganizationalLocationId-select","AHMEDABAD")
        self.send_keys(By.ID, "AdvanceAmount","10000")
        self.click_element(By.ID, "btnSave-VehicleTripAdvanceVehicleTripSessionName661")
        time.sleep(1)

        #Submit Details
        self.click_element(By.ID, "mysubmit")
        time.sleep(1)




