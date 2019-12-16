# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 10:58:18 2019

@author: Paul
"""

# Solution to Advent of Code Day 15: Oxygen System

import random
import numpy as np
import matplotlib.pyplot as plt
import time

def read_data(filename):
    """
    Reads csv file into a list, and converts string entries to ints, then turns 
    the list into a dictionary of memory locations and their valuesfor in intcode.
    """
    
    data = []
    
    f = open(filename, 'r')
    for line in f:
        data += line.strip('\n').split(',')
    
    int_data = [int(i) for i in data]
    f.close() 
    
    data_dict = {k:int_data[k] for k in range(len(int_data))}
    
    return data_dict


def run_intcode(program, phase_input, power_input, position, mem_state, rel_base_mem, initialised):
    """
    Takes data, dict of memory location : value ints to run int_code on.
    Takes phase input - phase to be used to initialise amplifier
    Takes power input - initial input or input from another amplifier
    Position - Position to start running the intcode from
    Initialised - Flag to determine if amplifier has been phase initialised or not
    Returns list of ints after intcode program has been run.
    
    Running Intcode program looks reads in the integers sequentially in sets of 4:
        data[i]      == Parameter Mode + Opcode (last two digits)
        data[i+1]    == Entry 1
        data[i+2]    == Entry 2
        data[i+3]    == Entry 3
        
    If Opcode == 1, the value of the opcode at index location = entry 1 and 2 
    in the program are summed and stored at the index location of entry 3. 
    
    If Opcode == 2, the value of the opcode at index location = entry 1 and 2 
    in the program are multiplied and stored at the index location of entry 3. 
    
    If Opcode == 3, the the single integer (input) is saved to the position given
    by index 1.
    
    If Opcode == 4, the program outputs the value of its only parameter. E.g. 4,50
    would output the value at address 50.
    
    If Opcode == 5 and entry 1 is != 0, the intcode position moves to the index stored
    at entry 2. Otherwise it does nothing.
    
    If Opcode == 6 and entry 1 is 0, the intcode postion moves to the index stored 
    at entry 2. Otherwise it does nothing.
    
    If Opcode == 7 and entry 1> entry 2, store 1 in position given by third param,
    otherwise store 0 at position given by third param.
    
    If Opcode == 8 and entry 1 = entry 2, store 1 in position given by third param,
    otherwise store 0 at position given by third param.
    
    If Opcode == 9 the relative base is changed by the value of its only parameter.
       
    If Opcode == 99, the program is completed and will stop running.
    
    Parameters are digits to the left of the opcode, read left to right:
        Parameter 0 -> Position mode - the entry is treated as an index location
        Parameter 1 -> Immediate mode - the entry is treated as a value
        Parameter 2 -> Relative mode - the entry is treated as position, but relative
                        base (starts at zero and changed by Opcode 9) is added.
    """
    
    
    data = program.copy()
    answer = mem_state
    params = [0, 0, 0]
    param_modes = ['', '', '']
   
    input_num = 1
    out_code = 0
    rel_base = rel_base_mem
    write_pos = 0
    
    # If the amplifier has not been initialised, use phase and input, otherwise just input
    if not initialised:
        input_num = 1
    else:
        input_num = 2
       
    i = position
    
    while (i < len(program)):
        
        #print("i = ", i)
        #print("Rel Base = ", rel_base)
        
        # Determine Opcode and parameter codes:       
        opcode_str = "{:0>5d}".format(data[i])
        #print(opcode_str)
        
        opcode = int(opcode_str[3:])
        param_modes[0] = opcode_str[2]
        param_modes[1] = opcode_str[1]
        param_modes[2] = opcode_str[0]
        
        #print("Opcode: ", opcode)

        
        op_lens = {1:4, 2:4, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4, 9:2, 99:2}
        
        # Set parameter values correctly depending on parameter mode.
        for j in range(op_lens[opcode] - 1):            
            if param_modes[j] == '0':
                try:
                    params[j] = data[data[i+j+1]]
                except KeyError:
                    if (i+j+1) not in data.keys():
                        data[i+j+1] = 0
                    if data[i+j+1] not in data.keys():
                        data[data[i+j+1]] = 0
                    params[j] = data[data[i+j+1]]                                 
            elif param_modes[j] == '1':
                try:
                    params[j] = data[i+j+1]
                except KeyError:
                    data[i+j+1] = 0
                    params[j] = data[i+j+1] 
            else:
                try:
                    params[j] = data[data[i+j+1] + rel_base]
                except KeyError:
                    if (i+j+1) not in data.keys():
                        data[i+j+1] = 0
                    if (data[i+j+1] + rel_base) not in data.keys():
                        data[data[i+j+1] + rel_base] = 0
                    params[j] = data[data[i+j+1] + rel_base]
        
        # Set write positions correctly for code 3
        if str(opcode) == '3':
            if param_modes[0] == '0':
                write_pos = data[i+1]
            else:
                write_pos = data[i+1] + rel_base
        # Set write positions correctly for codes 1,2,7,8
        if str(opcode) in ['1','2','7','8']:
            if param_modes[2] == '0':
                write_pos = data[i+3]
            else:
                write_pos = data[i+3] + rel_base
        
        #print("Write-pos:", write_pos)        
        #print(params, param_modes)
            
        # If opcode is 1, add relevant entries:
        if opcode == 1:
            data[write_pos] = params[0] + params[1]
            i += 4
        # If opcode is 2, multiply the relevant entries:    
        elif opcode == 2:
            data[write_pos] = params[0] * params[1]
            i += 4
        # If opcode is 3, store input value at required location.
        elif opcode == 3:
            if input_num == 1:
                data[write_pos] = phase_input
                input_num += 1
            elif input_num == 2:
                data[write_pos] = power_input
            else:
                print("Problem with the Program: Too many inputs needed")
                out_code = -1
                break
            i += 2;
        # If opcode is 4, print out the input stored at specified location.
        elif opcode == 4:
            answer = params[0]
            #print("Program output: ", answer)
            i += 2
            break
        # If the opcode is 5 and the next parameter !=0, jump forward
        elif opcode == 5:
            if params[0] != 0:
                i = params[1]
            else:
                i += 3
        # If the opcode is 6 and next parameter is 0, jump forward
        elif opcode == 6:
            if params[0] == 0:
                i = params[1]
            else:
                i += 3
        # If the opcode is 7, carry out less than comparison and store 1/0 at loc 3
        elif opcode == 7:
            if params[0] < params[1]:
                data[write_pos] = 1
            else:
                data[write_pos] = 0                
            i += 4               
        # If the opcode is 8, carry out equality comparison and store 1/0 at loc 3        
        elif opcode == 8:
            if params[0] == params[1]:
                data[write_pos] = 1
            else:
                data[write_pos] = 0              
            i += 4
        # If the opcode is 9, change the relative base by its only parameter
        elif opcode == 9:
            rel_base += params[0]
            i += 2
        # If the opcode is 99, halt the intcode    
        elif opcode == 99:
            print("Program ended by halt code")
            out_code = 99
            break
        # If opcode is anything else something has gone wrong!
        else:
            print("Problem with the Program: Incorrect Intcode")
            outcode = -1
            break       
      
    return data, answer, out_code, i, rel_base


class Room(object):
    """
    Class symbolising the oxygen system room of the ship, consisting of traversible areas,
    walls and the oxygen system itself.
    """
    def __init__(self, rob_start):
        """ Initialise room """
        
        self.room_squares = {}
        
        self.room_squares[rob_start] = 1
                
                
    def update_square(self, position, move_code, status_code):
        """ Mark a tile as wall (0), floor (1) or oxygen system (2) """
        
        if status_code == 1:
            self.room_squares[position] = 1
            
        elif status_code == 2:
            self.room_squares[position] = 2
        
        else:
            pos_x, pos_y = position
            facing = {1:(0,1), 2:(0,-1), 3:(-1, 0), 4:(1,0)}
            dx, dy = facing[move_code]
            self.room_squares[(pos_x + dx, pos_y + dy)] = 0
    
    def get_square(self, position):
        """ Returns the identity of the square at position, if known else -1 """
        
        if position in self.room_squares:
            return self.room_squares[position]
        else:
            return -1
        
        
class Robot(object):
    """
    Class symbolising the repair robot, can move NSEW, has a position in the room.
    
    The robot runs an intcode program and can take input instructions to control
    its movement.
    
    Will move in a straight line until it hits a wall, and pick another direction
    at random.
    
    Returns the next move_code to be input into the program
    """
    def __init__(self, start_pos, room):
        self.x , self.y = start_pos
        self.pos = (self.x, self.y)
        self.room = room
        
    def move_Robot(self, move_code, status_code):
        """ Move the robot to a new location if possible, and draw wall/movement
        on room map.
        """
        
        moves = {1:(0,1), 2:(0,-1), 3:(-1, 0), 4:(1,0)}
        # If move was successful update robot position
        if status_code == 1 or status_code == 2:
            dx, dy = moves[move_code]
            
            self.x = self.x + dx
            self.y = self.y + dy
            self.pos = (self.x, self.y)
        
        # Update the map
        self.room.update_square(self.pos, move_code, status_code)
        
    def run_Robot(self, program):
        """ Runs a painting robot using an intcode, moving around the room until
        the oxygen system is found. Returns number of steps needed to reach the O2 sys. """
        
        # Initialise visualisation of room map
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)       
        fig.show()
    
        # Initialise Intcode program arguments        
        data = program.copy()
        prog_pos = 0
        phase = 0
        status_code = 0
        init = True
        out_code = -1
        rel_base_mem = 0
        move_code = 4
    
        # Initialise simulation parameters
        moves = 0
        move_set = {4:[4,2,1,3], 3:[3,1,2,4], 2:[2,3,4,1], 1:[1,4,3,2]}
        start_found = False
        
        
        print("Repair Robot is Mapping the Room")
        # Repeat steps until oxygen generator reached
        while not start_found:
            
            moves += 1
            #print(moves)
            
            # Set end condition of simulation - returning to start location
            if self.pos == (25,25) and moves > 100:
                start_found = True
                
            if status_code == 2:
                o2_pos = self.pos
                        
            # Update room visualisation
            picture = dict_to_image(self.room.room_squares, self.pos)
            ax1.clear()
            ax1.imshow(picture)
            fig.canvas.draw()
            
            # Robot searches maze by hugging the right wall. First check if robot can move right:
            data, status_code, out_code, prog_pos, rel_base_mem = run_intcode(data, phase, move_set[move_code][1], prog_pos, status_code, rel_base_mem, init)
            self.move_Robot(move_set[move_code][1], status_code)
            # If move was possible, move skip to the next iteration, moving in new direction:
            if status_code > 0:
                move_code = move_set[move_code][1]
                continue
            # If movement not possible, try moving straight:
            data, status_code, out_code, prog_pos, rel_base_mem = run_intcode(data, phase, move_set[move_code][0], prog_pos, status_code, rel_base_mem, init)
            self.move_Robot(move_set[move_code][0], status_code)
            if status_code > 0:
                move_code = move_set[move_code][0]
                continue
            # If straight movement not possible, try moving left:
            data, status_code, out_code, prog_pos, rel_base_mem = run_intcode(data, phase, move_set[move_code][2], prog_pos, status_code, rel_base_mem, init)
            self.move_Robot(move_set[move_code][2], status_code)
            if status_code > 0:
                move_code = move_set[move_code][2]
                continue
            # If all other directions blocked, move backwards:
            data, status_code, out_code, prog_pos, rel_base_mem = run_intcode(data, phase, move_set[move_code][3], prog_pos, status_code, rel_base_mem, init)
            self.move_Robot(move_set[move_code][3], status_code)
            if status_code > 0:
                move_code = move_set[move_code][3]
                continue
            
            
        print("Simulation Complete!")
        plt.savefig('day_15_maze.png')
        print("Moves to complete mapping: ",moves)
        print("O2 System is located at: ", o2_pos)
        #time.sleep(10)
        plt.close()
    
        
        return moves, self.room.room_squares, o2_pos

  
def dict_to_image(screen, position):
    """ Takes a dict of room locations and their block type output by RunGame.
    Renders the current state of the game screen.    
    """     
    
    picture = np.zeros((50, 50))
    
    # Color tiles according to what they represent on screen:.  
    for tile in screen:
        pos_x, pos_y = tile
        if screen[tile] == 0:
            picture[pos_y][pos_x] = 255
        if screen[tile] == 1:
            picture[pos_y][pos_x] = 140
        if screen[tile] == 2:
            picture[pos_y][pos_x] = 50
    
    rob_x, rob_y = position
    picture[rob_y][rob_x] = 200
    
    return picture


def BFS(map_dict, start, end, verbose):
    """
    BFS algorithm to find the shortest path between the start and end points
    on the map, following the map given by map_dict
    
    If an invalid end location is given then it will return the longest possible
    path and its length.
    
    Returns the length of the shortest route, and the overall path.
    """
    
    initPath = [start]
    pathQueue = [initPath]
    
    longest = 0
    longest_path = []
    
    moves = {1:(0,1), 2:(0,-1), 3:(-1, 0), 4:(1,0)}
      
    
    while len(pathQueue) != 0:
        # Get and remove oldest element of path queue:
        tmpPath = pathQueue.pop(0)
        
        if verbose:
            print('Current BFS path: ', tmpPath)
        lastNode = tmpPath[-1]
        
        if len(tmpPath) > longest:
            longest = len(tmpPath)
            longest_path = tmpPath    
        
        # If the last node in the path is the end, shortest route found
        if lastNode == end:
            return tmpPath, len(tmpPath)
        # Otherwise add all new possible paths to path queue:
        for i in range(1,5,1):
            dx, dy = moves[i]
            pos_x, pos_y = lastNode
            testpos = (pos_x + dx, pos_y + dy)
            # Check if legit path and not backtracking
            if map_dict[testpos] > 0 and testpos not in tmpPath:
                newPath = tmpPath + [testpos]
                pathQueue.append(newPath)
                
    # If no path found return longest path:
    return longest_path, longest

          
program_input = read_data('day15input.txt')
#print(program_input)

# Part 1 map the room:
room = Room((25,25))
rob = Robot((25,25), room)
moves, end_status, o2_pos = rob.run_Robot(program_input)
img = dict_to_image(end_status, (25,25))
plt.imshow(img)
plt.show()

# Once room is mapped carry out BFS on the map to 
shortest_path, path_length = BFS(end_status, (25,25), o2_pos, False)
print('Part 1: Minumum no. of moves to reach O2 system: ', path_length - 1)

# Part 2: Need to find the longest possible path from the o2 generator, can be done using
# BFS with no end condition.
longest_path, path_length2 = BFS(end_status, o2_pos, (-1,-1), False)
print('Part 2: Time to fill room with o2: ', path_length2 - 1)
time.sleep(5)