import tkinter as tk
import random
import numpy as np

sleep_matrix = np.zeros((100, 100))


class GridWindow(tk.Frame):
    def __init__(self, parent, rows, cols, size=6):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.size = size
        self.canvas = tk.Canvas(self, width=cols * size, height=rows * size)
        self.canvas.pack()
        self.rectangles = [[self.canvas.create_rectangle(
            c * size, r * size, (c + 1) * size, (r + 1) * size,
            fill="white", outline="black"
        ) for c in range(cols)] for r in range(rows)]

    def set_rectangle_color(self, row, col, color):
        self.canvas.itemconfig(self.rectangles[row][col], fill=color)


# set random cubes to represent person
def create_grid(parent, p):
    rows = 100
    cols = 100
    grid_window = GridWindow(parent, rows, cols)
    for i in range(rows):
        for j in range(cols):
            color = "blue" if random.random() < p else "white"
            grid_window.set_rectangle_color(i, j, color)
    return grid_window


# set level of skepticism for random people based on the restrictions
def make_colors(grid_window, s1, s2, s3, s4):
    rows = grid_window.rows
    cols = grid_window.cols
    persons = []
    for i in range(rows):
        for j in range(cols):
            color = grid_window.canvas.itemcget(grid_window.rectangles[i][j], "fill")
            if color == "blue":
                persons.append((i, j))
    for p in persons:
        rand = random.random()
        if rand <= s1:
            grid_window.set_rectangle_color(p[0], p[1], "purple")
        elif rand <= (s1 + s2):
            grid_window.set_rectangle_color(p[0], p[1], "gray")
        elif rand <= (s1 + s2 + s3):
            grid_window.set_rectangle_color(p[0], p[1], "yellow")
        else:
            grid_window.set_rectangle_color(p[0], p[1], "green")


# this method is for part B
def update_make_colors(grid_window):
    rows = grid_window.rows
    cols = grid_window.cols
    persons = []
    for i in range(rows):
        for j in range(cols):
            color = grid_window.canvas.itemcget(grid_window.rectangles[i][j], "fill")
            if color == "blue":
                persons.append((i, j))
    for p in persons:
        # place each person in different line based on his level skepticism
        if p[0] % 4 == 0:
            grid_window.set_rectangle_color(p[0], p[1], "purple")
        elif p[0] % 4 == 1:
            grid_window.set_rectangle_color(p[0], p[1], "yellow")
        elif p[0] % 4 == 2:
            grid_window.set_rectangle_color(p[0], p[1], "green")
        else:
            grid_window.set_rectangle_color(p[0], p[1], "gray")


# when level of skepticism going down
def update_color(color):
    if color == "green":
        return "yellow"
    elif color == "yellow":
        return "gray"
    elif color == "gray":
        return "purple"


# check if neighbour can receive rummer based on his level of skepticism
def check_neighbour(grid_window, x, y, received_matrix):
    # return if the cube not part of the grid
    if not (100 > x >= 0) or not (100 > y >= 0):
        return
    color = grid_window.canvas.itemcget(grid_window.rectangles[x][y], "fill")

    # if person got rummer from more then 1 neighbour his level of skepticism going down
    if received_matrix[x][y] >= 2:
        color = update_color(color)

    # s4
    if color == "green":
        return
    # s1
    if color == "purple":
        grid_window.set_rectangle_color(x, y, "red")
    percent = random.random()
    # s2
    if color == "gray":
        if percent < 0.333:
            grid_window.set_rectangle_color(x, y, "red")
    # s3
    if color == "yellow":
        if percent < 0.666:
            grid_window.set_rectangle_color(x, y, "red")


