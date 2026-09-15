import pygame


class ThemeVisuel:

    # --- Couleurs de fond ---
    FOND_PRINCIPAL   = (15, 17, 21)
    FOND_PANEL       = (23, 26, 32)
    FOND_PANEL_CLAIR = (31, 35, 43)
    FOND_SLOT        = (27, 30, 37)
    FOND_SLOT_HOVER  = (38, 43, 52)
    FOND_SLOT_ACTIF  = (44, 58, 55)

    # --- Bordures ---
    BORDURE          = (48, 54, 64)
    BORDURE_CLAIRE   = (70, 78, 90)
    BORDURE_ACCENT   = (0, 200, 210)

    # --- Accents sémantiques ---
    ACCENT_CYAN      = (0, 200, 210)
    ACCENT_JAUNE     = (222, 178, 74)
    ACCENT_VERT      = (94, 210, 140)
    ACCENT_ROUGE     = (220, 92, 98)
    ACCENT_MAGENTA   = (188, 120, 222)
    ACCENT_BLEU      = (90, 150, 235)
    ACCENT_BLEU      = (90, 140, 235)

    # --- Texte ---
    TEXTE_PRINCIPAL   = (228, 231, 235)
    TEXTE_SECONDAIRE  = (140, 146, 158)
    TEXTE_DESACTIVE   = (85, 90, 100)

    _polices = {}

    @classmethod
    def police(cls, taille, gras=False):
        cle = (taille, gras)
        if cle not in cls._polices:
            chemin = pygame.font.match_font("consolas,dejavusansmono,couriernew,monospace")
            if chemin:
                police = pygame.font.Font(chemin, taille)
                police.set_bold(gras)
            else:
                police = pygame.font.SysFont("monospace", taille, bold=gras)
            cls._polices[cle] = police
        return cls._polices[cle]

    @staticmethod
    def rect_proportionnel(largeur_ecran, hauteur_ecran, x_pct, y_pct, w_pct, h_pct):
        return pygame.Rect(
            int(largeur_ecran * x_pct),
            int(hauteur_ecran * y_pct),
            int(largeur_ecran * w_pct),
            int(hauteur_ecran * h_pct),
        )

    @classmethod
    def dessiner_panel(cls, surface, rect, titre=None, bordure_accent=False):
        pygame.draw.rect(surface, cls.FOND_PANEL, rect, border_radius=8)
        couleur_bordure = cls.BORDURE_ACCENT if bordure_accent else cls.BORDURE
        pygame.draw.rect(surface, couleur_bordure, rect, width=1, border_radius=8)
        if titre:
            police_titre = cls.police(min(20, max(14, rect.height // 22)), gras=True)
            surface.blit(police_titre.render(titre.upper(), True, cls.TEXTE_SECONDAIRE),
                         (rect.x + 16, rect.y + 12))

    @classmethod
    def dessiner_bouton(cls, surface, rect, texte, survole=False, actif=False, couleur_accent=None):
        couleur_accent = couleur_accent or cls.ACCENT_CYAN
        if actif:
            fond = tuple(min(255, c + 25) for c in cls.FOND_SLOT_ACTIF)
            bordure = couleur_accent
        elif survole:
            fond = cls.FOND_SLOT_HOVER
            bordure = cls.BORDURE_CLAIRE
        else:
            fond = cls.FOND_SLOT
            bordure = cls.BORDURE
        pygame.draw.rect(surface, fond, rect, border_radius=6)
        pygame.draw.rect(surface, bordure, rect, width=1, border_radius=6)

        marge_interne = 12
        taille = max(11, rect.height // 3)
        police = cls.police(taille)
        while police.size(texte)[0] > rect.width - marge_interne and taille > 9:
            taille -= 1
            police = cls.police(taille)

        surface_texte = police.render(texte, True, cls.TEXTE_PRINCIPAL)
        if surface_texte.get_width() > rect.width - marge_interne:
            while texte and police.size(texte + "…")[0] > rect.width - marge_interne:
                texte = texte[:-1]
            surface_texte = police.render(texte + "…", True, cls.TEXTE_PRINCIPAL)

        surface.blit(surface_texte, surface_texte.get_rect(center=rect.center))