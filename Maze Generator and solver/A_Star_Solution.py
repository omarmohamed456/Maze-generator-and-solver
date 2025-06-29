
from maze_generator import *

from GeneralSearch import *

from GeneralSearch import get_neighbors

from GUI import *

import heapq

#A star

def manhattan_distance(a, b):
    """Heuristic function: Manhattan distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(grid, start_cell, end_cell):

    # Initializing components
    open_list = []  # Priority queue (min-heap)
    heapq.heappush(open_list, (0, start_cell))  # (f_score, position)

    g_score = {start_cell: 0}

    parent = {}  # To reconstruct path
    explored = set()


    start_time = time.time() #start timer
    path_steps = 0

    found = False

    while open_list:
        _, current = heapq.heappop(open_list) # _ means the first item in the tuple is ignored ## it is not needed the position of the cell is needed but the f score is not
        path_steps += 1

        if current == end_cell:
            found = True
            break

        explored.add(current) #visited and explored
        x, y = current

        #core algorithm
        for neighbor in get_neighbors(grid, x, y):
            if neighbor in explored: #skip visited and explored
                continue #skip this iteration

            temporary_g = g_score[current] + 1  # new g(n) cost (1 step)

            if neighbor not in g_score or temporary_g < g_score[neighbor]: #if this is the first time to calculate f(n) to this neighbour ## check the g_score in the dict for the neighbour if the temporary is shorter ###if both are false we just check next iteration
                g_score[neighbor] = temporary_g
                f_score = temporary_g + manhattan_distance(neighbor, end_cell) #calcualte f for the cell
                heapq.heappush(open_list, (f_score, neighbor))
                parent[neighbor] = current #path

    # Reconstruct path
    path = []
    if found:
        cell = end_cell
        while cell != start_cell:
            path.append(cell)
            cell = parent[cell]
        path.append(start_cell)
        path.reverse()

    end_time = time.time()

    return path, found,len(path) ,path_steps, end_time - start_time


def show_a_star_results_window(path, found, path_len, path_steps, elapsed_time):
    def run_window():
        window = tk.Tk()
        window.title("a_star Algorithm Results")
        window.geometry("300x300")

        ttk.Label(window, text="✔ Search Results", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Label(window, text=f"✔ Path found: {found}", font=("Arial", 12)).pack()
        ttk.Label(window, text=f"✔ Path cost: {path_len}", font=("Arial", 12)).pack()
        ttk.Label(window, text=f"✔ Steps taken: {path_steps}", font=("Arial", 12)).pack()
        ttk.Label(window, text=f"✔ Time: {elapsed_time:.6f} s", font=("Arial", 12)).pack()
        ttk.Button(window, text="Close", command=window.destroy).pack(pady=10)

        window.mainloop()
    threading.Thread(target=run_window).start()


def a_star_visualize_gui(grid, start, end, screen, maze_area, delay):
    open_set = []
    heapq.heappush(open_set, (0, start))

    g_score = {start: 0}
    parent = {}
    visited = set()

    found = False
    path_steps = 0
    path = []

    while open_set:
        _, current = heapq.heappop(open_set)
        path_steps += 1

        visited.add(current)
        x, y = current

        # Frontier includes all positions in open_set (ignore the current popped)
        frontier = [pos for _, pos in open_set if pos != current]

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
            if neighbor in visited:
                continue

            tentative_g = g_score[current] + 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f_score = tentative_g + manhattan_distance(neighbor, end)
                heapq.heappush(open_set, (f_score, neighbor))
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
