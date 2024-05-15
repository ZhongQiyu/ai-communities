import requests
from bs4 import BeautifulSoup

# URL of the paper on openreview
url = "https://openreview.net/pdf?id=b6Wym03blGW"

# Download the page
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract features
    conference = "N/A"  # Conference details may not be available in the PDF
    venue_group = "N/A"  # Venue group may not be available in the PDF
    title = soup.title.string if soup.title else "N/A"
    keywords = "N/A"  # Keywords are often not included in the PDF
    authors = "N/A"  # Authors need to be extracted from specific areas of the PDF
    date = "N/A"  # Date may not be available in the PDF
    read_num = "N/A"  # Read count not usually included in the PDF
    code_url = "N/A"  # Code URL usually not included in the PDF
    
    print(f"URL: {url}")
    print(f"Title: {title}")
    print(f"Conference: {conference}")
    print(f"Venue Group: {venue_group}")
    print(f"Keywords: {keywords}")
    print(f"Authors: {authors}")
    print(f"Date: {date}")
    print(f"Read Number: {read_num}")
    print(f"Code URL: {code_url}")
else:
    print(f"Failed to download the page: {response.status_code}")
