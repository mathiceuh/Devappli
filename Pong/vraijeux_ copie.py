import pygame
from random import randint

# Initialisation de Pygame
pygame.init()

# Initialisation de la bibliothèque sonore de Pygame
pygame.mixer.init()

# Définition des polices
font20 = pygame.font.Font('freesansbold.ttf', 20)
font40 = pygame.font.Font('freesansbold.ttf', 40)

score_filename = "scores.txt"

# Définition des couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)
Couleur_random = (randint(100, 255), randint(100, 255), randint(100, 255))

# Définition de la taille de l'écran
LONGUEUR, LARGEUR = 900, 600

# Création de la fenêtre du jeu
Ecran = pygame.display.set_mode((LONGUEUR, LARGEUR))
pygame.display.set_caption("Pong")

# Paramètres du timer
Timer = pygame.time.Clock()
FPS = 210

# Chargement des fichiers audio
collision_sound = pygame.mixer.Sound('sonballe.mp3')


class Joueur:
    def __init__(self, x, y, EPAISSEUR, LONGUEUR, couleur, Score):
        # Initialisation du joueur
        self.x = x
        self.y = y
        self.JLONGUEUR = LONGUEUR
        self.EPAISSEUR = EPAISSEUR
        self.couleur = couleur
        self.playerRect = pygame.Rect(x, y, EPAISSEUR, LONGUEUR)
        self.Score = Score

    def monter(self):
        # Déplacement vers le haut
        if self.y - 1 > 41:
            self.y -= 1
            self.playerRect = pygame.Rect(self.x, self.y, self.EPAISSEUR, self.JLONGUEUR)


    def descendre(self):
        # Déplacement vers le bas
        if self.y + 1 < LARGEUR - self.JLONGUEUR-4:
            self.y += 1
            self.playerRect = pygame.Rect(self.x, self.y, self.EPAISSEUR, self.JLONGUEUR)


    def droite(self, P):
        # Déplacement vers la droite (pour P1 et P2)
        if P == "P1":
            if self.x + 1 < LONGUEUR // 2 - 100:
                self.x += 1
                self.playerRect = pygame.Rect(self.x, self.y, self.EPAISSEUR, self.JLONGUEUR)

        if P == "P2":
            if self.x + 1 < LONGUEUR - 30:
                self.x += 1
                self.playerRect = pygame.Rect(self.x, self.y, self.EPAISSEUR, self.JLONGUEUR)

    def gauche(self, P):
        # Déplacement vers la gauche (pour P1 et P2)
        if P == "P1":
            if self.x - 1 >= 20:
                self.x -= 1
                self.playerRect = pygame.Rect(self.x, self.y, self.EPAISSEUR, self.JLONGUEUR)
        if P == "P2":
            if self.x - 1 >= LONGUEUR // 2 + 100:
                self.x -= 1
                self.playerRect = pygame.Rect(self.x, self.y, self.EPAISSEUR, self.JLONGUEUR)

    def display(self):
        # Affichage du joueur
        pygame.draw.rect(Ecran, self.couleur, self.playerRect)

    def getRect(self):
        # Récupération du rectangle du joueur
        return self.playerRect

    def SizeMax(self):
        # Agrandissement du joueur
        if self.y <= 63:
            self.JLONGUEUR = 150
            self.playerRect = pygame.Rect(self.x, self.y, self.EPAISSEUR, self.JLONGUEUR)

        elif self.y >= LARGEUR-129:
            self.JLONGUEUR = 150
            self.y -= 50
            self.playerRect = pygame.Rect(self.x, self.y, self.EPAISSEUR, self.JLONGUEUR)
        else:
            self.JLONGUEUR = 150
            self.y -= 25
            self.playerRect = pygame.Rect(self.x, self.y, self.EPAISSEUR, self.JLONGUEUR)

    def Normal(self):
        # Rétablissement de la taille normale du joueur
        self.JLONGUEUR = 100
        self.EPAISSEUR = 10
        self.y += 25
        self.playerRect = pygame.Rect(self.x, self.y, self.EPAISSEUR, self.JLONGUEUR)


