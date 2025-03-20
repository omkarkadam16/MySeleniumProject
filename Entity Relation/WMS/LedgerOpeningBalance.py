import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import unittest
import time
from selenium.common import exceptions as ex
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class EntityRelation(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
		cls.driver.maximize_window()
		cls.wait= WebDriverWait(cls.driver, 10)

	def send_keys(self, by, value, text):
		"""Send text to an input field when it becomes visible."""
		element = self.wait.until(EC.visibility_of_element_located((by, value)))
		if element.is_enabled():
			element.clear()
			element.send_keys(text)
		else:
			raise Exception(f"Element located by ({by}, {value}) is not enabled.")

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

	def click_element(self, by, value, retries=2):
		"""Click an element, retrying if necessary."""
		for attempt in range(retries):
			try:
				element = self.wait.until(EC.element_to_be_clickable((by, value)))
				element.click()
				return True
			except (ex.ElementClickInterceptedException, ex.StaleElementReferenceException, ex.TimeoutException):
				print(f"[WARNING] Attempt {attempt + 1} failed, retrying...")
		try:
			element = self.driver.find_element(by, value)
			self.driver.execute_script("arguments[0].click();", element)
			return True
		except:
			return False

	def test_master(self):
		self.driver.get("http://103.30.74.232/WMSBLR/")
		self.driver.find_element(By.ID, "Login").send_keys("admin")
		self.driver.find_element(By.ID, "Password").send_keys("admin99")
		self.driver.find_element(By.ID, "btnLogin").click()
		print("Login successful")

		for links in ["Administration",
					  "Implementation »",
					  "Entity Relation",]:
			self.driver.find_element(By.LINK_TEXT, links).click()

		if self.switch_frames("LinkId-select"):
			element = self.driver.find_element(By.ID, "LinkId-select")
			element.send_keys("Ledger Opening Balance")
			element.send_keys(Keys.TAB)
			print("Ledger Opening Balance selected")

			df = pd.read_excel("JV(Cash & Bank).xlsx", engine="openpyxl")

			for index, row in df.iterrows():
				try:
					print(f"Processing AsmQualifiedName: {row['AsmQualifiedName']}")

					self.send_keys(By.ID, "AsmQualifiedName", row['AsmQualifiedName'])
					self.send_keys(By.ID, "EntityCode", row['Entity Code'])
					self.send_keys(By.ID, "EntityName", row['Entity Name'])
					self.send_keys(By.ID, "ParentEntityCode", row['Parent Entity Code'])
					self.send_keys(By.ID, "PrimaryGroupColumns", row['Primary Group Column'])
					self.send_keys(By.ID, "PropertyName", row['Property Name'])
					if self.click_element(By.ID, "btnSave-ImportEntityColumnSessionName782"):
						df.at[index, "Status"] = "Passed"
					else:
						df.at[index, "Status"] = "Failed"

				except Exception as e:
					print(f"Failed to process AsmQualifiedName {row['AsmQualifiedName']}: {str(e)}")

				df.to_excel("JV(Cash & Bank).xlsx", index=False, engine="openpyxl")
				print("✅ KJV(Cash & Bank) Completed! Check JV(Cash & Bank).xlsx for results.")

