from GUI import *

from BFS_Solution import *
from DFS_Solution import *
from A_Star_Solution import *

from maze_generator import *

import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 20
PADDING = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (230, 230, 230)
DARK_GRAY = (100, 100, 100)

FONT = pygame.font.SysFont("arial", 30)
SMALL_FONT = pygame.font.SysFont("arial", 24)

# maze size
rows = len(grid)
cols = len(grid[0]) if rows > 0 else 0
maze_width = cols * CELL_SIZE
maze_height = rows * CELL_SIZE

MAZE_WIDTH = maze_width + PADDING
MAZE_HEIGHT = maze_height + PADDING

# Screen size
WIDTH = max(900, MAZE_WIDTH + 100)
HEIGHT = max(1000, MAZE_HEIGHT + 300)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator & Solver")

# Maze display area (centered)
MAZE_X = (WIDTH - MAZE_WIDTH) // 2
MAZE_Y = 120
MAZE_AREA = pygame.Rect(MAZE_X, MAZE_Y, MAZE_WIDTH, MAZE_HEIGHT)

# Button class
class Button:
    def __init__(self, rect, text, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.hover = False

    def draw(self, surface):
        color = DARK_GRAY if self.hover else BLACK
        pygame.draw.rect(surface, WHITE, self.rect)
        pygame.draw.rect(surface, color, self.rect, 2)
        text_surf = SMALL_FONT.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hover:
            self.callback()


# Exit handler
def exit_button():
    pygame.quit()
    sys.exit()


# Top label
top_label = FONT.render("Welcome!", True, BLACK)

# Buttons setup
buttons = []
button_width = 120
button_height = 40
button_gap = 20
bottom_margin = 180


#buttons actions
def bfs_info():
    result = bfs(grid, start_cell, end_cell)
    show_BFS_results_window(*result)
def dfs_info():
    result = dfs(grid, start_cell, end_cell)
    show_DFS_results_window(*result)
def a_star_info():
    result = a_star(grid, start_cell, end_cell)
    show_a_star_results_window(*result)
def all_info():
    result1 = bfs(grid, start_cell, end_cell)

    result2 = dfs(grid, start_cell, end_cell)

    result3 = a_star(grid, start_cell, end_cell)

    show_all_results_window(*result1, *result2, *result3)
def bfs_visualize():
    bfs_visualize_gui(grid, start_cell, end_cell, screen, MAZE_AREA, delay = 0.5)
def dfs_visualize():
    dfs_visualize_gui(grid, start_cell, end_cell, screen, MAZE_AREA, delay = 0.5)
def a_star_visualize():
    a_star_visualize_gui(grid, start_cell, end_cell, screen, MAZE_AREA, delay = 0.5)


# BFS section
bfs_x_center = WIDTH // 6
bfs_section_y = HEIGHT - bottom_margin
bfs_label = SMALL_FONT.render("BFS", True, BLACK)
bfs_label_rect = bfs_label.get_rect(center=(bfs_x_center, bfs_section_y))
bfs_x_start = bfs_x_center - button_width - button_gap // 2
bfs_y_start = bfs_section_y + 30
# buttons
buttons.append(Button((bfs_x_start, bfs_y_start, button_width, button_height), "info", bfs_info))
buttons.append(Button((bfs_x_start + button_width + button_gap, bfs_y_start, button_width, button_height), "Steps",
                      bfs_visualize))

# #buttons.append(Button((x_start, y_start, button_width, button_height), "info", on_info_button_click())) this directly call the function whoile the button is being created
# buttons.append(Button((x_start, y_start, button_width, button_height), "info", on_info_button_click))

# DFS section
dfs_x_center = WIDTH // 2
dfs_section_y = HEIGHT - bottom_margin
dfs_label = SMALL_FONT.render("DFS", True, BLACK)
dfs_label_rect = dfs_label.get_rect(center=(dfs_x_center, dfs_section_y))
dfs_x_start = dfs_x_center - button_width - button_gap // 2
dfs_y_start = dfs_section_y + 30
# buttons
buttons.append(Button((dfs_x_start, dfs_y_start, button_width, button_height), "info", dfs_info))
buttons.append(Button((dfs_x_start + button_width + button_gap, dfs_y_start, button_width, button_height), "Steps",
                      dfs_visualize))

# A* section

astar_x_center = WIDTH * 5 // 6
astar_section_y = HEIGHT - bottom_margin
astar_label = SMALL_FONT.render("A*", True, BLACK)
astar_label_rect = astar_label.get_rect(center=(astar_x_center, astar_section_y))
astar_x_start = astar_x_center - button_width - button_gap // 2
astar_y_start = astar_section_y + 30
# buttons
buttons.append(Button((astar_x_start, astar_y_start, button_width, button_height), "info", a_star_info))
buttons.append(Button((astar_x_start + button_width + button_gap, astar_y_start, button_width, button_height), "Steps",
                      a_star_visualize))

# Put labels in a list for later rendering
sections = [
    (bfs_label, bfs_label_rect),
    (dfs_label, dfs_label_rect),
    (astar_label, astar_label_rect),
]

# Display All section
all_label = SMALL_FONT.render("Display all", True, BLACK)
all_label_rect = all_label.get_rect(center=(WIDTH // 2, HEIGHT - 80))
buttons.append(Button((WIDTH // 2 - 130, HEIGHT - 50, 120, 40), "Info", all_info))
buttons.append(Button((WIDTH // 2 + 10, HEIGHT - 50, 120, 40), "Exit", exit_button))


# Maze drawing
def draw_maze(screen, grid, maze_rect):

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    #calcualte the maze size in pixels
    maze_width_px = cols * CELL_SIZE
    maze_height_px = rows * CELL_SIZE
    #to center the maze inside the maze area
    offset_x = maze_rect.x + (maze_rect.width - maze_width_px) // 2  #offset os where the maze starts
    offset_y = maze_rect.y + (maze_rect.height - maze_height_px) // 2

    for y in range(rows):
        for x in range(cols):
            cell = grid[y][x]
            px = offset_x + x * CELL_SIZE
            py = offset_y + y * CELL_SIZE

            # Draw white background for every cell
            pygame.draw.rect(screen, (210, 250, 130), (px, py, CELL_SIZE, CELL_SIZE))  # change maze background

            if not (cell & 1):  # N
                pygame.draw.line(screen, BLACK, (px, py), (px + CELL_SIZE, py), 2)
            if not (cell & 2):  # S
                pygame.draw.line(screen, BLACK, (px, py + CELL_SIZE), (px + CELL_SIZE, py + CELL_SIZE), 2)
            if not (cell & 8):  # W
                pygame.draw.line(screen, BLACK, (px, py), (px, py + CELL_SIZE), 2)
            if not (cell & 4):  # E
                pygame.draw.line(screen, BLACK, (px + CELL_SIZE, py), (px + CELL_SIZE, py + CELL_SIZE), 2)


# Main loop
running = True
while running:
    screen.fill(WHITE)
    screen.blit(top_label, (WIDTH // 2 - top_label.get_width() // 2, 30))

    pygame.draw.rect(screen, WHITE, MAZE_AREA)  # Make maze area white
    # pygame.draw.rect(screen, BLACK, MAZE_AREA, 3)
    draw_maze(screen, grid, MAZE_AREA)

    for label, label_rect in sections:
        screen.blit(label, label_rect)

    screen.blit(all_label, all_label_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in buttons:
            button.handle_event(event)

    for button in buttons:
        button.draw(screen)

    pygame.display.flip()

pygame.quit()