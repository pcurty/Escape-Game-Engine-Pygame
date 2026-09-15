from objet import Objet
from meuble import Meuble
from salle import Salle
from joueur import Joueur
from interface_pygame import InterfaceSortiePygame, ControleurDeJeu, ApplicationPygame


# ======================================================================
# NIVEAU 1 — Complexe F.I.C.S.  (9 salles)
# ======================================================================
def construire_niveau_1(sortie):
    carte = Objet("Carte", "Une carte magnétique vierge.", nom_affichage="Carte Magnétique")
    puce = Objet("Puce", "Une puce RFID non formatée.", nom_affichage="Puce RFID")
    badge = Objet("Badge", "Un badge RFID complet et activé.", nom_affichage="Badge RFID")

    fusible_grille = Objet("FusibleGrille", "Un fusible visiblement grillé, noirci par une surtension.", nom_affichage="Fusible Grillé")
    pince = Objet("Pince", "Une pince à dénuder, encore fonctionnelle.", nom_affichage="Pince à Dénuder")
    fusible = Objet("Fusible", "Un fusible neuf, ressoudé avec soin.", nom_affichage="Fusible Réparé")

    cle_rouillee = Objet("CleRouillee", "Une clé mécanique bloquée par la rouille.", nom_affichage="Clé Rouillée")
    huile = Objet("Huile", "Un petit flacon d'huile pour mécanismes.", nom_affichage="Huile Mécanique")
    cle_generateur = Objet("CleGenerateur", "Une clé mécanique qui tourne à nouveau librement.", nom_affichage="Clé du Générateur")

    loupe = Objet("Loupe", "Une loupe grossissante à monture en laiton.", nom_affichage="Loupe Grossissante")
    page_dechiree = Objet("PageDechiree", "Une page arrachée, encre presque effacée.", nom_affichage="Page Déchirée")
    page_lisible = Objet("PageLisible", "La page déchirée, relue à la loupe.",
                          "Fragment retrouvé : '...code des archives : 7723...'", nom_affichage="Page Déchiffrée")

    gants = Objet("Gants", "Des gants anti-acide, nécessaires pour entrer au laboratoire.", nom_affichage="Gants de Protection")
    cle_usb = Objet("CleUsb", "Une clé USB sécurisée avec le firmware universel.", nom_affichage="Clé USB")
    cle_ascenseur = Objet("CleAscenseur", "Une clé électronique clignotante, éjectée du terminal après le redémarrage.", nom_affichage="Clé d'Ascenseur")

    memo = Objet("Memo", "Un post-it froissé jaune.", "Rappel pour la porte de l'atelier : 8421", nom_affichage="Post-it Froissé")
    journal_ingenieur = Objet("Journal", "Le journal de bord d'un ingénieur du complexe.",
                               "Extrait : 'Code administrateur de la salle serveur : 9057. Ne pas le noter ailleurs.'", nom_affichage="Journal de Bord")

    stylo = Objet("Stylo", "Un stylo bille sans encre.", nom_affichage="Stylo (sans encre)")
    boulon = Objet("Boulon", "Un boulon rouillé de 10mm.", nom_affichage="Boulon Rouillé")
    tasse = Objet("Tasse", "Une tasse à café vide, ébréchée.", nom_affichage="Tasse Ébréchée")
    tournevis = Objet("Tournevis", "Un tournevis cruciforme, la panne est usée.", nom_affichage="Tournevis Usé")
    bonbon = Objet("Bonbon", "Un vieux bonbon à la menthe, encore emballé.", nom_affichage="Bonbon à la Menthe")
    vieux_rapport = Objet("Rapport", "Un rapport d'incident poussiéreux.",
                           "'...fuite de gaz mineure en 2019, sans conséquence...' Rien d'utile ici.", nom_affichage="Rapport d'Incident")
    carte_postale = Objet("CartePostale", "Une carte postale d'une station balnéaire, jamais envoyée.", nom_affichage="Carte Postale")
    chiffon = Objet("Chiffon", "Un chiffon graisseux, bon pour rien d'autre que salir les mains.", nom_affichage="Chiffon Graisseux")

    armoire = Meuble("Armoire", "Une armoire métallique de rangement.", nom_affichage="Armoire", materiau="metal")
    armoire.ajouter_un_objet(carte); armoire.ajouter_un_objet(memo); armoire.ajouter_un_objet(stylo)

    caisse = Meuble("Caisse", "Une vieille caisse à outils.", nom_affichage="Caisse à Outils", materiau="bois")
    caisse.ajouter_un_objet(puce); caisse.ajouter_un_objet(boulon); caisse.ajouter_un_objet(pince)

    etabli = Meuble("Etabli", "Un établi couvert de limaille de fer.", nom_affichage="Établi", materiau="bois")
    etabli.ajouter_un_objet(fusible_grille); etabli.ajouter_un_objet(tournevis)

    tiroir = Meuble("Tiroir", "Le tiroir du bas du bureau de direction.", nom_affichage="Tiroir", materiau="bois")
    tiroir.ajouter_un_objet(cle_usb); tiroir.ajouter_un_objet(tasse)
    tiroir.ajouter_un_objet(huile); tiroir.ajouter_un_objet(page_dechiree); tiroir.ajouter_un_objet(gants)

    generateur = Meuble("Generateur", "Le générateur de secours du complexe. Le tableau électrique est ouvert.", nom_affichage="Générateur", materiau="metal")

    etagere_soussol = Meuble("Etagere", "Une étagère métallique branlante.", nom_affichage="Étagère", materiau="metal")
    etagere_soussol.ajouter_un_objet(chiffon)

    armoire_chimique = Meuble("ArmoireChimique", "Une armoire de stockage réactifs, fermée par un simple loquet.", nom_affichage="Armoire à Réactifs", materiau="metal")
    armoire_chimique.ajouter_un_objet(bonbon)

    bureau_labo = Meuble("BureauLabo", "Un bureau encombré de notes de recherche.", nom_affichage="Bureau du Laboratoire", materiau="bois")
    bureau_labo.ajouter_un_objet(journal_ingenieur)

    canape = Meuble("Canape", "Un canapé défoncé, avachi dans un coin.", nom_affichage="Canapé", materiau="cuir")
    canape.ajouter_un_objet(loupe); canape.ajouter_un_objet(carte_postale)

    etagere_archives = Meuble("EtagereArchives", "Des étagères pleines de classeurs poussiéreux.", nom_affichage="Étagère d'Archives", materiau="metal")
    etagere_archives.ajouter_un_objet(vieux_rapport); etagere_archives.ajouter_un_objet(cle_rouillee)

    console_serveurs = Meuble("ConsoleServeurs", "La console principale, encore tiède après le redémarrage.", nom_affichage="Console des Serveurs", materiau="electronique")
    console_serveurs.ajouter_un_objet(cle_ascenseur)

    sas_entree = Salle("Sas de décontamination",
                        "L'entrée stérile du complexe. La grande porte derrière vous est scellée.",
                        indice_de_la_salle="Cette armoire métallique mérite d'être fouillée avant de partir.")
    couloir = Salle("Couloir central",
                     "Un long couloir industriel. Les néons grésillent au-dessus de plusieurs portes closes.",
                     indice_de_la_salle="Ce couloir dessert plusieurs pièces ; certaines resteront fermées "
                                        "tant que vous n'aurez pas l'objet ou le code adapté.")
    atelier = Salle("Atelier de prototypage",
                     "Des imprimantes 3D en veille s'entassent sur les établis.",
                     indice_de_la_salle="L'établi cache un fusible grillé ; une pince, quelque part dans "
                                        "cet atelier, pourrait bien le sauver.")
    bureau = Salle("Bureau de la direction",
                    "La pièce est en désordre. Des plans sont étalés sur le bureau.",
                    indice_de_la_salle="Le tiroir semble avoir été rempli à la hâte : chaque objet qu'il "
                                       "contient trouvera une utilité ailleurs dans le complexe.")
    sous_sol = Salle("Sous-sol technique",
                      "L'air y est plus froid. Un générateur imposant occupe tout un mur.",
                      indice_de_la_salle="Le tableau électrique du générateur n'attend qu'un fusible en "
                                         "état de marche ; peut-être en avez-vous déjà réparé un.")
    labo = Salle("Laboratoire d'analyse",
                  "Des paillasses stériles, des flacons étiquetés, une odeur âcre de solvant.",
                  indice_de_la_salle="Le journal qui traîne sur ce bureau contient peut-être plus qu'un "
                                     "simple compte-rendu de recherche.")
    archives = Salle("Archives",
                      "Des rayonnages métalliques croulent sous des classeurs jaunis par le temps.",
                      indice_de_la_salle="Ces vieilles étagères pourraient encore cacher une clé rouillée, "
                                         "utile ailleurs dans le complexe.")
    salle_repos = Salle("Salle de repos",
                         "Une machine à café hors service et des fauteuils élimés.",
                         indice_de_la_salle="Ce canapé avachi cache peut-être une vieille loupe, utile "
                                            "pour déchiffrer un texte trouvé ailleurs.")
    serveur = Salle("Salle des serveurs",
                     "Le cœur du système. Les machines redémarrent lentement.",
                     indice_de_la_salle="La console principale semble avoir éjecté quelque chose après "
                                        "le redémarrage ; jetez-y un œil.")

    sas_entree.ajouter_un_meuble(armoire)
    atelier.ajouter_un_meuble(caisse); atelier.ajouter_un_meuble(etabli)
    bureau.ajouter_un_meuble(tiroir)
    sous_sol.ajouter_un_meuble(generateur); sous_sol.ajouter_un_meuble(etagere_soussol)
    labo.ajouter_un_meuble(armoire_chimique); labo.ajouter_un_meuble(bureau_labo)
    salle_repos.ajouter_un_meuble(canape)
    archives.ajouter_un_meuble(etagere_archives)
    serveur.ajouter_un_meuble(console_serveurs)

    sas_entree.ajouter_une_sortie("nord", couloir, False, None, None, "")
    couloir.ajouter_une_sortie("sud", sas_entree, False, None, None, "")

    couloir.ajouter_une_sortie("est", atelier, True, None, "8421", "Un digicode bloque l'accès à l'atelier.")
    atelier.ajouter_une_sortie("ouest", couloir, False, None, None, "")

    couloir.ajouter_une_sortie("ouest", bureau, True, badge, None, "Le lecteur clignote en rouge. Il faut un badge RFID.")
    bureau.ajouter_une_sortie("est", couloir, False, None, None, "")

    couloir.ajouter_une_sortie("nord", salle_repos, False, None, None, "")
    salle_repos.ajouter_une_sortie("sud", couloir, False, None, None, "")

    couloir.ajouter_une_sortie("bas", sous_sol, True, cle_generateur, None, "La trappe est cadenassée.")
    sous_sol.ajouter_une_sortie("haut", couloir, False, None, None, "")

    atelier.ajouter_une_sortie("est", labo, True, gants, None, "Accès interdit sans gants de protection.")
    labo.ajouter_une_sortie("ouest", atelier, False, None, None, "")

    bureau.ajouter_une_sortie("nord", archives, True, None, "7723", "Un digicode protège les archives.")
    archives.ajouter_une_sortie("sud", bureau, False, None, None, "")

    couloir.ajouter_une_sortie("nord-est", serveur, True, cle_usb, "9057",
                                "Le sas exige l'insertion de la clé administrateur ET un code.")
    serveur.ajouter_une_sortie("sud-ouest", couloir, False, None, None, "")

    recettes = [
        ("Carte", "Puce", badge),
        ("FusibleGrille", "Pince", fusible),
        ("CleRouillee", "Huile", cle_generateur),
        ("Loupe", "PageDechiree", page_lisible),
    ]

    return {
        "salle_depart": sas_entree,
        "salle_finale": serveur,
        "salle_repli": couloir,
        "recettes": recettes,
        "objets_partages": {
            "Fusible": fusible,
            "Badge": badge,
            "CleGenerateur": cle_generateur,
            "PageLisible": page_lisible,
            "CleAscenseur": cle_ascenseur,
        },
    }


