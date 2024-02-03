import pygame
import os
import MineSweeper

GRID_WIDTH = 10
GAME = MineSweeper.Minesweeper(GRID_WIDTH)

HEIGHT = 1000
WIDTH = 1.1*HEIGHT
SYMBOL_WIDTH, SYMBOL_HEIGHT = HEIGHT/GRID_WIDTH, HEIGHT/GRID_WIDTH

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
CELL = pygame.Rect(0, 0, SYMBOL_WIDTH + 2, SYMBOL_HEIGHT + 2)

FPS = 60
pygame.display.set_caption("Minesweeper")

BOMB_IMAGE = pygame.image.load(os.path.join("Assets", "Bomb.png"))
BOMB = pygame.transform.scale(BOMB_IMAGE, (SYMBOL_WIDTH, SYMBOL_HEIGHT))
FLAG_IMAGE = pygame.image.load(os.path.join("Assets", "Flag.png"))
FLAG = pygame.transform.scale(FLAG_IMAGE, (SYMBOL_WIDTH, SYMBOL_HEIGHT))

def main():
    pygame.font.init()
    clock = pygame.time.Clock()
    PLACEFLAG = True
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
                x, y = pygame.mouse.get_pos()
                handleClick(x, y, GAME, PLACEFLAG)

        if not GAME.playing:
            run=False
            if GAME.didWin():
                alert_message("You win!")
            else:
                alert_message("You lose!")

        draw_window(PLACEFLAG)

    pygame.quit()

def draw_status_bar(PLACEFLAG):
    ICON_POSITION = (WIDTH - 100, 10)

    if PLACEFLAG == True:
        WIN.blit(FLAG, ICON_POSITION)
    elif PLACEFLAG == False:
        WIN.blit(BOMB, ICON_POSITION)

def draw_window(PLACEFLAG):
    WIN.fill(WHITE)

    draw_status_bar(PLACEFLAG)
    draw_game_board()
    pygame.display.update()

def handleClick(x, y, GAME, PLACEFLAG):
    # find which cell was clicked
    i = int(x // SYMBOL_WIDTH)
    j = int(y // SYMBOL_HEIGHT)

    GAME.placeSymbol(i, j, PLACEFLAG)

def alert_message(message):
    font = pygame.font.Font(None, 50)  # Set the font and size for the message text
    text_surface = font.render(message, True, (0, 0, 0))  # Render the message text
    text_rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))  # Center the text on the screen
    #WIN.fill(WHITE)  # Clear the screen
    pygame.draw.rect(WIN, GREY, (WIDTH / 4, HEIGHT / 4, WIDTH / 2, HEIGHT / 2))  # Draw a big box
    WIN.blit(text_surface, text_rect)  # Draw the message text on the screen
    pygame.display.update()  # Update the display
    pygame.time.delay(3000)  # Delay for 3 seconds

def draw_game_board():
    font = pygame.font.Font(None, 30)  # Set the font and size for the number text
    for i in range(GRID_WIDTH):
        for j in range(GRID_WIDTH):
            if GAME.playerBoard[i][j] == 7:
                WIN.blit(FLAG, (i * SYMBOL_WIDTH, j * SYMBOL_HEIGHT))
            elif GAME.playerBoard[i][j] == 6:
                WIN.blit(BOMB, (i * SYMBOL_WIDTH, j * SYMBOL_HEIGHT))
            elif GAME.playerBoard[i][j] == 0:
                CELL.x = int(i * SYMBOL_WIDTH)
                CELL.y = int(j * SYMBOL_HEIGHT)
                pygame.draw.rect(WIN, GREY, CELL, 2)
            else:
                cell_value = GAME.playerBoard[i][j]
                CELL.x = int(i * SYMBOL_WIDTH)
                CELL.y = int(j * SYMBOL_HEIGHT)
                pygame.draw.rect(WIN, GREY, CELL, 2)
                text_surface = font.render(str(cell_value), True, (0, 0, 0))  # Render the number text
                text_rect = text_surface.get_rect(center=(CELL.x + SYMBOL_WIDTH / 2, CELL.y + SYMBOL_HEIGHT / 2))  # Center the text inside the cell
                WIN.blit(text_surface, text_rect)  # Draw the number text onto the cell


if __name__ == "__main__":
    main()
