import pygame
import sys
from pygame.locals import *

KOLOR_BIALY = (255, 255, 255)
KOLOR_CZERWONY = (255, 0, 0)
KOLOR_CZARNY = (0, 0, 0)

SZEROKOSC_PLANSZY = 1024
DLUGOSC_PLANSZY = 700
SZEROKOSC_CELU = 94	
DLUGOSC_CELU = 15
SZEROKOSC_KLADKI = 150
DLUGOSC_KLADKI = 20	
TAB_CELE_X = 10	
TAB_CELE_Y = 7
PREDKOSC_PILKI = 2
WIELKOSC_PILKI = 10	

# Klasa celu
class Cel(pygame.sprite.Sprite):
	# Inicjalizowanie celu
    def __init__(this):
        pygame.sprite.Sprite.__init__(this)
        this.image = pygame.Surface((SZEROKOSC_CELU, DLUGOSC_CELU))
        this.rect = this.image.get_rect()	
        this.name = 'cel'


# Klasa pilki
class Pilka(pygame.sprite.Sprite):
	# Inicjalizowanie pilki
    def __init__(this):
        pygame.sprite.Sprite.__init__(this)
        this.name = 'pilka'					
        this.ruch = False												
        this.image = pygame.Surface((WIELKOSC_PILKI, WIELKOSC_PILKI))
        this.image.fill(KOLOR_BIALY)				
        this.rect = this.image.get_rect()		
        this.wsp_x = PREDKOSC_PILKI				
        this.wsp_y = PREDKOSC_PILKI		
	
	# Aktualizacja pozycji pilki
    def update(this, myszka, cele, kladka, *args):
		# Pilka podaza za myszka kiedy nie wykonano ruchu
        if this.ruch == False:
            this.rect.centerx = myszka

        else:
            this.rect.y += this.wsp_y
            this.rect.x += this.wsp_x
            grupa = pygame.sprite.Group(kladka, cele)
            lista_zderzen = pygame.sprite.spritecollide(this, grupa, False)	
			
            if len(lista_zderzen) > 0:
                for sprite in lista_zderzen:
                    if sprite.name == 'cel':
                        sprite.kill()															# Usuwanie trafionego celu
                this.wsp_y *= -1																# Zmiana kierunku pilki na przeciwny     

			# Kontrolowanie odbicia pilki od prawej sciany
            if this.rect.right > SZEROKOSC_PLANSZY:
                this.wsp_x *= -1
                this.rect.right = SZEROKOSC_PLANSZY

			# Kontrolowanie odbicia pilki od lewej sciany
            elif this.rect.left < 0:
                this.wsp_x *= -1
                this.rect.left = 0

			# Kontrolowanie odbicia pilki od gornej sciany
            if this.rect.top < 0:
                this.wsp_y *= -1
                this.rect.top = 0
			
			# Kontrolowanie odbicia pilki od dolnej sciany
            if this.rect.bottom > DLUGOSC_PLANSZY:
				this.stworzEkranGameOver()						
				
	# Tworzenie ekranu Game Over
    def stworzEkranGameOver(this):
        screen = pygame.display.set_mode([1024, 700])								
        background_image = pygame.image.load("gameover.png").convert()				
 
        while True:
            for event in pygame.event.get():
				# Obsluga zakonczenia rozgrywki
                if event.type == QUIT:
                    sys.exit()
			
            screen.blit(background_image, [0,0])								
            pygame.display.flip()														
			
# Klasa kladki
class Kladka(pygame.sprite.Sprite):
	# Inicjalizowanie kladki
    def __init__(this):
        pygame.sprite.Sprite.__init__(this)
        this.image = pygame.Surface((SZEROKOSC_KLADKI, DLUGOSC_KLADKI))						
        this.image.fill(KOLOR_BIALY)													
        this.rect = this.image.get_rect()										
        this.name = 'kladka' 													

	# Aktualizacja pozycji kladki
    def update(this, myszka, *args):
		# Jezeli kursor ruszy sie gdziekolwiek
        if this.rect.x >= 0 and this.rect.right <= SZEROKOSC_PLANSZY:
            this.rect.centerx = myszka

		# Jezeli kursor wyjedzie poza lewa czesc planszy
        if this.rect.x < 0:
            this.rect.x = 0

		# Jezeli kursor wyjedzie poza prawa czesc planszy
        elif this.rect.right > SZEROKOSC_PLANSZY:
            this.rect.right = SZEROKOSC_PLANSZY
        
    
