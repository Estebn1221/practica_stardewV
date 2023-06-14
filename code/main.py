import pygame, sys 
from settings import *
from level import Level #clase Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #width, height
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Munch valley')
        self.level = Level()

    """-> Ejecucion del juego <-"""   
    def run(self): 
        while True:
            #Event loop 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() #cerrar ventana -> cerrar juego
                    sys.exit() # -> salir del loop
                    
            dt = self.clock.tick()/1000 # Delta time
            self.level.run(dt) # -> Llama a la funcion run()
            pygame.display.update()
            
if __name__ == '__main__': 
    game = Game()
    game.run()