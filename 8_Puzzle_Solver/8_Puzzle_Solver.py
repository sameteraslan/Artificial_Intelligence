#!/usr/bin/env python
# coding: utf-8

#-------------------------


import random
import copy


#-------------------------


asagi_ok = "    ↓    "
cizgi = "---------"        


#-------------------------


def create_random_matrix():
    initial_matrix = [[], [], []]
    current_random = sayac = satir = sutun = 0 
    while sayac < 9:
        current_random = int(random.uniform(1,9))
        if current_random in initial_matrix[0] or current_random in initial_matrix[1] or current_random in initial_matrix[2]:
            continue
        if satir == 1 and sutun == 1:
            initial_matrix[satir].append(0)
            satir += 1
            sayac += 1
        elif satir > 2:
            satir = 0
            sutun += 1
        else:
            initial_matrix[satir].append(current_random)
            sayac += 1
            satir += 1
    return initial_matrix

def make_zero_cost_dict():
    out_dict = {}
    for i in range(1, 9):
        out_dict[i] = 0
    return out_dict

def calculate_cost_of_number(initial_matrix, goal_matrix, number):
    satir_1, sutun_1 = find_number(initial_matrix, number)
    satir_2, sutun_2 = find_number(goal_matrix, number)
    return abs(satir_1 - satir_2) + abs(sutun_1 - sutun_2)

def calculate_total_cost(initial_matrix, goal_matrix):
    total = 0
    for i in range(9):
        total += calculate_cost_of_number(initial_matrix, goal_matrix, i)
    return total
def calculate_total_position_cost(initial_matrix, goal_matrix):
    total = 0
    satir = 0
    for i in initial_matrix:
        for j in range(len(i)):
            if i[j] != goal_matrix[satir][j]:
                total += 1
        satir += 1
    return total        

def min_cost_matrix(matrix_list, goal_matrix):
    min_cost = 999999
    index = 0
    min_cost_index = 0
    min_cost_index_list = []
    for i in matrix_list:
        cost = calculate_total_cost(i, goal_matrix)
        cost = cost + 3 * calculate_total_position_cost(i, goal_matrix)
        cost = int(cost)
        if cost == 0:
            return index
        if min_cost > cost:
            min_cost = cost
            min_cost_index = index 
            min_cost_index_list = [min_cost_index]
        elif min_cost == cost:
            min_cost = cost
            min_cost_index = index
            min_cost_index_list.append(min_cost_index)
        index += 1
    return int(random.uniform(0,len(min_cost_index_list)))

def find_number(matrix, number):
    satir = sutun = 0
    for i in matrix:
        if number in i:
            for j in i:
                if j == number:
                    return satir, sutun
                sutun += 1
        satir += 1

def print_matrix(matrix):
    for i in matrix:
        print(i)
        
def find_possible_movements(matrix, number = 0):
    #                     r  l  d  u
    possible_movements = [0, 0, 0, 0]
    row, col = find_number(matrix, number)
    if row == 0:   #down
        possible_movements[2] = 1
    elif row == 1: #down and up
        possible_movements[2] = 1
        possible_movements[3] = 1
    elif row == 2: #up
        possible_movements[3] = 1
        
    if col == 0:   #right
        possible_movements[0] = 1
    elif col == 1: #rigth and left
        possible_movements[0] = 1
        possible_movements[1] = 1
    elif col == 2: #left
        possible_movements[1] = 1
    return possible_movements

def swap_number(matrix, direction, number = 0):
    new_matrix = copy.deepcopy(matrix)
    row, col = find_number(new_matrix, number)
    if direction == "r":
        new_matrix[row][col], new_matrix[row][col + 1] = new_matrix[row][col + 1], new_matrix[row][col]
    elif direction == "l":
        new_matrix[row][col], new_matrix[row][col - 1] = new_matrix[row][col - 1], new_matrix[row][col] 
    elif direction == "d":
        new_matrix[row][col], new_matrix[row + 1][col] = new_matrix[row + 1][col], new_matrix[row][col]
    elif direction == "u":
        new_matrix[row][col], new_matrix[row - 1][col] = new_matrix[row - 1][col], new_matrix[row][col]
    return new_matrix

def search_goal(matrix, goal_matrix, print_steps = False):
    counter = 0
    prev_matrix = []
    possible_movements = find_possible_movements(matrix, 0)
    while matrix != goal_matrix:
        next_step_matrixes = []
        if possible_movements[0] == 1: #right
            next_step_matrixes.append(swap_number(matrix, "r"))
        if possible_movements[1] == 1: #left
            next_step_matrixes.append(swap_number(matrix, "l"))
        if possible_movements[2] == 1: #down
            next_step_matrixes.append(swap_number(matrix, "d"))
        if possible_movements[3] == 1: #up
            next_step_matrixes.append(swap_number(matrix, "u"))
        index = min_cost_matrix(next_step_matrixes, goal_matrix)
        new_matrix = next_step_matrixes[index]
        if prev_matrix == next_step_matrixes[index]:
            next_step_matrixes.remove(next_step_matrixes[index])
            new_matrix = next_step_matrixes[0]
        prev_matrix = matrix
        matrix = new_matrix
        possible_movements = find_possible_movements(matrix, 0)
        print("Step {}:".format(counter))
        if print_steps:
            print_matrix(matrix)
            print(asagi_ok)
        counter += 1
    print("Found at: {}. iteration".format(counter - 1))


#-------------------------


goal_matrix = [[0, 1, 2], 
               [3, 4, 5], 
               [6, 7, 8]]

matrix =      [[3, 1, 2],
               [6, 4, 5],
               [7, 0, 8]]

print("Initial Matrix:")
print_matrix(matrix)
print(cizgi)
print(cizgi)
print("Goal Matrix:")
print_matrix(goal_matrix)


#-------------------------

search_goal(matrix, goal_matrix, True)
