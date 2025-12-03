import requests
import json


url1 = requests.get("https://pro2025.azurewebsites.net/journals")
url2 = requests.get("https://pro2025.azurewebsites.net/journals?year_established=2000")
url3 = requests.get("https://pro2025.azurewebsites.net/books?genre=Fantasy&year_published=2020")
url4_1 = requests.get("https://pro2025.azurewebsites.net/books")
def check_status(url4_1):
    try:
        resp = requests.get(url4_1, timeout=10)
        if resp.status_code == 200:
            print(f"Savienojums ar {url4_1}: statusa kods 200 — veiksmīgi saņemti dati.")
        else:
            print(f"Savienojums ar {url4_1}: statusa kods {resp.status_code} — pārbaudiet URL vai serveri.")
        return resp
    except Exception as e:
        print(f"Kļūda, mēģinot piekļūt {url4_1}: {e}")
        raise
    
response = check_status("https://pro2025.azurewebsites.net/books")
data = response.json()


url4_1 = requests.get("https://pro2025.azurewebsites.net/books")
for book in data:
    print(book)