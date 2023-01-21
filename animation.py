import pygame

#definir classe qui va gérer les animations
class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, sprite_name):
        super().__init__()
        self.image = pygame.image.load(f"PygameAssets-main/{sprite_name}.png")

#définir fonction pour c harger les images d'un sprite
def load_animation_images(sprite_name):
    #charger les 24 images du sprite
    images=[]
    #récuperer le hemin du dossier
    path = f"PygameAssets-main{sprite_name}/{sprite_name}"
    
    #boucler pour chaque image
    for i in range(1, 24):
       image_path =  path + i + '.png'
       images.append(pygame.image.load(image_path))

    #renvoyer le contenu de la liste
    return images

#définir dictionnaire qui va contenir les images de chaques sprite
#mummy -> [mummy1.png, mummy2.png, ...]
animations ={
    'mummy' : load_animation_images('mummy')
}