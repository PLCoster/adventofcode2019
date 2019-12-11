# -*- coding: utf-8 -*-
"""
Created on Mon Dec  11 11:36:59 2019

@author: Paul
"""
# OOP approach to Advent of Code 2019 Day 11 - Hull Painting Robot
from PIL import Image
import numpy as np

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

class Hull(object):
    """
    Class symbolising the hull of the ship, panel locations and the colour they
    are painted.
    """
    def __init__(self, width, height, start_white):
        """ Initialise hull with all panels painted start-black """
        self.width = width
        self.height = height
        self.area = height * width
        
        self.hull_squares = {}
        
        for i in range(self.height):
            for j in range(self.width):
                self.hull_squares[(j, i)] = 'start-black'
                
        if start_white == 1:
            self.hull_squares[(0,0)] = 'white'
                
    def paint_Hull(self, position, paint_col):
        """ Paint hull tile at position color paint_col """
        self.hull_squares[position] = paint_col
        
    def get_painted(self):
        """ Returns number of tiles that have been painted by the robot """
        painted = 0
        
        for tile in self.hull_squares:
            if self.hull_squares[tile] == 'black' or self.hull_squares[tile] == 'white':
                painted += 1
                
        return painted
    
    def get_color_code(self, position):
        """ Returns the color code of the tile at position """
        if position not in self.hull_squares:
            self.hull_squares[position] = 'start-black'
     
        if self.hull_squares[position] == 'white':
            return 1
        else:
            return 0
        
        
class Robot(object):
    """
    Class symbolising the hull-painting robot, has a direction and facing, exists
    on a hull object and responds to instructions from the intcode program.
    """
    def __init__(self, start_pos, start_face, hull):
        self.x , self.y = start_pos
        self.pos = (self.x, self.y)
        self.facing = start_face
        self.hull = hull
        
    def move_Robot(self):
        """ Move the robots position according to its facing """
        moves = {'UP': (0, 1), 'DOWN': (0, -1), 'LEFT': (-1, 0), 'RIGHT':(1, 0)}
        
        self.x = self.x + moves[self.facing][0]
        self.y = self.y + moves[self.facing][1]
        
        self.pos = (self.x, self.y)
        
    def paint_Robot(self, p_code):
        """ Paint a square on the board according to a code given by the intcode """
        if p_code == 0:
            paint_col = 'black'
        if p_code == 1:
            paint_col = 'white'
            
        self.hull.paint_Hull(self.pos, paint_col)
        
    def turn_Robot(self, t_code):
        """ Changes a robots facing according to the code it receives """
        turns = {'UP' : ['LEFT', 'RIGHT'], 'LEFT' : ['DOWN', 'UP'], 'DOWN' : ['RIGHT', 'LEFT'], 'RIGHT': ['UP', 'DOWN']}
        
        if t_code == 0:
            self.facing = turns[self.facing][0]
        else:
            self.facing = turns[self.facing][1]
            
       # print("Robot facing :", self.facing)
            
    def run_Robot(self, program):
        """ Runs a painting robot using an intcode to paint the hull. Returns number
        of painted tiles during operation. """
        
        data = program.copy()
        prog_pos = 0
        phase = 0
        output = 0
        init = True
        out_code = -1
        rel_base_mem = 0
        moves = 0
        
        print("Robot is painting the hull")
        # Repeat steps until end of program halt code received
        while out_code != 99:
            # Check tile color then run intcode until output received
            input_num = self.hull.get_color_code(self.pos)
            data, output, out_code, prog_pos, rel_base_mem = run_intcode(data, phase, input_num, prog_pos, output, rel_base_mem, init)
            # Paint panel at current position according to output
            self.paint_Robot(output)
            # Run program again until second output received
            data, output, out_code, prog_pos, rel_base_mem = run_intcode(data, phase, input_num, prog_pos, output, rel_base_mem, init)
            # Turn and move robot according to output
            self.turn_Robot(output)
            self.move_Robot()
            moves += 1
            
        print("Robot instructions complete!")
        print("Tiles Painted by Robot: ", self.hull.get_painted())
        print("Moves: ", moves)
        
        # Return dict of poainted hull squares
        return self.hull.hull_squares
  
def hull_to_image(painted_tiles):
    """ Takes a dict of tile locations and their paint color output by the
    run_Robot method.

    Returns a 2d array representing the hull tiles with 0 for black and 255 for white.
    """
    # Create empty 2d array
    picture = np.zeros((6, 42))
   
    # If tile in dict is marked as white, store 255 in array location.
    for tile in painted_tiles:
        pos_x, pos_y = tile
        if painted_tiles[tile] == 'white':
            picture[-pos_y][pos_x] = 255
       
    
    return picture  
          
    
program_input = read_data("day11input.txt")
#print(program)

# Part 1:
test_hull = Hull(1, 1, 0)
test_robot = Robot((0,0), 'UP', test_hull)
painted_tiles1 = test_robot.run_Robot(program_input)

# Part 2:
hull = Hull(1, 1, 1)
robot = Robot((0, 0), 'UP', hull)
painted_tiles2 = robot.run_Robot(program_input)
               
picture =  hull_to_image(painted_tiles2) 

img = Image.fromarray(picture) #PKFPAZRP
img.show() 