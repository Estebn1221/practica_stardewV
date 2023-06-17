import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water
from pytmx.util_pygame import load_pygame
from support import *

class Level:
    def __init__(self):
        # obtiene la display surface
        self.display_surface = pygame.display.get_surface() #obtiene las dims de la surface de main
        # sprite groups
        self.all_sprites = CameraGroup()
        
        self.setup()
        self.overlay = Overlay(self.player)
        
     
    def  setup(self):
        tmx_data = load_pygame('c:/Users/esteb/OneDrive/Email attachments/Documents/Proyectos/Programacion/juego_stardewV/data/map.tmx')
        for layer in ['HouseFloor', 'HouseFurnitureBottom','HouseWalls', 'HouseFurnitureTop', 'Fence']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                if layer == 'HouseFloor' or layer == 'HouseFurnitureBottom': #house
                    Generic((x*TITLE_SIZE, y*TITLE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])
                elif layer == 'HouseWalls' or layer == 'HouseFurnitureTop': 
                    Generic((x*TITLE_SIZE, y*TITLE_SIZE), surf, self.all_sprites, LAYERS['main'])
                else: #fence
                    Generic((x*TITLE_SIZE, y*TITLE_SIZE), surf, self.all_sprites, LAYERS['main'])
        # Water  
        water_frames = import_folder('c:/Users/esteb/OneDrive/Email attachments/Documents/Proyectos/Programacion/juego_stardewV//graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            Water((x*TITLE_SIZE, y*TITLE_SIZE), water_frames, self.all_sprites)             
                    
        # Crear al jugador
        self.player = Player((500, 500), self.all_sprites)
        
        # Crear otros sprites y elementos
        Generic(
            pos = (0,0),
            surf = pygame.image.load('c:/Users/esteb/OneDrive/Email attachments/Documents/Proyectos/Programacion/juego_stardewV/graphics/world/ground.png').convert_alpha(),
            groups = self.all_sprites,
            z = LAYERS['ground'])
        
        
    
    def run(self, dt): #deltaTime para independencia de frames
        self.display_surface.fill('black')
        """Funciones de draw y update para los sprites"""
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt) #Llama al update de player
        
        self.overlay.display()
        
class CameraGroup(pygame.sprite.Group): ##Nota: Ver video de cameras
    """Optimizado para no tener que pasar la dislplay_surface para
    que ocurra el draw"""
    def __init__(self):
        super().__init__() ##Para que el grupo funcione por si mismo
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        
    def custom_draw(self, player):
        """Queremos una camara que apunte siempre al jugados, y siga su rectangulo de 
        posicion, y que muestre la mitad del ancho de pantalla, y la mitad de la altura de pantalla."""
        self.offset.x = player.rect.centerx - SCREEN_WIDTH/2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT/2
        for layer in LAYERS.values():
            for sprite in self.sprites(): # metodo
                """Esto es lo que le suele pasar a un grupo para
                el metodo .draw -> Imita a la funcion draw"""
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
        