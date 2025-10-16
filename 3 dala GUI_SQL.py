import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3

# ========================
# Klase Gramata
# ========================
class Gramata:
    def __init__(self, nosaukums="Nav norādīts", lappušu_skaits=0, ISBN="Nav norādīts",
                 autors=None, zanrs=None, izdosanas_gads=None, pieejamibas_statuss=None):
        self.nosaukums = nosaukums
        self.lappušu_skaits = lappušu_skaits
        self.ISBN = ISBN
        self.autors = autors
        self.zanrs = zanrs
        self.izdosanas_gads = izdosanas_gads
        self.pieejamibas_statuss = pieejamibas_statuss

    def aprekinat(self, kaveto_dienu_skaits):
        kav_maksa = self.lappušu_skaits * 0.01 * kaveto_dienu_skaits
        return round(kav_maksa, 2)


# ========================
# Apakšklase Fantazija
# ========================
class Fantazija(Gramata):
    def aprekinat(self, kaveto_dienu_skaits):
        pamata = super().aprekinat(kaveto_dienu_skaits)
        return round(pamata + pamata * 0.01, 2)


# ========================
# Klase GramatuKatalogs ar SQLite
# ========================
class GramatuKatalogs:
    def __init__(self, db_name="gramatas.db"):
        self.db_name = db_name
        self._izveidot_tabulu()

    def _izveidot_tabulu(self):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS gramatas (
                nosaukums TEXT,
                autors TEXT,
                zanrs TEXT,
                lappuses INTEGER,
                ISBN TEXT PRIMARY KEY,
                gads TEXT,
                statuss TEXT
            )
        """)
        conn.commit()
        conn.close()

    def pievienot(self, gramata):
        try:
            conn = sqlite3.connect(self.db_name)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO gramatas (nosaukums, autors, zanrs, lappuses, ISBN, gads, statuss)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (gramata.nosaukums, gramata.autors, gramata.zanrs, gramata.lappušu_skaits,
                  gramata.ISBN, gramata.izdosanas_gads, gramata.pieejamibas_statuss))
            conn.commit()
            conn.close()
            messagebox.showinfo("Veiksmīgi", f'Grāmata "{gramata.nosaukums}" pievienota datubāzei!')
        except sqlite3.IntegrityError:
            messagebox.showwarning("Dublikāts", "Grāmata ar šādu ISBN jau eksistē!")

    def atjauninat_statusu(self, ISBN, jauns_statuss):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute("UPDATE gramatas SET statuss=? WHERE ISBN=?", (jauns_statuss, ISBN))
        conn.commit()
        if cur.rowcount > 0:
            messagebox.showinfo("Atjaunināts", f'Statuss atjaunināts uz "{jauns_statuss}".')
        else:
            messagebox.showwarning("Nav atrasta", f'Grāmata ar ISBN "{ISBN}" nav atrasta katalogā.')
        conn.close()

    def nonemt(self, ISBN):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute("DELETE FROM gramatas WHERE ISBN=?", (ISBN,))
        conn.commit()
        if cur.rowcount > 0:
            messagebox.showinfo("Dzēsts", f'Grāmata ar ISBN "{ISBN}" ir dzēsta no datubāzes.')
        else:
            messagebox.showwarning("Nav atrasta", f'Grāmata ar ISBN "{ISBN}" nav atrasta.')
        conn.close()

    def ieladet_visas(self):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute("SELECT * FROM gramatas")
        rindas = cur.fetchall()
        conn.close()
        return rindas


# ========================
# GUI klase ar datubāzi
# ========================
class GramatuApp:
    def __init__(self, root):
        self.katalogs = GramatuKatalogs()
        self.root = root
        self.root.title("Grāmatu katalogs (ar SQLite datubāzi)")
        self.root.geometry("950x800")

        # Ievades lauki
        self.frame_inputs = tk.Frame(root)
        self.frame_inputs.pack(pady=10)

        labels = ["Nosaukums", "Autors", "Žanrs", "Lappušu skaits", "ISBN", "Gads", "Pieejamības statuss"]
        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(self.frame_inputs, text=label + ":").grid(row=i, column=0, sticky="e", padx=5)
            entry = tk.Entry(self.frame_inputs, width=45)
            entry.grid(row=i, column=1, pady=2)
            self.entries[label] = entry

        tk.Button(self.frame_inputs, text="Pievienot grāmatu", command=self.pievienot_gramatu,
                  bg="#4CAF50", fg="blue", width=25).grid(row=7, column=1, pady=10)

        # Tabula (Treeview)
        self.tree = ttk.Treeview(root, columns=("Nosaukums", "Autors", "Žanrs", "Lappuses", "ISBN", "Gads", "Statuss"),
                                 show="headings", height=12)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(pady=10)

        # Pogas
        frame_bottom = tk.Frame(root)
        frame_bottom.pack()

        tk.Button(frame_bottom, text="Atjaunināt statusu", command=self.atjauninat_statusu,
                  bg="#2196F3", fg="blue").grid(row=0, column=0, padx=5)
        tk.Button(frame_bottom, text="Dzēst grāmatu", command=self.nonemt_gramatu,
                  bg="#f44336", fg="blue").grid(row=0, column=1, padx=5)
        tk.Button(frame_bottom, text="Aprēķināt kavējuma maksu", command=self.aprekinat_maksu,
                  bg="#9C27B0", fg="blue").grid(row=0, column=2, padx=5)
        tk.Button(frame_bottom, text="Atsvaidzināt sarakstu", command=self.atjaunot_tabulu,
                  bg="#607D8B", fg="blue").grid(row=0, column=3, padx=5)

        # Ielādē datus no datubāzes
        self.atjaunot_tabulu()

    def pievienot_gramatu(self):
        d = {k: e.get() for k, e in self.entries.items()}
        try:
            lappuses = int(d["Lappušu skaits"])
        except ValueError:
            messagebox.showerror("Kļūda", "Lappušu skaitam jābūt veselam skaitlim!")
            return

        if d["Žanrs"].lower() == "fantāzija":
            g = Fantazija(d["Nosaukums"], lappuses, d["ISBN"], d["Autors"], d["Žanrs"],
                          d["Gads"], d["Pieejamības statuss"])
        else:
            g = Gramata(d["Nosaukums"], lappuses, d["ISBN"], d["Autors"], d["Žanrs"],
                        d["Gads"], d["Pieejamības statuss"])

        self.katalogs.pievienot(g)
        self.atjaunot_tabulu()

    def atjaunot_tabulu(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for rinda in self.katalogs.ieladet_visas():
            self.tree.insert("", "end", values=rinda)

    def atjauninat_statusu(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Izvēle", "Izvēlies grāmatu, kurai mainīt statusu!")
            return
        item = self.tree.item(selected[0])
        isbn = item["values"][4]
        jauns_statuss = simpledialog.askstring("Jauns statuss", "Ievadi jauno statusu:")
        if jauns_statuss:
            self.katalogs.atjauninat_statusu(isbn, jauns_statuss)
            self.atjaunot_tabulu()

    def nonemt_gramatu(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Izvēle", "Izvēlies grāmatu, ko dzēst!")
            return
        item = self.tree.item(selected[0])
        isbn = item["values"][4]
        self.katalogs.nonemt(isbn)
        self.atjaunot_tabulu()

    def aprekinat_maksu(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Izvēle", "Izvēlies grāmatu!")
            return
        item = self.tree.item(selected[0])
        isbn = item["values"][4]
        try:
            dienas = int(simpledialog.askstring("Kavētās dienas", "Ievadi kavēto dienu skaitu:"))
        except (ValueError, TypeError):
            messagebox.showerror("Kļūda", "Nepareizs dienu skaits!")
            return

        nosaukums = item["values"][0]
        lappuses = int(item["values"][3])
        zanrs = str(item["values"][2])

        if zanrs.lower() == "fantāzija":
            g = Fantazija(nosaukums, lappuses, isbn)
        else:
            g = Gramata(nosaukums, lappuses, isbn)

        maksa = g.aprekinat(dienas)
        messagebox.showinfo("Rezultāts", f'Grāmatas "{nosaukums}" kavējuma maksa ir {maksa:.2f} EUR.')


# ========================
# Programmas palaišana
# ========================
if __name__ == "__main__":
    root = tk.Tk()
    app = GramatuApp(root)
    root.mainloop()
