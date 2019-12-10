# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 21:43:42 2019

@author: Paul
"""

import math

def read_data(filename):
    """
    Reads asteroid map and outputs a list of asteroid positions
    """
    
    data = ''
    asteroid_list = []
    i = 0
    
    f = open(filename, 'r')
    for line in f:       
        data = line.strip('\n')    
        for j in range(len(data)):
            if data[j] == '#':
                asteroid_list.append((j, i))
        i += 1
        
    f.close()   
    
    return asteroid_list


def find_relative_positions(asteroid_list):
    """
    Takes list of asteroid positions.
    
    Finds the relative position of every other asteroid to each asteroid,
    and returns a dictionary with keys of asteroid positions and values of a tuple the
    relative position of each other asteroid, and its manhattan distance to the key asteroid.
    
    The order of the relative positions is sorted closest to longest distance.
    """
    
    data = asteroid_list[:]
    relative_pos = {}
    
    # Iterate over all asteroids and add each as a key with a list as value
    print("Finding relative positions from each asteroid to every other asteroid.")
    for i in range(len(data)):
        relative_pos[data[i]] = []
        
        # For each asteroid key, add all other asteroids relative positions as values
        for j in range(len(data)):
            if data[i] != data[j]:
                rel_coords = (data[j][0] - data[i][0], data[j][1] - data[i][1])
                rel_dist = ((rel_coords[0])**2 + (rel_coords[1])**2)**0.5
                rel_dist = (round(rel_dist, 3),)
                relative_pos[data[i]].append(rel_coords + rel_dist)
        
        # Sort the list from closest to furthest asteroids
        relative_pos[data[i]].sort(key= lambda tup: tup[2])
                    
    return relative_pos
    

def find_visible(relative_asteroid_positions):
    """
    Takes a dictionary with keys of asteroid positions and
    values of list of tuples containing the relative positions and euclidean
    distances to each asteroid.
    
    For each asteroid it then determines which other asteroids are visible
    (not blocked directly by another asteroid).
    
    Returns a dict with keys of asteroids and values a list of the relative positions
    of visible asteroids from the key asteroid.
    """
    
    visible = {}
    data = relative_asteroid_positions.copy()
    
    # Iterate through each asteroid key and add each to the visible dict
    print("Searching for visible asteroids from each asteroid.")
    for entry in data:
        visible[entry] = []
        check = data[entry][:]
        visible[entry].append(check[0])
        #print("finding visible asteroids from: ", entry)
        
        # Iterate through the asteroids around the current asteroid
        for i in range(1, len(check), 1):
            blocked = False
            # If the surrounding asteroid is not along the same vector as another, add to list
            for j in range(len(visible[entry])):
                vis =  visible[entry][:]
                # Check not to divide by zero
                if vis[j][0] == 0:
                    if check[i][0] == 0 and check[i][1] * vis[j][1] > 0:
                        blocked = True
                elif vis[j][1] == 0:
                    if check[i][1] == 0 and check[i][0] * vis[j][0] > 0:
                        blocked = True               
                # Check otherwise if asteroid lies on same vector as visible asteroid
                elif check[i][0]/vis[j][0] == check[i][1]/vis[j][1]:
                    # Check the asteroid lies on same side as visible asteroid
                    if check[i][0] * vis[j][0] > 0 and check[i][0] * vis[j][0] > 0:
                        blocked = True
            if not blocked:
                visible[entry].append(check[i])
                    
    return visible

def find_max_visible(visible_asteroid_dict):
    """
    Takes a dictionary containing keys: asteroid positions values: relative positions
    of visible asteroids from the key asteroid.
    
    Returns the position of the asteroid with the most visible asteroids, and the
    number of visible asteroids.
    """
    
    best_result = -1
    print("Finding asteroid location with most visible asteroids.")
    
    for asteroid in visible_asteroid_dict:
        test_result = len(visible_asteroid_dict[asteroid])
        
        if test_result > best_result:
            best_result = test_result
            best_ast = asteroid
            
    return best_ast, best_result

def find_asteroid_angles(relative_asteroids):
    """
    Takes a list of the positions of relative asteroids and their euclidean distance
    from an asteroid.
    
    Uses dot product to deterimine the angle between each asteroid and the 'North'
    vector (0, -1).
    
    Returns a list of each relative asteroid position, its euclidean distance and
    relative angle, sorted in order of increasing angle and increasing distance.
    """
    
    relative_angles = []
    
    for entry in relative_asteroids:
        #Check for asteroids in angle 0 to pi around asteroid
        mag_a = 1
        mag_b = (entry[0]**2 + entry[1]**2)**0.5
        dot = -1 * entry[1]
        if entry[0] >= 0:          
            angle = math.acos(dot/mag_b)
        elif entry[0] < 0:
            angle = math.acos(-dot/mag_b) + math.pi
        
        angle = round(angle, 3)
        
        relative_angles.append(entry + (angle,))
    
    relative_angles.sort(key= lambda tup: tup[3])
    
    return relative_angles

def laser(asteroid_angles):
    """
    Takes list of relative asteroid positions with manhattan distances and
    relative angles from (0,1), sorted in order of increasing angle and increasing
    distance where angles are equal.
    
    Simulates firing a laser from 0 radians (along (0,1)) to 2 pi radians and
    destroying the first asteroid on each angle during the rotation.
    
    Returns a list of the asteroid relative positions, distances and angles in
    order from first to last destroyed.
    """
    
    destruct_ord = []
    asteroids = asteroid_angles[:]
    i = 0
    
    # Run until all asteroids have been destroyed
    while len(asteroids) > 0:
        angles_hit = []
        asteroids_to_remove = []
        #print("Starting new laser rotation")
        # Find any asteroids on angles not yet hit by the laser and add them to removal list
        for entry in asteroids:
            if entry[3] not in angles_hit:
                angles_hit.append(entry[3])
                destruct_ord.append(entry)
                asteroids_to_remove.append(entry)
        
        # Remove the destroyed asteroids for the next spin of the laser        
        for entry in asteroids_to_remove:
            #print("Removed: ", entry, i)
            i += 1
            asteroids.remove(entry)
            
    
    return destruct_ord
        
    
    
asteroids = read_data('day10input.txt')
#print(asteroids)

relative = find_relative_positions(asteroids)
#print(relative)

visible = find_visible(relative)
best, number = find_max_visible(visible)
#print(best, number)
print("Part 1 Answer: Asteroid at " + str(best) + " with num visible: " + str(number))


best_pos_angles = find_asteroid_angles(relative[(8,16)])
#print(best_pos_angles)

order = laser(best_pos_angles)
ast_200 = (order[199][0] + 8, order[199][1] + 16)
print("Part 2 Answer: Asteroid at " + str(ast_200) + " is last to be destroyed.")

#day10test1.txt