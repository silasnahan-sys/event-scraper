import uuid # For unique event IDs
import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event

# Add the URLs from your list here
urls = [
    "https://www.aeronautbrewing.com",
    "https://artsatthearmory.org"
]

def create_ical_feed():
    c = Calendar()
    
        for url in urls:
        print(f"Scraping: {url}")
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for item in soup.find_all('h2'): 
                e = Event()
                e.name = item.get_text(strip=True)
                e.begin = '2026-05-20 19:00:00' 
                e.uid = str(uuid.uuid4())
                c.events.add(e)
        except Exception as err:
            print(f"Error scraping {url}: {err}") # <--- This must line up with 'try'


    # SAVE THE FILE
    with open('indie-events.ics', 'w', encoding='utf-8') as f:
        f.writelines(c.serialize_iter())
    print("Success! 'indie-events.ics' has been created.")

create_ical_feed()