# ======================================================================
# NIVEAU 2 — Entrepôt Portuaire Nocturne  (10 salles)
# ======================================================================
def construire_niveau_2(salle_serveur_n1, cle_ascenseur_n1):
    note_chiffree = Objet("NoteChiffree", "Une note couverte de chiffres sans queue ni tête.", nom_affichage="Note Chiffrée")
    calculatrice = Objet("Calculatrice", "Une calculatrice de poche, l'écran encore lisible.", nom_affichage="Calculatrice")
    note_decodee = Objet("NoteDecodee", "La note, enfin décryptée.",
                          "Résultat du calcul : code de la chambre froide : 1206", nom_affichage="Note Décodée")
    carton_vide = Objet("CartonVide", "Un carton d'emballage vide, écrasé.", nom_affichage="Carton Vide")

    passe_technique = Objet("PasseTechnique", "Un passe magnétique 'Technique' générique.", nom_affichage="Passe Technique")
    gants_uses = Objet("GantsUses", "De vieux gants de manutention, trop percés pour servir.", nom_affichage="Gants Usés")

    encre_invisible = Objet("EncreInvisible", "Un flacon d'encre réactive à la chaleur.", nom_affichage="Encre Invisible")
    manuel_obsolete = Objet("ManuelObsolete", "Un manuel de procédure entièrement périmé.",
                             "'...articles retirés du catalogue en 2011...' Sans intérêt.", nom_affichage="Manuel Obsolète")

    ticket_dechire = Objet("TicketDechire", "Un ticket de quai à moitié déchiré.",
                            "Lisible malgré tout : code du bureau du chef : 5390", nom_affichage="Ticket Déchiré")
    etiquette = Objet("Etiquette", "Une étiquette de container vierge.", nom_affichage="Étiquette Vierge")
    radio_cassee = Objet("RadioCassee", "Une radio VHF au boîtier fendu.", nom_affichage="Radio Cassée")

    puce_cryptee = Objet("PuceCryptee", "Une puce RFID chiffrée, incompatible avec un lecteur standard.", nom_affichage="Puce Cryptée")
    clef_rouillee2 = Objet("ClefRouillee2", "Une clé qui ne correspond à aucune serrure des environs.", nom_affichage="Vieille Clé (sans usage apparent)")
    badge_maitre = Objet("BadgeMaitre", "Un badge RFID reprogrammé, aux accès étendus.", nom_affichage="Badge Maître")

    anneau_cle = Objet("AnneauCle", "Un solide anneau métallique, sans clé dessus.", nom_affichage="Anneau de Clés")
    chiffon2 = Objet("Chiffon2", "Un autre chiffon graisseux, décidément on en trouve partout.", nom_affichage="Chiffon Graisseux")
    trousseau = Objet("Trousseau", "Un trousseau composé d'une vieille clé mécanique et d'un anneau neuf.", nom_affichage="Trousseau de Clés")

    cle_passe_finale = Objet("ClePasseFinale", "Une clé lourde, gravée d'un sigle inconnu.", nom_affichage="Clé de Passage")
    page_decodee = Objet("PageDecodee", "La page du complexe F.I.C.S., relue à l'encre réactive.",
                          "Un second message apparaît : code du sas de sortie : 8842", nom_affichage="Page Décodée")

    table_affichage_contenu1 = ticket_dechire
    table_affichage_contenu2 = etiquette
    table_affichage_contenu3 = radio_cassee

    sas_transfert = Salle("Sas de transfert",
                           "Un sas métallique encore vibrant du trajet. L'air sent le sel et le diesel.",
                           indice_de_la_salle="Ce sas ne mène qu'à un seul endroit : avancez.")
    hall = Salle("Hall de l'entrepôt",
                 "Un immense hall métallique, des rangées de conteneurs à perte de vue.",
                 indice_de_la_salle="Ce hall dessert presque tout l'entrepôt ; le tableau d'affichage "
                                     "mérite un coup d'œil avant de choisir une direction.")
    quai = Salle("Quai de chargement",
                 "Le vent s'engouffre entre des piles de caisses et de conteneurs.",
                 indice_de_la_salle="Un chiffre ne veut rien dire sans l'outil pour le décoder.")
    chambre_froide = Salle("Chambre froide",
                            "Un froid mordant. D'anciennes carcasses d'étagères couvertes de givre.",
                            indice_de_la_salle="Le froid conserve bien des choses, même une encre normalement invisible.")
    bureau_chef = Salle("Bureau du chef d'entrepôt",
                         "Un bureau exigu, des plannings punaisés partout aux murs.",
                         indice_de_la_salle="Une puce seule ne débloque rien : il lui faut un lecteur "
                                            "compatible, que vous possédez peut-être déjà.")
    local_electrique = Salle("Local électrique",
                              "Un tableau électrique ouvert grésille faiblement.",
                              indice_de_la_salle="Un fusible que vous avez déjà réparé pourrait revivre ici.")
    atelier_maintenance = Salle("Atelier de maintenance",
                                 "Des pièces détachées entassées sur des étagères métalliques.",
                                 indice_de_la_salle="Un anneau sans clé ne sert à rien ; une vieille clé "
                                                     "mécanique pourrait s'y marier.")
    salle_controle = Salle("Salle de contrôle",
                            "Des écrans de surveillance, presque tous éteints.",
                            indice_de_la_salle="Une porte plus loin exige un trousseau complet : une "
                                                "vieille clé mécanique et un anneau tout neuf, assemblés ensemble.")
    conteneur_secret = Salle("Conteneur scellé",
                              "Un conteneur aménagé en bureau clandestin.",
                              indice_de_la_salle="Ce coffre dissimulé cache une clé lourde, gravée d'un "
                                                  "sigle qui vous sera utile bien plus loin.")
    sas_sortie = Salle("Sas de sortie de l'entrepôt",
                        "Une lourde porte blindée, la dernière de cet entrepôt.",
                        indice_de_la_salle="Vous y êtes presque : au-delà de cette porte, un tout nouveau "
                                            "bâtiment vous attend.")

    tableau_affichage = Meuble("TableauAffichage", "Un panneau d'affichage couvert de notes punaisées.", nom_affichage="Tableau d'Affichage", materiau="bois")
    tableau_affichage.ajouter_un_objet(table_affichage_contenu1)
    tableau_affichage.ajouter_un_objet(table_affichage_contenu2)
    tableau_affichage.ajouter_un_objet(table_affichage_contenu3)

    caisses = Meuble("Caisses", "Des caisses de fret éventrées.", nom_affichage="Caisses de Fret", materiau="bois")
    caisses.ajouter_un_objet(note_chiffree); caisses.ajouter_un_objet(calculatrice); caisses.ajouter_un_objet(carton_vide)

    conteneur_quai = Meuble("Conteneur", "Un conteneur resté ouvert sur le quai.", nom_affichage="Conteneur Ouvert", materiau="metal")
    conteneur_quai.ajouter_un_objet(passe_technique); conteneur_quai.ajouter_un_objet(gants_uses)

    etageres_froides = Meuble("EtageresFroides", "Des étagères couvertes de givre.", nom_affichage="Étagères Givrées", materiau="metal")
    etageres_froides.ajouter_un_objet(encre_invisible); etageres_froides.ajouter_un_objet(manuel_obsolete)

    bureau_meuble = Meuble("Bureau", "Un bureau encombré de plannings.", nom_affichage="Bureau du Chef", materiau="bois")
    bureau_meuble.ajouter_un_objet(puce_cryptee); bureau_meuble.ajouter_un_objet(clef_rouillee2)

    tableau_electrique = Meuble("TableauElectrique", "Un tableau électrique dont plusieurs fusibles ont sauté.", nom_affichage="Tableau Électrique", materiau="electronique")

    etabli_portuaire = Meuble("EtabliPortuaire", "Un établi couvert de pièces détachées.", nom_affichage="Établi Portuaire", materiau="bois")
    etabli_portuaire.ajouter_un_objet(anneau_cle); etabli_portuaire.ajouter_un_objet(chiffon2)

    coffre_conteneur = Meuble("CoffreConteneur", "Un petit coffre dissimulé sous une bâche.", nom_affichage="Coffre Dissimulé", materiau="metal")
    coffre_conteneur.ajouter_un_objet(cle_passe_finale)

    sas_transfert.ajouter_une_sortie("nord", hall, False, None, None, "")
    hall.ajouter_une_sortie("sud", sas_transfert, False, None, None, "")

    hall.ajouter_une_sortie("est", quai, False, None, None, "")
    quai.ajouter_une_sortie("ouest", hall, False, None, None, "")

    hall.ajouter_une_sortie("ouest", bureau_chef, True, None, "5390", "Un digicode protège ce bureau.")
    bureau_chef.ajouter_une_sortie("est", hall, False, None, None, "")

    hall.ajouter_une_sortie("bas", local_electrique, True, passe_technique, None,
                             "Il faut un passe technique pour descendre.")
    local_electrique.ajouter_une_sortie("haut", hall, False, None, None, "")

    hall.ajouter_une_sortie("nord", salle_controle, True, badge_maitre, None,
                             "Le lecteur exige un badge maître.")
    salle_controle.ajouter_une_sortie("sud", hall, False, None, None, "")

    quai.ajouter_une_sortie("nord", chambre_froide, True, None, "1206", "Un digicode gèle l'accès.")
    chambre_froide.ajouter_une_sortie("sud", quai, False, None, None, "")

    local_electrique.ajouter_une_sortie("est", atelier_maintenance, True, None, None,
                                         "Le passage est bloqué : le tableau électrique doit être réparé.")
    atelier_maintenance.ajouter_une_sortie("ouest", local_electrique, False, None, None, "")

    salle_controle.ajouter_une_sortie("est", conteneur_secret, True, trousseau, None,
                                       "Il faut un trousseau complet pour ouvrir ce conteneur.")
    conteneur_secret.ajouter_une_sortie("ouest", salle_controle, False, None, None, "")

    hall.ajouter_une_sortie("nord-est", sas_sortie, True, cle_passe_finale, "8842",
                             "Une clé ET un code sont exigés pour sortir de l'entrepôt.")
    sas_sortie.ajouter_une_sortie("sud-ouest", hall, False, None, None, "")

    salle_serveur_n1.ajouter_une_sortie("est", sas_transfert, True, cle_ascenseur_n1, None,
                                         "Il manque la clé d'ascenseur pour franchir ce passage.")
    sas_transfert.ajouter_une_sortie("ouest", salle_serveur_n1, False, None, None, "")

    hall.ajouter_un_meuble(tableau_affichage)
    quai.ajouter_un_meuble(caisses); quai.ajouter_un_meuble(conteneur_quai)
    chambre_froide.ajouter_un_meuble(etageres_froides)
    bureau_chef.ajouter_un_meuble(bureau_meuble)
    local_electrique.ajouter_un_meuble(tableau_electrique)
    atelier_maintenance.ajouter_un_meuble(etabli_portuaire)
    conteneur_secret.ajouter_un_meuble(coffre_conteneur)

    recettes = [
        ("NoteChiffree", "Calculatrice", note_decodee),
        ("Badge", "PuceCryptee", badge_maitre),
        ("CleGenerateur", "AnneauCle", trousseau),
        ("PageLisible", "EncreInvisible", page_decodee),
    ]

    porte_local_vers_atelier = local_electrique.dictionnaire_des_sorties_possibles["est"]

    config_activables = {
        "TableauElectrique": {
            "objet_requis": None,
            "message_ok": "Vous replacez le fusible réparé au niveau 1 : le tableau reprend vie, "
                          "une trappe s'ouvre vers l'atelier de maintenance.",
            "message_manque": "Il manque un fusible en état de marche pour réparer ce tableau.",
            "portes_a_deverouiller": [porte_local_vers_atelier],
        }
    }

    return {
        "salle_depart": sas_transfert,
        "salle_finale": sas_sortie,
        "recettes": recettes,
        "config_activables": config_activables,
        "objets_partages": {
            "BadgeMaitre": badge_maitre,
            "ClePasseFinale": cle_passe_finale,
        },
    }


