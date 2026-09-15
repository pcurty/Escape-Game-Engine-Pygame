class Salle:
    def __init__(self, nom_de_la_salle, description_de_la_salle, indice_de_la_salle=""):
        self.nom_de_la_salle = nom_de_la_salle
        self.description_de_la_salle = description_de_la_salle
        self.indice_de_la_salle = indice_de_la_salle
        self.dictionnaire_des_sorties_possibles = {}
        self.dictionnaire_des_objets_presents = {}
        self.dictionnaire_des_meubles_presents = {}
        self.nombre_objets_disponibles = 0

    def ajouter_une_sortie(self, direction_de_la_sortie, salle_de_destination, est_verrouillee, objet_requis_pour_deverouiller, code_requis, message_porte_verrouillee):
        self.dictionnaire_des_sorties_possibles[direction_de_la_sortie] = {
            "salle_de_destination": salle_de_destination,
            "est_verrouillee": est_verrouillee,
            "objet_requis": objet_requis_pour_deverouiller,
            "code_requis": code_requis,
            "message_verrou": message_porte_verrouillee
        }

    def ajouter_un_objet(self, nouvel_objet_a_ajouter):
        self.dictionnaire_des_objets_presents[nouvel_objet_a_ajouter.nom_de_objet] = nouvel_objet_a_ajouter
        self.nombre_objets_disponibles += 1

    def ajouter_un_meuble(self, nouveau_meuble_a_ajouter):
        self.dictionnaire_des_meubles_presents[nouveau_meuble_a_ajouter.nom_du_meuble] = nouveau_meuble_a_ajouter