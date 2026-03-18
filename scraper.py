import uuid # For unique event IDspython scraper.py

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
    
 # Logic specifically for Aeronaut Brewing
    response = requests.get("https://www.aeronautbrewing.com")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Aeronaut uses 'article' tags for each event
    for item in soup.find_all('article'): 
        e = Event()
        # Find the title inside the <h2>
        e.name = item.find('h2').get_text(strip=True)
        
        # Find the date (this part is tricky and needs a 'date parser' later)
        # For now, let's set it to 'Tomorrow' so you can see it easily
        e.begin = '2026-03-19 19:00:00' 
        
        try:
            # (your scraping code is in here)
            c.events.add(e)
        except Exception as err:
            print(f"Error scraping {url}: {err}")


    # SAVE THE FILE
    with open('indie-events.ics', 'w', encoding='utf-8') as f:
        f.writelines(c.serialize_iter())
    print("Success! 'indie-events.ics' has been created.")

create_ical_feed()
