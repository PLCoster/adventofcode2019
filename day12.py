# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 21:34:53 2019

@author: Paul
"""

# Solution to Advent of Code Day 12 N-Body Problem

import math

def lcm(a, b):
    """ Calculate and return lowest common multiple for a and b """
    return abs(a*b) // math.gcd(a, b)


class Moon(object):
    """ Class to represent an individual moon """
    def __init__(self, pos_list, name):
        
        self.start_pos = pos_list[:]
        self.position = pos_list[:]      
        self.velocity = [0, 0, 0]
        self.name = name
        
        self.pot_eng = 0
        
        for i in range(3):
            self.pot_eng += abs(self.position[i])
            
        self.kin_eng = 0
        
        self.tot_eng = 0
     
    def get_name(self):
        return self.name
        
        
    def update_velocity(self, other_moon):
        """ Update velocity of this moon wrt another moon """
        for i in range(3):
            if self.position[i] < other_moon.position[i]:
                self.velocity[i] += 1
            elif self.position[i] > other_moon.position[i]:
                self.velocity[i] -= 1
                
        #print(str(self.name) + ' velocty updated by ' str(other_moon.get_name()) +'. New velocity: ' + str(self.velocity))
        
    def update_position(self):
        """ Update position of this moon based on its speed """
        for i in range(3):
            self.position[i] += self.velocity[i]
        
        #print(self.name + ' updated velocity to: ' + str(self.velocity))
        
    def update_pot_eng(self):
        """ Update and return the potential energy of the moon """
        self.pot_eng = 0
        for i in range(3):
            self.pot_eng += abs(self.position[i])
            
        return self.pot_eng
    
    def update_kin_eng(self):
        """ Update and return the kinetic energy of the moon """
        self.kin_eng = 0
        for i in range(3):
            self.kin_eng += abs(self.velocity[i])
            
        return self.kin_eng
    
    def update_total_eng(self):
        
        return self.update_pot_eng() * self.update_kin_eng()
        
            

class Moon_Sim(object):
    """ Class to represent simulation of moon movement """
    def __init__(self, Moon_list):
        self.moons = Moon_list
        
    def run_Sim(self, steps):
        """ Runs similation for steps number of time steps.
        Each step updates the velocity of the moons and then their positions.
        Returns the total combined energy of all the moons at the end of the simulation.
        """
        
        print("Running moon simulation...")
        
        # Run sim for given number of steps
        for i in range(steps):
            
            #print("Simulation Step: ", i+1)
        
            # Update velocities based on the other moons
            for moon1 in self.moons:
                for moon2 in self.moons:
                    if moon1.name == moon2.name:
                        continue
                    else:
                        moon1.update_velocity(moon2)
            
            # Update position of each moon
            for moon in self.moons:
                moon.update_position()
                #print(moon.name + ' position: ' + str(moon.position))
        
        # Calculate and return total system energy after simulation        
        system_energy = 0
        for moon in self.moons:
            system_energy += moon.update_total_eng()
            
        return system_energy
    
    def run_history_sim(self):
        """ Runs similation until it reaches its initial state again, for each
        axis, to determine the periodicity. Returns the periodicity in steps of each axis
        """
        
        repeats_found = False
        x_per = 0
        y_per = 0
        z_per = 0      
        
        i = 0
        print("Running Simulation to find repeated initial x, y, z state...")
        
        # Run sim for given number of steps
        while repeats_found == False:
            
            # print("Simulation Step: ", i+1)
      
            # Update velocities based on the other moons
            for moon1 in self.moons:
                for moon2 in self.moons:
                    if moon1.name == moon2.name:
                        continue
                    else:
                        moon1.update_velocity(moon2)
            
            # Update position of each moon
            for moon in self.moons:
                moon.update_position()
                #print(moon.name + ' position: ' + str(moon.position))
            
            # Find if velocities are repeated on any axis:
            x_found = True
            y_found = True
            z_found = True
            
            for moon in self.moons:
                              
                if moon.velocity[0] != 0 or moon.position[0] != moon.start_pos[0] or x_per:
                    x_found = False
                
                if moon.velocity[1] != 0 or moon.position[1] != moon.start_pos[1] or y_per:
                    y_found = False

                if moon.velocity[2] != 0 or moon.position[2] != moon.start_pos[2] or z_per:
                    z_found = False
                    
            if x_found == True and not x_per:
                x_per = i+1
                print('X period found!')
            if y_found == True and not y_per:
                y_per = i+1
                print('Y period found!')
            if z_found == True and not z_per:
                z_per = i+1
                print('Z period found!')
            
            if x_per and y_per and z_per:
                print('All periods found!')
                repeats_found = True
                                 
            i += 1    
                
        return x_per, y_per, z_per
    
# Part1 Test Input for 10 steps, result should be 179 at 10 steps
#Io = Moon([-1, 0, 2], 'Io')
#Europa = Moon([2, -10, -7], 'Europa')
#Ganymede = Moon([4, -8, 8], 'Ganymede')
#Callisto = Moon([3, 5, -1], 'Callisto')
#test_system = Moon_Sim([Io, Europa, Ganymede, Callisto])
#test_system_energy = test_system.run_Sim(10)  
#print("Test Input Energy Result: ", test_system_energy)           
        
# Part 1: Run for 1000 steps:
Io = Moon([-15, 1, 4], 'Io')
Europa = Moon([1, -10, -8], 'Europa')
Ganymede = Moon([-5, 4, 9], 'Ganymede')
Callisto = Moon([4, 6, -2], 'Callisto')
pt1_system = Moon_Sim([Io, Europa, Ganymede, Callisto])
pt1_system_energy = pt1_system.run_Sim(1000)  
print("Part 1: Total Energy: ", pt1_system_energy)

# Part2:
Io = Moon([-15, 1, 4], 'Io')
Europa = Moon([1, -10, -8], 'Europa')
Ganymede = Moon([-5, 4, 9], 'Ganymede')
Callisto = Moon([4, 6, -2], 'Callisto')
pt2_system = Moon_Sim([Io, Europa, Ganymede, Callisto])
x_per, y_per, z_per = pt2_system.run_history_sim()  

answer = lcm(x_per, lcm(y_per, z_per))
print("Part 2: Periodicity of moon system: ", answer )

# Part 2 Explanation:
# 1. The movement of the moons is deterministic: at each step the positions
# of the moons depend on the previous state of the system, and the system
# could easily be run in reverse from any step to return to the initial step.
# 2. Each axis x, y, z interacts independently of the other two axes.
# 3. If the system does repeat any previous state when run, it can only reach
# that state by stepping through all the previous steps i.e. for the system to repeat
# its state found after 1 step of the simulation, it must first reach the step 0 state.
# Therefore the first state to be repeated will be the initial condition of the system.
# Hence we can search independantly for the periodicity of the x, y and z axes to return
# to the initial state of the system. Once the periodicity of these are found, we can
# then find the lowest common multiple (lcm) of the three periods in order to find the earliest
# step where the initial x,y,z conditions will be met again.
