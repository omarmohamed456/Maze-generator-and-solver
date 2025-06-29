
from maze_generator import *

from GeneralSearch import *

from GUI import *


from GeneralSearch import get_neighbors

#DFS
def dfs(grid, start_cell, end_cell):
    # Initializing components
    stack = []  # to be visited (LIFO)
    visited = set()
    parent = {}  # to track the path
    start_time = time.time()  # timer

    stack.append(start_cell)
    visited.add(start_cell)

    found = False  # end condition
    path_steps = 0

    # Core DFS
    while stack:
        current = stack.pop()  # get the next cell (LIFO)
        x, y = current
        path_steps += 1

        if current == end_cell:
            found = True
            break

        for neighbor in get_neighbors(grid, x, y):
            if neighbor not in visited:
                stack.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    # To get the final path
    path = []
    if found:

        cell = end_cell #start from end to start

        while cell != start_cell: #condition to end
            path.append(cell)
            cell = parent[cell] 

        path.append(start_cell) #add the start cell
        path.reverse() #to be start to end

    end_time = time.time()

    return path, found,len(path) ,path_steps, end_time - start_time


def show_DFS_results_window(path, found, path_len, path_steps, elapsed_time):
    def run_window():
        window = tk.Tk()
        window.title("DFS Algorithm Results")
        window.geometry("300x300")

        ttk.Label(window, text="✔ Search Results", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Label(window, text=f"✔ Path found: {found}", font=("Arial", 12)).pack()
        ttk.Label(window, text=f"✔ Path cost: {path_len}", font=("Arial", 12)).pack()
        ttk.Label(window, text=f"✔ Steps taken: {path_steps}", font=("Arial", 12)).pack()
        ttk.Label(window, text=f"✔ Time: {elapsed_time:.6f} s", font=("Arial", 12)).pack()
        ttk.Button(window, text="Close", command=window.destroy).pack(pady=10)

        window.mainloop()
    threading.Thread(target=run_window).start()


def dfs_visualize_gui(grid, start, end, screen, maze_area, delay):
    stack = []
    visited = set()
    parent = {}

    stack.append(start)
    visited.add(start)

    found = False
    path_steps = 0
    path = []

    while stack:
        current = stack.pop()
        x, y = current
        path_steps += 1

        # Frontier is what's currently in the stack, excluding the current node
        frontier = [pos for pos in stack if pos != current]

        draw_visualization(screen, grid, visited, current, path, frontier, maze_area, start, end)

        pygame.time.delay(int(delay * 1000))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if current == end:
            found = True
            break

        for neighbor in get_neighbors(grid, x, y):
            if neighbor not in visited:
                stack.append(neighbor)
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
        draw_visualization(screen, grid, visited, current, path, frontier, maze_area, start, end)
        pygame.time.delay(int(delay * 1000))

    return path
