import time
import math
import random
import struct
import pygame

from theme import ThemeVisuel as T


# ======================================================================
# 0. GÉNÉRATEUR DE SONS — synthèse pure, aucun fichier audio externe
# ======================================================================
class GenerateurSon:
    """
    Génère de courts bips/mélodies et une ambiance en boucle, entièrement en
    mémoire (ondes calculées à la main), et les joue via pygame.mixer. Aucun
    fichier .wav/.mp3 n'est lu ni téléchargé : tout est calculé au lancement,
    donc ça fonctionne immédiatement après un simple `pip install pygame`.

    Si aucune sortie audio n'est disponible sur la machine (ou si le mixer
    échoue à s'initialiser), le jeu continue simplement sans son.
    """

    FREQUENCE_ECHANTILLONNAGE = 22050

    # nom_evenement -> (notes [(fréquence_Hz, durée_s), ...], volume, forme d'onde)
    DEFINITIONS = {
        "succes":   ([(523, 0.07), (659, 0.07), (784, 0.12)], 0.30, "sinus"),
        "erreur":   ([(220, 0.11), (175, 0.16)], 0.30, "carre"),
        "indice":   ([(880, 0.06), (1046, 0.10)], 0.22, "sinus"),
        "victoire": ([(523, 0.11), (659, 0.11), (784, 0.11), (1047, 0.28)], 0.35, "sinus"),
        "tac":      ([(320, 0.025)], 0.16, "carre"),  # léger, générique : repli si matériau inconnu
    }

    # materiau -> (durée_s, volume, freq_debut, freq_fin, proportion_de_bruit, forme)
    # Chaque "texture" mélange un ton qui glisse (grincement) avec du bruit filtré,
    # sous une enveloppe qui décroît vite (effet "impact" + résonance courte).
    TEXTURES = {
        "bois":         (0.32, 0.26, 210, 145, 0.35, "sinus"),   # grincement de bois
        "metal":        (0.26, 0.30, 520, 360, 0.15, "carre"),   # clang métallique
        "cuir":         (0.22, 0.20, 165, 130, 0.55, "sinus"),   # craquement de vieux cuir
        "electronique": (0.16, 0.20, 900, 1300, 0.05, "carre"),  # petit bip numérique
    }

    def __init__(self):
        self.disponible = False
        self._cache = {}
        self.volume_effets = 0.75  # multiplicateur global, réglable depuis les paramètres en jeu
        try:
            pygame.mixer.init(frequency=self.FREQUENCE_ECHANTILLONNAGE, size=-16, channels=1)
            self.disponible = True
        except Exception:
            self.disponible = False

    # ------------------------------------------------------------------
    # Bips courts (succès / erreur / indice / victoire / tac)
    # ------------------------------------------------------------------
    def _generer_ton(self, frequence_hz, duree_s, volume, forme):
        nb_echantillons = max(1, int(self.FREQUENCE_ECHANTILLONNAGE * duree_s))
        fondu_echant = max(1, min(nb_echantillons // 4, int(0.015 * self.FREQUENCE_ECHANTILLONNAGE)))
        valeurs = []
        for i in range(nb_echantillons):
            t = i / self.FREQUENCE_ECHANTILLONNAGE
            phase = 2 * math.pi * frequence_hz * t
            if forme == "carre":
                brute = 1.0 if math.sin(phase) >= 0 else -1.0
            else:
                brute = math.sin(phase)
            enveloppe = 1.0
            if i < fondu_echant:
                enveloppe = i / fondu_echant
            elif i > nb_echantillons - fondu_echant:
                enveloppe = (nb_echantillons - i) / fondu_echant
            echantillon = int(brute * enveloppe * volume * 32767)
            valeurs.append(max(-32768, min(32767, echantillon)))
        return struct.pack("<%dh" % len(valeurs), *valeurs)

    def _construire_son(self, notes, volume, forme):
        morceaux = [self._generer_ton(freq, duree, volume, forme) for freq, duree in notes]
        return pygame.mixer.Sound(buffer=b"".join(morceaux))

    # ------------------------------------------------------------------
    # Textures de matériaux (bruits de meubles : bois / métal / cuir / électronique)
    # ------------------------------------------------------------------
    def _generer_texture(self, duree_s, volume, freq_debut, freq_fin, proportion_bruit, forme):
        nb = max(1, int(self.FREQUENCE_ECHANTILLONNAGE * duree_s))
        fondu = max(1, min(nb // 4, int(0.02 * self.FREQUENCE_ECHANTILLONNAGE)))
        valeurs = []
        phase = 0.0
        bruit_filtre = 0.0
        for i in range(nb):
            progression = i / nb
            freq_instant = freq_debut + (freq_fin - freq_debut) * progression
            phase += 2 * math.pi * freq_instant / self.FREQUENCE_ECHANTILLONNAGE
            ton = (1.0 if math.sin(phase) >= 0 else -1.0) if forme == "carre" else math.sin(phase)

            bruit_brut = random.uniform(-1.0, 1.0)
            bruit_filtre += 0.25 * (bruit_brut - bruit_filtre)  # passe-bas simple -> bruit plus "sourd"

            brute = ton * (1 - proportion_bruit) + bruit_filtre * proportion_bruit

            enveloppe = 1.0
            if i < fondu:
                enveloppe = i / fondu
            elif i > nb - fondu:
                enveloppe = (nb - i) / fondu
            decroissance = math.exp(-3.0 * progression)  # effet "impact puis résonance qui s'éteint"

            echantillon = int(brute * enveloppe * decroissance * volume * 32767)
            valeurs.append(max(-32768, min(32767, echantillon)))
        return struct.pack("<%dh" % len(valeurs), *valeurs)

    def jouer(self, nom_evenement):
        if not self.disponible:
            return
        if nom_evenement in self.DEFINITIONS:
            if nom_evenement not in self._cache:
                notes, volume, forme = self.DEFINITIONS[nom_evenement]
                try:
                    self._cache[nom_evenement] = self._construire_son(notes, volume, forme)
                except Exception:
                    self.disponible = False
                    return
            son = self._cache[nom_evenement]
            son.set_volume(self.volume_effets)
            son.play()
        elif nom_evenement in self.TEXTURES:
            if nom_evenement not in self._cache:
                try:
                    self._cache[nom_evenement] = pygame.mixer.Sound(buffer=self._generer_texture(*self.TEXTURES[nom_evenement]))
                except Exception:
                    self.disponible = False
                    return
            son = self._cache[nom_evenement]
            son.set_volume(self.volume_effets)
            son.play()
        # sinon : matériau/évènement inconnu -> silence plutôt qu'une erreur

    # ------------------------------------------------------------------
    # Ambiance en boucle (nappe sonore discrète, sinueuse)
    # ------------------------------------------------------------------
    def _generer_ambiance(self, duree_s=48):
        """
        Composition d'ambiance sombre et sinueuse, en boucle SANS à-coup :
          - une nappe grave à 4 oscillateurs légèrement dissonants, chacun modulé
            par un LFO d'amplitude lent à nombre ENTIER de cycles sur la durée
            totale -> la phase de chaque composant retombe exactement sur son
            point de départ à la fin du buffer, donc le bouclage est inaudible ;
          - un motif mélodique épars et grave : quelques notes isolées qui
            apparaissent et s'effacent en douceur (fenêtre en cosinus, donc
            chaque note commence ET finit à zéro : aucune coupure possible,
            où qu'elle tombe dans le morceau) ;
          - un très léger voile de bruit filtré (façon vent lointain), estompé
            aux deux extrémités du buffer pour ne jamais créer de claquement
            au point de bouclage.
        """
        # (fréquence_Hz, nb entier de cycles du LFO d'amplitude sur la durée totale)
        oscillateurs = [
            (55, 3),
            (82, 5),
            (130, 7),
            (174, 11),
        ]
        # (instant de départ_s, fréquence_Hz, durée_s, volume au pic) — notes éparses, dissonantes
        notes_motif = [
            (4.0, 220, 3.0, 0.11),
            (11.0, 233, 2.5, 0.09),
            (17.5, 196, 3.2, 0.11),
            (24.0, 246, 2.8, 0.09),
            (30.5, 220, 3.0, 0.11),
            (37.0, 261, 2.5, 0.08),
            (43.0, 196, 3.5, 0.12),
        ]

        nb = int(self.FREQUENCE_ECHANTILLONNAGE * duree_s)
        taper_bruit_echant = int(1.0 * self.FREQUENCE_ECHANTILLONNAGE)  # 1s de fondu, aux 2 bords, pour le bruit uniquement
        bruit_filtre = 0.0
        valeurs = []

        for i in range(nb):
            t = i / self.FREQUENCE_ECHANTILLONNAGE

            # --- Nappe continue (parfaitement périodique par construction) ---
            drone = 0.0
            for freq, cycles_lfo in oscillateurs:
                ton = math.sin(2 * math.pi * freq * t)
                lfo = 0.5 + 0.5 * math.sin(2 * math.pi * (cycles_lfo / duree_s) * t)
                drone += ton * lfo
            drone = (drone / len(oscillateurs)) * 0.55

            # --- Motif épars (chaque note démarre et finit à zéro : jamais de coupure) ---
            motif = 0.0
            for depart, freq, duree_note, volume_pic in notes_motif:
                if depart <= t < depart + duree_note:
                    local_t = t - depart
                    enveloppe = 0.5 * (1 - math.cos(2 * math.pi * local_t / duree_note))
                    motif += math.sin(2 * math.pi * freq * t) * enveloppe * volume_pic

            # --- Voile de bruit, estompé aux bords pour rester sans à-coup au bouclage ---
            bruit_brut = random.uniform(-1.0, 1.0)
            bruit_filtre += 0.05 * (bruit_brut - bruit_filtre)
            enveloppe_bord = 1.0
            if i < taper_bruit_echant:
                enveloppe_bord = i / taper_bruit_echant
            elif i > nb - taper_bruit_echant:
                enveloppe_bord = (nb - i) / taper_bruit_echant
            bruit = bruit_filtre * 0.05 * enveloppe_bord

            total = drone + motif + bruit
            echantillon = int(total * 32767)
            valeurs.append(max(-32768, min(32767, echantillon)))

        return struct.pack("<%dh" % len(valeurs), *valeurs)

    def obtenir_ambiance(self):
        if not self.disponible:
            return None
        if "_ambiance" not in self._cache:
            try:
                self._cache["_ambiance"] = pygame.mixer.Sound(buffer=self._generer_ambiance())
            except Exception:
                self.disponible = False
                return None
        return self._cache["_ambiance"]


# ======================================================================
# 1. INTERFACE DE SORTIE — remplace print()/input() dans joueur.py
# ======================================================================
class InterfaceSortiePygame:
    """
    Implémentation graphique de l'interface de sortie attendue par Joueur.
    Ne contient AUCUNE règle de jeu : uniquement de la présentation (et,
    en plus, un petit bip synthétique selon le type de message).
    """

    def __init__(self, taille_historique=200):
        self.messages = []          # liste de (type, texte, timestamp)
        self.taille_historique = taille_historique
        self.sons = GenerateurSon()

    def afficher(self, type_message, texte, son=None):
        self.messages.append((type_message, texte, time.time()))
        if len(self.messages) > self.taille_historique:
            self.messages.pop(0)
        # Par défaut : succès/erreur déclenchent leur son habituel. `son=` permet de
        # remplacer ce comportement (ex: un simple "tac" léger pour fouiller/ramasser,
        # en gardant la fanfare de succès réservée aux vraies validations : codes, portes).
        nom_son = son if son is not None else (type_message if type_message in ("succes", "erreur") else None)
        if nom_son:
            self.sons.jouer(nom_son)

    def jouer_son(self, nom_evenement):
        """Permet au contrôleur de déclencher un son qui n'est pas lié à un message (indice, victoire...)."""
        self.sons.jouer(nom_evenement)

    def couleur_pour_type(self, type_message):
        return {
            "succes": T.ACCENT_VERT,
            "erreur": T.ACCENT_ROUGE,
            "info": T.ACCENT_MAGENTA,
        }.get(type_message, T.TEXTE_PRINCIPAL)


# ======================================================================
# 2. CONTRÔLEUR — LE PONT entre les clics souris et le moteur logique
# ======================================================================
class ControleurDeJeu:
    """
    Seul point de contact entre l'UI Pygame et le moteur (Joueur/Salle/...).
    Aucune règle de jeu ici : uniquement des appels aux méthodes existantes
    de Joueur, et la gestion d'état propre à l'UI (sélection en cours,
    générateur, condition de victoire).
    """

    def __init__(self, joueur, sortie, salle_serveur, salle_repli_si_pas_alimente):
        self.joueur = joueur
        self.sortie = sortie
        self.salle_serveur = salle_serveur
        self.salle_repli = salle_repli_si_pas_alimente

        self.generateur_actif = False
        self.selection_combinaison = None   # nom d'objet en attente d'une 2e sélection
        self.modale_code_ouverte = False
        self.jeu_termine = False
        self.jeu_gagne = False

        # Meubles "activables" génériques (au-delà du Générateur historique du niveau 1) :
        # nom_meuble -> {"objet_requis": Objet|None, "message_ok": str, "message_manque": str,
        #                "portes_a_deverouiller": [dict_porte, ...], "victoire": bool}
        # Rempli depuis main.py une fois le monde construit (permet de référencer les vraies portes).
        self.meubles_activables = {}

    # ---- Déplacement -------------------------------------------------
    def on_click_sortie(self, direction):
        if self.modale_code_ouverte or self.jeu_termine:
            return
        resultat = self.joueur.se_deplacer(direction)
        if resultat == "CODE_REQUIS":
            self.modale_code_ouverte = True
        else:
            self._verifier_arrivee_serveur()

    def on_soumission_code(self, code_saisi):
        self.joueur.valider_code(code_saisi)
        self.modale_code_ouverte = False
        self._verifier_arrivee_serveur()

    def on_annulation_modale_code(self):
        self.joueur.annuler_saisie_code()
        self.modale_code_ouverte = False

    # ---- Indices -------------------------------------------------
    def on_demande_indice(self):
        if self.modale_code_ouverte or self.jeu_termine:
            return
        salle = self.joueur.salle_actuelle
        indice = getattr(salle, "indice_de_la_salle", "") or "Aucun indice n'est nécessaire ici."
        self.sortie.afficher("info", f"[Indice] {indice}")
        self.sortie.jouer_son("indice")

    def _verifier_arrivee_serveur(self):
        if self.joueur.salle_actuelle is not self.salle_serveur:
            return
        if self.generateur_actif:
            self.sortie.afficher("succes", "Les serveurs redémarrent avec succès ! Un accès inattendu s'ouvre non loin.")
        else:
            self.sortie.afficher("erreur", "Erreur : aucune alimentation électrique détectée.")
            self.sortie.afficher("info", "Il faut activer le générateur principal ! Retour au couloir.")
            self.joueur.salle_precedente = self.joueur.salle_actuelle
            self.joueur.salle_actuelle = self.salle_repli

    # ---- Meubles -------------------------------------------------
    def on_click_meuble(self, nom_meuble):
        if self.modale_code_ouverte or self.jeu_termine:
            return
        if nom_meuble == "Generateur":
            if self.generateur_actif:
                self.sortie.afficher("info", "Le générateur est déjà actif.")
            elif "Fusible" not in self.joueur.inventaire_du_joueur:
                self.sortie.afficher("erreur", "Le tableau électrique claque : il manque un fusible en état de marche.")
            else:
                self.generateur_actif = True
                self.sortie.afficher("succes", "Vous installez le fusible et activez le Générateur. Un bourdonnement sourd résonne dans le complexe.")
            return

        if nom_meuble in self.meubles_activables:
            config = self.meubles_activables[nom_meuble]
            if config.get("_actif"):
                self.sortie.afficher("info", "Ce mécanisme est déjà activé.")
                return
            objet_requis = config.get("objet_requis")
            if objet_requis and objet_requis.nom_de_objet not in self.joueur.inventaire_du_joueur:
                self.sortie.afficher("erreur", config["message_manque"])
                return
            config["_actif"] = True
            self.sortie.afficher("succes", config["message_ok"])
            for porte in config.get("portes_a_deverouiller", []):
                porte["est_verrouillee"] = False
            if config.get("victoire"):
                self.jeu_termine = True
                self.jeu_gagne = True
                self.sortie.jouer_son("victoire")
            return

        self.joueur.fouiller_un_meuble(nom_meuble)

    # ---- Objets au sol -------------------------------------------------
    def on_click_objet_salle(self, nom_objet):
        if self.modale_code_ouverte or self.jeu_termine:
            return
        self.joueur.ramasser_un_objet(nom_objet)

    # ---- Inventaire -------------------------------------------------
    def on_clic_gauche_inventaire(self, nom_objet):
        if self.modale_code_ouverte or self.jeu_termine:
            return
        if self.selection_combinaison is None:
            self.selection_combinaison = nom_objet
            self.sortie.afficher("info", f"'{nom_objet}' sélectionné. Cliquez un second objet pour combiner (clic droit pour lire).")
        elif self.selection_combinaison == nom_objet:
            self.selection_combinaison = None
        else:
            self.joueur.combiner_objets(self.selection_combinaison, nom_objet)
            self.selection_combinaison = None

    def on_clic_droit_inventaire(self, nom_objet):
        if self.modale_code_ouverte or self.jeu_termine:
            return
        self.joueur.lire_un_objet(nom_objet)
        self.selection_combinaison = None


# ======================================================================
# 3. PANEL DE BASE
# ======================================================================
class Panel:
    """Classe abstraite : dessine une zone et sait dire ce qu'il y a sous un point."""

    def __init__(self):
        self.zones_cliquables = {}   # nom_logique -> pygame.Rect

    def dessiner(self, surface, rect, contexte):
        raise NotImplementedError

    def detecter_clic(self, pos):
        for nom, zone_rect in self.zones_cliquables.items():
            if zone_rect.collidepoint(pos):
                return nom
        return None


# ======================================================================
# 4. PANEL SALLE — description + sorties cliquables
# ======================================================================
class PanelSalle(Panel):
    def dessiner(self, surface, rect, contexte):
        self.zones_cliquables.clear()
        salle = contexte.joueur.salle_actuelle

        T.dessiner_panel(surface, rect, titre=salle.nom_de_la_salle)

        # Bouton discret d'indice, en haut à droite du panel
        bouton_indice = pygame.Rect(rect.right - 130, rect.y + 12, 114, 30)
        T.dessiner_bouton(surface, bouton_indice, "💡 Indice", couleur_accent=T.ACCENT_JAUNE)
        self.zones_cliquables["__indice__"] = bouton_indice

        police_desc = T.police(max(14, rect.height // 24))
        y = rect.y + 50
        for ligne in self._decouper_texte(salle.description_de_la_salle, police_desc, rect.width - 40):
            surface.blit(police_desc.render(ligne, True, T.TEXTE_PRINCIPAL), (rect.x + 20, y))
            y += police_desc.get_height() + 4

        # Sorties cliquables, réparties en lignes (partant du bas du panel)
        # Le nom affiché est celui de la SALLE DE DESTINATION (plus clair que "est"/"ouest"
        # pour un nouveau joueur) ; la direction technique reste la clé interne inchangée.
        sorties = list(salle.dictionnaire_des_sorties_possibles.keys())
        if sorties:
            largeur_min = 150
            hauteur_bouton = 56
            marge = 10
            largeur_disponible = rect.width - 40
            colonnes = max(1, min(len(sorties), largeur_disponible // (largeur_min + marge)))
            largeur_bouton = min(220, (largeur_disponible - (colonnes - 1) * marge) // colonnes)
            nb_lignes = -(-len(sorties) // colonnes)  # arrondi supérieur
            y_premiere_ligne = rect.bottom - 20 - nb_lignes * hauteur_bouton - (nb_lignes - 1) * marge

            police_bouton = T.police(13)

            for index, direction in enumerate(sorties):
                col = index % colonnes
                ligne = index // colonnes
                x = rect.x + 20 + col * (largeur_bouton + marge)
                y = y_premiere_ligne + ligne * (hauteur_bouton + marge)
                porte = salle.dictionnaire_des_sorties_possibles[direction]
                bouton_rect = pygame.Rect(x, y, largeur_bouton, hauteur_bouton)

                verrouillee = porte["est_verrouillee"]
                salle_destination = porte["salle_de_destination"]
                vient_de_la = (contexte.joueur.salle_precedente is salle_destination)

                texte_nom = ("🔒 " if verrouillee else "") + salle_destination.nom_de_la_salle
                lignes_texte = self._decouper_deux_lignes(texte_nom, police_bouton, largeur_bouton - 16)

                if vient_de_la:
                    fond, bordure, largeur_bordure = T.FOND_SLOT, T.ACCENT_VERT, 2
                elif verrouillee:
                    fond, bordure, largeur_bordure = T.FOND_SLOT, T.ACCENT_ROUGE, 1
                else:
                    fond, bordure, largeur_bordure = T.FOND_SLOT, T.ACCENT_CYAN, 1

                pygame.draw.rect(surface, fond, bouton_rect, border_radius=6)
                pygame.draw.rect(surface, bordure, bouton_rect, width=largeur_bordure, border_radius=6)

                couleur_texte = T.ACCENT_VERT if vient_de_la else T.TEXTE_PRINCIPAL
                hauteur_ligne = police_bouton.get_height()
                y_texte = bouton_rect.centery - (len(lignes_texte) * hauteur_ligne) // 2
                for i, ligne_texte in enumerate(lignes_texte):
                    rendu = police_bouton.render(ligne_texte, True, couleur_texte)
                    surface.blit(rendu, rendu.get_rect(center=(bouton_rect.centerx, y_texte + i * hauteur_ligne + hauteur_ligne // 2)))

                if vient_de_la:
                    police_retour = T.police(10)
                    rendu_retour = police_retour.render("↩ vous venez de là", True, T.ACCENT_VERT)
                    surface.blit(rendu_retour, (bouton_rect.x + 6, bouton_rect.y + 3))

                self.zones_cliquables[direction] = bouton_rect

    @staticmethod
    def _decouper_deux_lignes(texte, police, largeur_max):
        mots = texte.split(" ")
        lignes, courante = [], ""
        for mot in mots:
            essai = f"{courante} {mot}".strip()
            if police.size(essai)[0] > largeur_max and courante:
                lignes.append(courante)
                courante = mot
                if len(lignes) == 2:
                    break
            else:
                courante = essai
        if courante and len(lignes) < 2:
            lignes.append(courante)
        if len(lignes) == 2 and police.size(lignes[1])[0] > largeur_max:
            while lignes[1] and police.size(lignes[1] + "…")[0] > largeur_max:
                lignes[1] = lignes[1][:-1]
            lignes[1] += "…"
        return lignes[:2]

    @staticmethod
    def _decouper_texte(texte, police, largeur_max):
        mots = texte.split(" ")
        lignes, ligne_courante = [], ""
        for mot in mots:
            essai = f"{ligne_courante} {mot}".strip()
            if police.size(essai)[0] > largeur_max and ligne_courante:
                lignes.append(ligne_courante)
                ligne_courante = mot
            else:
                ligne_courante = essai
        if ligne_courante:
            lignes.append(ligne_courante)
        return lignes


# ======================================================================
# 5. PANEL MEUBLES + OBJETS AU SOL (zone centrale d'interaction)
# ======================================================================
class PanelInteractionsSalle(Panel):
    HAUTEUR_CARTE = 46
    MARGE_CARTE = 8

    def __init__(self):
        super().__init__()
        self.scroll_meubles = 0
        self.scroll_objets = 0
        self._max_scroll_meubles = 0
        self._max_scroll_objets = 0
        self._zone_meubles = None
        self._zone_objets = None

    def defiler(self, pos, delta):
        """Fait défiler la colonne (meubles ou objets) survolée par la souris."""
        if self._zone_meubles and self._zone_meubles.collidepoint(pos):
            self.scroll_meubles = max(0, min(self._max_scroll_meubles, self.scroll_meubles - delta))
        elif self._zone_objets and self._zone_objets.collidepoint(pos):
            self.scroll_objets = max(0, min(self._max_scroll_objets, self.scroll_objets - delta))

    def dessiner(self, surface, rect, contexte):
        self.zones_cliquables.clear()
        salle = contexte.joueur.salle_actuelle
        T.dessiner_panel(surface, rect, titre="Éléments de la pièce")

        souris = pygame.mouse.get_pos()
        pas_carte = self.HAUTEUR_CARTE + self.MARGE_CARTE
        largeur_carte = (rect.width - 60) // 2
        x_meubles = rect.x + 20
        x_objets = rect.x + 40 + largeur_carte

        y_entetes = rect.y + 50
        police = T.police(15)
        surface.blit(police.render("MEUBLES (clic = fouiller)", True, T.TEXTE_SECONDAIRE), (x_meubles, y_entetes))
        surface.blit(police.render("OBJETS AU SOL (clic = ramasser)", True, T.TEXTE_SECONDAIRE), (x_objets, y_entetes))
        y_liste = y_entetes + 28

        zone_meubles = pygame.Rect(x_meubles, y_liste, largeur_carte, rect.bottom - y_liste - 12)
        zone_objets = pygame.Rect(x_objets, y_liste, largeur_carte, rect.bottom - y_liste - 12)
        self._zone_meubles, self._zone_objets = zone_meubles, zone_objets

        meubles = list(salle.dictionnaire_des_meubles_presents.items())
        objets = list(salle.dictionnaire_des_objets_presents.items())

        lignes_visibles_meubles = max(1, zone_meubles.height // pas_carte)
        lignes_visibles_objets = max(1, zone_objets.height // pas_carte)
        self._max_scroll_meubles = max(0, len(meubles) - lignes_visibles_meubles)
        self._max_scroll_objets = max(0, len(objets) - lignes_visibles_objets)
        self.scroll_meubles = max(0, min(self.scroll_meubles, self._max_scroll_meubles))
        self.scroll_objets = max(0, min(self.scroll_objets, self._max_scroll_objets))

        clip_precedent = surface.get_clip()

        # --- Colonne meubles ---
        surface.set_clip(zone_meubles)
        for index in range(self.scroll_meubles, len(meubles)):
            nom_meuble, meuble = meubles[index]
            y = zone_meubles.y + (index - self.scroll_meubles) * pas_carte
            r = pygame.Rect(x_meubles, y, largeur_carte, self.HAUTEUR_CARTE)
            if r.bottom < zone_meubles.top or r.top > zone_meubles.bottom:
                continue
            vide = not meuble.dictionnaire_des_objets_contenus and nom_meuble not in ("Generateur", "TableauElectrique", "CoeurReacteur")
            couleur = T.TEXTE_DESACTIVE if vide else T.ACCENT_JAUNE
            T.dessiner_bouton(surface, r, meuble.nom_affichage, survole=r.collidepoint(souris), couleur_accent=couleur)
            if r.clip(zone_meubles).height >= r.height - 4:
                self.zones_cliquables[f"meuble::{nom_meuble}"] = r
        surface.set_clip(clip_precedent)

        # --- Colonne objets au sol ---
        surface.set_clip(zone_objets)
        for index in range(self.scroll_objets, len(objets)):
            nom_objet, objet = objets[index]
            y = zone_objets.y + (index - self.scroll_objets) * pas_carte
            r = pygame.Rect(x_objets, y, largeur_carte, self.HAUTEUR_CARTE)
            if r.bottom < zone_objets.top or r.top > zone_objets.bottom:
                continue
            T.dessiner_bouton(surface, r, objet.nom_affichage, survole=r.collidepoint(souris), couleur_accent=T.ACCENT_VERT)
            if r.clip(zone_objets).height >= r.height - 4:
                self.zones_cliquables[f"objet_salle::{nom_objet}"] = r
        surface.set_clip(clip_precedent)

        # --- Indicateurs de défilement discrets ---
        self._dessiner_indicateur_scroll(surface, zone_meubles, self.scroll_meubles, self._max_scroll_meubles, len(meubles), lignes_visibles_meubles)
        self._dessiner_indicateur_scroll(surface, zone_objets, self.scroll_objets, self._max_scroll_objets, len(objets), lignes_visibles_objets)

    @staticmethod
    def _dessiner_indicateur_scroll(surface, zone, scroll, max_scroll, total, visibles):
        if max_scroll <= 0:
            return
        piste = pygame.Rect(zone.right - 5, zone.y, 3, zone.height)
        pygame.draw.rect(surface, T.FOND_SLOT, piste, border_radius=2)
        proportion = visibles / max(1, total)
        hauteur_curseur = max(16, int(piste.height * proportion))
        position_relative = scroll / max_scroll
        y_curseur = piste.y + int((piste.height - hauteur_curseur) * position_relative)
        pygame.draw.rect(surface, T.ACCENT_JAUNE, pygame.Rect(piste.x, y_curseur, piste.width, hauteur_curseur), border_radius=2)

    def declencher(self, cle, controleur):
        prefixe, nom = cle.split("::", 1)
        if prefixe == "meuble":
            controleur.on_click_meuble(nom)
        elif prefixe == "objet_salle":
            controleur.on_click_objet_salle(nom)


# ======================================================================
# 6. PANEL INVENTAIRE — grille cliquable (clic gauche = sélection combinaison,
#    clic droit = lecture)
# ======================================================================
class PanelInventaire(Panel):
    TAILLE_SLOT = 92
    MARGE = 12
    HAUTEUR_DETAIL = 74
    ORDRE_TAGS = [None, "rouge", "vert", "bleu"]  # cycle au clic ; None = pas de marquage

    def __init__(self):
        super().__init__()
        self.scroll_lignes = 0       # index de la première ligne de la grille affichée
        self._max_scroll_lignes = 0  # recalculé à chaque dessin, utilisé pour clamper le défilement
        self.tags = {}               # nom_technique -> "rouge" | "vert" | "bleu" | None, choisi par le joueur
        self.zones_tags = {}         # nom_technique -> pygame.Rect (pastille cliquable dans le coin du slot)

    def defiler(self, delta):
        """delta > 0 = molette vers le haut (remonter), delta < 0 = molette vers le bas (descendre)."""
        self.scroll_lignes = max(0, min(self._max_scroll_lignes, self.scroll_lignes - delta))

    def detecter_zone_tag(self, pos):
        for nom_technique, zone_rect in self.zones_tags.items():
            if zone_rect.collidepoint(pos):
                return nom_technique
        return None

    def cycler_tag(self, nom_technique):
        """Fait passer le marquage couleur de l'objet à l'état suivant (choix libre du joueur)."""
        actuel = self.tags.get(nom_technique)
        index_suivant = (self.ORDRE_TAGS.index(actuel) + 1) % len(self.ORDRE_TAGS)
        nouveau = self.ORDRE_TAGS[index_suivant]
        if nouveau is None:
            self.tags.pop(nom_technique, None)
        else:
            self.tags[nom_technique] = nouveau

    @staticmethod
    def _couleur_tag(nom_tag):
        return {"rouge": T.ACCENT_ROUGE, "vert": T.ACCENT_VERT, "bleu": T.ACCENT_BLEU}.get(nom_tag)

    def dessiner(self, surface, rect, contexte):
        self.zones_cliquables.clear()
        self.zones_tags.clear()
        T.dessiner_panel(surface, rect, titre="Inventaire")

        zone_grille = pygame.Rect(rect.x, rect.y + 40, rect.width, rect.height - 40 - self.HAUTEUR_DETAIL)
        zone_detail = pygame.Rect(rect.x, rect.bottom - self.HAUTEUR_DETAIL, rect.width, self.HAUTEUR_DETAIL)

        # Tri alphabétique (insensible à la casse) sur le nom affiché, pour s'y retrouver facilement.
        objets = sorted(contexte.joueur.inventaire_du_joueur.items(), key=lambda paire: paire[1].nom_affichage.lower())
        colonnes = max(1, (rect.width - 20) // (self.TAILLE_SLOT + self.MARGE))
        pas_ligne = self.TAILLE_SLOT + self.MARGE

        total_lignes = max(1, (len(objets) + colonnes - 1) // colonnes)
        lignes_visibles = max(1, zone_grille.height // pas_ligne)
        self._max_scroll_lignes = max(0, total_lignes - lignes_visibles)
        self.scroll_lignes = max(0, min(self.scroll_lignes, self._max_scroll_lignes))

        souris = pygame.mouse.get_pos()
        objet_survole = None

        police_nom = T.police(12, gras=True)
        police_icone = T.police(26, gras=True)

        clip_precedent = surface.get_clip()
        surface.set_clip(zone_grille)

        premier_index_visible = self.scroll_lignes * colonnes
        for index in range(premier_index_visible, len(objets)):
            nom_technique, objet = objets[index]
            col = index % colonnes
            ligne_relative = (index // colonnes) - self.scroll_lignes
            x = rect.x + 16 + col * pas_ligne
            y = zone_grille.y + 6 + ligne_relative * pas_ligne
            slot_rect = pygame.Rect(x, y, self.TAILLE_SLOT, self.TAILLE_SLOT)

            if slot_rect.bottom < zone_grille.y or slot_rect.top > zone_grille.bottom:
                continue

            survole = slot_rect.collidepoint(souris) and zone_grille.collidepoint(souris)
            if survole:
                objet_survole = objet

            couleur_tag = self._couleur_tag(self.tags.get(nom_technique))
            selectionne = (contexte.selection_combinaison == nom_technique)
            if selectionne:
                fond, bordure, largeur_bordure = T.FOND_SLOT_ACTIF, T.ACCENT_CYAN, 2
            elif survole:
                fond, bordure, largeur_bordure = T.FOND_SLOT_HOVER, T.BORDURE_CLAIRE, 2
            elif couleur_tag:
                fond, bordure, largeur_bordure = T.FOND_SLOT, couleur_tag, 2
            else:
                fond, bordure, largeur_bordure = T.FOND_SLOT, T.BORDURE, 1

            pygame.draw.rect(surface, fond, slot_rect, border_radius=8)
            pygame.draw.rect(surface, bordure, slot_rect, width=largeur_bordure, border_radius=8)

            couleur_icone = T.ACCENT_CYAN if (selectionne or survole) else T.TEXTE_SECONDAIRE
            initiale = police_icone.render(objet.nom_affichage[0].upper(), True, couleur_icone)
            surface.blit(initiale, initiale.get_rect(center=(slot_rect.centerx, slot_rect.top + 30)))

            for i, ligne_texte in enumerate(self._decouper_deux_lignes(objet.nom_affichage, police_nom, self.TAILLE_SLOT - 12)):
                texte_rendu = police_nom.render(ligne_texte, True, T.TEXTE_PRINCIPAL)
                surface.blit(texte_rendu, texte_rendu.get_rect(center=(slot_rect.centerx, slot_rect.bottom - 26 + i * 15)))

            # Pastille de marquage couleur, en haut à gauche du slot — cliquable, choix libre du joueur
            pastille_rect = pygame.Rect(slot_rect.x + 5, slot_rect.y + 5, 14, 14)
            if couleur_tag:
                pygame.draw.circle(surface, couleur_tag, pastille_rect.center, 7)
                pygame.draw.circle(surface, T.FOND_PANEL, pastille_rect.center, 7, width=1)
            else:
                pygame.draw.circle(surface, T.TEXTE_DESACTIVE, pastille_rect.center, 6, width=1)

            # Seuls les slots réellement visibles sont cliquables (évite de cliquer à travers le clip)
            zone_visible = slot_rect.clip(zone_grille)
            if zone_visible.height >= slot_rect.height - 4:
                self.zones_cliquables[nom_technique] = slot_rect
                # zone de clic de la pastille un peu plus large que son dessin, pour rester facile à viser
                self.zones_tags[nom_technique] = pastille_rect.inflate(10, 10)

        surface.set_clip(clip_precedent)

        # Indicateur de défilement discret (barre verticale à droite de la grille)
        if self._max_scroll_lignes > 0:
            piste = pygame.Rect(zone_grille.right - 6, zone_grille.y, 4, zone_grille.height)
            pygame.draw.rect(surface, T.FOND_SLOT, piste, border_radius=2)
            proportion = lignes_visibles / total_lignes
            hauteur_curseur = max(20, int(piste.height * proportion))
            position_relative = self.scroll_lignes / self._max_scroll_lignes if self._max_scroll_lignes else 0
            y_curseur = piste.y + int((piste.height - hauteur_curseur) * position_relative)
            curseur = pygame.Rect(piste.x, y_curseur, piste.width, hauteur_curseur)
            pygame.draw.rect(surface, T.ACCENT_CYAN, curseur, border_radius=2)

        # --- Zone de détail : objet survolé, sinon objet sélectionné pour combinaison ---
        pygame.draw.line(surface, T.BORDURE, (rect.x + 12, zone_detail.y), (rect.right - 12, zone_detail.y), 1)
        police_titre = T.police(15, gras=True)
        police_desc = T.police(12)

        cible = objet_survole
        if cible is None and contexte.selection_combinaison in contexte.joueur.inventaire_du_joueur:
            cible = contexte.joueur.inventaire_du_joueur[contexte.selection_combinaison]

        if cible:
            surface.blit(police_titre.render(cible.nom_affichage, True, T.ACCENT_CYAN), (zone_detail.x + 16, zone_detail.y + 8))
            for i, ligne_texte in enumerate(self._decouper_texte(cible.description_de_objet, police_desc, rect.width - 32)[:2]):
                surface.blit(police_desc.render(ligne_texte, True, T.TEXTE_SECONDAIRE), (zone_detail.x + 16, zone_detail.y + 30 + i * 16))
        elif not objets:
            surface.blit(police_desc.render("Votre inventaire est vide pour l'instant.", True, T.TEXTE_DESACTIVE),
                         (zone_detail.x + 16, zone_detail.y + 24))
        else:
            surface.blit(police_desc.render("Survolez un objet, ou cliquez la pastille pour le marquer d'une couleur.", True, T.TEXTE_DESACTIVE),
                         (zone_detail.x + 16, zone_detail.y + 24))

    @staticmethod
    def _decouper_deux_lignes(texte, police, largeur_max):
        mots = texte.split(" ")
        lignes, courante = [], ""
        for mot in mots:
            essai = f"{courante} {mot}".strip()
            if police.size(essai)[0] > largeur_max and courante:
                lignes.append(courante)
                courante = mot
                if len(lignes) == 2:
                    break
            else:
                courante = essai
        if courante and len(lignes) < 2:
            lignes.append(courante)
        if len(lignes) == 2 and police.size(lignes[1])[0] > largeur_max:
            while lignes[1] and police.size(lignes[1] + "…")[0] > largeur_max:
                lignes[1] = lignes[1][:-1]
            lignes[1] += "…"
        return lignes[:2]

    @staticmethod
    def _decouper_texte(texte, police, largeur_max):
        mots = texte.split(" ")
        lignes, courante = [], ""
        for mot in mots:
            essai = f"{courante} {mot}".strip()
            if police.size(essai)[0] > largeur_max and courante:
                lignes.append(courante)
                courante = mot
            else:
                courante = essai
        if courante:
            lignes.append(courante)
        return lignes

    def declencher(self, nom_objet, controleur, bouton_souris):
        if bouton_souris == 1:
            controleur.on_clic_gauche_inventaire(nom_objet)
        elif bouton_souris == 3:
            controleur.on_clic_droit_inventaire(nom_objet)


# ======================================================================
# 7. PANEL LOG — remplace la console
# ======================================================================
class PanelLog(Panel):
    def __init__(self):
        super().__init__()
        self.scroll_messages = 0        # 0 = au plus récent ; augmente en remontant dans l'historique
        self._max_scroll_messages = 0

    def defiler(self, delta):
        """delta > 0 = molette vers le haut (voir les messages plus anciens)."""
        self.scroll_messages = max(0, min(self._max_scroll_messages, self.scroll_messages + delta))

    def dessiner(self, surface, rect, contexte):
        T.dessiner_panel(surface, rect, titre="Journal de bord")
        police = T.police(14)
        ligne_hauteur = police.get_height() + 6
        zone_texte = pygame.Rect(rect.x, rect.y + 46, rect.width, rect.height - 56)
        nb_lignes_visibles = max(1, zone_texte.height // ligne_hauteur)

        tous_les_messages = contexte.sortie.messages
        self._max_scroll_messages = max(0, len(tous_les_messages) - nb_lignes_visibles)
        self.scroll_messages = max(0, min(self.scroll_messages, self._max_scroll_messages))

        fin = len(tous_les_messages) - self.scroll_messages
        debut = max(0, fin - nb_lignes_visibles)
        messages_visibles = tous_les_messages[debut:fin]

        clip_precedent = surface.get_clip()
        surface.set_clip(zone_texte)
        y = zone_texte.y
        for type_message, texte, _ts in messages_visibles:
            couleur = contexte.sortie.couleur_pour_type(type_message)
            surface.blit(police.render(f"› {texte}", True, couleur), (rect.x + 16, y))
            y += ligne_hauteur
        surface.set_clip(clip_precedent)

        if self.scroll_messages > 0:
            police_indic = T.police(11)
            texte_indic = "▲ messages plus anciens — molette pour remonter"
            surface.blit(police_indic.render(texte_indic, True, T.TEXTE_SECONDAIRE), (rect.x + 16, rect.y + 26))

        if self._max_scroll_messages > 0:
            piste = pygame.Rect(rect.right - 10, zone_texte.y, 4, zone_texte.height)
            pygame.draw.rect(surface, T.FOND_SLOT, piste, border_radius=2)
            proportion = nb_lignes_visibles / max(1, len(tous_les_messages))
            hauteur_curseur = max(20, int(piste.height * proportion))
            position_relative = 1 - (self.scroll_messages / self._max_scroll_messages if self._max_scroll_messages else 0)
            y_curseur = piste.y + int((piste.height - hauteur_curseur) * position_relative)
            pygame.draw.rect(surface, T.ACCENT_CYAN, pygame.Rect(piste.x, y_curseur, piste.width, hauteur_curseur), border_radius=2)


# ======================================================================
# 8. MODALE DE SAISIE DE CODE — remplace l'ancien input()
# ======================================================================
class ModaleCode:
    def __init__(self):
        self.texte_saisi = ""

    def gerer_evenement(self, event, controleur):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                controleur.on_soumission_code(self.texte_saisi)
                self.texte_saisi = ""
            elif event.key == pygame.K_ESCAPE:
                controleur.on_annulation_modale_code()
                self.texte_saisi = ""
            elif event.key == pygame.K_BACKSPACE:
                self.texte_saisi = self.texte_saisi[:-1]
            elif event.unicode.isprintable() and len(self.texte_saisi) < 12:
                self.texte_saisi += event.unicode

    def dessiner(self, surface, largeur_ecran, hauteur_ecran):
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 160))
        surface.blit(voile, (0, 0))

        largeur, hauteur = 420, 180
        rect = pygame.Rect((largeur_ecran - largeur) // 2, (hauteur_ecran - hauteur) // 2, largeur, hauteur)
        T.dessiner_panel(surface, rect, titre="Digicode requis", bordure_accent=True)

        police = T.police(18)
        surface.blit(police.render("Entrez le code d'accès :", True, T.TEXTE_PRINCIPAL), (rect.x + 24, rect.y + 55))

        champ_rect = pygame.Rect(rect.x + 24, rect.y + 90, largeur - 48, 40)
        pygame.draw.rect(surface, T.FOND_SLOT, champ_rect, border_radius=6)
        pygame.draw.rect(surface, T.ACCENT_CYAN, champ_rect, width=2, border_radius=6)

        curseur = "_" if int(time.time() * 2) % 2 == 0 else ""
        police_saisie = T.police(20, gras=True)
        surface.blit(police_saisie.render(self.texte_saisi + curseur, True, T.ACCENT_CYAN), (champ_rect.x + 10, champ_rect.y + 8))

        police_aide = T.police(12)
        surface.blit(police_aide.render("Entrée = valider   |   Échap = annuler", True, T.TEXTE_SECONDAIRE),
                     (rect.x + 24, rect.bottom - 30))


# ======================================================================
# 9. APPLICATION — boucle principale, mise en page adaptative plein écran
# ======================================================================
class ApplicationPygame:
    def __init__(self, joueur, controleur, sortie):
        pygame.init()
        pygame.display.set_caption("F.I.C.S. — Terminal de contrôle")

        info = pygame.display.Info()
        self.largeur, self.hauteur = info.current_w, info.current_h
        self.plein_ecran = True
        self.ecran = pygame.display.set_mode((self.largeur, self.hauteur), pygame.RESIZABLE)

        self.horloge = pygame.time.Clock()
        self.joueur = joueur
        self.controleur = controleur
        self.sortie = sortie

        self.panel_salle = PanelSalle()
        self.panel_interactions = PanelInteractionsSalle()
        self.panel_inventaire = PanelInventaire()
        self.panel_log = PanelLog()
        self.modale_code = ModaleCode()

        self.actif = True
        self.etat = "accueil"  # "accueil" puis "jeu"

        self.objectif_texte = (
            "atteindre le cœur du réacteur, tout au bout de l'installation, en réactivant "
            "ce qui doit l'être en chemin."
        )

        self.lore_titre = "F.I.C.S. — Fondation Industrielle de Contrôle et Sécurité"
        self.lore_paragraphes = [
            "L'installation F.I.C.S. a cessé toute transmission il y a six heures. Aucune "
            "explication, aucune alerte : juste le silence. Vous êtes le seul agent de terrain "
            "disponible dans la région, et votre mission est simple en apparence : entrer, "
            "comprendre ce qui s'est passé, et rétablir les systèmes vitaux du complexe.",

            "Mais rien, ici, n'est vraiment simple. Plus vous progresserez dans les couloirs, plus "
            "vous découvrirez que ce silence n'était pas un accident. Portes verrouillées, "
            "documents éparpillés, indices soigneusement dissimulés : quelqu'un a voulu ralentir "
            "toute intrusion. Et le complexe n'est que le début — au-delà se cachent un entrepôt "
            "portuaire, puis une zone dont l'accès est, officiellement, interdit à quiconque.",

            "À vous de fouiller, de combiner, de déchiffrer... et d'aller jusqu'au bout.",
        ]
        self.instructions = [
            ("Clic gauche sur une sortie", "Vous déplacer vers la salle affichée sur le bouton."),
            ("Clic gauche sur un meuble", "Le fouiller pour révéler ce qu'il contient."),
            ("Clic gauche sur un objet au sol", "Le ramasser dans votre inventaire."),
            ("Survoler un objet de l'inventaire", "Voir son nom complet et sa description."),
            ("Clic gauche sur 2 objets de l'inventaire", "Tenter de les combiner pour en créer un nouveau."),
            ("Clic droit sur un objet de l'inventaire", "Le lire, s'il contient un texte."),
            ("Clic sur la pastille d'un objet", "Le marquer d'une couleur (rouge/vert/bleu) comme vous voulez."),
            ("Pastille verte sur une sortie", "Indique la salle d'où vous venez."),
            ("Molette de la souris", "Faire défiler l'inventaire, le journal ou les longues listes."),
            ("Bouton 💡 Indice", "Un indice discret est proposé dans chaque salle si vous bloquez."),
            ("Bouton ⚙ (coin supérieur droit)", "Régler séparément le volume de la musique et celui des effets sonores."),
            ("Touche F11", "Basculer entre plein écran et fenêtré."),
        ]

        # --- Musique d'ambiance en boucle (synthétisée, aucun fichier) ---
        self.volume_musique = 0.20
        self.parametres_ouverts = False
        self.canal_ambiance = None
        if self.sortie.sons.disponible:
            son_ambiance = self.sortie.sons.obtenir_ambiance()
            if son_ambiance:
                try:
                    self.canal_ambiance = pygame.mixer.Channel(0)
                    self.canal_ambiance.set_volume(self.volume_musique)
                    self.canal_ambiance.play(son_ambiance, loops=-1)
                except Exception:
                    self.canal_ambiance = None

    # ---- Contexte partagé passé aux panels pour la lecture d'état ----
    class _Contexte:
        def __init__(self, joueur, sortie, selection_combinaison):
            self.joueur = joueur
            self.sortie = sortie
            self.selection_combinaison = selection_combinaison

    def _calculer_zones(self):
        """Recalcule les rects de mise en page à chaque frame -> adaptatif au resize."""
        L, H = self.largeur, self.hauteur
        rect_salle = T.rect_proportionnel(L, H, 0.02, 0.07, 0.62, 0.28)
        rect_interactions = T.rect_proportionnel(L, H, 0.02, 0.37, 0.62, 0.31)
        rect_log = T.rect_proportionnel(L, H, 0.02, 0.70, 0.62, 0.28)
        rect_inventaire = T.rect_proportionnel(L, H, 0.66, 0.07, 0.32, 0.91)
        return rect_salle, rect_interactions, rect_log, rect_inventaire

    def _dessiner_bandeau_objectif(self):
        """Bande fine et permanente en haut de l'écran, pour ne jamais perdre le but de vue."""
        hauteur = max(28, int(self.hauteur * 0.045))
        bandeau = pygame.Rect(0, 0, self.largeur, hauteur)
        pygame.draw.rect(self.ecran, T.FOND_PANEL, bandeau)
        pygame.draw.line(self.ecran, T.BORDURE, (0, hauteur), (self.largeur, hauteur), 1)

        police = T.police(max(13, hauteur // 2))
        texte = f"🎯 Objectif : {self.objectif_texte}"
        rendu = police.render(texte, True, T.ACCENT_JAUNE)
        self.ecran.blit(rendu, rendu.get_rect(midleft=(18, hauteur // 2)))

    def _traiter_evenement_accueil(self, event):
        if event.type == pygame.QUIT:
            self.actif = False
            return
        if event.type == pygame.VIDEORESIZE:
            self.largeur, self.hauteur = event.w, event.h
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            self._basculer_plein_ecran()
            return
        if event.type == pygame.MOUSEBUTTONDOWN and self._gerer_clic_controles_son(event.pos):
            return
        if event.type == pygame.MOUSEBUTTONDOWN or (
            event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE)
        ):
            self.etat = "jeu"
            return

    # ---- Bouton ⚙ et panneau de volumes (musique d'ambiance + effets sonores) ----
    def _rect_bouton_parametres(self):
        taille = 36
        return pygame.Rect(self.largeur - taille - 16, 16, taille, taille)

    def _rect_panneau_parametres(self):
        largeur, hauteur = 240, 148
        bouton = self._rect_bouton_parametres()
        return pygame.Rect(self.largeur - largeur - 16, bouton.bottom + 8, largeur, hauteur)

    def _rects_lignes_volume(self, rect_panneau):
        """Retourne les rects (moins, plus) pour chaque ligne : musique puis effets sonores."""
        y_musique = rect_panneau.y + 46
        y_effets = rect_panneau.y + 100
        lignes = {}
        for nom, y_ligne in (("musique", y_musique), ("effets", y_effets)):
            lignes[nom] = (
                pygame.Rect(rect_panneau.x + 16, y_ligne, 32, 32),
                pygame.Rect(rect_panneau.right - 48, y_ligne, 32, 32),
                y_ligne,
            )
        return lignes

    def _gerer_clic_controles_son(self, pos):
        if self._rect_bouton_parametres().collidepoint(pos):
            self.parametres_ouverts = not self.parametres_ouverts
            return True
        if self.parametres_ouverts:
            rect_panneau = self._rect_panneau_parametres()
            lignes = self._rects_lignes_volume(rect_panneau)

            rect_moins, rect_plus, _y = lignes["musique"]
            if rect_moins.collidepoint(pos):
                self._ajuster_volume_musique(-0.1)
                return True
            if rect_plus.collidepoint(pos):
                self._ajuster_volume_musique(0.1)
                return True

            rect_moins, rect_plus, _y = lignes["effets"]
            if rect_moins.collidepoint(pos):
                self._ajuster_volume_effets(-0.1)
                return True
            if rect_plus.collidepoint(pos):
                self._ajuster_volume_effets(0.1)
                return True

            if rect_panneau.collidepoint(pos):
                return True  # clic dans le panneau, hors bouton : on absorbe pour ne pas cliquer "à travers"
        return False

    def _ajuster_volume_musique(self, delta):
        self.volume_musique = max(0.0, min(1.0, round(self.volume_musique + delta, 2)))
        if self.canal_ambiance:
            self.canal_ambiance.set_volume(self.volume_musique)

    def _ajuster_volume_effets(self, delta):
        self.sortie.sons.volume_effets = max(0.0, min(1.0, round(self.sortie.sons.volume_effets + delta, 2)))

    def _dessiner_ligne_volume(self, rect_panneau, y_ligne, libelle, valeur):
        rect_moins = pygame.Rect(rect_panneau.x + 16, y_ligne, 32, 32)
        rect_plus = pygame.Rect(rect_panneau.right - 48, y_ligne, 32, 32)
        T.dessiner_bouton(self.ecran, rect_moins, "−", couleur_accent=T.ACCENT_JAUNE)
        T.dessiner_bouton(self.ecran, rect_plus, "+", couleur_accent=T.ACCENT_JAUNE)

        pourcentage = int(round(valeur * 100))
        texte = f"{libelle} : {'coupé' if pourcentage == 0 else str(pourcentage) + '%'}"
        police = T.police(13, gras=True)
        rendu = police.render(texte, True, T.TEXTE_PRINCIPAL)
        self.ecran.blit(rendu, rendu.get_rect(center=(rect_panneau.centerx, y_ligne - 10)))

    def _dessiner_controles_son(self):
        rect_bouton = self._rect_bouton_parametres()
        T.dessiner_bouton(self.ecran, rect_bouton, "⚙", survole=False, couleur_accent=T.ACCENT_CYAN)
        if not self.parametres_ouverts:
            return
        rect_panneau = self._rect_panneau_parametres()
        T.dessiner_panel(self.ecran, rect_panneau, titre="Volumes", bordure_accent=True)

        lignes = self._rects_lignes_volume(rect_panneau)
        _rm, _rp, y_musique = lignes["musique"]
        _rm, _rp, y_effets = lignes["effets"]
        self._dessiner_ligne_volume(rect_panneau, y_musique, "Musique", self.volume_musique)
        self._dessiner_ligne_volume(rect_panneau, y_effets, "Effets", self.sortie.sons.volume_effets)

        if not self.sortie.sons.disponible:
            police_aide = T.police(11)
            aide = police_aide.render("Audio indisponible sur cette machine.", True, T.TEXTE_DESACTIVE)
            self.ecran.blit(aide, (rect_panneau.x + 14, rect_panneau.bottom - 18))

    @staticmethod
    def _decouper_texte_accueil(texte, police, largeur_max):
        mots = texte.split(" ")
        lignes, courante = [], ""
        for mot in mots:
            essai = f"{courante} {mot}".strip()
            if police.size(essai)[0] > largeur_max and courante:
                lignes.append(courante)
                courante = mot
            else:
                courante = essai
        if courante:
            lignes.append(courante)
        return lignes

    def _dessiner_accueil(self):
        self.ecran.fill(T.FOND_PRINCIPAL)
        zone = T.rect_proportionnel(self.largeur, self.hauteur, 0.06, 0.04, 0.88, 0.92)
        T.dessiner_panel(self.ecran, zone, bordure_accent=True)

        largeur_colonne = (zone.width - 100) // 2
        x_gauche = zone.x + 40
        x_droite = zone.x + 60 + largeur_colonne

        # --- Titre, centré en haut du panneau ---
        police_titre = T.police(max(20, zone.width // 42), gras=True)
        y = zone.y + 30
        for ligne in self._decouper_texte_accueil(self.lore_titre, police_titre, zone.width - 80):
            rendu = police_titre.render(ligne, True, T.ACCENT_CYAN)
            self.ecran.blit(rendu, rendu.get_rect(midtop=(zone.centerx, y)))
            y += rendu.get_height() + 4
        y += 14
        pygame.draw.line(self.ecran, T.BORDURE, (zone.x + 40, y), (zone.right - 40, y), 1)
        y_debut_colonnes = y + 24

        # --- Colonne gauche : le lore ---
        police_section = T.police(max(16, zone.width // 70), gras=True)
        police_lore = T.police(max(13, zone.width // 105))
        y = y_debut_colonnes
        rendu_section = police_section.render("SITUATION", True, T.ACCENT_JAUNE)
        self.ecran.blit(rendu_section, (x_gauche, y))
        y += rendu_section.get_height() + 12
        for paragraphe in self.lore_paragraphes:
            for ligne in self._decouper_texte_accueil(paragraphe, police_lore, largeur_colonne):
                rendu = police_lore.render(ligne, True, T.TEXTE_PRINCIPAL)
                self.ecran.blit(rendu, (x_gauche, y))
                y += police_lore.get_height() + 5
            y += 12

        # --- Colonne droite : comment jouer ---
        police_action = T.police(max(13, zone.width // 110), gras=True)
        police_desc = T.police(max(12, zone.width // 120))
        y = y_debut_colonnes
        rendu_section = police_section.render("COMMENT JOUER", True, T.ACCENT_JAUNE)
        self.ecran.blit(rendu_section, (x_droite, y))
        y += rendu_section.get_height() + 12
        for action, description in self.instructions:
            rendu_action = police_action.render(f"› {action}", True, T.ACCENT_CYAN)
            self.ecran.blit(rendu_action, (x_droite, y))
            y += rendu_action.get_height() + 2
            for ligne in self._decouper_texte_accueil(description, police_desc, largeur_colonne - 14):
                rendu_desc = police_desc.render(ligne, True, T.TEXTE_SECONDAIRE)
                self.ecran.blit(rendu_desc, (x_droite + 14, y))
                y += rendu_desc.get_height() + 3
            y += 10

        # --- Message de démarrage, clignotant ---
        if int(time.time() * 1.5) % 2 == 0:
            police_prompt = T.police(max(15, zone.width // 65), gras=True)
            rendu_prompt = police_prompt.render(
                "Cliquez ou appuyez sur ENTRÉE pour commencer", True, T.ACCENT_VERT
            )
            self.ecran.blit(rendu_prompt, rendu_prompt.get_rect(midbottom=(zone.centerx, zone.bottom - 20)))

    def _traiter_evenement(self, event):
        if event.type == pygame.QUIT:
            self.actif = False
            return
        if event.type == pygame.VIDEORESIZE:
            self.largeur, self.hauteur = event.w, event.h
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            self._basculer_plein_ecran()
            return
        if event.type == pygame.MOUSEBUTTONDOWN and self._gerer_clic_controles_son(event.pos):
            return

        if self.controleur.modale_code_ouverte:
            self.modale_code.gerer_evenement(event, self.controleur)
            return

        if event.type == pygame.MOUSEWHEEL:
            pos = pygame.mouse.get_pos()
            rect_salle, rect_interactions, rect_log, rect_inventaire = self._calculer_zones()
            if rect_inventaire.collidepoint(pos):
                self.panel_inventaire.defiler(event.y)
            elif rect_log.collidepoint(pos):
                self.panel_log.defiler(event.y)
            elif rect_interactions.collidepoint(pos):
                self.panel_interactions.defiler(pos, event.y)
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            cible_tag = self.panel_inventaire.detecter_zone_tag(pos)
            if cible_tag:
                self.panel_inventaire.cycler_tag(cible_tag)
                return

            cible = self.panel_salle.detecter_clic(pos)
            if cible == "__indice__":
                self.controleur.on_demande_indice()
                return
            elif cible:
                self.controleur.on_click_sortie(cible)
                return

            cible = self.panel_interactions.detecter_clic(pos)
            if cible:
                self.panel_interactions.declencher(cible, self.controleur)
                return

            cible = self.panel_inventaire.detecter_clic(pos)
            if cible:
                self.panel_inventaire.declencher(cible, self.controleur, event.button)
                return

    def _basculer_plein_ecran(self):
        self.plein_ecran = not self.plein_ecran
        if self.plein_ecran:
            info = pygame.display.Info()
            self.largeur, self.hauteur = info.current_w, info.current_h
            self.ecran = pygame.display.set_mode((self.largeur, self.hauteur), pygame.RESIZABLE)
        else:
            self.largeur, self.hauteur = 1280, 720
            self.ecran = pygame.display.set_mode((self.largeur, self.hauteur), pygame.RESIZABLE)

    def _dessiner_bandeau_victoire(self):
        voile = pygame.Surface((self.largeur, self.hauteur), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 190))
        self.ecran.blit(voile, (0, 0))
        police = T.police(42, gras=True)
        texte = police.render("INSTALLATION SAUVÉE — VICTOIRE", True, T.ACCENT_VERT)
        self.ecran.blit(texte, texte.get_rect(center=(self.largeur // 2, self.hauteur // 2)))
        police_aide = T.police(16)
        aide = police_aide.render("Échap pour quitter", True, T.TEXTE_SECONDAIRE)
        self.ecran.blit(aide, aide.get_rect(center=(self.largeur // 2, self.hauteur // 2 + 50)))

    def lancer(self):
        while self.actif:
            for event in pygame.event.get():
                if self.etat == "accueil":
                    self._traiter_evenement_accueil(event)
                    continue
                if self.controleur.jeu_termine and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.actif = False
                    continue
                self._traiter_evenement(event)

            if self.etat == "accueil":
                self._dessiner_accueil()
                self._dessiner_controles_son()
                pygame.display.flip()
                self.horloge.tick(60)
                continue

            self.ecran.fill(T.FOND_PRINCIPAL)

            contexte = self._Contexte(self.joueur, self.sortie, self.controleur.selection_combinaison)
            rect_salle, rect_interactions, rect_log, rect_inventaire = self._calculer_zones()

            if not self.controleur.jeu_termine:
                self._dessiner_bandeau_objectif()
                self.panel_salle.dessiner(self.ecran, rect_salle, contexte)
                self.panel_interactions.dessiner(self.ecran, rect_interactions, contexte)
                self.panel_inventaire.dessiner(self.ecran, rect_inventaire, contexte)

            self.panel_log.dessiner(self.ecran, rect_log, contexte)

            if self.controleur.modale_code_ouverte:
                self.modale_code.dessiner(self.ecran, self.largeur, self.hauteur)

            if self.controleur.jeu_termine and self.controleur.jeu_gagne:
                self._dessiner_bandeau_victoire()

            self._dessiner_controles_son()

            pygame.display.flip()
            self.horloge.tick(60)

        pygame.quit()