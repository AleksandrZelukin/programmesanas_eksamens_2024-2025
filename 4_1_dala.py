import requests
import json
import statistics
import random
from collections import defaultdict

url1 = requests.get("https://pro2025.azurewebsites.net/journals")
url2 = requests.get("https://pro2025.azurewebsites.net/journals?year_established=2000")
url3 = requests.get("https://pro2025.azurewebsites.net/books?genre=Fantasy&year_published=2020")


url41 = requests.get("https://pro2025.azurewebsites.net/books")
def check_status(url41):
    try:
        resp = requests.get(url41, timeout=10)
        if resp.status_code == 200:
            print(f"Savienojums ar {url41}: statusa kods 200 — veiksmīgi saņemti dati.")
        else:
            print(f"Savienojums ar {url41}: statusa kods {resp.status_code} — pārbaudiet URL vai serveri.")
        return resp
    except Exception as e:
        print(f"Kļūda, mēģinot piekļūt {url41}: {e}")
        raise