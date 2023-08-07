# Import the require library
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# We are setting up Selenium
options = webdriver.ChromeOptions()
#  We wish to Run browser in headless mode (no GUI)
options.add_argument('--headless')
# we are setting up the driver
driver = webdriver.Chrome(options=options)

# We are opening the webpage where the report is located
report_url = "https://exmaple.com/report"
driver.get(report_url)

# We are Waiting the report to refresh(change this condition as needed)
refreshed_element_locator = (By.ID, "report-data")
wait = WebDriverWait(driver, timeout=60)
# We need to wait until...
wait.until(EC.text_to_be_present_in_element(refreshed_element_locator, "Updated Data"))

# We are check to see if the report data is updated as expected
refreshed_data = driver.find_element(*refreshed_element_locator).text
expected_data = "Updated Data"
# taking care of the if and else block
if refreshed_data == expected_data:
    print("Report refreshed properly.")
else:
    print("Report did not refresh properly.")

# We are Close the browser
driver.quit()
