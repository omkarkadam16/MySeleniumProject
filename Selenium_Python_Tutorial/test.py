from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import unittest


class ItemMasterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(
            service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
        )
        cls.driver.implicitly_wait(30)

    def test_item_master(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/Login")

        # Login
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "Login"))
        ).send_keys("Riddhi")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "Password"))
        ).send_keys("OMSGN9")
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "btnLogin"))
        ).click()

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Transportation"))
        ).click()

        # Navigate through menu items
        for link_text in ["Transportation Master »", "Common Masters »", "Item Master"]:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.LINK_TEXT, link_text))
            ).click()

        # Switch to correct iframe for 'New Record' button
        driver.switch_to.default_content()
        for iframe in driver.find_elements(By.TAG_NAME, "iframe"):
            driver.switch_to.frame(iframe)
            if WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.ID, "btn_NewRecord"))
            ):
                break
            driver.switch_to.default_content()

        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "btn_NewRecord"))
        ).click()

        # Switch to iframe and enter Product Name
        driver.switch_to.default_content()
        for iframe in driver.find_elements(By.TAG_NAME, "iframe"):
            driver.switch_to.frame(iframe)
            if WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.ID, "TransportProductName"))
            ):
                break
            driver.switch_to.default_content()

        WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "TransportProductName"))
        ).send_keys("Vegetables")

        # Switch to iframe and select Commodity Type
        driver.switch_to.default_content()
        for iframe in driver.find_elements(By.TAG_NAME, "iframe"):
            driver.switch_to.frame(iframe)
            if WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.ID, "CommodityTypeId"))
            ):
                break
            driver.switch_to.default_content()

        select = Select(
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "CommodityTypeId"))
            )
        )
        select.select_by_visible_text("FOOD ITEMS")

        # Submit form
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "mysubmit"))
        ).click()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
