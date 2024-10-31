import pygame
import math
import random

# Initialisation de Pygame
pygame.init()

# Fenêtre du jeu
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# couleur
YELLOW = (255, 255, 0)
BLUE = (0, 25, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
BROWN = (165, 42, 42)
RED = (255, 0, 0)
GREY = (200, 200, 200)
DARKGREY = (50, 50, 50)
ORANGE = (255, 128, 0)
WHITE = (255,255,255)

#image des phases de la lune

tailleimg = (280,280)

image_lune = [
    pygame.transform.scale(pygame.image.load("nouvelleLune.png"), tailleimg),
    pygame.transform.scale(pygame.image.load("premierCroissant.png"), tailleimg),
    pygame.transform.scale(pygame.image.load("premierQuartier.png"), tailleimg),
    pygame.transform.scale(pygame.image.load("gibbeuseCroissante.png"), tailleimg),
    pygame.transform.scale(pygame.image.load("pleineLune.png"), tailleimg),
    pygame.transform.scale(pygame.image.load("gibbeuseDecroissante.png"), tailleimg),
    pygame.transform.scale(pygame.image.load("dernierQuartier.png"), tailleimg),
    pygame.transform.scale(pygame.image.load("dernierCroissant.png"), tailleimg)
]

#liste des musiques 
liste_musiques = [
    "DayOne.mp3",
    "CornfieldChase.mp3",
    "WhereWereGoing.mp3",
    "NoTimeForCaution.mp3"
]

index_musique = 0

# images pour les boutons
tailleimage = (70,70)
image_lire = pygame.transform.scale(pygame.image.load("lire.png"), tailleimage)  # triangle de lecture
image_pause = pygame.transform.scale(pygame.image.load("pause.png"), tailleimage)  # deux barres pour arrêter
image_prec = pygame.transform.scale(pygame.image.load("prec.png"), tailleimage)
image_suiv = pygame.transform.scale(pygame.image.load("suiv.png"), tailleimage)

# Récupére les dimensions de la fenêtre pour mettre la page en plein écran
width_window, height_window = pygame.display.get_surface().get_size()

# Détermine les coordonnées du centre de la page par rapport a l'ecran
centre_x = width_window // 2
centre_y = height_window // 2

class Bouton:
    # dessiner un bouton
    def dessiner_bouton(surface, txt, rect, couleur):
        pygame.draw.rect(surface, couleur, rect)
        font = pygame.font.SysFont("comicsansms", 25)
        surface_texte = font.render(txt, True, BLACK)
        rectangle_txt = surface_texte.get_rect(center=rect.center)
        #coodonées et dimensions du rectangle du txt + centrer txt 
        surface.blit(surface_texte, rectangle_txt)
        #dessine une surface
        
class Bouton_eruption:
    #classe bouton pour les eruptions
    def __init__(self, x, y, w, h, couleur, texte):
        self.rect = pygame.Rect(x, y, w, h)
        self.couleur = couleur
        self.texte = texte
        self.font = pygame.font.SysFont("comicsansms", 25)
        
    def dessiner(self, surface):
        pygame.draw.rect(surface, self.couleur, self.rect)
        surface_texte = self.font.render(self.texte, True, BLACK)
        rect_texte = surface_texte.get_rect(center=self.rect.center)
        surface.blit(surface_texte, rect_texte)
        
    def est_clique(self, pos):
        return self.rect.collidepoint(pos)
        
        
# classe bouton pr la musique
class BoutonMusique:
    def __init__(self, x, y, image_lire, image_pause):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.image_lire = image_lire
        self.image_pause = image_pause
        self.en_pause = True  # demarre en etat de pause

    def dessiner(self, surface):
        if self.en_pause:
            surface.blit(self.image_lire, self.rect.topleft)  # image de lecture
        else:
            surface.blit(self.image_pause, self.rect.topleft)  # image de pause
        
    def est_clique(self, pos):
        return self.rect.collidepoint(pos)
    
# creer boutons de contrôle de la musique
bouton_lire_pause = BoutonMusique(1400, 800, image_lire, image_pause)
bouton_prec = BoutonMusique(1320, 800, image_prec, image_prec) 
bouton_suiv = BoutonMusique(1480, 800, image_suiv, image_suiv) 

class Meteorite:
    def __init__(self):
        self.x = random.randint(0, width_window)
        self.y = 0
        self.vitesse_y = random.uniform(5, 10)  # vitesse verticale
        self.vitesse_x = -random.uniform(2, 5)   # vitesse horizontale
        self.taille = random.randint(2, 5)

    def mouvement(self):
        # faaire descendre la meteorite
        self.y += self.vitesse_y
        self.x += self.vitesse_x

    def dessiner(self, surface):
        # Dessine la météorite
        pygame.draw.circle(surface, GREY, (self.x, int(self.y)), self.taille)

# Classe Planete
class Planet:
    def __init__(self, color, rayon_x, rayon_y, speed, size):
        self.color = color
        self.rayon_x = rayon_x
        self.rayon_y = rayon_y
        self.speed = speed
        self.size = size
        self.angle = 0

    def mouvP(self, en_pause):
        #deplacement des planetes si pas en pause
        if not en_pause:
            self.x = centre_x + self.rayon_x * math.cos(self.angle)
            self.y = centre_y + self.rayon_y * math.sin(self.angle)
            self.angle += self.speed

    def drawP(self, surface):
        #affiche les planetes
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

# Classe Satellite 
class Satellite:
    def __init__(self, color, rayon_x, rayon_y, speed, size, planet_parent):
        self.color = color
        self.rayon_x = rayon_x
        self.rayon_y = rayon_y
        self.speed = speed
        self.size = size
        self.angle = 0
        self.planet_parent = planet_parent

    def mouvS(self,en_pause):
        #mouvement des sattelites si pas en pause
        if not en_pause:
            self.x = self.planet_parent.x + self.rayon_x * math.cos(self.angle)
            self.y = self.planet_parent.y + self.rayon_y * math.sin(self.angle)
            self.angle += self.speed

    def drawS(self, surface):
        #affiche les satellittes
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

#calsse eruptiobn solaire
class eruptionSolaire:
    def __init__(self):
        # postiton aléatoire autour du soleil
        self.angle = random.uniform(0, 2 * math.pi) #en randiant
        self.distance = 90  # distance p/r au centre du soleil
        self.vitesse = random.uniform(1, 2)  # vitesse d'extension de l'éruption
        self.taille = random.randint(2, 4)  # taille de l'eruption
        self.opacite = 255  # niveau de transparence au depart
    
    def mouvement(self):
        # eruption qui s'éloigne du soleil
        self.distance += self.vitesse - 3*(self.vitesse/4)
        # reduction de l'opacite
        self.opacite = max(0, self.opacite - 5)
        
    def draw(self, surface):
        # coordonnées euption
        x = centre_x + self.distance * math.cos(self.angle)
        y = centre_y + self.distance * math.sin(self.angle)
        # dessine cercle
        surface_eruption = pygame.Surface((self.taille * 2, self.taille * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface_eruption, (255, 69, 0, self.opacite), (self.taille, self.taille), self.taille)
        surface.blit(surface_eruption, (x - self.taille, y - self.taille))


# Classe Système Solaire
class SystemeSolaire:
    def __init__(self):
        self.planets = []
        self.satellites = []
        self.eruptions = []  # lsite eruptions solaires
        self.meteorites = []

    def add_planet(self, planet):
        self.planets.append(planet)

    def add_satellite(self, satellite):
        self.satellites.append(satellite)
        
    def ajoutermeteorite(self):
        self.meteorites.append(Meteorite())
        
    def add_eruption(self):
        self.eruptions.append(eruptionSolaire())

    def mouvement(self, en_pause):
        #mouvement si ce n'est pas en pause
        for planet in self.planets:
            planet.mouvP(en_pause)
        for satellite in self.satellites:
            satellite.mouvS(en_pause)
            
        for eruption in self.eruptions:
            eruption.mouvement()
            
        for meteorite in self.meteorites:
            meteorite.mouvement()

    def draw(self, surface,eruption_visible):
        
        for meteorite in self.meteorites:
            meteorite.dessiner(surface)
            
        # dessine eruptions solaires si visible
        if eruption_visible:
            for eruption in self.eruptions:
                eruption.draw(surface)
        
        # Dessiner le Soleil
        pygame.draw.circle(surface, YELLOW, (centre_x, centre_y), 90)
        # Dessiner les planètes et les satellites
        for planet in self.planets:
            planet.drawP(surface)
        for satellite in self.satellites:
            satellite.drawS(surface)
            
        
        # enelver eruptions terminees
        eruptions_a_garder = []
        for eruption in self.eruptions:
            if eruption.opacite > 0:
                eruptions_a_garder.append(eruption)
                
    def enlevermeteorite(self):
        # enelve meteorites qui sortent de l'ecran
        self.meteorites = [m for m in self.meteorites if m.y < height_window and m.x < width_window]

        
class Lune:
    def det_phase_lune(angle_lune):
        #determine la phase de lune a afficher
        nb_de_phase = len(image_lune) #nb de phase
        phase = int((angle_lune % (2 * math.pi)) / (2 * math.pi / nb_de_phase))
        #reparti les angles sur les differentes phases
        
        return phase

    def dessiner_lune(visible,phase):
        #affichage des phases de la lune
        if visible:
            pygame.draw.rect(window, WHITE, pygame.Rect(1250,50,300,300))
            #affiche l'image de la phase
            window.blit(image_lune[phase], (1260, 60))

# Fonction principale
def main():
    # Créer le système solaire
    systeme_solaire = SystemeSolaire()

    # ajoute des planètes
    terre = Planet(BLUE, 220, 180, 0.029, 10)
    mercure = Planet(GREY, 140, 100, 0.047, 4)
    venus = Planet(ORANGE, 160, 140, 0.035, 9)
    mars = Planet(RED, 300, 240, 0.024, 5)
    
    systeme_solaire.add_planet(terre)
    systeme_solaire.add_planet(mercure)
    systeme_solaire.add_planet(venus)
    systeme_solaire.add_planet(mars)

    # ajoute des satellites
    lune = Satellite(GREY, 30, 22, 0.1, 3, terre)
    systeme_solaire.add_satellite(lune)
    
    #controle visibilité de la fenetre de la lune
    fenetre_lune_visible = False
    
    #pause
    en_pause = False
    
    premierTour = True
    
    # variable pr activer/désactiver les meteorites et les eruptions
    eruption_visible = True
    meteorites_actives = True
    
    
    # creation des boutons
    bouton_ouvrir_fermer = pygame.Rect(1520, 50, 30, 30)
    bouton_stop = pygame.Rect(100, 50, 100, 50)
    boutonEruption = Bouton_eruption(100, 150, 200, 50, ORANGE, "eruptions: on")
    boutonMeteorite = Bouton_eruption(100, 250, 200, 50, ORANGE, "météorites: on")
    
    global index_musique
    musique_joue = False
    pygame.mixer.music.load(liste_musiques[index_musique])  # chargement premiere musique
    
    
    # Boucle du jeu
    en_cours = True
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_ouvrir_fermer.collidepoint(event.pos):  # si bouton cliqué
                    fenetre_lune_visible = not fenetre_lune_visible #afficher ou pas

                if bouton_stop.collidepoint(event.pos):  # pause
                    en_pause = not en_pause
                    
                if boutonMeteorite.est_clique(event.pos):
                    meteorites_actives = not meteorites_actives
                    if meteorites_actives:
                        boutonMeteorite.texte = "météorites: on"
                    else:
                        boutonMeteorite.texte = "météorites: off"
                        
                if boutonEruption.est_clique(event.pos):
                    eruption_visible = not eruption_visible
                    if eruption_visible:
                        boutonEruption.texte = "eruptions: on"
                    else:
                        boutonEruption.texte = "eruptions: off"

                if bouton_lire_pause.est_clique(event.pos):
                    if musique_joue:
                        pygame.mixer.music.pause()
                        bouton_lire_pause.en_pause = True
                    else:
                        pygame.mixer.music.unpause()
                        bouton_lire_pause.en_pause = False
                    musique_joue = not musique_joue
                    
                    if premierTour:
                        if musique_joue: 
                            pygame.mixer.music.play(0)
                            premierTour = False

                    
                if bouton_prec.est_clique(event.pos):
                    index_musique = (index_musique - 1) % len(liste_musiques)
                    pygame.mixer.music.load(liste_musiques[index_musique])
                    if musique_joue:
                        pygame.mixer.music.play(0)

                if bouton_suiv.est_clique(event.pos):
                    index_musique = (index_musique + 1) % len(liste_musiques)
                    pygame.mixer.music.load(liste_musiques[index_musique])
                    if musique_joue:
                        pygame.mixer.music.play(0)

        window.fill(BLACK)
        
        # ajout de meteorites si actives
        if meteorites_actives and random.random() < 0.1:
            systeme_solaire.ajoutermeteorite()

        
        #  cadre autour des commandes de musique
        
        cadreW = width_window - 320
        pygame.draw.rect(window, DARKGREY, (cadreW, height_window - 110, 300, 100), 0, 5)

        # dessiner boutons contrôle de musique
        bouton_lire_pause.dessiner(window)
        bouton_prec.dessiner(window)
        bouton_suiv.dessiner(window)

        # afficher titre musique en cours
        font = pygame.font.SysFont("comicsansms", 20)
        titre_musique = font.render(liste_musiques[index_musique], True, WHITE)
        window.blit(titre_musique, (cadreW , height_window - 140))
        
        # proba apparition d'une nouvelle eruption
        if random.random() < 0.03:
            systeme_solaire.add_eruption()

        # Mise à jour des positions
        systeme_solaire.mouvement(en_pause)
        
        systeme_solaire.enlevermeteorite()

        # affice le système solaire
        systeme_solaire.draw(window,eruption_visible)
        
        #fenetre de la lune
        phase_actuelle_lune = Lune.det_phase_lune(lune.angle)
        
        # afficher la fenêtre des phases de la Lune si elle est visible
        Lune.dessiner_lune(fenetre_lune_visible, phase_actuelle_lune)
        
        #dessiner boutons
        
        if fenetre_lune_visible:
            Bouton.dessiner_bouton(window, "x", bouton_ouvrir_fermer, RED) #fermer
        else:
            Bouton.dessiner_bouton(window, "o", bouton_ouvrir_fermer, CYAN) #ouvrir
            
        Bouton.dessiner_bouton(window, "stop", bouton_stop, ORANGE)
        
        boutonEruption.dessiner(window)
        boutonMeteorite.dessiner(window)

        # Mettre à jour l'affichage
        pygame.display.update()

    
        pygame.time.Clock().tick(60)

    pygame.quit()

# Lancer le programme
main()