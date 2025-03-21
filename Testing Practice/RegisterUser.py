from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
import selenium.common.exceptions as ex
from webdriver_manager.chrome import ChromeDriverManager

class RegisterUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()
        cls.wait=WebDriverWait(cls.driver,5)

    def click_element(self,by,value,retry=2):
        for attempt in range(retry):
            try:
                self.wait.until(EC.element_to_be_clickable((by,value))).click()
                return True
            except (ex.ElementClickInterceptedException,ex.StaleElementReferenceException,ex.TimeoutException):
                print(f"[WARNING] Attempt {attempt + 1} failed, retrying...")

        try:
            element=self.driver.find_element(by,value)
            self.driver.execute_script("arguments[0].click();",element)
            return True
        except:
            return False

    def send_keys(self,by,value,text):
        element=self.wait.until(EC.visibility_of_element_located((by,value)))
        element.clear()
        element.send_keys(text)

    def switch_frames(self,element_id):
        driver=self.driver
        driver.switch_to.default_content()
        iframes=driver.find_elements(By.TAG_NAME,"iframe")
        for iframe in iframes:
            driver.switch_to.frame(iframe)
            try:
                if driver.find_element(By.ID,element_id):
                    return True

            except ex.NoSuchElementException:
                driver.switch_to.default_content()
        return False

    def checkbox(self, checkbox_id):
        """Selects a checkbox if not already selected and verifies it."""
        checkbox = self.driver.find_element(By.ID, checkbox_id)
        if not checkbox.is_selected():
            checkbox.click()
            print(f"Selected checkbox: {checkbox_id}")

    def select_dropdown(self, by, value, option_text):
        self.wait.until(EC.visibility_of_element_located((by,value)))
        dropdown=Select(self.driver.find_element(by,value))
        dropdown.select_by_visible_text(option_text)
        print(f"Selected dropdown option: {option_text}")


    def test_register_user(self):
        driver=self.driver
        driver.get("https://testautomationpractice.blogspot.com/")
        print("Navigated to Automation Exercise")

        self.send_keys(By.ID,"name","Omkar Kadam")
        print("Entered name")

        self.send_keys(By.ID,"email","omkarkadam058@gmail.com")
        print("Entered email")

        self.send_keys(By.ID,"phone","9284326684")
        print("Entered phone number")

        self.send_keys(By.ID,"textarea","Post, Turbhe, Tal - Poladpur, Dist- Raigad")
        print("Entered address")

        self.click_element(By.ID,"male")
        print("Selected gender")

        for days in ["monday","tuesday","thursday","friday","saturday"]:
            self.checkbox(days)
            print(f"Selected {days}")

        self.select_dropdown(By.ID,"country","India")
        self.select_dropdown(By.ID,"colors","Blue")
        self.select_dropdown(By.ID,"animals","Dog")
        self.send_keys(By.ID,"datepicker","01/01/2023")
        print("Selected date")

        self.click_element(By.ID,"txtDate")
        years = Select(self.driver.find_element(By.CLASS_NAME, "ui-datepicker-year"))
        years.select_by_visible_text("2020")
        months=Select(self.driver.find_element(By.CLASS_NAME,"ui-datepicker-month"))
        months.select_by_visible_text("Oct")
        self.click_element(By.XPATH,"/html/body/div[5]/table/tbody/tr[3]/td[6]/a")
        print("Selected date")



        time.sleep(1)
        self.driver.save_screenshot("Registration Form.png")