# Klasa rozgrywki
class Rozgrywka(object):
	# Inicjalizowanie rozgrywki
    def __init__(this):
        pygame.init()																
        this.wyswietl_powierzchnie, this.wyswietl_prostokaty = this.stworzOknoGry()			
        this.myszka = 0																	
        this.cele = this.stworzCele()													
        this.kladka = this.stworzKladke()												
        this.pilka = this.stworzPilke()													
        this.obiekty = pygame.sprite.Group(this.cele, this.kladka, this.pilka)				
		
	# Tworzenie okna gry
    def stworzOknoGry(this):
        pygame.display.set_caption('Arkanoid v1.0')											
        wyswietl_powierzchnie = pygame.display.set_mode((SZEROKOSC_PLANSZY, DLUGOSC_PLANSZY))
        wyswietl_prostokaty = wyswietl_powierzchnie.get_rect()							
        wyswietl_powierzchnie.fill(KOLOR_CZARNY)										

        return wyswietl_powierzchnie, wyswietl_prostokaty

	# Tworzenie pilki
    def stworzPilke(this):
        pilka = Pilka()																	
        pilka.rect.bottom = this.kladka.rect.top												# Pilka na dole

        return pilka

	# Tworzenie kladki
    def stworzKladke(this):
        kladka = Kladka()																	
        kladka.rect.bottom = this.wyswietl_prostokaty.bottom									# Kladka na dole

        return kladka

	# Tworzenie celow
    def stworzCele(this):
        cele = pygame.sprite.Group()												
        
        for i in range(TAB_CELE_Y):
            for j in range(TAB_CELE_X):
                cel = Cel()															
                cel.rect.x = j * (SZEROKOSC_CELU + 10)								
                cel.rect.y = i * (DLUGOSC_CELU + 10)								
                cel.image.fill(KOLOR_CZERWONY)									
                cele.add(cel)											
				
        return cele  
	
	# Tworzenie ekranu You Win
    def stworzEkranYouWin(this):
        screen = pygame.display.set_mode([1024, 768])								
        background_image = pygame.image.load("youwin.png").convert()					
 
        while True:
            for event in pygame.event.get():
				# Obsluga zakonczenia rozgrywki
                if event.type == QUIT:
                    sys.exit()
			
            screen.blit(background_image, [0,0])											
            pygame.display.flip()															

	# Obsluga wejscia
    def wejscie(this):
        for event in pygame.event.get():
			# Obsluga zakonczenia rozgrywki
            if event.type == QUIT:
				sys.exit()

			# Obsluga myszki
            if event.type == MOUSEMOTION:
                this.myszka = event.pos[0]

			# Obsluga przyciskow myszy do wyrzucenia pilki
            elif event.type == MOUSEBUTTONUP:
				this.pilka.ruch = True

	# Obsluga rozgrywki
    def graj(this):
        while this.cele:
            this.wyswietl_powierzchnie.fill(KOLOR_CZARNY)										# Aktualizowanie tla
            this.obiekty.update(this.myszka, this.cele, this.kladka)							# Aktualizowanie obiektow
            this.obiekty.draw(this.wyswietl_powierzchnie)										# Rysowanie obiektow
            pygame.display.update()																# Aktualizowanie ekranu
            this.wejscie()        																# Obsluga wejscia
		        
        this.stworzEkranYouWin()														
   
if __name__ == '__main__':
    gra = Rozgrywka()																			# Tworzenie rozgrywki
    gra.graj()																					# Uruchomienie rozgrywki
   
