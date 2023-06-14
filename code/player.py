import pygame
from settings import *
from support import *
from timer import Timer

"""Aqui se desarrolla el sprite del player"""

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group) #Hace que perteneza al grupo de all_sprites
        self.import_assets()
        
        self.status = 'down_idle' #key 
        self.frame_index = 0

        # general setup
        """Quiero que la image sea del dic en una llave que depende del status, y animacion
        depende de la lista."""
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.z = LAYERS['main'] ## Z dimension
        
        # movement
        """Debido a que self.rect moveria a la figura con valores enteros
        es mejor crear un vector que almacene la posicion exacta a la que
        se quiere ir, y luego darsela al self.rect"""
        self.direction = pygame.math.Vector2() #vector de (x,y)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 300
        
        # timers
        self.timers = {
            'tool use': Timer(400, self.use_tool),
            'tool switch': Timer(500),
            'seed use': Timer(400, self.use_seed),
            'seed switch': Timer(1000)
        }
        # tools
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]
        
        # seeds
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]
     
    def use_tool(self):
        # return self.selected_tool
        pass
    
    def use_seed(self):
        # return self.selected_seed
        pass
    
    def import_assets(self):
        """Debido a que son demasiadas animaciones, 
        lo mejor es crear un diccionario que asocie
        una accion a una carpeta con animaciones"""
        self.animations = {'up': [], 'down': [], 'left': [],'right': [],
'right_idle':[], 'left_idle':[], 'up_idle': [], 'down_idle':[],
'right_hoe':[], 'left_hoe':[], 'up_hoe': [], 'down_hoe':[],
'right_axe':[], 'left_axe':[], 'up_axe': [], 'down_axe':[],
'right_water':[], 'left_water': [], 'up_water': [], 'down_water':[]}
        for animation in self.animations.keys():
            character_path = 'c:/Users/esteb/OneDrive/Email attachments/Documents/Proyectos/Programacion/juego_stardewV/graphics/character/' + animation #acede a la carpeta segun la llave del dic
            self.animations[animation] = import_folder(character_path) #A cada llave le importo las animaciones.
           
    def animate(self, dt):
        """Esta funcion genera la animacion para cualquier lista que se genere"""
        self.frame_index += 4 * dt ## -> Esta es la tasa de cambio entre animaciones
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]
    
    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timers['tool use'].active:
            # horizontal
            if keys[pygame.K_a]:
                self.direction.x = -1 
                self.status = 'left' 
            elif keys[pygame.K_d]:      
                self.direction.x = 1
                self.status = 'right'  
            else:self.direction.x = 0
            # vertical
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1  
                self.status = 'down'
            else: self.direction.y = 0
            
        ## tool use
        if keys[pygame.K_SPACE]:
            self.timers['tool use'].activate()
            self.direction = pygame.math.Vector2() ##detiene al jugador
            self.frame_index = 0
    
        ## change tool
        if keys[pygame.K_q] and not self.timers['tool switch'].active:
            self.timers['tool switch'].activate()
            self.tool_index += 1
            if self.tool_index >= len(self.tools):
                self.tool_index = 0
            self.selected_tool = self.tools[self.tool_index]
        
        ## seed use
        if keys[pygame.K_LSHIFT]:
            self.timers['seed use'].activate()
            self.direction = pygame.math.Vector2() ##detiene al jugador
            self.frame_index = 0
    
        ## change seed
        if keys[pygame.K_r] and not self.timers['seed switch'].active:
            self.timers['seed switch'].activate()
            self.seed_index += 1
            if self.seed_index >= len(self.seeds):
                self.seed_index = 0
            self.selected_seed = self.seeds[self.seed_index]
                
    def get_status(self):
        # idle
        if self.direction.magnitude() == 0: ##Si se dejo de mover
            # self.status += '_idle'   ##Mal porque se agregaria una y otra vez
            self.status = self.status.split('_')[0] + '_idle'
            """El self.status anterior deberia ser correspondiente al mov que
            tuvo antes de detenerse, por lo que le agrego el _idle (que genio :D)(manipula 
            strings)(mas optimizado que mi metodo)"""       
        # tool use
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool
            
        # if self.timers['seeds use'].active:
        #     self.status = self_'_' + 
    
    def update_timers(self):
        for timer in self.timers.values(): #valores de un dic
            timer.update()
            
    def move(self, dt):
        # vector normalizado
        """Debido a que la velocidad en mov diagonal 
        es mucho mayor, se debe normalizar el vector"""
        if self.direction.magnitude() > 0: #revisa si el vector no es 0
            self.direction = self.direction.normalize()
            # print(self.direction)   
        # horiz move
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x
        # vert move
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y
            
    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.move(dt) #frame rate indep
        self.animate(dt)
        
    