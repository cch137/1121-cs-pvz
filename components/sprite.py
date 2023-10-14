import pygame

class Sprite(pygame.sprite.Sprite):
    bg_color: str = None

    def __init__(self, image: pygame.Surface | (int, int)):
        if type(image) == pygame.Surface:
            self.image = image
        elif type(image) == tuple:
            if type(image[0]) == int and type(image[1]) == int:
                self.image = pygame.Surface((image[0], image[1]))
        else:
            raise 'Invalid image'
        self.rect = self.image.get_rect()

    def addEventListener(event: str, listener: function):
        pass

    def removeEventListener(event: str, listener: function):
        pass

    def dispatchEvent(event: str):
        pass

class Grid(Sprite):
    pass

class Character(Sprite):
    pass
