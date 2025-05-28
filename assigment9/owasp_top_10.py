from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Set up the Selenium driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode (no browser UI)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the OWASP Top Ten page
url = "https://owasp.org/www-project-top-ten/"
driver.get(url)

# Let the page load completely
time.sleep(3)

# Find all the Top 10 items (titles and links)
top_10_data = []
for i in range(1, 11):
    try:
        xpath = f"(//a[contains(@href, 'A0{i}') or contains(@href, 'A1{i-1}')])[1]"
        element = driver.find_element(By.XPATH, xpath)
        title = element.text.strip()
        link = element.get_attribute('href')
        top_10_data.append({"title": title, "link": link})
    except Exception as e:
        print(f"Failed to extract item {i}: {e}")

# Close the browser
driver.quit()

# Print data to verify
for item in top_10_data:
    print(item)

# Save to CSV
df = pd.DataFrame(top_10_data)
df.to_csv("owasp_top_10.csv", index=False)
