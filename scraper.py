import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
import uuid
from datetime import datetime, timedelta

# The list of sites from your PDF
urls = [
    "https://www.aeronautbrewing.com",
    "https://artsatthearmory.org",
    "https://www.cambridgema.gov"
]

def create_ical_feed():
    # 1. Initialize the calendar inside the function
    c = Calendar()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    for url in urls:
        print(f"Scraping: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            found_on_page = 0
            for item in soup.find_all(['h1', 'h2', 'h3']):
                title_text = item.get_text(strip=True)
                
                if len(title_text) > 5 and "Event" not in title_text:
                    e = Event()
                    e.name = title_text
                    
                    # Set to Tomorrow (March 19, 2026) for your test
                    tomorrow = datetime.now() + timedelta(days=1)
                    e.begin = tomorrow.strftime('%Y-%m-%d 19:00:00')
                    
                    # Unique ID for every event to prevent duplicates
                    e.uid = f"batch1-{uuid.uuid4()}" 
                    e.description = f"Source: {url}"
                    
                    c.events.add(e)
                    found_on_page += 1
            
            print(f"  -> Successfully added {found_on_page} items.")
                    
        except Exception as err:
            print(f"  -> Error at {url}: {err}")

    # 2. SAVE THE FILE (Indented INSIDE the function so it can see 'c')
    # newline='\r\n' ensures the CRLF format that Outlook/Google requires
    with open('indie-events.ics', 'w', newline='\r\n', encoding='utf-8') as f:
        f.writelines(c.serialize_iter())
    
    print(f"\nSUCCESS! Total events in file: {len(c.events)}")

# 3. This tells Python to run the function when you type 'python scraper.py'
if __name__ == "__main__":
    create_ical_feed()
