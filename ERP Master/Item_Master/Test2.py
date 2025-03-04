from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest


class LoginPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(
            service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
        )
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    def test_Commodity_Master(self):
        driver = self.driver
        driver.get("http://r-logic9.com/RlogicDemoFtl/Login")

    @classmethod
    def tearDownClass(cls):
        """Closes the browser after tests are complete."""
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
