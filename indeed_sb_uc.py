from seleniumbase import Driver
import pandas as pd
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_jobs():
    # Initialize the undetected Chrome driver
    driver = Driver(uc=True, headless=False)
    
    try:
        # Navigate to the page with job listings (using Indeed as example)
        print("Navigating to job search page...")
        driver.get("https://www.indeed.com/jobs?q=paralegal&l=Brooklyn%2C+NY")
        
        # Wait for page to load
        time.sleep(5)
        
        # Find all job listing elements
        print("Finding job listings...")
        job_elements = driver.find_elements(By.CSS_SELECTOR, 'li.css-1ac2h1w')
        
        print(f"Found {len(job_elements)} job listings")
        jobs_data = []
        
        for i, job_element in enumerate(job_elements):
            try:
                print(f"Processing job {i+1}/{len(job_elements)}")
                
                # Extract job title
                title_element = job_element.find_element(By.CSS_SELECTOR, 'span[id^="jobTitle"]')
                title = title_element.text if title_element else "N/A"
                
                # Extract company name
                company_element = job_element.find_element(By.CSS_SELECTOR, 'span[data-testid="company-name"]')
                company = company_element.text if company_element else "N/A"
                
                # Extract location
                location_element = job_element.find_element(By.CSS_SELECTOR, 'div[data-testid="text-location"]')
                location = location_element.text if location_element else "N/A"
                
                # Extract job snippet/description
                snippet_element = job_element.find_element(By.CSS_SELECTOR, 'div.css-1vlebyu')
                snippet = snippet_element.text if snippet_element else "N/A"
                
                # Extract job link
                link_element = job_element.find_element(By.CSS_SELECTOR, 'a.jcs-JobTitle')
                link = link_element.get_attribute('href') if link_element else "N/A"
                
                # Extract benefits if available
                benefits_elements = job_element.find_elements(By.CSS_SELECTOR, 'div.mosaic-provider-jobcards-1f1q1js')
                benefits = [benefit.text for benefit in benefits_elements] if benefits_elements else []
                
                # Store the job data
                job_data = {
                    'Title': title,
                    'Company': company,
                    'Location': location,
                    'Snippet': snippet,
                    'Link': link,
                    'Benefits': ', '.join(benefits)
                }
                
                jobs_data.append(job_data)
                
            except Exception as e:
                print(f"Error extracting data from job element {i+1}: {e}")
                continue
        
        # Create a DataFrame
        df = pd.DataFrame(jobs_data)
        
        # Export to Excel
        df.to_excel('job_listings.xlsx', index=False)
        
        # Export to CSV
        df.to_csv('job_listings.csv', index=False)
        
        # Export to JSON
        with open('job_listings.json', 'w') as f:
            json.dump(jobs_data, f, indent=4)
        
        print("Data extraction and export completed successfully!")
        print(f"Extracted {len(jobs_data)} job listings")
        
        return jobs_data

    finally:
        # Close the driver
        driver.quit()

if __name__ == "__main__":
    scrape_jobs()