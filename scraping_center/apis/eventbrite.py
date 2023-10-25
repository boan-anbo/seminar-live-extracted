import requests
from bs4 import BeautifulSoup

def fetch_eventbrite_one_by_id(event_id: str):
    response = requests.get(f'https://www.eventbriteapi.com/v3/events/{event_id}/', headers={'Authorization': 'Bearer 2XGFXVEVQUX62UCDIRIQ'}).json()
    return response

def fetch_eventbrite_one_by_url(url: str):
    url = url
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    try:
        event_id_div = soup.find_all("a", class_="listing-panel-actions__btn")
        event_id = event_id_div[0]['data-eid']
        return fetch_eventbrite_one_by_id(event_id)
    except:
        raise
