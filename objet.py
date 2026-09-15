class Objet:
    def __init__(self, nom_de_objet, description_de_objet, texte_lisible=None, nom_affichage=None):
        self.nom_de_objet = nom_de_objet
        self.description_de_objet = description_de_objet
        self.texte_lisible = texte_lisible
        self.nom_affichage = nom_affichage or nom_de_objet