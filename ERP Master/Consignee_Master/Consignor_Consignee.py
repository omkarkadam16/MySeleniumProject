from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time

class TestMaster(unittest.TestCase):
	@classmethod
	def setupClass(cls):
		cls.driver=webdriver.Chrome(service=Service(r"C:\Users\user\Downloads\WebDrivers\chromedriver.exe"))
		cls.wait=WebDriverWait(cls.driver,5)
		cls.driver.maximize_window()

	def test_consignor_consignee(self):
		driver=self.driver
		driver.get("http://r-logic9.com/RlogicDemoFtl/")