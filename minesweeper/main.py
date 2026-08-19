import os
import random
import sys
import pygame
import time

pygame.init()

winning_count = 0

# Einstellungen & Farben
WIDTH, HEIGHT = 800, 600
FPS = 60
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
ROT = (255, 0, 0)
GRUEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()
FONT_MAIN = pygame.font.Font(None, 36)
FONT_BTN = pygame.font.Font(None, 24)

class Block:
    def __init__(self, x, y):
        self.is_revealed = False
        self.is_flagged = False
        self.is_bomb = False
        self.neighbour_mine_number = 0
        self.xpos = x
        self.ypos = y

    def show(self) -> str:
        if self.is_revealed:
            if self.is_flagged:
                return "P"
            elif not self.is_bomb:
                return str(self.neighbour_mine_number)
            else:
                return "X"
        return ""

    def calculate_neighbours(self, grid, area_leng):
        if self.is_bomb:
            return
        count = 0
        for row in range(-1, 2):
            for col in range(-1, 2):
                nx, ny = self.xpos + row, self.ypos + col
                if 0 <= nx < area_leng and 0 <= ny < area_leng:
                    if grid[nx][ny].is_bomb:
                        count += 1
        self.neighbour_mine_number = count
        if self.neighbour_mine_number == 0 and self.is_revealed:
            for row in range(-1, 2):
                for col in range(-1, 2):
                    nx, ny = self.xpos + row, self.ypos + col
                    if 0 <= nx < area_leng and 0 <= ny < area_leng:
                        if not grid[nx][ny].is_revealed and not grid[nx][ny].is_flagged:
                            grid[nx][ny].is_revealed = True
                            grid[nx][ny].calculate_neighbours(grid, area_leng)
                            

def run_game():
    area_leng = 10
    number_of_bombs = 12
    grid = [[Block(i, j) for j in range(area_leng)] for i in range(area_leng)]

    # Bomben platzieren
    count = 0
    while count < number_of_bombs:
        rx, ry = random.randint(0, area_leng - 1), random.randint(0, area_leng - 1)
        if not grid[rx][ry].is_bomb:
            grid[rx][ry].is_bomb = True
            count += 1

    # Nachbarn einmalig vorberechnen
    for row in grid:
        for block in row:
            block.calculate_neighbours(grid, area_leng)

    running = True
    while running:
        clock.tick(FPS)
        clicked_tile = None
        mouse_button = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_tile = event.pos
                mouse_button = event.button

        screen.fill(WEISS)
        text_title = FONT_MAIN.render("Willkommen zu Minesweeper", True, SCHWARZ)
        screen.blit(text_title, (50, 30))

        # Spielfeld zeichnen
        for i in range(area_leng):
            for j in range(area_leng):
                rect = pygame.Rect(i * 45 + 100, j * 45 + 75, 45, 45)
                pygame.draw.rect(screen, SCHWARZ, rect, 1)

                skipp = False
                # Klick-Auswertung
                if clicked_tile and rect.collidepoint(clicked_tile):
                    if mouse_button == 3 and not grid[i][j].is_revealed:
                        grid[i][j].is_flagged = not grid[i][j].is_flagged
                        action = "placed" if grid[i][j].is_flagged else "removed"
                        print(f"Flag {action} at ({i}, {j})")
                    elif mouse_button == 1 and not grid[i][j].is_flagged:
                        if not grid[i][j].is_revealed:
                            grid[i][j].is_revealed = True
                            grid[i][j].calculate_neighbours(grid, area_leng)
                            print(f"Tile revealed at ({i}, {j})")
                            if grid[i][j].is_bomb:
                                return "GAME_OVER"

                if grid[i][j].is_revealed:
                    txt = FONT_MAIN.render(grid[i][j].show(), True, SCHWARZ)
                    screen.blit(txt, (rect.x + 15, rect.y + 10))
                if grid[i][j].is_flagged:
                    txt = FONT_MAIN.render("P", True, ROT)
                    screen.blit(txt, (rect.x + 15, rect.y + 10))

        winning_count = sum(
            1
            for row in grid
            for block in row
            if block.is_revealed and not block.is_bomb
        )
        if winning_count == (area_leng * area_leng) - number_of_bombs:
            return "WIN"

        pygame.display.flip()

def show_screen(message, color):
    while True:
        clock.tick(FPS)
        screen.fill(WEISS)

        txt = FONT_MAIN.render(message, True, color)
        screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - 50))

        btn_retry = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 20, 120, 40)
        btn_exit = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 80, 120, 40)

        pygame.draw.rect(screen, SCHWARZ, btn_retry, 2)
        pygame.draw.rect(screen, SCHWARZ, btn_exit, 2)

        txt_retry = FONT_BTN.render("Try Again", True, SCHWARZ)
        txt_exit = FONT_BTN.render("Exit", True, SCHWARZ)

        screen.blit(txt_retry, (btn_retry.centerx - txt_retry.get_width() // 2, btn_retry.centery - txt_retry.get_height() // 2))
        screen.blit(txt_exit, (btn_exit.centerx - txt_exit.get_width() // 2, btn_exit.centery - txt_exit.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_retry.collidepoint(event.pos):
                    return True
                elif btn_exit.collidepoint(event.pos):
                    return False

        pygame.display.flip()

# Hauptschleife
while True:
    result = run_game()
    if result == "GAME_OVER":
        if not show_screen("Game Over! You hit a bomb.", ROT):
            break
    elif result == "WIN":
        if not show_screen("Congratulations! You won!", GRUEN):
            break

pygame.quit()
sys.exit()