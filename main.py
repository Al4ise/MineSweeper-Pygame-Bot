import pygame
import os
import MineSweeper

WIDTH, HEIGHT = 808, 808
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

FPS = 60
SYMBOL_WIDTH, SYMBOL_HEIGHT = 42, 42
pygame.display.set_caption("Minesweeper")

CELL = pygame.Rect(0, 0, SYMBOL_WIDTH + 2, SYMBOL_HEIGHT + 2)
BOMB_IMAGE = pygame.image.load(os.path.join("Assets", "Bomb.png"))
BOMB = pygame.transform.scale(BOMB_IMAGE, (SYMBOL_WIDTH, SYMBOL_HEIGHT))
FLAG_IMAGE = pygame.image.load(os.path.join("Assets", "Flag.png"))
FLAG = pygame.transform.scale(FLAG_IMAGE, (SYMBOL_WIDTH, SYMBOL_HEIGHT))


def draw_window(PLACEFLAG):
    WIN.fill(WHITE)
    pygame.draw.rect(WIN, GREY, CELL, 2)
    if PLACEFLAG == True:
        WIN.blit(FLAG, (WIDTH - 100, 10))
    elif PLACEFLAG == False:
        WIN.blit(BOMB, (WIDTH - 100, 10))
    pygame.display.update()


def main():
    block = pygame.Rect(0, 0, SYMBOL_WIDTH + 4, SYMBOL_HEIGHT + 4)
    clock = pygame.time.Clock()
    PLACEFLAG = True
    game = MineSweeper.Minesweeper(10)
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                # Change the flag/bomb
                if event.key == pygame.K_f:
                    PLACEFLAG = not PLACEFLAG
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Place Flag/Bomb
                if PLACEFLAG == True:
                    # Place Flag
                    MineSweeper.placeFlag(game, event.pos)
                elif PLACEFLAG == False:
                    # Place Bomb
                    MineSweeper.evaluateSpace(game, event.pos)

        draw_window(PLACEFLAG)

    pygame.quit()


if __name__ == "__main__":
    main()
