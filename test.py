import tkinter as tk
import random
from statistics import mean

import numpy as np
from matplotlib import pyplot as plt

sleep_matrix = np.zeros((100, 100))
colors = {"white": 0, "blue": 5, "red": -1, "purple": 1, "gray": 2, "yellow": 3, "green": 4}


def create_grid(p):
    rows = 100
    cols = 100
    grid_window = np.zeros((100, 100))
    for i in range(rows):
        for j in range(cols):
            color = "blue" if random.random() < p else "white"
            grid_window[i, j] = colors[color]
    return grid_window


def make_colors(grid_window, s1, s2, s3):
    persons = []
    for i in range(100):
        for j in range(100):
            color = grid_window[i][j]
            if color == 5:
                persons.append((i, j))
    for p in persons:
        rand = random.random()
        if rand <= s1:
            grid_window[p[0], p[1]] = colors["purple"]
        elif rand <= (s1 + s2):
            grid_window[p[0], p[1]] = colors["gray"]
        elif rand <= (s1 + s2 + s3):
            grid_window[p[0], p[1]] = colors["yellow"]
        else:
            grid_window[p[0], p[1]] = colors["green"]


def update_color(color):
    if color == 4:
        return 3
    elif color == 3:
        return 2
    elif color == 2:
        return 1


def check_neighbour(grid_window, x, y, received_matrix):
    if not(100 > x >= 0) or not(100 > y >= 0):
        return
    color = grid_window[x][y]

    if received_matrix[x][y] >= 2:
        color = update_color(color)

    # s4
    if color == 4:
        return
    # s1
    if color == 1:
        grid_window[x, y] = colors["red"]
    percent = random.random()
    # s2
    if color == 2:
        if percent < 0.333:
            grid_window[x, y] = colors["red"]
    # s3
    if color == 3:
        if percent < 0.666:
            grid_window[x, y] = colors["red"]


def make_red(grid_window, num_of_iterations, l_generations):
    persons = []
    for i in range(100):
        for j in range(100):
            color = grid_window[i][j]
            if color != 0:
                persons.append((i, j))

    red_cube = random.choice(persons)
    grid_window[red_cube[0], red_cube[1]] = colors["red"]

    for i in range(num_of_iterations + 1):
        reds = []
        for i in range(100):
            for j in range(100):
                color = grid_window[i][j]
                if color == -1:
                    reds.append((i, j))
        received_matrix = np.zeros((100, 100))
        for r in reds:
            if (100 > r[0] >= 0) and (100 > r[1]-1 >= 0):
                received_matrix[r[0]][r[1]-1] = received_matrix[r[0]][r[1]-1] + 1
            if (100 > r[0] >= 0) and (100 > r[1] + 1 >= 0):
                received_matrix[r[0]][r[1]+1] = received_matrix[r[0]][r[1]+1] + 1
            if (100 > r[0] - 1 >= 0) and (100 > r[1] >= 0):
                received_matrix[r[0]-1][r[1]] = received_matrix[r[0]-1][r[1]] + 1
            if (100 > r[0] + 1 >= 0) and (100 > r[1] >= 0):
                received_matrix[r[0]+1][r[1]] = received_matrix[r[0]+1][r[1]] + 1

            if 0 < sleep_matrix[r[0]][r[1]] < l_generations:
                sleep_matrix[r[0]][r[1]] = sleep_matrix[r[0]][r[1]] + 1
            else:
                sleep_matrix[r[0]][r[1]] = 0
                check_neighbour(grid_window, r[0], r[1]-1, received_matrix)
                check_neighbour(grid_window, r[0], r[1]+1, received_matrix)
                check_neighbour(grid_window, r[0]-1, r[1], received_matrix)
                check_neighbour(grid_window, r[0]+1, r[1], received_matrix)
                sleep_matrix[r[0]][r[1]] = sleep_matrix[r[0]][r[1]] + 1

    # test for graph
    reds = []
    for i in range(100):
        for j in range(100):
            color = grid_window[i][j]
            if color == -1:
                reds.append((i, j))
    return len(reds)


def submit(values):
    # print("Input values:")
    # for title, value in zip(titles, values):
    #     print(f"{title}: {value}")
    grid_window = create_grid(float(values[0]))
    make_colors(grid_window, float(values[3]), float(values[4]), float(values[5]))
    return make_red(grid_window, num_of_iterations=int(values[2]), l_generations=int(values[1]))


def create_graph():
    fig, ax = plt.subplots()
    x_pos = np.arange(len(n_values))
    ax.bar(x_pos, num_of_red_cubes)

    # add labels and title
    ax.set_xticks(x_pos)
    ax.set_xticklabels(n_values)
    ax.set_ylabel('number of receivers')
    ax.set_xlabel('n values')

    # display the plot
    plt.show()


# Add labels to input values
titles = ["P", "L", "N", "S1", "S2", "S3", "S4"]

p_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
l_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
n_values = [10, 50, 100, 200]
num_of_red_cubes = []

for n in n_values:
    default_values = [0.8, 3, n, 0.4, 0.1, 0.1, 0.4]
    list_of_ans = []
    for i in range(10):
        list_of_ans.append(submit(default_values))
    num_of_red_cubes.append(mean(list_of_ans))

print(num_of_red_cubes)

# create the bar plot
create_graph()