# ======================================================================
# NIVEAU 3 — Zone Restreinte / Cœur du Réacteur  (11 salles)
# ======================================================================
def construire_niveau_3(sas_sortie_n2):
    carnet_de_bord = Objet("CarnetDeBord", "Un carnet de bord relié en cuir, encore tiède d'avoir été manipulé.",
                            "Dernière entrée : 'Code du poste de garde changé : 3305.'", nom_affichage="Carnet de Bord")
    badge_visiteur = Objet("BadgeVisiteur", "Un badge visiteur périmé depuis longtemps.", nom_affichage="Badge Visiteur")
    formulaire = Objet("Formulaire", "Un formulaire d'accès, jamais rempli.", nom_affichage="Formulaire Vierge")

    clef_magnetique = Objet("ClefMagnetique", "Une clef magnétique, encore chaude d'avoir été utilisée récemment.", nom_affichage="Clé Magnétique")
    menottes = Objet("Menottes", "Une paire de menottes verrouillées, sans intérêt ici.", nom_affichage="Menottes")

    cartouches = Objet("Cartouches", "Une boîte de cartouches vide.", nom_affichage="Boîte de Cartouches")
    detecteur = Objet("Detecteur", "Un détecteur de fréquences portatif.", nom_affichage="Détecteur de Fréquences")
    levier = Objet("Levier", "Un lourd levier métallique.", nom_affichage="Levier Métallique")
    fiole_reactif = Objet("FioleReactif", "Une fiole d'un réactif à l'odeur âcre.", nom_affichage="Fiole de Réactif")

    composant_electronique = Objet("ComposantElectronique", "Un composant électronique isolé, encore fonctionnel.", nom_affichage="Composant Électronique")
    cable_use = Objet("CableUse", "Un câble usé jusqu'à la trame.", nom_affichage="Câble Usé")

    badge_scanner = Objet("BadgeScanner", "Le badge maître, couplé au détecteur, affiche désormais un code à l'écran.",
                           "Écran du scanner : 'Code de la tour de contrôle : 6689.'", nom_affichage="Badge Scanner")

    carte_acces = Objet("CarteAcces", "Une carte d'accès de haut niveau.", nom_affichage="Carte d'Accès")
    protocole_urgence = Objet("ProtocoleUrgence", "Un protocole d'urgence scellé, désormais ouvert.",
                               "Dernière ligne : 'Code du cœur de réacteur : 7719.'", nom_affichage="Protocole d'Urgence")
    cafe_froid = Objet("CafeFroid", "Un café froid, oublié depuis des heures.", nom_affichage="Café Froid")

    solution_reveillante = Objet("SolutionReveillante", "Un mélange instable, une étiquette improvisée collée dessus.",
                                  "Étiquette griffonnée à la hâte : 'Code du labo : 4471.'", nom_affichage="Solution Réveillante")
    component_final = Objet("ComponentFinalL3", "Un composant scellé, visiblement central à un mécanisme plus large.", nom_affichage="Composant Central")
    echantillon_inutile = Objet("EchantillonInutile", "Un échantillon non étiqueté, probablement sans valeur.", nom_affichage="Échantillon Inconnu")
    notes_assemblage = Objet(
        "NotesAssemblage",
        "Une feuille de calcul annotée à la main, collée sur le composant.",
        "Protocole d'assemblage (dernière page retrouvée) :\n"
        "1) Associer la carte d'accès de la tour de contrôle à l'ancienne clé de passage "
        "rapportée de l'entrepôt portuaire -> produit une clé hybride.\n"
        "2) Associer cette clé hybride au composant central de cette table -> produit la "
        "clé maîtresse. Elle seule, avec le code du protocole d'urgence, ouvre le réacteur.",
        nom_affichage="Notes d'Assemblage"
    )

    clef_hybride = Objet("ClefHybride", "Deux clés de provenances très différentes, assemblées en une seule.", nom_affichage="Clé Hybride")
    cle_maitresse = Objet("CleMaitresseUniverselle", "Une clé composite, fruit de trois niveaux de sécurité distincts.", nom_affichage="Clé Maîtresse")

    uniforme = Objet("Uniforme", "Un uniforme d'agent, taille trop petite.", nom_affichage="Uniforme")
    talkie_casse = Objet("TalkieCasse", "Un talkie-walkie hors service.", nom_affichage="Talkie-Walkie Cassé")
    note_infirmerie = Objet("NoteInfirmerie", "Une note glissée dans une poche d'uniforme.",
                             "'Code infirmerie, à ne pas oublier : 1111.'", nom_affichage="Note d'Infirmerie")

    antiseptique = Objet("Antiseptique", "Un flacon d'antiseptique à moitié vide.", nom_affichage="Antiseptique")
    bandage = Objet("Bandage", "Un rouleau de bandage, encore emballé.", nom_affichage="Bandage")
    carte_stagiaire = Objet("CarteStagiaire", "Une carte de stagiaire, encore valide.", nom_affichage="Carte de Stagiaire")

    rapport_zone = Objet("RapportZone", "Un rapport de zone, largement caviardé.",
                          "Ce qui n'est pas noirci : '...rien d'anormal à signaler...'", nom_affichage="Rapport de Zone")
    insigne = Objet("Insigne", "Un vieil insigne métallique, sans valeur apparente.", nom_affichage="Vieil Insigne")

    panneau_securite = Meuble("PanneauSecurite", "Un panneau d'affichage sécurité, couvert de consignes.", nom_affichage="Panneau de Sécurité", materiau="bois")
    panneau_securite.ajouter_un_objet(carnet_de_bord)
    panneau_securite.ajouter_un_objet(badge_visiteur)
    panneau_securite.ajouter_un_objet(formulaire)

    armoire_poste = Meuble("ArmoirePoste", "L'armoire personnelle du garde de faction.", nom_affichage="Armoire du Poste", materiau="metal")
    armoire_poste.ajouter_un_objet(clef_magnetique)
    armoire_poste.ajouter_un_objet(menottes)

    casiers = Meuble("Casiers", "Des casiers métalliques entrouverts.", nom_affichage="Casiers", materiau="metal")
    casiers.ajouter_un_objet(cartouches)
    casiers.ajouter_un_objet(detecteur)
    casiers.ajouter_un_objet(levier)
    casiers.ajouter_un_objet(fiole_reactif)

    panneau_tunnel = Meuble("PanneauTunnel", "Un panneau de raccordement électrique dans le tunnel.", nom_affichage="Panneau du Tunnel", materiau="electronique")
    panneau_tunnel.ajouter_un_objet(composant_electronique)
    panneau_tunnel.ajouter_un_objet(cable_use)

    pupitre_controle = Meuble("PupitreControle", "Un pupitre de contrôle couvert de voyants clignotants.", nom_affichage="Pupitre de Contrôle", materiau="electronique")
    pupitre_controle.ajouter_un_objet(carte_acces)
    pupitre_controle.ajouter_un_objet(protocole_urgence)
    pupitre_controle.ajouter_un_objet(cafe_froid)

    table_recherche = Meuble("TableRecherche", "Une table de laboratoire couverte d'instruments de précision.", nom_affichage="Table de Recherche", materiau="metal")
    table_recherche.ajouter_un_objet(component_final)
    table_recherche.ajouter_un_objet(echantillon_inutile)
    table_recherche.ajouter_un_objet(notes_assemblage)

    casiers_personnel = Meuble("CasiersPersonnel", "Des casiers de vestiaire, la plupart entrouverts.", nom_affichage="Casiers du Personnel", materiau="metal")
    casiers_personnel.ajouter_un_objet(uniforme)
    casiers_personnel.ajouter_un_objet(talkie_casse)
    casiers_personnel.ajouter_un_objet(note_infirmerie)

    armoire_pharmacie = Meuble("ArmoirePharmacie", "Une petite armoire à pharmacie entrouverte.", nom_affichage="Armoire à Pharmacie", materiau="metal")
    armoire_pharmacie.ajouter_un_objet(antiseptique)
    armoire_pharmacie.ajouter_un_objet(bandage)
    armoire_pharmacie.ajouter_un_objet(carte_stagiaire)

    etagere_archives_zone = Meuble("EtagereArchivesZone", "Des étagères de dossiers classés sans grand soin.", nom_affichage="Étagère d'Archives", materiau="metal")
    etagere_archives_zone.ajouter_un_objet(rapport_zone)
    etagere_archives_zone.ajouter_un_objet(insigne)

    coeur_reacteur = Meuble("CoeurReacteur", "Le cœur du réacteur, enfin accessible, vibrant doucement.", nom_affichage="Cœur du Réacteur", materiau="electronique")

    sas_entree = Salle("Sas de la zone restreinte",
                        "Un sas blindé, encore plus sécurisé que tout ce que vous avez vu jusqu'ici.",
                        indice_de_la_salle="Vous voilà dans une zone bien plus surveillée. Restez attentif.")
    hall = Salle("Hall de sécurité",
                 "Un hall aseptisé, des caméras tournent lentement dans chaque coin.",
                 indice_de_la_salle="Le panneau de sécurité de ce hall pourrait bien afficher plus que "
                                     "de simples consignes.")
    poste_garde = Salle("Poste de garde",
                         "Un poste de garde abandonné à la hâte, un café encore fumant.",
                         indice_de_la_salle="Ce poste donne accès à d'autres pièces de la zone ; une "
                                            "clef traîne peut-être encore dans les affaires du garde.")
    armurerie = Salle("Armurerie",
                       "Des casiers vides pour la plupart, quelques objets oubliés.",
                       indice_de_la_salle="Ce détecteur ne sert que couplé à un badge capable de scanner ; "
                                          "le badge maître rapporté de l'entrepôt fera peut-être l'affaire. "
                                          "Quant à la fiole de réactif, elle ferait des étincelles au "
                                          "contact d'un composant électronique.")
    tunnel_maintenance = Salle("Tunnel de maintenance",
                                "Un tunnel étroit, des câbles courent le long des parois.",
                                indice_de_la_salle="Ce composant électronique pourrait bien réagir, "
                                                    "littéralement, avec un réactif chimique trouvé ailleurs.")
    tour_controle = Salle("Tour de contrôle",
                           "Une salle en hauteur, vue dégagée sur toute l'installation.",
                           indice_de_la_salle="Le pupitre affiche encore le dernier protocole d'urgence "
                                               "consulté ; il vaut la peine d'être lu en entier. Et cette "
                                               "carte d'accès semble taillée pour un autre système que "
                                               "celui-ci — une vieille clé rapportée d'ailleurs s'y adapterait.")
    labo_recherche = Salle("Laboratoire de recherche",
                            "Un laboratoire ultramoderne, tout y est étiqueté au millimètre.",
                            indice_de_la_salle="Une feuille collée sur le composant de la table détaille, "
                                                "étape par étape, comment assembler la clé finale : "
                                                "lisez-la avant de combiner quoi que ce soit.")
    salle_reacteur = Salle("Cœur du réacteur",
                            "La salle la plus profonde de l'installation. Un vrombissement sourd emplit l'air.",
                            indice_de_la_salle="Le cœur du réacteur n'attend plus qu'une main pour être réactivé.")
    vestiaires = Salle("Vestiaires",
                        "Des rangées de casiers métalliques, la plupart vides.",
                        indice_de_la_salle="Une note glissée dans une poche d'uniforme a échappé à "
                                            "l'inventaire officiel.")
    infirmerie = Salle("Infirmerie",
                        "Une petite infirmerie de fortune, quelques lits pliants.",
                        indice_de_la_salle="Cette carte de stagiaire, encore valide, pourrait bien "
                                            "ouvrir d'autres portes de la zone.")
    archives_zone = Salle("Archives de la zone",
                           "Des rayonnages de dossiers plus récents que ceux de l'entrepôt.",
                           indice_de_la_salle="Ces archives ne contiennent que de vieux dossiers ; ou presque.")

    hall.ajouter_un_meuble(panneau_securite)
    poste_garde.ajouter_un_meuble(armoire_poste)
    armurerie.ajouter_un_meuble(casiers)
    tunnel_maintenance.ajouter_un_meuble(panneau_tunnel)
    tour_controle.ajouter_un_meuble(pupitre_controle)
    labo_recherche.ajouter_un_meuble(table_recherche)
    vestiaires.ajouter_un_meuble(casiers_personnel)
    infirmerie.ajouter_un_meuble(armoire_pharmacie)
    archives_zone.ajouter_un_meuble(etagere_archives_zone)
    salle_reacteur.ajouter_un_meuble(coeur_reacteur)

    sas_entree.ajouter_une_sortie("nord", hall, False, None, None, "")
    hall.ajouter_une_sortie("sud", sas_entree, False, None, None, "")

    hall.ajouter_une_sortie("est", poste_garde, True, None, "3305", "Un digicode protège le poste de garde.")
    poste_garde.ajouter_une_sortie("ouest", hall, False, None, None, "")

    hall.ajouter_une_sortie("ouest", armurerie, True, clef_magnetique, None, "L'armurerie est fermée à clef.")
    armurerie.ajouter_une_sortie("est", hall, False, None, None, "")

    hall.ajouter_une_sortie("bas", tunnel_maintenance, True, levier, None, "La trappe est bloquée de l'intérieur.")
    tunnel_maintenance.ajouter_une_sortie("haut", hall, False, None, None, "")

    hall.ajouter_une_sortie("haut", tour_controle, True, None, "6689", "Un digicode verrouille l'ascenseur.")
    tour_controle.ajouter_une_sortie("bas", hall, False, None, None, "")

    hall.ajouter_une_sortie("nord", labo_recherche, True, carte_acces, "4471",
                             "Une carte d'accès ET un code sont exigés.")
    labo_recherche.ajouter_une_sortie("sud", hall, False, None, None, "")

    hall.ajouter_une_sortie("sud-est", vestiaires, False, None, None, "")
    vestiaires.ajouter_une_sortie("nord-ouest", hall, False, None, None, "")

    hall.ajouter_une_sortie("sud-ouest", infirmerie, True, None, "1111", "Un digicode ferme l'infirmerie.")
    infirmerie.ajouter_une_sortie("nord-est", hall, False, None, None, "")

    hall.ajouter_une_sortie("nord-ouest", archives_zone, True, carte_stagiaire, None,
                             "Il faut un badge stagiaire valide pour entrer.")
    archives_zone.ajouter_une_sortie("sud-est", hall, False, None, None, "")

    labo_recherche.ajouter_une_sortie("nord", salle_reacteur, True, cle_maitresse, "7719",
                                       "La porte du réacteur exige une clé composite ET un code.")
    salle_reacteur.ajouter_une_sortie("sud", labo_recherche, False, None, None, "")

    sas_sortie_n2.ajouter_une_sortie("est", sas_entree, False, None, None, "")
    sas_entree.ajouter_une_sortie("ouest", sas_sortie_n2, False, None, None, "")

    recettes = [
        ("BadgeMaitre", "Detecteur", badge_scanner),
        ("FioleReactif", "ComposantElectronique", solution_reveillante),
        ("ClePasseFinale", "CarteAcces", clef_hybride),
        ("ClefHybride", "ComponentFinalL3", cle_maitresse),
    ]

    config_activables = {
        "CoeurReacteur": {
            "objet_requis": None,
            "message_ok": "Vous posez la main sur le cœur du réacteur. Toutes les installations "
                          "reprennent vie simultanément. C'est terminé.",
            "message_manque": "",
            "victoire": True,
        }
    }

    return {
        "salle_depart": sas_entree,
        "recettes": recettes,
        "config_activables": config_activables,
    }


