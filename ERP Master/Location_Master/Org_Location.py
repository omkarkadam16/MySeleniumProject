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

class LocationMaster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver=webdriver.Chrome(service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe"))
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(3)

    def click_element(self,by,value,timeout=2):
        WebDriverWait(self.driver,timeout).until(EC.element_to_be_clickable((by,value))).click()

    def send_keys(self,by,value,text,timeout=2):
        AB=WebDriverWait(self.driver,timeout).until(EC.visibility_of_element_located((by,value)))
        AB.clear()
        AB.send_keys(text)

    def dropdown(self,by,value,option_text,timeout=2):
        WebDriverWait(self.driver,timeout).until(EC.visibility_of_element_located((by,value)))
        Drops=Select(self.driver.find_element(by,value))
        Drops.select_by_visible_text(option_text)

    def autocomplete(self,by,value,text,timeout=2):
        AC=WebDriverWait(self.driver,timeout).until(EC.visibility_of_element_located((by,value)))
        AC.clear()
        AC.send_keys(text)
        time.sleep(2)

        suggestions= WebDriverWait(self.driver,timeout).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"ui-menu-item")))
        for suggestion in suggestions:
            if text.lower() in suggestion.text.lower():
                suggestion.click()
                return
        AC.send_keys(Keys.DOWN)
        AC.send_keys(Keys.ENTER)

    def switch_frames(self,element_id):
        driver=self.driver
        driver.switch_to.default_content()
        for iframe in driver.find_elements(By.TAG_NAME,"iframe"):
            driver.switch_to.frame(iframe)
            try:
                if driver.find_element(By.ID,element_id):
                    return True
            except:
                driver.switch_to.default_content()
        return False

    def test_location(self):
        driver=self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/Login")

        self.send_keys(By.ID, "Login", "Riddhi")
        self.send_keys(By.ID, "Password", "OMSGN9")
        self.click_element(By.ID, "btnLogin")
        print("Login successful")

        menus = [
            "Common",
            "Organisational Hierarchy »",
            "Organisation Location",
        ]

        for link_test in menus:
            self.click_element(By.LINK_TEXT, link_test)

        if self.switch_frames("btn_NewRecord"):
            self.click_element(By.ID, "btn_NewRecord")

        if self.switch_frames("Code"):
            self.send_keys(By.ID, "Code", "TUR")
