
from maze_generator import *

from GUI import *

import tkinter as tk
from tkinter import ttk
import threading

import pygame



#constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

CELL_SIZE = 20
PADDING = 50
DARK_GRAY = (100, 100, 100)


pygame.init()  # Initialize pygame modules before using font or other subsystems

FONT = pygame.font.SysFont("arial", 30)
SMALL_FONT = pygame.font.SysFont("arial", 24)

# Compute maze size
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


###used in to visualize
def get_neighbors(grid, x, y): 

    neighbors = [] #to store tubles of connected cells 

    for direction in [N, S, E, W]:

        if grid[y][x] & direction: #checks from which side is the cell open open = no wall no wall = path #it uses and bitwise operator
            nx, ny = x + DX[direction], y + DY[direction]

            if 0 <= nx < width and 0 <= ny < height: #if condition to make sure we don't go out of maze
                neighbors.append((nx, ny))

    return neighbors


def draw_visualization(screen, grid, visited, current, path, frontier, maze_rect, start=None, end=None):
    screen.fill(WHITE)

    # top label
    top_label = FONT.render("Pathfinding Visualization", True, BLACK)
    screen.blit(top_label, (WIDTH // 2 - top_label.get_width() // 2, 30))

    rows = len(grid)
    cols = len(grid[0])
    offset_x = maze_rect.x
    offset_y = maze_rect.y

    for y in range(rows):
        for x in range(cols):
            px = offset_x + x * CELL_SIZE
            py = offset_y + y * CELL_SIZE
            pos = (x, y)

            if pos == start or pos == end:
                color = (128, 0, 128)  # Purple
            elif pos == current:
                color = (255, 0, 0)  # Red
            elif pos in path:
                color = (255, 255, 0)  # Yellow
            elif pos in frontier:
                color = (0, 255, 0)  # Green
            elif pos in visited:
                color = (0, 0, 255)  # Blue
            else:
                color = (210, 250, 130)  # Default

            pygame.draw.rect(screen, color, (px, py, CELL_SIZE, CELL_SIZE))

            # Wall rendering
            cell = grid[y][x]
            if not (cell & 1):  # N
                pygame.draw.line(screen, BLACK, (px, py), (px + CELL_SIZE, py), 2)
            if not (cell & 2):  # S
                pygame.draw.line(screen, BLACK, (px, py + CELL_SIZE), (px + CELL_SIZE, py + CELL_SIZE), 2)
            if not (cell & 8):  # W
                pygame.draw.line(screen, BLACK, (px, py), (px, py + CELL_SIZE), 2)
            if not (cell & 4):  # E
                pygame.draw.line(screen, BLACK, (px + CELL_SIZE, py), (px + CELL_SIZE, py + CELL_SIZE), 2)

    pygame.display.update()


def show_all_results_window(bfs_path, bfs_found, bfs_len, bfs_steps, bfs_time,
                            dfs_path, dfs_found, dfs_len, dfs_steps, dfs_time,
                            astar_path, astar_found, astar_len, astar_steps, astar_time):
    def run_window():
        window = tk.Tk()
        window.title("All Search Algorithm Results")
        window.geometry("600x400")
        window.resizable(False, False)

        style = ttk.Style()
        style.configure("TLabelframe", background="#f0f0f0")
        style.configure("TLabelframe.Label", font=("Arial", 12, "bold"))
        style.configure("TLabel", font=("Arial", 11), background="#f0f0f0")

        frame = ttk.Frame(window, padding=20)
        frame.pack(fill="both", expand=True)

        def add_algo_result(parent, title, found, path_len, steps, elapsed_time):
            box = ttk.LabelFrame(parent, text=title, padding=15, width=170, height=140)
            box.pack(side="left", expand=True, fill="both", padx=10)

            ttk.Label(box, text=f"✔ Path found: {found}").pack(anchor="w", pady=2)
            ttk.Label(box, text=f"✔ Path cost: {path_len}").pack(anchor="w", pady=2)
            ttk.Label(box, text=f"✔ Steps taken: {steps}").pack(anchor="w", pady=2)
            ttk.Label(box, text=f"✔ Time: {elapsed_time:.6f} s").pack(anchor="w", pady=2)

        # Add result boxes
        add_algo_result(frame, "BFS", bfs_found, bfs_len, bfs_steps, bfs_time)
        add_algo_result(frame, "DFS", dfs_found, dfs_len, dfs_steps, dfs_time)
        add_algo_result(frame, "A*", astar_found, astar_len, astar_steps, astar_time)

        ttk.Button(window, text="Close", command=window.destroy).pack(pady=10)

        window.mainloop()

    threading.Thread(target=run_window).start()

