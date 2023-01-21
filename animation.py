import pygame
import random

#definir classe qui va gérer les animations
class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, sprite_name):
        super().__init__()
        self.image = pygame.image.load(f"PygameAssets-main/{sprite_name}.png")
        self.current_image = 0 #commencer l'animation à l'image 0
        self.images = animations.get(sprite_name)
        self.animation = False
    
    #Définir méthode pour démarrer anim
    def start_animation(self):
        self.animation = True

    #définir méthode pour animer le sprite
    def animate(self, loop = False):
        #verifier si l'anim est active
        if self.animation:
            #passer à l'image suivante
            self.current_image += random.randint(0, 1)

            #vérifier si on est au bout de l'anim
            if self.current_image >= len(self.images):
                #remettre l'anim au départ
                self.current_image = 0
                #si l'animation n'est pas en mode boucle 
                if loop == False:
                    #désactivation de l'anim
                    self.animation = False
            #modifier l'image de l'animation précédente par la suivante
            self.image = self.images[self.current_image]
        

#définir fonction pour c harger les images d'un sprite
def load_animation_images(sprite_name):
    #charger les 24 images du sprite
    images=[]
    #récuperer le hemin du dossier
    path = f"PygameAssets-main/{sprite_name}/{sprite_name}"
    
    #boucler pour chaque image
    for i in range(1, 24):
       image_path =  path + str(i) + '.png'
       images.append(pygame.image.load(image_path))

    #renvoyer le contenu de la liste
    return images

#définir dictionnaire qui va contenir les images de chaques sprite
#mummy -> [mummy1.png, mummy2.png, ...]
animations ={
    'mummy' : load_animation_images('mummy'),
    'player' : load_animation_images('player')
}