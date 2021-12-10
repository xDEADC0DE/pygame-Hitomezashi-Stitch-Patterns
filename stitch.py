import pygame
import sys
import unicodedata

# configuration Pygame
DEBUG = True
TAILLE_ECRAN = 900
TITRE = 'Hitomezashi Stitch Patterns'
FPS = 60
screen = pygame.display.set_mode((TAILLE_ECRAN,TAILLE_ECRAN))
pygame.display.set_caption(TITRE)
pygame.init()

# polices
pygame.font.init()
POLICE_MOTS = pygame.font.SysFont('arial', 30)

# options du jeu
TAILLE_MOTS = 20
COULEUR_POINTS_GRILLE = 'gray'
COULEUR_POINTS_TRAITS = 'black'
TAILLE_TRAITS = 5
INTERVALLE = TAILLE_ECRAN//(TAILLE_MOTS+2)

def draw(mot_1: str, mot_2: str, x_actif: bool):
	screen.fill('white')

	# grille
	for colonne in range(INTERVALLE, TAILLE_ECRAN, INTERVALLE):
		for ligne in range(INTERVALLE, TAILLE_ECRAN, INTERVALLE):
			pygame.draw.rect(screen, COULEUR_POINTS_GRILLE, pygame.Rect(colonne,ligne, TAILLE_TRAITS,TAILLE_TRAITS))

	mot_1 = f'{mot_1:<{TAILLE_MOTS}}'
	mot_2 = f'{mot_2:<{TAILLE_MOTS}}'

	if x_actif:
		couleur_x = 'blue'
		couleur_y = 'black'
	else:
		couleur_x = 'black'
		couleur_y = 'blue'

	# lignes
	for n,lettre in enumerate(mot_2):
		screen.blit(POLICE_MOTS.render(lettre, 1, couleur_x), (INTERVALLE//3, INTERVALLE+n*INTERVALLE))
		if not lettre == ' ':
			start_on = unicodedata.normalize('NFKD', lettre)[0] in ('aeiouy')
			draw_ligne(n+1,start_on)

	# colonnes
	for n,lettre in enumerate(mot_1):
		screen.blit(POLICE_MOTS.render(lettre, 1, couleur_y), (INTERVALLE+15+n*INTERVALLE, 0))
		if not lettre == ' ':
			start_on = unicodedata.normalize('NFKD', lettre)[0] in ('aeiouy')
			draw_colonne(n+1,start_on)

	# unicode normalize
	#u"".join([c for c in unicodedata.normalize('NFKD', event.unicode) if not unicodedata.combining(c)])
	pygame.display.update()


def draw_ligne(ligne: int, start_on: bool):
	for colonne in range(0,TAILLE_MOTS):
		if start_on:
			pygame.draw.rect(screen, COULEUR_POINTS_TRAITS,
				pygame.Rect(INTERVALLE+colonne*INTERVALLE, ligne*INTERVALLE-(TAILLE_TRAITS/2), INTERVALLE+TAILLE_TRAITS,10))
		start_on = not start_on

def draw_colonne(colonne: int, start_on: bool):
	for ligne in range(0,TAILLE_MOTS):
		if start_on:
			pygame.draw.rect(screen, COULEUR_POINTS_TRAITS,
				pygame.Rect(colonne*INTERVALLE-(TAILLE_TRAITS/2), INTERVALLE+ligne*INTERVALLE-(TAILLE_TRAITS/2), 10,INTERVALLE+2*TAILLE_TRAITS))
		start_on = not start_on

def completer_mot(mot: str, caractere: str) -> str:
	mot = mot + caractere
	if len(mot)>TAILLE_MOTS-1:
		mot = mot[1:]
	return mot

def main():
	clock = pygame.time.Clock()
	jouer = True

	if DEBUG:
		print('intervale = {:d}'.format(INTERVALLE))

	mot_x = mot_y = ''
	mode_colonne = False
	draw(mot_x, mot_y, mode_colonne)

	while jouer:
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()

				elif (event.key == pygame.K_KP_ENTER) or (event.key == pygame.K_RETURN):
					mode_colonne = not mode_colonne

				elif event.key == pygame.K_BACKSPACE:
					if mode_colonne:
						mot_y = mot_y[:-1]
					else:
						mot_x = mot_x[:-1]

				else:
					if mode_colonne:
						mot_y = completer_mot(mot_y, event.unicode)
					else:
						mot_x = completer_mot(mot_x, event.unicode)

				# Visuals : draw()
				draw(mot_x, mot_y, mode_colonne)

if __name__ == "__main__":
	main()
