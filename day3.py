# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 10:14:01 2019

@author: Paul
"""

def read_data(filename):
    """
    Reads input data and splits up directions and distance.
    """
    
    data = []
    
    f = open(filename, 'r')
    for line in f:
        data += line.strip('\n').split(',')
    
    
    f.close()   
    
    return data


def create_path(wire):
    """
    Takes a list of tuples containing instructions as to the wire path.
    e.g. ('R', 124) -> Right 124 units
  
    Generates and returns a list of tuples representing the coordinates
    that a wire travels along on its path.
    """
    
    path = []
    position = [0, 0]
    path.append(position[:])
    
    for i in range(len(wire)):
        
        if wire[i][0] == 'U':
            for j in range(wire[i][1]):
                position[0] += 1
                path.append(position[:])
                
        if wire[i][0] == 'D':
            for j in range(wire[i][1]):
                position[0] -= 1
                path.append(position[:])
                
        if wire[i][0] == 'R':
            for j in range(wire[i][1]):
                position[1] += 1
                path.append(position[:])
                
        if wire[i][0] == 'L':
            for j in range(wire[i][1]):
                position[1] -= 1
                path.append(position[:])           
    
    return path


def find_closest_cross(wire1_path, wire2_path):
    """
    Compare the coordinates of two wire paths to find the crossing point 
    closest (Manhattan Distance) to the origin (0,0).
    
    Returns a list of crossing points, the closest crossing point and its distance to the start point
    """
    
    best_result = -1
    crossing_list = []
    
    for i in range(len(wire1_path)):
        if wire1_path[i] in wire2_path and wire1_path[i] != [0,0]:
            
            test_result = abs(wire1_path[i][0]) + abs(wire1_path[i][1])
            crossing_list.append(wire1_path[i])
            
            if best_result == -1:
                best_cross = wire1_path[i][:]
                best_result = test_result
            
            elif test_result < best_result:
                best_cross = wire1_path[i][:]
                best_result = test_result
                
    return crossing_list, best_cross, best_result


def find_shortest_cross(wire1_path, wire2_path, crossing_list):
    """
    Takes wire1_path and wire2_path, lists containing two-element lists representing the coordinates
    of the path each wire takes, and crossing_list, a list of coordinate points where the two wires meet.

    Returns the crossing point and with the shortest total wire distance of both wires from the origin,
    and its total wire length from the origin from both wires.
    """   

    shortest = -1

    for i in range(len(crossing_list)):
        test_result = wire1_path.index(crossing_list[i]) + wire2_path.index(crossing_list[i])
        
        if shortest == -1:
            shortest_cross = crossing_list[i][:]
            shortest = test_result
        
        elif test_result < shortest:
            shortest_cross = crossing_list[i][:]
            shortest = test_result
            
    return shortest_cross, shortest

data = read_data("day3input.txt")

wire1 = [(i[0], int(i[1:])) for i in data[:301]]
wire2 = [(i[0], int(i[1:])) for i in data[301:]]

# Extra Wires to test with
#wire3 = [('R', 75), ('D', 30), ('R', 83), ('U', 83), ('L', 12), ('D', 49), ('R', 71), ('U', 7), ('L', 72)]
#wire4 = [('U', 62), ('R', 66), ('U', 55), ('R', 34), ('D', 71), ('R', 55), ('D', 58), ('R', 83)]

print('Generating wire 1 path')
wire1_path = create_path(wire1)
print('Generating wire 2 path')
wire2_path = create_path(wire2)
print('Searching for crossover points')
crossing_list, closest_cross, distance = find_closest_cross(wire1_path, wire2_path)

print('Crossing points: ', crossing_list)
print('Closest crossing point: ', closest_cross)
print('Closest Distance: ', distance)

shortest_cross, shortest_dist = find_shortest_cross(wire1_path, wire2_path, crossing_list)
print('Shortest Crossing Point: ', shortest_cross)
print('Shortest Distance: ', shortest_dist)