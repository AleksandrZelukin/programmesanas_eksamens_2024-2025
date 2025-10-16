import sqlite3
from datetime import date

# ============================================
# Datubāzes izveide
# ============================================

conn = sqlite3.connect("2_dala.db")
cursor = conn.cursor()

# ============================================
# 1.1. Tabula GRAMATAS
# ============================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS GRAMATAS (
    gr_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nosaukums TEXT NOT NULL,
    autors TEXT NOT NULL,
    zanrs TEXT,
    izdosanas_gads INTEGER CHECK(izdosanas_gads > 0),
    lappusu_skaits INTEGER CHECK(lappusu_skaits > 0),
    cena REAL
);
""")

# ============================================
# 1.2. Tabula LIETOTAJI
# ============================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS LIETOTAJI (
    liet_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vards TEXT NOT NULL,
    uzvards TEXT NOT NULL,
    personas_kods TEXT UNIQUE,
    registracijas_datums DATE
);
""")

# ============================================
# 1.3. Tabula STATISTIKA
# ============================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS STATISTIKA (
    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    lietotaja_id INTEGER NOT NULL,
    gramatas_id INTEGER NOT NULL,
    izsniegsanas_datums DATE NOT NULL,
    atgriesanas_datums DATE,
    FOREIGN KEY (lietotaja_id) REFERENCES LIETOTAJI(liet_id),
    FOREIGN KEY (gramatas_id) REFERENCES GRAMATAS(gr_id)
);
""")

# ============================================
# Papildu tabulas bibliotēku uzdevumiem
# ============================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS BIBLIOTEKAS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nosaukums TEXT NOT NULL,
    adrese TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS EKSEMPLARI (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bibliotekas_id INTEGER,
    gramatas_id INTEGER,
    daudzums INTEGER,
    FOREIGN KEY (bibliotekas_id) REFERENCES BIBLIOTEKAS(id),
    FOREIGN KEY (gramatas_id) REFERENCES GRAMATAS(gr_id)
);
""")

# ============================================
# Datu ievietošana
# ============================================

cursor.executemany("""
INSERT INTO GRAMATAS (nosaukums, autors, zanrs, izdosanas_gads, lappusu_skaits, cena)
VALUES (?, ?, ?, ?, ?, ?)
""", [
    ('Epifānijas', 'Imants Ziedonis', 'dzeja', 2022, 304, 12.50),
    ('Stari', 'Jānis Eglītis', 'romāns', 2006, 180, 8.90),
    ('Nakts krāsas', 'Pēteris Eglītis', 'stāsti', 2006, 210, 9.40),
    ('Ceļš uz mājām', 'Anna Ozola', 'romāns', 2010, 250, 11.00)
])

cursor.executemany("""
INSERT INTO LIETOTAJI (vards, uzvards, personas_kods, registracijas_datums)
VALUES (?, ?, ?, ?)
""", [
    ('Anna', 'Ozola', '010101-12345', '2024-03-12'),
    ('Jānis', 'Bērziņš', '020202-67890', '2024-05-10')
])

cursor.executemany("""
INSERT INTO STATISTIKA (lietotaja_id, gramatas_id, izsniegsanas_datums, atgriesanas_datums)
VALUES (?, ?, ?, ?)
""", [
    (1, 1, '2025-09-01', '2025-09-20'),
    (2, 2, '2025-09-15', '2025-09-30')
])

cursor.executemany("""
INSERT INTO BIBLIOTEKAS (nosaukums, adrese)
VALUES (?, ?)
""", [
    ('Rīgas Centrālā bibliotēka', 'Brīvības iela 49, Rīga'),
    ('Liepājas bibliotēka', 'Graudu iela 15, Liepāja'),
    ('Valmieras bibliotēka', 'Rīgas iela 10, Valmiera')
])

cursor.executemany("""
INSERT INTO EKSEMPLARI (bibliotekas_id, gramatas_id, daudzums)
VALUES (?, ?, ?)
""", [
    (1, 1, 6),  # Epifānijas - 6 eksemplāri Rīgā
    (2, 1, 3),  # Epifānijas - 3 eksemplāri Liepājā
    (3, 2, 5)   # Stari - 5 eksemplāri Valmierā
])

conn.commit()

# ============================================
# 2. uzdevums — SQL vaicājumi
# ============================================

print("2.1. Visu bibliotēku ID, nosaukumi un adreses:")
for row in cursor.execute("SELECT id, nosaukums, adrese FROM BIBLIOTEKAS;"):
    print(row)

print("\n2.2. Grāmatas, kas izdotas 2006. gadā:")
for row in cursor.execute("SELECT nosaukums, autors FROM GRAMATAS WHERE izdosanas_gads = 2006;"):
    print(row)

print("\n2.3. Vidējā cena tām grāmatām, kuru autors satur 'Eglītis':")
for row in cursor.execute("SELECT AVG(cena) AS videja_cena FROM GRAMATAS WHERE autors LIKE '%Eglītis%';"):
    print(row)

print("\n2.4. Bibliotēku adreses, kur vismaz piecos eksemplāros ir 'Epifānijas' (Imants Ziedonis):")
for row in cursor.execute("""
SELECT B.adrese
FROM BIBLIOTEKAS B
JOIN EKSEMPLARI E ON B.id = E.bibliotekas_id
JOIN GRAMATAS G ON E.gramatas_id = G.gr_id
WHERE G.nosaukums = 'Epifānijas'
  AND G.autors = 'Imants Ziedonis'
  AND E.daudzums >= 5;
"""):
    print(row)

# ============================================
# Beigas
# ============================================

conn.close()
print("\n✅ Datubāze izveidota un vaicājumi izpildīti veiksmīgi!")
