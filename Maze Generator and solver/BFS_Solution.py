
from GeneralSearch import *
from collections import deque
from maze_generator import *

from GeneralSearch import get_neighbors
from GeneralSearch import draw_visualization
from GUI import *

# BFS

# Orginal BFS
def bfs(grid, start_cell, end_cell):
    # initalizing components

    queue = deque()  # to be visited
    visited = set()
    parent = {}  # to track path
    start_time = time.time()  # timer

    queue.append((0, start_cell))  # (depth, (x, y)) #tuples 
    visited.add(start_cell)

    found = False  # end condition
    path_steps = 0  #

    # core BFS
    while queue:
        depth, current = queue.popleft()  # get next cell out from the queue  FIFO
        x, y = current  # set x y
        path_steps += 1

        if current == end_cell:  # end condition  (exploration)
            found = True
            break

        for neighbor in get_neighbors(grid, x, y):

            if neighbor not in visited:
                queue.append((depth + 1, neighbor))  # add to be explored
                visited.add(neighbor)  # add same neighbor to visited
                parent[neighbor] = current

            # to get the final path
    path = []
    if found:

        cell = end_cell  # start from end to start

        while cell != start_cell:  # condition to end
            path.append(cell)
            cell = parent[cell]

        path.append(start_cell)  # add the start cell
        path.reverse()  # to be start to end

    end_time = time.time()  # end of timer

    return path, found, len(path), path_steps, end_time - start_time


def show_BFS_results_window(path, found, path_len, path_steps, elapsed_time):
    def run_window():
        window = tk.Tk()
        window.title("BFS Algorithm Results")
        window.geometry("300x300")

        ttk.Label(window, text="✔ Search Results", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Label(window, text=f"✔ Path found: {found}", font=("Arial", 12)).pack()
        ttk.Label(window, text=f"✔ Path cost: {path_len}", font=("Arial", 12)).pack()
        ttk.Label(window, text=f"✔ Steps taken: {path_steps}", font=("Arial", 12)).pack()
        ttk.Label(window, text=f"✔ Time: {elapsed_time:.6f} s", font=("Arial", 12)).pack()
        ttk.Button(window, text="Close", command=window.destroy).pack(pady=10)

        window.mainloop()

    threading.Thread(target=run_window).start()


def bfs_visualize_gui(grid, start, end, screen, maze_area, delay):
    queue = deque()
    visited = set()
    parent = {}

    queue.append((0, start))
    visited.add(start)

    found = False
    path_steps = 0
    path = []

    while queue:
        depth, current = queue.popleft()
        x, y = current
        path_steps += 1

        frontier = [pos for _, pos in queue if pos != current]
        # draw_visualization(screen, grid, visited, current, path, frontier, maze_area)
        draw_visualization(screen, grid, visited, current, path, frontier, maze_area, start, end)

        pygame.time.delay(int(delay * 1000))  # delay still needs to be passed or defined
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if current == end:
            found = True
            break

        for neighbor in get_neighbors(grid, x, y):
            if neighbor not in visited:
                queue.append((depth + 1, neighbor))
                visited.add(neighbor)
                parent[neighbor] = current

    if found:
        cell = end
        while cell != start:
            path.append(cell)
            cell = parent[cell]
        path.append(start)
        path.reverse()

    # Final path rendering
    for step in path:
        # draw_visualization(screen, grid, visited, step, path, [], maze_area)
        draw_visualization(screen, grid, visited, current, path, frontier, maze_area, start, end)

        pygame.time.delay(int(delay * 1000))

    return path