# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 09:56:09 2019

@author: Paul
"""
import copy


def read_data(filename):
    """
    Reads orbital map file into a list
    """
    
    data = []
    
    f = open(filename, 'r')
    for line in f:
        data += line.strip().split('\n')
    
    f.close()   
    
    return data

def direct_orbits(map):
    """
    Takes map, a list of orbital map orbit instructions.
    Return a dictionary consisting of 
        keys: each orbital object
        values: the object the object in keys is directly orbiting.
    """
    
    orbits_dict = {}
    
    print("Building direct orbit dictionary....")
    
    # Iterate through map and add each orbital object and the object it directly orbits
    for entry in map:                   
            orbits_dict[entry[4:]] = [entry[:3]]        
    
    return orbits_dict

def all_orbits(direct):
    """
    Takes a dict with keys of orbital bodies and values of the orbital body 
    the key body is directly orbiting.
    Returns a dictionary with values of all direct and indirect orbits of each
    object as the values. Indirect orbits are shown as 1 item lists inside the orbit list.
    
    Also returns the total number of direct and indirect orbits in the map.
    """
    
    ind_orbits_dict = copy.deepcopy(direct)
    
    print("Building indirect orbit dictionary....")
    
    # Iterate through all orbital objects in the direct orbits dictionary
    for planet, orbiting in direct.items():
                
        orbit_found = True
        
        # Start by looking for the object each one is directly orbiting
        to_find = orbiting[0][:]
        
        # If an indirect orbit is found, then that objects direct orbit must be checked
        while orbit_found:
            
            orbit_found = False 
            
            # Iterate through the orbit list to find the next orbit
            for entry in direct:   
                
                # If another orbit is found, search for the orbit of that new object
                if to_find == entry:
                    ind_orbits_dict[planet].append(direct[entry][:][0])
                    orbit_found = True
                    to_find = direct[entry][:][0]
               
    num_orbits = 0

    # Count total orbits in the dictionary
    for entry in ind_orbits_dict.values():
        num_orbits += len(entry)
        
    return ind_orbits_dict, num_orbits


def find_orbital_distance(obj_1, obj_2, ind_orbs):
    """
    Takes two strings, obj_1 and obj_2 and a dictionary of all the direct and
    indirect orbits in the orbital map.
    
    Searches for a common orbit in the orbit lists of both objects and then 
    determines the number of orbits from each object to the common orbit.
    
    Returns the minimum number of orbital transfers required such that both
    objects are orbiting the same body.
    """
    
    orbits1 = ind_orbs[obj_1]
    orbits2 = ind_orbs[obj_2]
    
    dist_orb1_com = 0
    dist_orb2_com = 0
    
    print("Finding common orbits....")
    
    for orbit in orbits1:
        if orbit in orbits2:
            print("Common orbit found: ", orbit)
            dist_orb1_com = orbits1.index(orbit)
            dist_orb2_com = orbits2.index(orbit)
            break
        
    return dist_orb1_com + dist_orb2_com
            
               

orbit_map = read_data("day6input.txt")
#orbit_map = read_data("day6testinput.txt") #Test input
#orbit_map = read_data("day6pt2testinput.txt") #Test input for part 2
#print(orbit_map)

direct_orbs = direct_orbits(orbit_map)
#print(direct_orbs)

indirect_orbs, num_orbs = all_orbits(direct_orbs)
#print(indirect_orbs)
print("Part 1: Total number of direct and indirect orbits: ", num_orbs)

transfers = find_orbital_distance('YOU', 'SAN', indirect_orbs)
print("Part 2: Number of orbital transfers required 'YOU' to 'SAN': ", transfers)



