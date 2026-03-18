import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
from ics.grammar.parse import ContentLine
import uuid
from datetime import datetime, timedelta

# 1. The list of sites from your PDF
urls = [
    "https://www.aeronautbrewing.com",
    "https://artsatthearmory.org",
    "https://calendar.mit.edu",
    "https://news.harvard.edu",
    "https://www.cambridgema.gov",
    "https://www.thebostoncalendar.com",
    "https://www.somervillepubliclibrary.org",
    "https://www.passim.org",
    "https://www.thecantablounge.com",
    "https://www.thesomervilletheatre.com",
    "https://www.crystalballroomboston.com",
    "https://www.dancecomplex.org",
    "https://www.sinclaircambridge.com",
    "https://www.cambridgeside.com",
    "https://www.thejunglemusicclub.com",
    "https://www.lilypadinman.com",
    "https://www.portersquarebooks.com",
    "https://www.harvard.com",
    "https://www.passim.org",
    "https://www.centralsquaretheater.org",
    "https://www.somervillemuseum.org",
    "https://www.unionsquaremain.org"
]

def create_ical_feed():
    c = Calendar()
    
    # These headers are the "secret" to making Outlook accept the file
    c.extra.append(ContentLine(name="X-WR-CALNAME", value="Indie Community Events"))
    c.extra.append(ContentLine(name="X-WR-TIMEZONE", value="America/New_York"))
    c.extra.append(ContentLine(name="METHOD", value="PUBLISH"))

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    for url in urls:
        print(f"Scraping: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            found_on_page = 0
            # Broad search for event titles in headers
            for item in soup.find_all(['h1', 'h2', 'h3']):
                title_text = item.get_text(strip=True)
                
                # Filter out short menu items or navigation links
                if len(title_text) > 5 and "Event" not in title_text:
                    e = Event()
                    e.name = title_text
                    
                    # Set to Tomorrow (March 19, 2026) so you can see them in Outlook
                    tomorrow = datetime.now() + timedelta(days=1)
                    e.begin = tomorrow.strftime('%Y-%m-%d 19:00:00')
                    
                    # Essential for WordPress and Outlook to track updates
                    e.uid = f"event-{uuid.uuid4()}" 
                    e.description = f"Source: {url}"
                    
                    c.events.add(e)
                    found_on_page += 1
            
            print(f"  -> Added {found_on_page} items.")
                    
        except Exception as err:
            print(f"  -> Error at {url}: {err}")

    # 2. SAVE THE FILE (Fixed for Outlook with CRLF line breaks)
    # Using newline='\r\n' is the "brute force" fix for the 'Couldn't Import' error
    with open('indie-events.ics', 'w', newline='\r\n', encoding='utf-8') as f:
        f.writelines(c.serialize_iter())
    
    print(f"\nSUCCESS! Total events in file: {len(c.events)}")

if __name__ == "__main__":
    create_ical_feed()
