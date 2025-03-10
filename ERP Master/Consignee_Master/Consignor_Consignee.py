from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import unittest
from selenium_helper import SeleniumHelper

class ConsigneeMaster(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver=webdriver.Chrome(service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe"))
        cls.wait=WebDriverWait(cls.driver,5)
        cls.driver.maximize_window()
        cls.helper=SeleniumHelper(cls.driver)



    def test_consignor_consignee(self):
        driver=self.driver
        driver.get("http://192.168.0.72/Rlogic9UataScript/Login")
        self.helper.send_keys(By.ID, "Login", "Riddhi")
        self.helper.send_keys(By.ID, "Password", "OMSGN9")
        self.helper.click_element(By.ID, "btnLogin")
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()