from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json
import time
import os

### Task 1-4: 

if not os.path.exists('assignment9'):
    os.makedirs('assignment9')

options = webdriver.ChromeOptions()
options.add_argument('--headless')  
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"
    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "li.cp-search-result-item"))
    )

    time.sleep(2)
    results_list = driver.find_elements(By.CSS_SELECTOR, "li.cp-search-result-item")

    print(f"Found {len(results_list)} book items")  # Debug info

    books = []
    for item in results_list:
        try:
            title = item.find_element(By.CSS_SELECTOR, "h2.cp-title span.title-content").text.strip()

            authors = []
            author_elements = item.find_elements(By.CSS_SELECTOR, "span.cp-author-link a")
            for author in author_elements:
                authors.append(author.text.strip())
            author_text = "; ".join(authors) if authors else "Unknown"
            format_year = "Unknown"
            try:
                format_year = item.find_element(
                    By.CSS_SELECTOR, "div.cp-format-info span.display-info-primary"
                ).text.strip()
            except:
                pass

            books.append({
                "Title": title,
                "Author": author_text,
                "Format-Year": format_year,
            })

        except Exception as e:
            print(f"Skipped one entry due to error: {str(e)}")
            continue

    if books:
        df = pd.DataFrame(books)
        
        print("\nFound books:")
        print(df.to_string(index=False))
        
        csv_path = os.path.join('assignment9', 'get_books.csv')
        df.to_csv(csv_path, index=False)
        print(f"\nResults saved to {csv_path}")
        
        json_path = os.path.join('assignment9', 'get_books.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
        print(f"Results saved to {json_path}")
        
        print("\nSample of CSV file:")
        print(pd.read_csv(csv_path).head().to_string(index=False))
        
        print("\nSample of JSON file:")
        with open(json_path, 'r', encoding='utf-8') as f:
            sample_data = json.load(f)[:2] 
            print(json.dumps(sample_data, indent=2))
    else:
        print("No books found matching the criteria")

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    driver.quit()

