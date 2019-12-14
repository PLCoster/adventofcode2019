# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 21:56:35 2019

@author: Paul
"""

# Solution to Advent of Code Day 14 Space Stoichiometry

import math

def read_reaction_data(filename):
    """
    Reads reaction data list into a dictionary consisting of keys of elements
    and the values being lists of the elements required to make the keys.
    """
    
    data = {}
    
    f = open(filename, 'r')
    for line in f:
        data_line = "".join([char for char in line if char not in '=,>\n']).split(' ')
        del data_line[-3]
        data[(int(data_line[-2]), data_line[-1])] = []
        for i in range(0, len(data_line) -2, 2):     
            data[(int(data_line[-2]), data_line[-1])].append([int(data_line[i]), data_line[i+1]])
        
    f.close() 
    
    return data

def find_ore_requirement(reaction_data, fuel_req):
    """ 
    Takes a dictionary of keys : reaction results and values : reaction inputs,
    and fuel_req, an int
    
    Works through the reactions in reverse to determine the amount of ORE
    required to produce fuel_req x Fuel, and returns that number
    """
                
    # Work backwards from fuel until we get to the ORE required:
    required = [[fuel_req, 'FUEL']]
    
    # Dict to hold any excess chems made by process
    excess_chem = {}
    
    ore_req = 0
    
    # Run until all materials required are 'ORE'
    while len(required) > 0:
        
        chem_req = required[0]
        
        # Use any excess chemicals first to meet requirements
        if chem_req[1] in excess_chem:
            while chem_req[0] > 0 and excess_chem[chem_req[1]] > 0:
                chem_req[0] -= 1
                excess_chem[chem_req[1]] -= 1
            
            # If the excess chemicals completely supply the chem required, remove it and move to next chem.
            if chem_req [0] == 0:
                required.pop(0)
                continue
        
        # Search reaction data for the first required chem
        for product in reaction_data:
            if product[1] == chem_req[1]:
                # Determine the number of reactions needed to meet requirement:
                n = math.ceil(chem_req[0]/product[0])
                    
                # Log any excess chems from the reaction
                if product[1] in excess_chem and product[0]*n > chem_req[0]:
                    excess_chem[product[1]] += product[0]*n - chem_req[0]
                elif product[0]*n > chem_req[0]:
                    excess_chem[product[1]] = product[0]*n - chem_req[0]
                
                # Add the chemicals required to the list of chems required
                for entry in reaction_data[product]:
                    added = False
                    for chem in required:
                        if entry[1] == chem[1]:
                            chem[0] += entry[0]*n
                            added = True
                    if not added:
                        required.append([entry[0]*n, entry[1]])
        
     
        # Once all required chemicals have been added to produce the first required chemical,
        # remove it from the list:
        required.pop(0)
        ore_removal = required[:]
        
        # Remove ORE for the next round:
        for entry in required:
            # If entry is Ore then add to ore requirement and remove from requirements
            if entry[1] == 'ORE':
                ore_req += entry[0]
                ore_removal.remove(entry)
        
        required = ore_removal[:]
             
        #print('Ore: ' , ore_req)
        #print("Excess Chems:", excess_chem)
    
    return ore_req                   
 

reaction_data = read_reaction_data('day14input.txt')
#reaction_data = read_reaction_data('day14_test.txt')

# Part 1
result = find_ore_requirement(reaction_data, 1)       
print("Part 1: Ore required to produce 1 fuel: ", result)

# Part 2 - Bisection search to find max fuel that can be prduced with 1 trillion ore:
high = 100000000
low = 0
mid = (high + low)//2
while high > low:
    result2 = find_ore_requirement(reaction_data, mid)
    if result2 > 1000000000000:
        high = mid - 1
    else:
        low = mid + 1
    mid = (high + low) // 2

print("Part 2: Max fuel made with 1 Trillion Ore: ", high)