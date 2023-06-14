import os # Para poder acceder a las carpetas del sistema
import pygame

"""La idea es que esta funcion vaya al path dado para
que importe las carpetas correspondientes a la animacion"""
def import_folder(path):
    surface_list = []
    
    #for root, dirs, files in walk(path):
    for (root,dirs,files) in os.walk(path): #los da como una lista
        # print(files)
        for image in files:
            # print(image)
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha() 
            surface_list.append(image_surf)
    return surface_list


"""Obtenemos finalmente un diccionario con una lista de surfaces
para cada llave del diccionario que corresponde a una accion del player."""