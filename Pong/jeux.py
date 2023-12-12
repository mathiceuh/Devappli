import pygame
from random import randint

pygame.init()
font20 = pygame.font.Font('freesansbold.ttf', 20)
font40 = pygame.font.Font('freesansbold.ttf', 40)

#Score
ancienScoreJoueur1 = 0
ancienScoreJoueur2 = 0
score_filename = "scores.txt"

# Couleur
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
BLEU = (0, 0, 255)
ROUGE = (255, 0, 0)
Couleur_random = (randint(100, 255), randint(100, 255), randint(100, 255))

# Taille
LONGUEUR, HAUTEUR = 900, 600

# Ecran
Ecran = pygame.display.set_mode((LONGUEUR, HAUTEUR))
pygame.display.set_caption("Pong")

# Timer
Timer = pygame.time.Clock()
FPS = 210

# Chargez les fichiers audio
collision_sound = pygame.mixer.Sound('sonballe.mp3')


class Joueur:
    def __init__(self, x, y, LONGUEUR, HAUTEUR, couleur, Score):
        self.x = x
        self.y = y
        self.JLONGUEUR = LONGUEUR
        self.JHAUTEUR = HAUTEUR
        self.couleur = couleur
        self.playerRect = pygame.Rect(x, y, LONGUEUR, HAUTEUR)
        self.Score = Score

    def monter(self):
        if self.y - 1 > 42:
            self.y -= 1
            self.playerRect = pygame.Rect(self.x, self.y, self.JLONGUEUR, self.JHAUTEUR)
        else:
            self.y = 41
            self.playerRect = pygame.Rect(self.x, self.y, self.JLONGUEUR, self.JHAUTEUR)

    def descendre(self):
        if self.y + 1 < HAUTEUR - self.JHAUTEUR-4:
            self.y += 1
            self.playerRect = pygame.Rect(self.x, self.y, self.JLONGUEUR, self.JHAUTEUR)
        else:
            self.y = HAUTEUR - self.JHAUTEUR-4
            self.playerRect = pygame.Rect(self.x, self.y, self.JLONGUEUR, self.JHAUTEUR)

    def droite(self, P):
        if P == "P1":
            if self.x + 1 < LONGUEUR // 2 - 100:
                self.x += 1
                self.playerRect = pygame.Rect(self.x, self.y, self.JLONGUEUR, self.JHAUTEUR)
            else:
                self.x = (LONGUEUR // 2) - 100
                self.playerRect = pygame.Rect(self.x, self.y, self.JLONGUEUR, self.JHAUTEUR)

        if P == "P2":
            if self.x + 1 < LONGUEUR - 30:
                self.x += 1
                self.playerRect = pygame.Rect(self.x, self.y, self.JLONGUEUR, self.JHAUTEUR)
            else:
                self.x = LONGUEUR - 30
                self.playerRect = pygame.Rect(self.x, self.y, self.JLONGUEUR, self.JHAUTEUR)

    def gauche(self, P):
        if P == "P1":
            if self.x - 1 >= 20:
                self.x -= 1
                self.playerRect = pygame.Rect(self.x, self.y, self.JLONGUEUR, self.JHAUTEUR)
            else:
                self.x = 20
                self.playerRect = pygame.Rect(self.x, self.y, self.JLONGUEUR, self.JHAUTEUR)

        if P == "P2":
            if self.x - 1 >= LONGUEUR // 2 + 100:
                self.x -= 1
                self.playerRect = pygame.Rect(self.x, self.y, self.JLONGUEUR, self.JHAUTEUR)
            else:
                self.x = LONGUEUR // 2 + 100
                self.playerRect = pygame.Rect(self.x, self.y, self.JLONGUEUR, self.JHAUTEUR)

    def display(self):
        pygame.draw.rect(Ecran, self.couleur, self.playerRect)

    def getRect(self):
        return self.playerRect

    def SizeMax(self):
        if self.y <= 38+25:
            self.JHAUTEUR = 150
            self.playerRect = pygame.Rect(self.x, self.y, self.JLONGUEUR, self.JHAUTEUR)

        elif self.y >= HAUTEUR-129:
            self.JHAUTEUR = 150
            self.y -= 50
            self.playerRect = pygame.Rect(self.x, self.y, self.JLONGUEUR, self.JHAUTEUR)
        else:
            self.JHAUTEUR = 150
            self.y -= 25
            self.playerRect = pygame.Rect(self.x, self.y, self.JLONGUEUR, self.JHAUTEUR)

    def Normal(self):
        self.JHAUTEUR = 100
        self.JLONGUEUR = 10
        self.y += 25
        self.playerRect = pygame.Rect(self.x, self.y, self.JLONGUEUR, self.JHAUTEUR)


class BONUS:
    def __init__(self):
        self.x = randint(LONGUEUR//2-80, LONGUEUR//2+80)
        self.y = randint(40, HAUTEUR-4)
        self.active = True

    def placer(self):
        # Changer la couleur du BONUS
        Couleur_random = (randint(100, 255), randint(100, 255), randint(100, 255))

        # Dessiner une étoile à la place du BONUS
        pygame.draw.polygon(Ecran, Couleur_random, [
            (self.x, self.y - 15), (self.x + 5, self.y - 5),
            (self.x + 15, self.y - 5), (self.x + 7, self.y + 5),
            (self.x + 10, self.y + 15), (self.x, self.y + 7),
            (self.x - 10, self.y + 15), (self.x - 7, self.y + 5),
            (self.x - 15, self.y - 5), (self.x - 5, self.y - 5)
        ])
    def collide(self, ball_rect):
        # Vérifie si le rectangle entourant le BONUS est en collision avec le rectangle de la balle
        bonus_rect = pygame.Rect(self.x - 15, self.y - 15, 30, 30)
        return bonus_rect.colliderect(ball_rect)


class Ball:
    def __init__(self, x, y, couleur):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.xFac = 1
        self.yFac = -1
        self.ball = pygame.draw.circle(Ecran, self.couleur, (self.x, self.y), 7)
        self.firstTime = 1

    def color_change(self):
        proportion = self.x / LONGUEUR
        self.couleur = (int(proportion * 255), int((1 - abs(2 * proportion - 1)) * 255), int((1 - proportion) * 255))

    def display(self):
        self.ball = pygame.draw.circle(Ecran, self.couleur, (self.x, self.y), 7)

    def update(self):
        self.x += self.xFac * 1.1
        self.y += self.yFac * 1.1
        if self.y <= 0 or self.y >= HAUTEUR - 13:
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
        self.x = LONGUEUR // 2
        self.y = HAUTEUR // 2
        self.xFac *= -1
        self.firstTime = 1

    def hit(self):
        self.xFac *= -1

    def getRect(self):
        return self.ball

    def collide(self, rect):
        return self.getRect().colliderect(rect)

def ecranAccueil():
    global ancienScoreJoueur1, ancienScoreJoueur2
    running = True

    while running:
        Ecran.fill(NOIR)
        texte_accueil = font20.render("Appuyez sur une touche pour démarrer", True, BLANC)
        texteRect = texte_accueil.get_rect()
        texteRect.center = (LONGUEUR // 2, HAUTEUR // 2)
        Ecran.blit(texte_accueil, texteRect)

        # Affichage des scores de la partie précédente
        texte_score1 = font20.render("Ancien score Joueur 1 : " + str(ancienScoreJoueur1), True, BLANC)
        texteRect1 = texte_score1.get_rect()
        texteRect1.center = (LONGUEUR // 2, HAUTEUR // 2 + 30)
        Ecran.blit(texte_score1, texteRect1)

        texte_score2 = font20.render("Ancien score Joueur 2 : " + str(ancienScoreJoueur2), True, BLANC)
        texteRect2 = texte_score2.get_rect()
        texteRect2.center = (LONGUEUR // 2, HAUTEUR // 2 + 60)
        Ecran.blit(texte_score2, texteRect2)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                return  # Démarrer le jeu lorsque n'importe quelle touche est pressée
def sauvegarder_scores():
    with open(score_filename, 'w') as file:
        file.write(f"{ancienScoreJoueur1}\n{ancienScoreJoueur2}")

def charger_scores():
    global ancienScoreJoueur1, ancienScoreJoueur2
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



def main():
    
    global ancienScoreJoueur1, ancienScoreJoueur2
    charger_scores()

    # Afficher l'écran d'accueil avec les scores de la partie précédente
    ecranAccueil()
    P1UP = False
    P1DOWN = False
    P1RIGHT = False
    P1LEFT = False
    P2UP = False
    P2DOWN = False
    P2RIGHT = False
    P2LEFT = False
    play = True
    time_player1 = 0
    time_player2 = 0
    LongP1 = 10
    HautP1 = 100
    LongP2 = 10
    HautP2 = 100
    BONUS1 = False
    BONUS2 = False
    player1Score, player2Score = 99, 0
    player1 = Joueur(20, HAUTEUR // 2 - 38, LongP1, HautP1, BLEU, player1Score)
    player2 = Joueur(LONGUEUR - 30, HAUTEUR // 2 - LongP2, LongP2, HautP2, ROUGE, player2Score)
    ball = Ball(LONGUEUR // 2, HAUTEUR // 2, BLANC)
    listOfPlayers = [player1, player2]
    first = BONUS()
    while play:
        print(first.y,first.x)
        Ecran.fill(NOIR)
        first.placer()
        ball.color_change()
        i = (HAUTEUR - 43) / 31
        j = 0
        while j <= HAUTEUR:
            pygame.draw.line(Ecran, BLANC, (LONGUEUR // 2 + 3, 40 + j), (LONGUEUR // 2 + 3, 38 + j + i), 3)
            pygame.draw.line(Ecran, BLANC, (LONGUEUR // 2 - 87, 40 + j), (LONGUEUR // 2 - 87, 38 + j + i), 1)
            pygame.draw.line(Ecran, BLANC, (LONGUEUR // 2 + 95, 40 + j), (LONGUEUR // 2 + 95, 38 + j + i), 1)
            j += i * 2
        pygame.draw.line(Ecran, BLANC, (0, HAUTEUR - 3), (LONGUEUR, HAUTEUR - 3), 4)
        pygame.draw.line(Ecran, BLANC, (0, 38), (LONGUEUR, 38), 4)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sauvegarder_scores()  # Sauvegarder les scores avant de quitter
                play = False
                

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sauvegarder_scores()  # Sauvegarder les scores avant de quitter
                    play = False  # Définit running sur False pour sortir de la boucle de jeu
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
                if event.key == pygame.K_LCTRL or BONUS2:
                    if time_player2 == 0:
                        time_player2 = 1000
                        player2.SizeMax()
                        BONUS2 = True


            if event.type == pygame.KEYUP:
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

        for player in range(len(listOfPlayers)):
            if pygame.Rect.colliderect(ball.getRect(), listOfPlayers[player].getRect()):
                ball.hit()
                collision_sound.play()  # Jouer le son de collision
                if player == 0:
                    listOfPlayers[player].x -= 2
                else:
                    listOfPlayers[player].x += 2
                    
        if ball.collide(pygame.Rect(0, 45 - 2, LONGUEUR, 4)):
                ball.yFac *= -1
        if first.active and first.collide(ball.getRect()):
                first.active = False  # Désactivez le BONUS lorsqu'il est touché par la balle
                # Réinitialisez la position du BONUS
                first.x = randint(LONGUEUR // 2 - 80, LONGUEUR // 2 + 80)
                first.y = randint(40, HAUTEUR - 4)
                first.active = True  # Réactivez le BONUS pour qu'il réapparaisse

        
        
        point = ball.update()

        if point == -1:
            player1Score += 1
            ancienScoreJoueur1 = player1Score  # Mettre à jour ancienScoreJoueur1 avec le nouveau score
        elif point == 1:
            player2Score += 1
            ancienScoreJoueur2 = player2Score  # Mettre à jour ancienScoreJoueur2 avec le nouveau score


        if point:
            ball.reset()

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


        player1.display()
        player2.display()
        ball.display()

        score1 = font40.render(str(player1Score), True, Couleur_random)
        score2 = font40.render(str(player2Score), True, Couleur_random)
        text = font20.render("PONG", True, (255, 255, 255))
        Ecran.blit(text, (LONGUEUR // 2 - 27, 10))
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
        pygame.display.update()
        Timer.tick(FPS)
        



if __name__ == "__main__":
    main()
    pygame.quit()
