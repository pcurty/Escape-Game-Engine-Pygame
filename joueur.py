class Joueur:

    def __init__(self, salle_de_depart, interface_sortie):
        self.salle_actuelle = salle_de_depart
        self.inventaire_du_joueur = {}
        self.nombre_objets_dans_invetaire = 0
        self.recettes = {}
        self.sortie = interface_sortie

        self.attente_deverouillage = None
        self.salle_precedente = None

    # ------------------------------------------------------------------
    # Recettes / combinaisons
    # ------------------------------------------------------------------
    def ajouter_recette(self, nom_obj1, nom_obj2, objet_resultat):
        cle = tuple(sorted([nom_obj1, nom_obj2]))
        self.recettes[cle] = objet_resultat

    def combiner_objets(self, nom_obj1, nom_obj2):
        if nom_obj1 in self.inventaire_du_joueur and nom_obj2 in self.inventaire_du_joueur:
            objet1 = self.inventaire_du_joueur[nom_obj1]
            objet2 = self.inventaire_du_joueur[nom_obj2]
            cle = tuple(sorted([nom_obj1, nom_obj2]))
            if cle in self.recettes:
                objet_resultat = self.recettes[cle]
                del self.inventaire_du_joueur[nom_obj1]
                del self.inventaire_du_joueur[nom_obj2]
                self.inventaire_du_joueur[objet_resultat.nom_de_objet] = objet_resultat
                self.nombre_objets_dans_invetaire -= 1
                self.sortie.afficher(
                    "succes",
                    f"Vous avez combiné '{objet1.nom_affichage}' et '{objet2.nom_affichage}' "
                    f"pour créer '{objet_resultat.nom_affichage}'."
                )
                return "COMBINAISON_OK"
            else:
                self.sortie.afficher("erreur", "Ces deux objets ne se combinent pas.")
                return "COMBINAISON_ECHEC"
        else:
            self.sortie.afficher("erreur", "Vous ne possédez pas ces objets dans votre inventaire.")
            return "OBJETS_MANQUANTS"

    # ------------------------------------------------------------------
    # Lecture
    # ------------------------------------------------------------------
    def lire_un_objet(self, nom_objet):
        if nom_objet in self.inventaire_du_joueur:
            objet = self.inventaire_du_joueur[nom_objet]
            if objet.texte_lisible:
                self.sortie.afficher("info", f"{objet.nom_affichage} : \"{objet.texte_lisible}\"")
            else:
                self.sortie.afficher("info", f"Il n'y a rien d'intéressant à lire sur '{objet.nom_affichage}'.")
        else:
            self.sortie.afficher("erreur", f"Vous n'avez pas cet objet dans votre inventaire.")

    # ------------------------------------------------------------------
    # Ramassage
    # ------------------------------------------------------------------
    def ramasser_un_objet(self, nom_de_objet_ramasser):
        if nom_de_objet_ramasser in self.salle_actuelle.dictionnaire_des_objets_presents:
            objet_recupere = self.salle_actuelle.dictionnaire_des_objets_presents.pop(nom_de_objet_ramasser)
            self.salle_actuelle.nombre_objets_disponibles -= 1
            self.inventaire_du_joueur[nom_de_objet_ramasser] = objet_recupere
            self.nombre_objets_dans_invetaire += 1
            self.sortie.afficher("succes", f"Vous avez ramassé '{objet_recupere.nom_affichage}'.", son="tac")
            self.sortie.afficher("info", objet_recupere.description_de_objet)
            return "RAMASSAGE_OK"
        else:
            self.sortie.afficher("erreur", "Il n'y a rien de tel ici.")
            return "RAMASSAGE_ECHEC"

    # ------------------------------------------------------------------
    # Déplacement — machine à états (remplace l'ancien input() bloquant)
    # ------------------------------------------------------------------
    def se_deplacer(self, direction_choisie_par_joueur):

        porte = self.salle_actuelle.dictionnaire_des_sorties_possibles.get(direction_choisie_par_joueur)

        if porte is None:
            self.sortie.afficher("erreur", f"Aucune sortie dans la direction '{direction_choisie_par_joueur}'.")
            return "AUCUNE_SORTIE"

        if porte["est_verrouillee"]:
            objet_requis = porte["objet_requis"]
            if objet_requis and objet_requis.nom_de_objet not in self.inventaire_du_joueur:
                self.sortie.afficher("erreur", porte["message_verrou"])
                return "VERROUILLEE"

            if porte["code_requis"]:
                self.attente_deverouillage = {"direction": direction_choisie_par_joueur, "porte": porte}
                return "CODE_REQUIS"

            if objet_requis:
                self.sortie.afficher(
                    "succes",
                    f"Mécanisme activé ! Vous déverrouillez l'accès avec '{objet_requis.nom_affichage}'."
                )
            porte["est_verrouillee"] = False

        self.salle_precedente = self.salle_actuelle
        self.salle_actuelle = porte["salle_de_destination"]
        return "DEPLACEMENT_OK"

    def valider_code(self, code_saisi):
        if not self.attente_deverouillage:
            return "AUCUNE_ATTENTE"

        porte = self.attente_deverouillage["porte"]

        if code_saisi == porte["code_requis"]:
            porte["est_verrouillee"] = False
            self.sortie.afficher("succes", "Code accepté ! La porte se déverrouille.")
            self.salle_precedente = self.salle_actuelle
            self.salle_actuelle = porte["salle_de_destination"]
            self.attente_deverouillage = None
            return "DEPLACEMENT_OK"
        else:
            self.sortie.afficher("erreur", "Code erroné.")
            self.attente_deverouillage = None
            return "CODE_ERRONE"

    def annuler_saisie_code(self):
        self.attente_deverouillage = None

    # ------------------------------------------------------------------
    # Fouille de meuble
    # ------------------------------------------------------------------
    def fouiller_un_meuble(self, nom_du_meuble_a_fouiller):
        if nom_du_meuble_a_fouiller in self.salle_actuelle.dictionnaire_des_meubles_presents:
            meuble = self.salle_actuelle.dictionnaire_des_meubles_presents[nom_du_meuble_a_fouiller]
            if meuble.dictionnaire_des_objets_contenus:
                self.sortie.afficher("succes", f"Vous fouillez '{meuble.nom_affichage}' et trouvez :", son=meuble.materiau)
                for nom_objet, objet in meuble.dictionnaire_des_objets_contenus.items():
                    self.sortie.afficher("info", f"  - {objet.nom_affichage}")
                    self.salle_actuelle.ajouter_un_objet(objet)
                meuble.dictionnaire_des_objets_contenus.clear()
                return "FOUILLE_OK"
            else:
                self.sortie.afficher("info", f"Vous avez déjà fouillé '{meuble.nom_affichage}' ou il est vide.")
                return "DEJA_FOUILLE"
        else:
            self.sortie.afficher("erreur", "Il n'y a rien de tel ici.")
            return "MEUBLE_INTROUVABLE"