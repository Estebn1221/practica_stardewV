import pygame

"""Nota: Todavia me cuesta un poco entender las partes
de los timers. --> Segun probe, la cinematica da el tiempo en el cual
se repetira la accion que se quiere ejecutar, por lo que 
en 1 seg se alcanzan a ejecutar dos veces toda la animacion"""
"""--> Por ejemplo, el timer para el tool_switch restringe el tiempo
para el cual al presionar la q, esta actuara, si el tiempo es muy pequeno,
dara cabida a que al presionar la q una vez, salga como si se hubiera presionado 
mas veces."""
class Timer:
    def __init__(self, duration, func = None):
        self.duration = duration
        self.func = func
        self.start_time = 0
        self.active = False
    
    def activate(self): #funcion para activar timer
        self.active = True
        self.start_time = pygame.time.get_ticks()
        
    def deactivate(self): #funcion para desactivar timer
        self.active = False
        self.start_time = 0
    
    def update(self):
        """Ya que update sera llamado varias veces, current_time
        es el tiempo que transcurre."""
        current_time = pygame.time.get_ticks() 
        if current_time - self.start_time >= self.duration: 
            """Si pasa esto, el timer deberia de acabarse."""
            self.deactivate()
            if self.func:
                self.func()
                