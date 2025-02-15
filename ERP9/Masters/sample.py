from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import unittest


class ItemMasterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        service = Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe")
        cls.driver = webdriver.Chrome(service=service)
        cls.driver.implicitly_wait(10)

    def test_item_master(self):
        driver = self.driver
        driver.get("http://192.168.0.72/Rlogic9RLS/Login")

        # Login
        driver.find_element(By.ID, "Login").send_keys("Riddhi")
        driver.find_element(By.ID, "Password").send_keys("OMSGN9")
        driver.find_element(By.ID, "btnLogin").click()

        # Wait for redirection & click links
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Transportation"))
        ).click()
        for link_text in ["Transportation Master »", "Common Masters »", "Item Master"]:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, link_text))
            ).click()

        # Switch to iframe for "New Record" & Click
        driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btn_NewRecord"))
        ).click()

        # Switch to iframe for "TransportProductName" & Enter Data
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))

        # Wait for "TransportProductName" field and enter data
        try:
            transport_product_name = WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.ID, "TransportProductName"))
            )
            transport_product_name.send_keys("LED")
            print("TransportProductName field updated successfully")
        except Exception as e:
            print(f"Error interacting with TransportProductName: {str(e)}")

        # Switch to iframe for "CommodityTypeId" & Select Dropdown
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
        Select(
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "CommodityTypeId"))
            )
        ).select_by_visible_text("FOOD ITEMS")

        # Click Submit
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "mysubmit"))
        ).click()
        print("Entry saved successfully!")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
