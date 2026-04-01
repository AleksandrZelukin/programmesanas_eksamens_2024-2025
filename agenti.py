# Lejupielādē, atver datni un datu struktūrā saglabā datus turpmākai izmantošanai. (2 punkti)
# Balstoties uz kolonnu “TIPS”, nofiltrē nederīgos datus, proti, ir jāpaliek tikai datiem, kas atbilst jebkuram no šiem tipiem: (3 punkti) · Izglītības iestāde; · Valsts iestāde.
# Atlasi tikai tādu iestāžu nosaukumus un adreses, kas atrodas Rīgā. (3 punkti)
# Sakārto datus pēc kolonnas “NOSAUKUMS” alfabēta secībā. (2 punkti)
# Pēc katra uzdevuma izpildes pārskatāmi izvadi iegūto rezultātu. (2 punkti)

import csv


# 1. Lejupielādē un atver datni
with open('agenti.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    data = list(reader)

print("1. Dati ir lejupielādēti:")
print(data[:2])

# 2. Filtrē pēc TIPS
valid_types = ['Izglītības iestāde', 'Valsts iestāde']
filtered_data = [row for row in data if row['TIPS'] in valid_types]
print("\n2. Noderīgie dati pēc filtra 'TIPS':")
print(filtered_data[:2])

# 3. Atlasi tikai Rīgā esošās iestādes
riga_data = [row for row in filtered_data if 'Rīga' in row['ADRESE']]
print("\n3. Iestādes, kas atrodas Rīgā:")
for row in riga_data[:2]:
    print(f"{row['NOSAUKUMS']} - {row['ADRESE']}")

# 4. Sakārto pēc NOSAUKUMS alfabēta secībā
sorted_data = sorted(riga_data, key=lambda x: x['NOSAUKUMS'])
print("\n4. Sakārtoti dati pēc nosaukuma:")
for row in sorted_data:
    print(f"{row['NOSAUKUMS']} - {row['ADRESE']}")