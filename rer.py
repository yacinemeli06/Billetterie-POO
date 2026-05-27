from abc import ABC, abstractmethod

class Train(ABC):
    def __init__(self, vitesse, prix_km):
        self.vitesse = vitesse    
        self.prix_km = prix_km    

    @abstractmethod
    def calcul_prix(self, distance, reduit=False):
        pass

    @abstractmethod
    def calcul_temps(self, distance):
        pass


class Shinkansen(Train):
    def __init__(self):
        super().__init__(vitesse=310, prix_km=5)
        self.plats = ["Sushi", "Tempura", "Bento au poulet"]
        self.boissons = ["Thé vert", "Saké", "Eau minérale"]
        self.desserts = ["Mochi", "Dorayaki", "Glace au thé matcha"]
        self.menu_choisi = None
        self.supplement = 5  
    def calcul_prix(self, distance, reduit=False):
        prix = self.prix_km * distance * (0.5 if reduit else 1)
        prix += self.supplement
        return prix

    def calcul_temps(self, distance):
        return distance / self.vitesse  

    def choisir_repas(self):
        def demander_choix(options, libelle):
            print(f"{libelle.capitalize()} disponibles :")
            #liste chaqu'un des  option numérotée
            for idx, opt in enumerate(options, 1):
                print(f"  {idx}. {opt}")
                # jusqu’à une saisie valide
            while True:
                sel = input(f"Saisir le numéro de {libelle} (1–{len(options)}) : ")
                # vérifi que la personne a tapé un chiffre valide
                if sel.isdigit() and 1 <= int(sel) <= len(options):
                    return options[int(sel) - 1]
                print("Entrée invalide, réessayez.")

        plat    = demander_choix(self.plats,    "le plat")
        boisson = demander_choix(self.boissons, "la boisson")
        dessert = demander_choix(self.desserts, "le dessert")
        self.menu_choisi = (plat, boisson, dessert)


class RER(Train):
    def __init__(self):
        super().__init__(vitesse=80, prix_km=2)
        self.retard_km = 2  

    def calcul_prix(self, distance, reduit=False):
        return self.prix_km * distance * (0.5 if reduit else 1)

    def calcul_temps(self, distance):
        return distance / self.vitesse + (self.retard_km * distance) / 60

    def retard_total(self, distance):
        return self.retard_km * distance  


def format_hhmm(heures):
    total_min = int(heures * 60)
    return f"{total_min//60:02d}h{total_min%60:02d}m"



while True:
    print("1) Shinkansen   2) RER")
    choix = input("Votre choix (1/2) : ")
    if choix in ("1", "2"):
        break


while True:
    try:
        distance = float(input("Distance à parcourir (km) : "))
        if distance > 0:
            break
    except ValueError:
        pass

while True:
    rep = input("Tarif réduit ? (o/n) : ").lower()
    if rep in ("o", "n"):
        reduit = (rep == "o")
        break

if choix == "1":
    train = Shinkansen()
    while True:
        rep = input("Ajouter un menu (+5 €) ? (o/n) : ").lower()
        if rep in ("o", "n"):
            if rep == "o":
                train.choisir_repas()
            break
else:
    train = RER()


prix = train.calcul_prix(distance, reduit)
temps = train.calcul_temps(distance)

# affichage du récap
print("\n--- Récapitulatif ---")
print(f"Distance : {distance} km")
print(f"Prix     : {prix:.2f} €")
print(f"Durée    : {format_hhmm(temps)}")

if isinstance(train, RER):
    print(f"Retard   : {int(train.retard_total(distance))} min")
else:
    if train.menu_choisi:
        print("Repas:", " / ".join(train.menu_choisi))
    else:
        print("Repas: (aucun)")

