class SkolenaDati:
    def __init__(self, vards, uzvards, klase):
        self.vards = vards
        self.uzvards = uzvards
        self.klase = klase
    def drukat (self):
        print(self.vards,self.uzvards, self.klase)
        
skolens1=SkolenaDati("Jānis","Bērziņš","10A")
skolens1.drukat()
skolens2=SkolenaDati("Anna","Kalniņa","11B")
skolens2.drukat()
skolens3=SkolenaDati("Pēteris","Ozoliņš","9C")
skolens3.drukat()