class Ball:
    def __init__(self, x, y, couleur):
        # Initialisation de la balle
        self.x = x
        self.y = y
        self.couleur = couleur
        self.xFac = 1
        self.yFac = -1
        self.ball = pygame.draw.circle(Ecran, self.couleur, (self.x, self.y), 7)
        self.firstTime = 1

    def color_change(self):
        # Changement de couleur de la balle en fonction de sa position
        proportion = self.x / LONGUEUR
        self.couleur = (int(proportion * 255), int((1 - abs(2 * proportion - 1)) * 255), int((1 - proportion) * 255))

    def display(self):
        # Affichage de la balle
        self.ball = pygame.draw.circle(Ecran, self.couleur, (self.x, self.y), 7)

    def update(self):
        # Mise à jour de la position de la balle et détection des collisions avec les bords de l'écran
        self.x += self.xFac
        self.y += self.yFac
        if self.y <= 41 or self.y >= LARGEUR - 13:
            self.yFac *= -1

        if self.x <= 0 and self.firstTime:
            self.firstTime = 0
            return 1

        elif self.x >= LONGUEUR and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    def reset(self):
        # Réinitialisation de la position de la balle
        self.x = LONGUEUR // 2
        self.y = LARGEUR // 2
        self.xFac *= -1
        self.firstTime = 1

    def hit(self):
        # Inversion du facteur de déplacement horizontal lorsqu'il y a une collision avec un joueur
        self.xFac *= -1

    def getRect(self):
        # Récupération du rectangle représentant la balle
        return self.ball

    def collide(self, rect):
        # Vérification de la collision entre la balle et un rectangle donné
        return self.getRect().colliderect(rect)

