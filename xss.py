import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO)

# Step 1: Crawling the Website using Selenium
def crawl_website(url):
    try:
        driver = webdriver.Chrome()  # Use appropriate webdriver based on your browser
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "input")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        input_fields = [field.get('name') for field in soup.find_all('input', {'type': 'text'})]
        input_fields += [field.get('name') for field in soup.find_all('textarea')]
        logging.debug("Extracted input fields: %s", input_fields)
        return input_fields
    except Exception as e:
        logging.error("An error occurred while crawling the website: %s", e)
        return None
    finally:
        if driver:
            driver.quit()

# Step 2: Identify Vulnerable Input Fields
def identify_vulnerable_fields(url, input_fields):
    vulnerable_fields = []
    if input_fields:
        for field in input_fields:
            if test_field_vulnerability(url, field):
                vulnerable_fields.append(field)
    return vulnerable_fields

# Function to test vulnerability of a field
def test_field_vulnerability(url, field):
    payload = "<script>alert('XSS')</script>"
    try:
        driver = webdriver.Chrome()  # Use appropriate webdriver based on your browser
        driver.get(url)
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, field)))
        element.send_keys(payload)
        element.submit()
        # Handle unexpected alerts
        try:
            WebDriverWait(driver, 2).until(EC.alert_is_present(), 'Timed out waiting for alert to appear')
            alert = driver.switch_to.alert
            alert.dismiss()
        except:
            pass
        # Check if the payload is present in the page source
        if payload in driver.page_source:
            return True
    except Exception as e:
        logging.error("An error occurred while testing field %s: %s", field, e)
    finally:
        if driver:
            driver.quit()
    return False

# Step 3: Main Function
def main(url):
    start_time = time.time()
    # Step 1: Crawl the website
    input_fields = crawl_website(url)
    if not input_fields:
        logging.error("Failed to crawl the website. Exiting.")
        return
    # Step 2: Identify vulnerable input fields
    vulnerable_fields = identify_vulnerable_fields(url, input_fields)
    if not vulnerable_fields:
        logging.info("No vulnerable fields found.")
        return
    logging.info("Vulnerable Fields:")
    logging.info("\t%s", "\n\t".join(vulnerable_fields))
    logging.info("Total execution time: %.2f seconds", time.time() - start_time)

# Example usage
if __name__ == "__main__":
    website_url = input("Enter the URL of the website to scan for XSS vulnerabilities: ")
    main(website_url)