def main():
    sortie = InterfaceSortiePygame()

    n1 = construire_niveau_1(sortie)
    n2 = construire_niveau_2(n1["salle_finale"], n1["objets_partages"]["CleAscenseur"])
    n3 = construire_niveau_3(n2["salle_finale"])

    n2["config_activables"]["TableauElectrique"]["objet_requis"] = n1["objets_partages"]["Fusible"]

    sortie.afficher("info", "=== BIENVENUE DANS L'INSTALLATION F.I.C.S. ===")
    sortie.afficher("info", "Objectif : atteindre le cœur du réacteur, bien au-delà du complexe de départ.")
    sortie.afficher("info", "Astuce : chaque salle possède un bouton Indice, discret mais utile.")

    joueur_principal = Joueur(n1["salle_depart"], sortie)
    for nom_obj1, nom_obj2, objet_resultat in n1["recettes"] + n2["recettes"] + n3["recettes"]:
        joueur_principal.ajouter_recette(nom_obj1, nom_obj2, objet_resultat)

    controleur = ControleurDeJeu(
        joueur=joueur_principal,
        sortie=sortie,
        salle_serveur=n1["salle_finale"],
        salle_repli_si_pas_alimente=n1["salle_repli"],
    )
    controleur.meubles_activables.update(n2["config_activables"])
    controleur.meubles_activables.update(n3["config_activables"])

    application = ApplicationPygame(joueur_principal, controleur, sortie)
    application.lancer()


if __name__ == "__main__":
    main()