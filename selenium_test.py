import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class AppUITest(unittest.TestCase):
    def test_home_page(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
        try:
            url = os.getenv("APP_URL", "http://localhost:5000")
            driver.get(url)
            self.assertIn("Monitoring, Logging", driver.title)
            self.assertTrue(driver.find_element(By.ID, "dashboard").text)
        finally:
            driver.quit()

if __name__ == "__main__":
    unittest.main()
