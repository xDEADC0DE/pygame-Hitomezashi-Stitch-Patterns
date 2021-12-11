import pygame
import sys
import unicodedata

# configuration Pygame
DEBUG = False
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
TAILLE_MOT_DEPART = 25
TAILLE_MOT_MINI = 3
TAILLE_MOT_MAXI = 50
MODE_COLONNE_DEPART = False
COULEUR_POINTS_GRILLE = 'gray'
COULEUR_POINTS_TRAITS = 'black'
TAILLE_TRAITS = 5

taille_mot = TAILLE_MOT_DEPART

def draw(mot_1: str, mot_2: str, x_actif: bool):
	intervalle = TAILLE_ECRAN//(taille_mot+1)

	screen.fill('white')

	# grille
	for colonne in range(0, taille_mot):
		for ligne in range(0, taille_mot):
			pygame.draw.rect(screen, COULEUR_POINTS_GRILLE, pygame.Rect(intervalle+colonne*intervalle,intervalle+ligne*intervalle, TAILLE_TRAITS,TAILLE_TRAITS))

	mot_1 = f'{mot_1:<{taille_mot}}'
	mot_2 = f'{mot_2:<{taille_mot}}'

	if x_actif:
		couleur_x = 'blue'
		couleur_y = 'black'
	else:
		couleur_x = 'black'
		couleur_y = 'blue'

	# lignes
	for n,lettre in enumerate(mot_2):
		texte = POLICE_MOTS.render(lettre, 1, couleur_x)
		screen.blit(texte, (intervalle//3, (intervalle-texte.get_height()//2) + (n*intervalle)))
		if not lettre == ' ':
			start_on = unicodedata.normalize('NFKD', lettre)[0] in ('aeiouy02468')
			draw_ligne(intervalle, n+1,start_on)

	# colonnes
	for n,lettre in enumerate(mot_1):
		texte = POLICE_MOTS.render(lettre, 1, couleur_y)
		screen.blit(texte, ((intervalle-texte.get_width()//2) + (n*intervalle), 0))
		if not lettre == ' ':
			start_on = unicodedata.normalize('NFKD', lettre)[0] in ('aeiouy02468')
			draw_colonne(intervalle, n+1,start_on)

	if DEBUG:
		print()
		print(f'taille_mot : {taille_mot}')
		print(f'intervale : {intervalle}')

	pygame.display.update()


def draw_ligne(intervalle: int, ligne: int, start_on: bool):
	for colonne in range(0,taille_mot-1):
		if start_on:
			pygame.draw.rect(screen, COULEUR_POINTS_TRAITS,
				pygame.Rect(intervalle+colonne*intervalle, ligne*intervalle-(TAILLE_TRAITS/2), intervalle+TAILLE_TRAITS,10))
		start_on = not start_on

def draw_colonne(intervalle: int, colonne: int, start_on: bool):
	for ligne in range(0,taille_mot-1):
		if start_on:
			pygame.draw.rect(screen, COULEUR_POINTS_TRAITS,
				pygame.Rect(colonne*intervalle-(TAILLE_TRAITS/2), intervalle+ligne*intervalle-(TAILLE_TRAITS/2), 10,intervalle+2*TAILLE_TRAITS))
		start_on = not start_on

def completer_mot(mot: str, caractere: str) -> str:
	# on ignore les espaces
	if caractere == ' ':
		return mot
		
	mot = mot + caractere
	if len(mot)>taille_mot:
		mot = mot[1:]
	return mot

def main():
	global taille_mot

	clock = pygame.time.Clock()
	jouer = True

	mot_x = mot_y = ''

	mode_colonne = MODE_COLONNE_DEPART
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

				elif (event.key == pygame.K_KP_PLUS) or (event.key == pygame.K_PLUS):
					if taille_mot < TAILLE_MOT_MAXI:
						taille_mot +=1

				elif (event.key == pygame.K_KP_MINUS) or (event.key == pygame.K_MINUS):
					if taille_mot > TAILLE_MOT_MINI:
						taille_mot -=1

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
