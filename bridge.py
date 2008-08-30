import pygame

def create_world(game):
    rect = pygame.Rect((0,800), (350, -250))
    rect.normalize()
    pygame.draw.rect(game.screen, (100,180,255), rect, 3)
    game.world.add.rect(rect.center, rect.width / 2, rect.height / 2,
        dynamic=False)
    rect = pygame.Rect((1200,800), (-350, -250))
    rect.normalize()
    pygame.draw.rect(game.screen, (100,180,255), rect, 3)
    game.world.add.rect(rect.center, rect.width / 2, rect.height / 2,
        dynamic=False)

