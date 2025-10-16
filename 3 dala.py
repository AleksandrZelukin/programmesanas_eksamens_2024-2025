# 1.1. uzdevums – klase "Gramata"
class Gramata:
    # 1.2. uzdevums – konstruktors
    def __init__(self, nosaukums="Nav norādīts", lappušu_skaits=0, ISBN="Nav norādīts",
                 autors=None, zanrs=None, izdosanas_gads=None, pieejamibas_statuss=None):
        self.nosaukums = nosaukums
        self.lappušu_skaits = lappušu_skaits
        self.ISBN = ISBN
        self.autors = autors
        self.zanrs = zanrs
        self.izdosanas_gads = izdosanas_gads
        self.pieejamibas_statuss = pieejamibas_statuss

        # Ja ir visi obligātie atribūti
        if nosaukums != "Nav norādīts" and lappušu_skaits != 0 and ISBN != "Nav norādīts":
            print(f'Grāmata "{self.nosaukums}" ir veiksmīgi izveidota.')
        else:
            print(f'Grāmata ar noklusētajām vērtībām ir izveidota.')

    # 1.4. uzdevums – metode izvadit()
    def izvadit(self):
        print(f"Grāmatas autors: {self.autors}")
        print(f'Grāmatas nosaukums: "{self.nosaukums}"')
        print(f"Grāmatas izdošanas gads: {self.izdosanas_gads}")

    # 1.5. uzdevums – metode aprekinat()
    def aprekinat(self, kaveto_dienu_skaits):
        kav_maksa = self.lappušu_skaits * 0.01 * kaveto_dienu_skaits
        kav_maksa = round(kav_maksa, 2)
        return kav_maksa


# 1.3. uzdevums – objekts "epifanijas"
epifanijas = Gramata(
    nosaukums="Epifānijas",
    lappušu_skaits=304,
    ISBN="9789934036101",
    autors="Imants Ziedonis",
    zanrs="dzeja",
    izdosanas_gads=2022,
    pieejamibas_statuss="pieejama"
)

# Izvade ar metodi izvadit()
epifanijas.izvadit()

# Aprēķins ar metodi aprekinat()
kav_maksa = epifanijas.aprekinat(5)
print(f'Grāmatas "{epifanijas.nosaukums}" kavējuma maksa ir {kav_maksa:.2f} EUR.')


# 1.6. uzdevums – apakšklase "Fantazija"
class Fantazija(Gramata):
    # 1.8. uzdevums – pārrakstīt metode aprekinat()
    def aprekinat(self, kaveto_dienu_skaits):
        pamata_maksa = super().aprekinat(kaveto_dienu_skaits)
        fantazijas_maksa = pamata_maksa + (pamata_maksa * 0.01)
        return round(fantazijas_maksa, 2)


# 1.7. uzdevums – objekts "harijs"
harijs = Fantazija(
    nosaukums="Harijs Poters un Filozofu akmens",
    lappušu_skaits=223,
    ISBN="9780747532699",
    autors="Dž. K. Roulinga",
    zanrs="fantāzija",
    izdosanas_gads=1997,
    pieejamibas_statuss="pieejama"
)

# Aprēķins ar pārrakstīto metodi
harija_maksa = harijs.aprekinat(10)
print(f'Grāmatas "{harijs.nosaukums}" kavējuma maksa ir {harija_maksa:.2f} EUR.')


# 1.9. uzdevums – klase "GramatuKatalogs"
class GramatuKatalogs:
    def __init__(self):
        self.gramatas = []

    # 1.11. uzdevums – metode pievienot()
    def pievienot(self, gramata):
        self.gramatas.append(gramata)
        print(f'Grāmata "{gramata.nosaukums}" ir veiksmīgi pievienota.')

    # 1.12. uzdevums – metode atjauninat_statusu()
    def atjauninat_statusu(self, ISBN, jauns_statuss):
        atrasta = False
        for g in self.gramatas:
            if g.ISBN == ISBN:
                g.pieejamibas_statuss = jauns_statuss
                print(f'Grāmatai ar ISBN "{ISBN}" statuss ir atjaunināts uz "{jauns_statuss}".')
                atrasta = True
                break
        if not atrasta:
            print(f'Grāmata ar ISBN "{ISBN}" nav atrasta katalogā.')

    # 1.13. uzdevums – metode nonemt()
    def nonemt(self, ISBN):
        atrasta = False
        for g in self.gramatas:
            if g.ISBN == ISBN:
                self.gramatas.remove(g)
                print(f'Grāmata ar ISBN "{ISBN}" ir veiksmīgi nodzēsta no kataloga.')
                atrasta = True
                break
        if not atrasta:
            print(f'Grāmata ar ISBN "{ISBN}" nav atrasta katalogā.')


# 1.10. uzdevums – objekts "katalogs"
katalogs = GramatuKatalogs()

# Pievienot grāmatas
katalogs.pievienot(epifanijas)
katalogs.pievienot(harijs)

# Atjaunināt statusu
katalogs.atjauninat_statusu("9780747532699", "nav pieejama")

# Noņemt grāmatu
katalogs.nonemt("9789934036101")
