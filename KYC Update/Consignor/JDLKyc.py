import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
import selenium.common.exceptions as ex
from webdriver_manager.chrome import ChromeDriverManager


class KycUpdate(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
		cls.driver.maximize_window()
		cls.wait= WebDriverWait(cls.driver, 10)

	def switch_frames(self,element_id):
		self.driver.switch_to.default_content()
		iframes= self.driver.find_elements(By.TAG_NAME,"iframe")
		for iframe in iframes:
			self.driver.switch_to.frame(iframe)
			try:
				if self.driver.find_element(By.ID,element_id):
					return True
			except ex.NoSuchElementException:
				self.driver.switch_to.default_content()
		return False

	def test_master(self):
		self.driver.get("http://192.168.0.72/Rlogic9JDL/")
		self.driver.find_element(By.ID, "Login").send_keys("Riddhi")
		self.driver.find_element(By.ID, "Password").send_keys("OMSGN9")
		self.driver.find_element(By.ID, "btnLogin").click()
		print("Login successful")

		for links in ["Transportation",
            "Transportation Master »",
            "Consignor/Consignee »",
            "Consignor / Consignee",]:
			self.driver.find_element(By.LINK_TEXT, links).click()

		if self.switch_frames("tgladdnclm"):
			self.driver.find_element(By.ID, "tgladdnclm").click()
		if self.switch_frames("txt_Extrasearch"):
			print("switch_frames found")
			element=self.wait.until(EC.visibility_of_element_located((By.ID,"txt_Extrasearch")))
			element.is_enabled()
			element.send_keys("6")
			self.driver.find_element(By.ID, "btn_Seach").click()
			self.driver.find_element(By.ID, "dd 6").click()
			print("dd 6 clicked")
			self.driver.find_element(By.LINK_TEXT, "Edit").click()
			print("Edit clicked")