class BONUS:
    def __init__(self):
        # Initialisation du bonus
        self.x = randint(LONGUEUR//2-80, LONGUEUR//2+80)
        self.y = randint(40, LARGEUR-4)
        self.active = True

    def placer(self):
        # Placement du bonus sur l'écran
        Couleur_random = (randint(100, 255), randint(100, 255), randint(100, 255))
        pygame.draw.polygon(Ecran, Couleur_random, [
            (self.x, self.y - 15), (self.x + 5, self.y - 5),
            (self.x + 15, self.y - 5), (self.x + 7, self.y + 5),
            (self.x + 10, self.y + 15), (self.x, self.y + 7),
            (self.x - 10, self.y + 15), (self.x - 7, self.y + 5),
            (self.x - 15, self.y - 5), (self.x - 5, self.y - 5)
        ])


    def collide(self, ball_rect):
        # Vérification de la collision entre le bonus et la balle
        bonus_rect = pygame.Rect(self.x - 15, self.y - 15, 30, 30)
        return bonus_rect.colliderect(ball_rect)



def ecranAccueil(ancienScoreJoueur1,ancienScoreJoueur2):
    running = True
    change_color_timer = 0
    couleur_texte = (randint(0, 255), randint(0, 255), randint(0, 255))

    while running:
        
        Ecran.fill(NOIR)
        # Affichage du décors d'accueil
        fond_ecran = pygame.image.load('fond_accueil.jpg')
        fond_ecran = pygame.transform.scale(fond_ecran, (LONGUEUR, LARGEUR))
        Ecran.blit(fond_ecran, (0, 0))
        
        # Affichage du texte d'accueil
        if pygame.time.get_ticks() - change_color_timer > 500:
            couleur_texte = (randint(0, 255), randint(0, 255), randint(0, 255))
            change_color_timer = pygame.time.get_ticks()
        texte_accueil = font20.render("Appuyez sur une touche pour démarrer", True, couleur_texte)
        texteRect = texte_accueil.get_rect()
        texteRect.center = (LONGUEUR // 2, LARGEUR // 2 + 20)
        Ecran.blit(texte_accueil, texteRect)

        # Affichage des scores de la partie précédente
        texte_score1 = font20.render("Ancien score Joueur 1 : " + str(ancienScoreJoueur1), True, couleur_texte)
        texteRect1 = texte_score1.get_rect()
        texteRect1.center = (LONGUEUR // 2 - 9, LARGEUR // 2 + 70)
        Ecran.blit(texte_score1, texteRect1)

        texte_score2 = font20.render("Ancien score Joueur 2 : " + str(ancienScoreJoueur2), True, couleur_texte)
        texteRect2 = texte_score2.get_rect()
        texteRect2.center = (LONGUEUR // 2 - 9, LARGEUR // 2 + 100)
        Ecran.blit(texte_score2, texteRect2)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                return  # Démarrer le jeu lorsque n'importe quelle touche est pressée
        


def sauvegarder_scores(player1Score,player2Score):
    ancienScoreJoueur1 = player1Score
    ancienScoreJoueur2 = player2Score
    with open(score_filename, 'w') as file:
        file.write(f"{ancienScoreJoueur1}\n{ancienScoreJoueur2}")






def main(FPS):
    # Initialisation des scores
    ancienScoreJoueur1 = 0
    ancienScoreJoueur2 = 0
    player1Score, player2Score = 0, 0
    try:
        with open(score_filename, 'r') as file:
            scores = file.readlines()
            if len(scores) >= 2:  # Vérifier si la liste contient au moins deux éléments
                ancienScoreJoueur1 = int(scores[0].strip())
                ancienScoreJoueur2 = int(scores[1].strip())
            else:
                print("Fichier de scores vide ou incomplet.")
    except FileNotFoundError:
        print("Fichier de scores non trouvé. Scores réinitialisés à zéro.")
        
    #Ajout de la musique (se joue en boucle)    
    pygame.mixer.music.load('musique.mp3')
    pygame.mixer.music.play(-1)  # -1 signifie que la musique se répète en boucle    
        
    # Afficher l'écran d'accueil avec les scores de la partie précédente
    ecranAccueil(ancienScoreJoueur1,ancienScoreJoueur2)

    # Initialisation des variables pour détecter les touches enfoncées
    P1UP = False
    P1DOWN = False
    P1RIGHT = False
    P1LEFT = False
    P2UP = False
    P2DOWN = False
    P2RIGHT = False
    P2LEFT = False

    # Initialisation des variables de temps pour les bonus de taille
    time_player1 = 0
    time_player2 = 0

    # Initialisation des dimensions des joueurs
    LongP1 = 10
    HautP1 = 100
    LongP2 = 10
    HautP2 = 100

    # Initialisation des flags pour les bonus
    BONUS1 = False
    BONUS2 = False

    # Création des objets Joueur et Balle
    player1 = Joueur(20, LARGEUR // 2 - 38, LongP1, HautP1, BLEU, player1Score)
    player2 = Joueur(LONGUEUR - 30, LARGEUR // 2 - LongP2, LongP2, HautP2, ROUGE, player2Score)
    ball = Ball(LONGUEUR // 2, LARGEUR // 2, BLANC)
    listOfPlayers = [player1, player2]
    first = BONUS()

    # Initialiser la valeur play a True
    play = True

    # Boucle principale du jeu
    while play:
        # Effacer l'écran avec la couleur de fond
        Ecran.fill(NOIR)
        
        # Placer le bonus et changer la couleur de la balle
        first.placer()
        ball.color_change()

        # Dessiner les lignes du milieu du terrain
        i = (LARGEUR - 43) / 31
        j = 0
        while j <= LARGEUR:
            pygame.draw.line(Ecran, BLANC, (LONGUEUR // 2 + 3, 40 + j), (LONGUEUR // 2 + 3, 38 + j + i), 3)
            pygame.draw.line(Ecran, BLANC, (LONGUEUR // 2 - 87, 40 + j), (LONGUEUR // 2 - 87, 38 + j + i), 1)
            pygame.draw.line(Ecran, BLANC, (LONGUEUR // 2 + 95, 40 + j), (LONGUEUR // 2 + 95, 38 + j + i), 1)
            j += i * 2

        # Dessiner les lignes du haut et du bas du terrain
        pygame.draw.line(Ecran, BLANC, (0, LARGEUR - 3), (LONGUEUR, LARGEUR - 3), 4)
        pygame.draw.line(Ecran, BLANC, (0, 38), (LONGUEUR, 38), 4)

        # Gérer les événements pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sauvegarder_scores(player1Score,player2Score)  # Sauvegarder les scores avant de quitter
                play = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sauvegarder_scores(player1Score,player2Score)  # Sauvegarder les scores avant de quitter
                    play = False  # Définit running sur False pour sortir de la boucle de jeu
                # Gestion des touches pour le déplacement et les bonus
                if event.key == pygame.K_z:
                    P1UP = True
                if event.key == pygame.K_s:
                    P1DOWN = True
                if event.key == pygame.K_d:
                    P1RIGHT = True
                if event.key == pygame.K_q:
                    P1LEFT = True
                if event.key == pygame.K_UP:
                    P2UP = True
                if event.key == pygame.K_DOWN:
                    P2DOWN = True
                if event.key == pygame.K_RIGHT:
                    P2RIGHT = True
                if event.key == pygame.K_LEFT:
                    P2LEFT = True
                if event.key == pygame.K_a or BONUS1:
                    if time_player1 == 0:
                        time_player1 = 1000
                        player1.SizeMax()
                        BONUS1 = True
                if event.key == pygame.K_RCTRL or BONUS2:
                    if time_player2 == 0:
                        time_player2 = 1000
                        player2.SizeMax()
                        BONUS2 = True

            if event.type == pygame.KEYUP:
                # Gestion des touches pour le déplacement
                if event.key == pygame.K_z:
                    P1UP = False
                if event.key == pygame.K_s:
                    P1DOWN = False
                if event.key == pygame.K_d:
                    P1RIGHT = False
                if event.key == pygame.K_q:
                    P1LEFT = False
                if event.key == pygame.K_UP:
                    P2UP = False
                if event.key == pygame.K_DOWN:
                    P2DOWN = False
                if event.key == pygame.K_RIGHT:
                    P2RIGHT = False
                if event.key == pygame.K_LEFT:
                    P2LEFT = False

        # Déplacement des joueurs en fonction des touches enfoncées
        if P1UP:
            player1.monter()
        if P1DOWN:
            player1.descendre()
        if P1RIGHT:
            player1.droite("P1")
        if P1LEFT:
            player1.gauche("P1")
        if P2UP:
            player2.monter()
        if P2DOWN:
            player2.descendre()
        if P2RIGHT:
            player2.droite("P2")
        if P2LEFT:
            player2.gauche("P2")

        # Gestion des collisions avec les joueurs
        for player in range(len(listOfPlayers)):
            if pygame.Rect.colliderect(ball.getRect(), listOfPlayers[player].getRect()):
                ball.hit()
                FPS += 15
                collision_sound.play()  # Jouer le son de collision
                if player == 0:
                    listOfPlayers[player].x -= 2
                else:
                    listOfPlayers[player].x += 2

        # Gestion des collisions avec le bonus
        if first.active and first.collide(ball.getRect()):
            first.active = False  # Désactivez le BONUS lorsqu'il est touché par la balle
            # Réinitialisez la position du BONUS
            first.x = randint(LONGUEUR // 2 - 80, LONGUEUR // 2 + 80)
            first.y = randint(40, LARGEUR - 4)
            first.active = True  # Réactivez le BONUS pour qu'il réapparaisse

        # Mise à jour de la position de la balle et vérification des points marqués
        point = ball.update()
        if point == -1:
            player1Score += 1
            FPS = 210
            ancienScoreJoueur1 = player1Score  # Mettre à jour ancienScoreJoueur1 avec le nouveau score
        elif point == 1:
            player2Score += 1
            FPS = 210
            ancienScoreJoueur2 = player2Score  # Mettre à jour ancienScoreJoueur2 avec le nouveau score

        # Réinitialisation de la balle en cas de point marqué
        if point:
            ball.reset()

        # Gestion du temps des bonus de taille
        if time_player1 != 0:
            time_player1 -= 1
            if time_player1 == 0:
                player1.Normal()
                BONUS1 = False

        if time_player2 != 0:
            time_player2 -= 1
            if time_player2 == 0:
                player2.Normal()
                BONUS2 = False

        # Affichage des éléments du jeu
        player1.display()
        player2.display()
        ball.display()

        # Affichage des scores et du titre
        score1 = font40.render(str(player1Score), True, Couleur_random)
        score2 = font40.render(str(player2Score), True, Couleur_random)
        text = font20.render("PONG", True, (255, 255, 255))
        Ecran.blit(text, (LONGUEUR // 2 - 27, 10))

        # Affichage des scores en fonction de leur valeur
        if player1Score > 99 or player2Score > 99:
            Ecran.blit(score1, (10, 60))
            Ecran.blit(score2, (LONGUEUR - 100, 60))
        else:
            if player1Score <= 9:
                Ecran.blit(score1, (LONGUEUR // 2 - 52, 60))
            if player2Score <= 9:
                Ecran.blit(score2, (LONGUEUR // 2 + 38, 60))
            if 9 < player1Score <= 99:
                Ecran.blit(score1, (LONGUEUR // 2 - 65, 60))
            if 9 < player2Score <= 99:
                Ecran.blit(score2, (LONGUEUR // 2 + 25, 60))

        # Mise à jour de l'affichage
        pygame.display.update()

        # Contrôle de la fréquence d'images par seconde
        Timer.tick(FPS)

# Exécution du jeu
if __name__ == "__main__":
    main(FPS)
    pygame.quit()
