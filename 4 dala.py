"""
Programma — pro2025_books_python_3_11.py
Valoda: Python 3.11

Šī programma izpilda uzdevumus 4.1–4.10, izmantojot URL:
https://pro2025.azurewebsites.net/books un https://pro2025.azurewebsites.net/journals

Lūdzu, palaidiet šo datni savā vidē, kur ir pieejams internets (programma izmanto bibliotēku `requests`).
Ja nav instalēta bibliotēka requests, instalējiet ar: pip install requests

Programma:
- pārbauda atbildes statusa kodu (200)
- izvada grāmatu informāciju formātā: Grāmata "<<nosaukums>>" (<<gads>>), <<lappušu skaits>> lpp.
- saglabā visu grāmatu nosaukumus JSON failā nosaukumi.json
- atrod visvecāko grāmatu
- aprēķina kopējo lappušu skaitu un vidējo cenu
- funkcija garakais_nosaukums()
- izveido datu struktūru ar visu grāmatu datiem (autora lauks "Nav norādīts", ja nav)
- izvade autoru sarakstam A–Z bez dublikātiem
- atrod autoru ar visvairāk grāmatām un izvada formātu
- izveido nejaušu 10 žurnālu sarakstu no /journals un nodrošina funkcijas pievienošanai sākumā un dzēšanai pēdējā

Autors: Jūsu vārds
Datne izveidota atbilstībā uzdevuma prasībām.
"""

import requests
import json
import statistics
import random
from collections import defaultdict

BOOKS_URL = "https://pro2025.azurewebsites.net/books"
JOURNALS_URL = "https://pro2025.azurewebsites.net/journals"

# 4.1. Izveido pieprasījumu uz norādīto URL
def check_status(url):
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            print(f"Savienojums ar {url}: statusa kods 200 — veiksmīgi saņemti dati.")
        else:
            print(f"Savienojums ar {url}: statusa kods {resp.status_code} — pārbaudiet URL vai serveri.")
        return resp
    except Exception as e:
        print(f"Kļūda, mēģinot piekļūt {url}: {e}")
        raise

# 4.2. Izvada datus par visām grāmatām
def print_books_list(books):
    for b in books:
        title = b.get('title', 'Bez nosaukuma')
        year = b.get('year', 'Gads nav')
        pages = b.get('pages', 'Lappušu skaits nav')
        print(f'Grāmata "{title}" ({year}), {pages} lpp.')

# 4.3. Iegūst visu grāmatu nosaukumus un ieraksta JSON
def save_titles_json(books, filename='nosaukumi.json'):
    titles = [b.get('title', '') for b in books]
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(titles, f, ensure_ascii=False, indent=2)
    print(f'Nosaukumi saglabāti failā: {filename}')

# 4.4. Atrod visvecāko grāmatu
def find_oldest_book(books):
    filtered = [b for b in books if isinstance(b.get('year'), int)]
    if not filtered:
        return None
    oldest = min(filtered, key=lambda x: x['year'])
    return oldest

# 4.5. Kopējais lappušu skaits un vidējā cena
def pages_and_average_price(books):
    pages = [b.get('pages') for b in books if isinstance(b.get('pages'), int)]
    prices = [b.get('price') for b in books if isinstance(b.get('price'), (int, float))]
    total_pages = sum(pages) if pages else 0
    avg_price = statistics.mean(prices) if prices else 0
    return total_pages, avg_price

# 4.6. garakais_nosaukums
def garakais_nosaukums(books):
    if not books:
        return None
    return max(books, key=lambda b: len(b.get('title','')))

# 4.7. Datu struktūra ar visu datu normalizāciju
def normalized_books(books):
    norm = []
    for b in books:
        nb = dict(b)  # copy
        if not nb.get('author'):
            nb['author'] = 'Nav norādīts'
        norm.append(nb)
    return norm

# 4.8. Autoru saraksts A-Z bez dublikātiem
def unique_authors_sorted(books):
    authors = {b.get('author','Nav norādīts') for b in books}
    return sorted(authors)

# 4.9. Autors ar visvairāk grāmatām
def author_with_most_books(books):
    counter = defaultdict(list)
    for b in books:
        counter[b.get('author','Nav norādīts')].append(b)
    if not counter:
        return None, []
    author, blist = max(counter.items(), key=lambda kv: len(kv[1]))
    return author, blist

