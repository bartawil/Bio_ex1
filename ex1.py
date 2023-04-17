import tkinter as tk
import random
import random
import time


class GridWindow(tk.Frame):
    def __init__(self, parent, rows, cols, size=6):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.size = size
        self.canvas = tk.Canvas(self, width=cols*size, height=rows*size)
        self.canvas.pack()
        self.rectangles = [[self.canvas.create_rectangle(
            c*size, r*size, (c+1)*size, (r+1)*size,
            fill="white", outline="black"
        ) for c in range(cols)] for r in range(rows)]

    def set_rectangle_color(self, row, col, color):
        self.canvas.itemconfig(self.rectangles[row][col], fill=color)


def create_grid(parent, p):
    rows = 100
    cols = 100
    grid_window = GridWindow(parent, rows, cols)
    for i in range(rows):
        for j in range(cols):
            color = "blue" if random.random() < p else "white"
            grid_window.set_rectangle_color(i, j, color)
    return grid_window


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


def check_neighbour(grid_window, x, y):
    color = grid_window.canvas.itemcget(grid_window.rectangles[x][y], "fill")
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


def make_red(grid_window, num_of_iterations):
    rows = grid_window.rows
    cols = grid_window.cols
    persons = []
    for i in range(rows):
        for j in range(cols):
            color = grid_window.canvas.itemcget(grid_window.rectangles[i][j], "fill")
            if color != "white":
                persons.append((i, j))

    red_cube = random.choice(persons)
    grid_window.set_rectangle_color(red_cube[0], red_cube[1], "red")

    for i in range(num_of_iterations + 1):
        reds = []
        for i in range(rows):
            for j in range(cols):
                color = grid_window.canvas.itemcget(grid_window.rectangles[i][j], "fill")
                if color == "red":
                    reds.append((i, j))
        time.sleep(0.02)
        for r in reds:
            check_neighbour(grid_window, r[0], r[1]-1)
            check_neighbour(grid_window, r[0], r[1]+1)
            check_neighbour(grid_window, r[0]-1, r[1])
            check_neighbour(grid_window, r[0]+1, r[1])



def submit():
    values = [entry_var.get() for entry_var in entry_vars]
    print("Input values:")
    for title, value in zip(titles, values):
        print(f"{title}: {value}")
    global new_window
    new_window = tk.Toplevel()
    new_window.geometry("1000x1000")
    new_window.title("Grid")
    grid_window = create_grid(new_window, float(values[0]))
    grid_window.grid(row=0, column=1, sticky="nsew")
    make_colors(grid_window, float(values[3]), float(values[4]), float(values[5]), float(values[6]))
    new_window.after(2000, lambda: make_red(grid_window, int(values[2])))

root = tk.Tk()
root.geometry("400x300")
root.title("Menu")

# Add labels to input values
titles = ["P", "L", "N", "S1", "S2", "S3", "S4"]
for i, title in enumerate(titles):
    label = tk.Label(root, text=title)
    label.grid(row=i, column=0, padx=5, pady=5)

entry_vars = []
default_values = [0.5, 4, 10, 0.1, 0.4, 0.4, 0.1]
for i in range(7):
    var = tk.StringVar(value=default_values[i])
    entry_vars.append(var)
    entry = tk.Entry(root, textvariable=var)
    entry.grid(row=i, column=1, padx=5, pady=5)

submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()