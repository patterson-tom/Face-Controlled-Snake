import pygame

from Player import Player

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

NUM_CELLS_X = DISPLAY_WIDTH/20
NUM_CELLS_Y = DISPLAY_HEIGHT/20
    
def main():
    pygame.init()
    gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption("Snake")

    main_loop(gameDisplay)

def main_loop(gameDisplay):
    backgroundColor = 0x000000
    gameExit = False

    #handler holds all the sprites in the game, and is responsible for updating and drawing them
    player = Player((5,5), gameDisplay, NUM_CELLS_X, NUM_CELLS_Y)
    #handler = Handler()
    
    clock = pygame.time.Clock()

    #game loop, executes 60 times per second
    while not gameExit:
            
        #checks for key events and moves player accordingly
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(backgroundColor)

        player.update()
        player.draw()
        
        
        
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