# 4.10. Žurnālu apstrāde
def random_journals_sample(journals, n=10):
    if len(journals) <= n:
        sample = journals[:]
    else:
        sample = random.sample(journals, n)
    # keep only title and publisher
    return [{'title': j.get('title',''), 'publisher': j.get('publisher','')} for j in sample]

class JournalList:
    def __init__(self, journals):
        # journals is list of dicts with keys title,publisher
        self.journals = journals[:]
    def add_at_start(self, title, publisher):
        self.journals.insert(0, {'title': title, 'publisher': publisher})
    def delete_last(self):
        if self.journals:
            self.journals.pop()
    def __str__(self):
        return '\n'.join([f"{i+1}. {j['title']} — {j['publisher']}" for i,j in enumerate(self.journals)])

# Helper to safely parse books JSON
def get_books_from_response(resp):
    try:
        data = resp.json()
        # assume data is list of book dicts
        if isinstance(data, dict) and 'data' in data:
            return data['data']
        return data
    except Exception:
        return []


def main():
    # 4.1
    try:
        resp = check_status(BOOKS_URL)
    except Exception:
        print('Nevar turpināt bez piekļuves books URL.')
        return

    books = get_books_from_response(resp)

    # 4.2
    print('\n--- Visas grāmatas ---')
    print_books_list(books)

    # 4.3
    save_titles_json(books, 'nosaukumi.json')

    # 4.4
    oldest = find_oldest_book(books)
    if oldest:
        print(f"\nVisvecākā grāmata: \"{oldest.get('title','Bez nosaukuma')}\"")
    else:
        print('\nNevar noteikt visvecāko grāmatu.')

    # 4.5
    total_pages, avg_price = pages_and_average_price(books)
    print(f"\nVisu grāmatu kopējais lappušu skaits: {total_pages}")
    print(f"Vidējā cena: {avg_price:.2f}")

    # 4.6
    longest = garakais_nosaukums(books)
    if longest:
        print(f"\nGarākais nosaukums: \"{longest.get('title','')}\"")
        print(f"Autors: {longest.get('author','Nav norādīts')}, Gads: {longest.get('year','-')}")

    # 4.7
    norm = normalized_books(books)

    # 4.8
    authors_sorted = unique_authors_sorted(norm)
    print('\n--- Autori A–Z (bez dublikātiem) ---')
    for a in authors_sorted:
        print(a)

    # 4.9
    author, blist = author_with_most_books(norm)
    if author:
        print(f"\nAutors, kuram ir visvairāk grāmatu ({len(blist)}), - {author}:")
        for i, b in enumerate(blist, 1):
            print(f'{i}. "{b.get("title","Bez nosaukuma")}"')

    # 4.10
    try:
        jresp = check_status(JOURNALS_URL)
    except Exception:
        print('\nNevar piekļūt žurnālu API.')
        return
    journals = []
    try:
        jdata = jresp.json()
        if isinstance(jdata, dict) and 'data' in jdata:
            journals = jdata['data']
        else:
            journals = jdata
    except Exception:
        journals = []

    sample = random_journals_sample(journals, 10)
    journal_list = JournalList(sample)
    print('\n--- Nejauši izvēlēti 10 žurnāli (nosaukums — izdevējs) ---')
    print(journal_list)

    # Demonstrācija: pievienojam jaunu žurnālu saraksta sākumā (lietotāja ievade)
    # Ja vēlaties, atkomentējiet zemāk un ievadiet datus
    #title = input('Ievadiet jaunā žurnāla nosaukumu: ')
    #publisher = input('Ievadiet jaunā žurnāla izdevēju: ')
    #journal_list.add_at_start(title, publisher)

    # Piemērs (bez lietotāja ievades):
    journal_list.add_at_start('Piemēra Žurnāls', 'Piemēru Izdevējs')
    print('\nPēc pievienošanas sākumā:')
    print(journal_list)

    # Dzēst pēdējo
    journal_list.delete_last()
    print('\nPēc pēdējā dzēšanas:')
    print(journal_list)

if __name__ == '__main__':
    main()
