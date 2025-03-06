from applitools.selenium import Eyes
from selenium import webdriver  # ✅ Correct import

# Initialize Applitools Eyes
eyes = Eyes()
eyes.api_key = "YOUR_API_KEY"

# Start WebDriver
driver = webdriver.Chrome()  # ✅ Correct usage

# Open Applitools session
eyes.open(driver, "Demo App", "Test Case 1")

# Navigate to your application
driver.get("http://192.168.0.72/Rlogic9RLS/Login")

# Capture and check the visual state
eyes.check_window("Homepage")

# Close the Applitools Eyes session
eyes.close()

# Quit the WebDriver
driver.quit()  # ✅ Always close WebDriver
