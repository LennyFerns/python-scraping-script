from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
import csv

# Set up the Selenium WebDriver (adjust path if necessary)
driver_path = "/Users/lennoxfernandes/Desktop/New Folder With Items/Python scrape logo/chromedriver-mac-arm64/chromedriver"  # Replace with your ChromeDriver path
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Open the webpage
url = "https://augmentedenterprisesummit.com/speakers/"
driver.get(url)

# Wait for the page to load completely
driver.implicitly_wait(10)  # Adjust the wait time as needed

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Locate all logo elements with classes that start with "wp-image-"
logos = soup.select('img[class^="wp-image-"]')  # CSS selector for classes that start with "wp-image-"

# Locate all speaker names and positions
names = soup.find_all('h4', class_='et_pb_module_header')  # Speaker names
positions = soup.find_all('p', class_='et_pb_member_position')  # Speaker positions

# Function to extract company name from the logo_url
def extract_company_name(url):
    filename = url.split('/')[-1]
    company_name = filename.split('-2024')[0]  # Adjust year if needed
    return company_name.replace('-', ' ')

# Extract data for all speakers and logos
data = []
for i in range(len(names)):
    name = names[i].text.strip() if i < len(names) else None
    position = positions[i].text.strip() if i < len(positions) else None
    
    # For the logos, you may not have a 1-to-1 relationship, so use the index only if available
    logo_url = logos[i].get('src') if i < len(logos) else None
    extracted_company_name = extract_company_name(logo_url) if logo_url else None

    data.append({
        "speaker_name": name,
        "position": position,
        "logo_url": logo_url,
        "extracted_company_name": extracted_company_name
    })

# Close the Selenium driver
driver.quit()

# Save data to a CSV file with the additional speaker name and position
csv_file = 'speakers_with_logos.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["speaker_name", "position", "logo_url", "extracted_company_name"])
    writer.writeheader()
    writer.writerows(data)

print(f"Speakers and logos have been extracted and saved to {csv_file}")