# this function spreading the rumor and colors the infected person as a red cube
def make_red(grid_window, num_of_iterations, l_generations):
    rows = grid_window.rows
    cols = grid_window.cols
    # get only the cubes that represent persons
    persons = []
    for i in range(rows):
        for j in range(cols):
            color = grid_window.canvas.itemcget(grid_window.rectangles[i][j], "fill")
            if color != "white":
                persons.append((i, j))

    # start the rummer from random person
    red_cube = random.choice(persons)
    grid_window.set_rectangle_color(red_cube[0], red_cube[1], "red")

    # spreading the rummer to neighbors
    for i in range(num_of_iterations + 1):
        # find at each iteration who already got the rummer
        reds = []
        for i in range(rows):
            for j in range(cols):
                color = grid_window.canvas.itemcget(grid_window.rectangles[i][j], "fill")
                if color == "red":
                    reds.append((i, j))
        # check who already received the rummer at this generation
        received_matrix = np.zeros((100, 100))
        for r in reds:
            if (100 > r[0] >= 0) and (100 > r[1] - 1 >= 0):
                received_matrix[r[0]][r[1] - 1] = received_matrix[r[0]][r[1] - 1] + 1
            if (100 > r[0] >= 0) and (100 > r[1] + 1 >= 0):
                received_matrix[r[0]][r[1] + 1] = received_matrix[r[0]][r[1] + 1] + 1
            if (100 > r[0] - 1 >= 0) and (100 > r[1] >= 0):
                received_matrix[r[0] - 1][r[1]] = received_matrix[r[0] - 1][r[1]] + 1
            if (100 > r[0] + 1 >= 0) and (100 > r[1] >= 0):
                received_matrix[r[0] + 1][r[1]] = received_matrix[r[0] + 1][r[1]] + 1

            # check who cannot send the rummer at this generation
            if 0 < sleep_matrix[r[0]][r[1]] < l_generations:
                sleep_matrix[r[0]][r[1]] = sleep_matrix[r[0]][r[1]] + 1
            else:
                sleep_matrix[r[0]][r[1]] = 0
                check_neighbour(grid_window, r[0], r[1] - 1, received_matrix)
                check_neighbour(grid_window, r[0], r[1] + 1, received_matrix)
                check_neighbour(grid_window, r[0] - 1, r[1], received_matrix)
                check_neighbour(grid_window, r[0] + 1, r[1], received_matrix)
                sleep_matrix[r[0]][r[1]] = sleep_matrix[r[0]][r[1]] + 1
            grid_window.update()
    reds = []
    for i in range(100):
        for j in range(100):
            color = grid_window.canvas.itemcget(grid_window.rectangles[i][j], "fill")
            if color == "red":
                reds.append((i, j))


# the code for part A start form here
def submit_A():
    values = [entry_var.get() for entry_var in entry_vars]
    global new_window
    new_window = tk.Toplevel()
    new_window.geometry("1000x1000")
    new_window.title("Simulation A")
    # set the random persons places
    grid_window = create_grid(new_window, float(values[0]))
    grid_window.grid(row=0, column=1, sticky="nsew")
    # set each person level of skepticism
    make_colors(grid_window, float(values[3]), float(values[4]), float(values[5]), float(values[6]))
    # start spreading the rummer
    make_red(grid_window, num_of_iterations=int(values[2]), l_generations=int(values[1]))


# the code for part B start from here
def submit_B():
    # get the values from the menu inputs
    values = [entry_var.get() for entry_var in entry_vars]
    global new_window
    new_window = tk.Toplevel()
    new_window.geometry("1000x1000")
    new_window.title("Simulation B")
    # set the random persons places
    grid_window = create_grid(new_window, float(values[0]))
    grid_window.grid(row=0, column=1, sticky="nsew")
    # set each person level of skepticism
    update_make_colors(grid_window)
    # start spreading the rummer
    make_red(grid_window, num_of_iterations=int(values[2]), l_generations=int(values[1]))


# initialize the GUI part
root = tk.Tk()
root.geometry("250x300")
root.title("Menu")

# Add labels to input values
titles = ["P", "L", "N", "S1", "S2", "S3", "S4"]
for i, title in enumerate(titles):
    label = tk.Label(root, text=title)
    label.grid(row=i, column=0, padx=5, pady=5)

# store the input values
entry_vars = []
# set default values for inputs
default_values = [0.8, 3, 100, 0.1, 0.4, 0.4, 0.1]
# get the input from the user
for i in range(7):
    var = tk.StringVar(value=default_values[i])
    entry_vars.append(var)
    entry = tk.Entry(root, textvariable=var)
    entry.grid(row=i, column=1, padx=5, pady=5)

# part A button
submit_button = tk.Button(root, text="Part A", command=submit_A)
submit_button.grid(row=7, column=0, columnspan=2, padx=0, pady=5)
# part B button
submit_button = tk.Button(root, text="Part B", command=submit_B)
submit_button.grid(row=7, column=1, columnspan=2, padx=100, pady=5)

root.mainloop()
