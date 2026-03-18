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
    c = Calendar()
    # Headers make your script look like a real browser so you don't get blocked
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    for url in urls:
        print(f"Scraping: {url}")
        try:
            # 1. Fetch the page
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 2. Extract Titles (Searching h1, h2, and h3 tags)
            found_on_page = 0
            for item in soup.find_all(['h1', 'h2', 'h3']):
                title_text = item.get_text(strip=True)
                
                # Filter out generic titles like "Menu", "Search", or "Contact"
                if len(title_text) > 5 and "Event" not in title_text:
                    e = Event()
                    e.name = title_text
                    
                    # 3. Set Date (Set to tomorrow, March 19, 2026, for your test)
                    tomorrow = datetime.now() + timedelta(days=1)
                    e.begin = tomorrow.strftime('%Y-%m-%d 19:00:00')
                    
                    # 4. Set Metadata (Essential for WordPress/Google to track updates)
                    e.uid = str(uuid.uuid4()) 
                    e.description = f"Source: {url}"
                    
                    c.events.add(e)
                    found_on_page += 1
            
            print(f"  -> Successfully added {found_on_page} items.")
                    
        except Exception as err:
            print(f"  -> Error at {url}: {err}")

    # 5. SAVE THE FILE (Fixed for Validators and WordPress)
    with open('indie-events.ics', 'w', newline='', encoding='utf-8') as f:
        # Use serialize_iter for the cleanest output
        f.writelines(c.serialize_iter())
    
    print(f"\nSUCCESS! Total events in file: {len(c.events)}")

if __name__ == "__main__":
    create_ical_feed()
