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

def draw(mot_1, mot_2):
	screen.fill('white')

	# grille
	for colonne in range(INTERVALLE, TAILLE_ECRAN, INTERVALLE):
		for ligne in range(INTERVALLE, TAILLE_ECRAN, INTERVALLE):
			pygame.draw.rect(screen, COULEUR_POINTS_GRILLE, pygame.Rect(colonne,ligne, TAILLE_TRAITS,TAILLE_TRAITS))

	mot_1 = f'{mot_1:<{TAILLE_MOTS}}'
	mot_2 = f'{mot_2:<{TAILLE_MOTS}}'

	# lignes
	for n,lettre in enumerate(mot_2):
		screen.blit(POLICE_MOTS.render(lettre, 1, 'black'), (INTERVALLE//3, INTERVALLE-15+n*INTERVALLE))
		if not lettre == ' ':
			start_on = unicodedata.normalize('NFKD', lettre)[0] in ('a')
			draw_ligne(n+1,start_on)

	# colonnes
	for n,lettre in enumerate(mot_1):
		screen.blit(POLICE_MOTS.render(lettre, 1, 'blue'), (INTERVALLE-8+n*INTERVALLE, 0))
		if not lettre == ' ':
			start_on = unicodedata.normalize('NFKD', lettre)[0] in ('aeiouy')
			draw_colonne(n+1,start_on)

	# unicode normalize
	#u"".join([c for c in unicodedata.normalize('NFKD', event.unicode) if not unicodedata.combining(c)])
	pygame.display.update()


def draw_ligne(ligne, start_on):
	for colonne in range(0,TAILLE_MOTS):
		if start_on:
			pygame.draw.rect(screen, COULEUR_POINTS_TRAITS,
				pygame.Rect(INTERVALLE+colonne*INTERVALLE, ligne*INTERVALLE-(TAILLE_TRAITS/2), INTERVALLE+TAILLE_TRAITS,10))
		start_on = not start_on

def draw_colonne(colonne, start_on):
	for ligne in range(0,TAILLE_MOTS):
		if start_on:
			pygame.draw.rect(screen, COULEUR_POINTS_TRAITS,
				pygame.Rect(colonne*INTERVALLE-(TAILLE_TRAITS/2), INTERVALLE+ligne*INTERVALLE-(TAILLE_TRAITS/2), 10,INTERVALLE+2*TAILLE_TRAITS))
		start_on = not start_on

def main():
	clock = pygame.time.Clock()
	jouer = True

	if DEBUG:
		print('intervale = {:d}'.format(INTERVALLE))

	mot_x = mot_y = ''#' ' * TAILLE_MOTS
	draw(mot_x, mot_y)

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

				mot_x = mot_x + event.unicode
				if len(mot_x)>TAILLE_MOTS:
					mot_x = mot_x[1:]

				mot_y = mot_y + event.unicode
				if len(mot_y)>TAILLE_MOTS-1:
					mot_y = mot_y[1:]

				# Visuals : draw()
				draw(mot_x, mot_y)

if __name__ == "__main__":
	main()
