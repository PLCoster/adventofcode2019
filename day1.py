# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 11:38:13 2019

@author: Paul
"""

# Advent of coding Day 1

def read_file(filename):
    """
    Reads input file and returns list of module weights from the input file
    """
    
    weights= []
    
    f = open(filename, 'r')
    for line in f:
        weight = line.strip('\n')
        weights.append(int(weight))
        
    return weights



def fuel_calc(filename):
    """
    Takes input of a file containing a single column of spacecraft module weights.
    Returns an int, the quantity of fuel required for all the modules.

    Fuel per module is calculated as (rounded down (mass / 3)) - 2
    """
    
    weights = read_file(filename)
    fuel_req = 0
      
    #print(weights)
    
    for weight in weights:
        fuel_req += int(weight/3) -2
        
    return('Fuel requirement is: ' +  str(fuel_req))
    

def fuel_calc_inc_fuel(filename):
    """
    Takes input of a file containing a single column of spacecraft module weights.
    Returns an int, the quantity of fuel required for all the modules and accounts
    for the fuel required to carry the extra fuel.

    Fuel per module is calculated as (rounded down (mass / 3)) - 2
    """

    weights = read_file(filename)
    fuel_req = 0
        
    #print(weights)
    
    for weight in weights:
        module_fuel = int(weight/3) -2
        fuel_req += module_fuel
                
        extra_fuel = int(module_fuel/3) -2
        
        while extra_fuel >= 0:
            fuel_req += extra_fuel
            new_fuel = int(extra_fuel/3) -2
            extra_fuel = new_fuel
        
    return('Fuel requirement accounting for extra fuel is: ' +  str(fuel_req))
  
print(fuel_calc('day1input.txt'))    
print(fuel_calc_inc_fuel('day1input.txt'))


