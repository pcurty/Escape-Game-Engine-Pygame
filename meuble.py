class Meuble:
    def __init__(self, nom_du_meuble, description_du_meuble, nom_affichage=None, materiau="bois"):
        self.nom_du_meuble = nom_du_meuble
        self.description_du_meuble = description_du_meuble
        self.nom_affichage = nom_affichage or nom_du_meuble
        self.materiau = materiau 
        self.dictionnaire_des_objets_contenus = {}

    def ajouter_un_objet(self, objet_a_ajouter):
        self.dictionnaire_des_objets_contenus[objet_a_ajouter.nom_de_objet] = objet_a_ajouter