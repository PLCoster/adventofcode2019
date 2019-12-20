# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 15:51:45 2019

@author: Paul
"""

# Solution to Advent of Code 2019 Day 17: Set and Forget

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


def run_intcode(program, phase_input, power_input, position, mem_state, rel_base_mem, inp_mem, initialised):
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
   
    out_code = 0
    rel_base = rel_base_mem
    write_pos = 0
    inp = inp_mem
    
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
                try:
                    data[write_pos] = power_input[inp]
                    inp += 1
                except IndexError:
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
      
    return data, answer, out_code, i, rel_base, inp


def calibrate_cameras(program, input_inst = [0], text_map = False):
    """
    Takes an intcode ASCII program and runs it, outputing the characters on
    screen to  represent the camera visuals.
    
    Returns a screen dictionary representing the camera visualisation at each coordinate.
    """
    
    #Initialise visualisation of room map
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
    inp_mem = 0
    output = 0
    output_last = 0
        
    # Dictionary to store a copy of the camera output
    screen = {}
    x_pos = 0
    y_pos = 0
    
    
    # Repeat steps until end of program reached
    while out_code!= 99 and output < 1000:
                             
        # Run intcode program
        data, output, out_code, prog_pos, rel_base_mem, inp_mem = run_intcode(data, phase, input_inst, prog_pos, status_code, rel_base_mem, inp_mem, init)

        
        if text_map and output in [46,35,10,60,62,94,86,118]:
            print(chr(output), end='') 
            
        if output != 10 and output in [46,35,60,62,94,86,118] :
            screen[(x_pos, y_pos)] = output
            x_pos += 1
        else:     
            x_pos = 0
            y_pos += 1    
          
        output_cur = output
        # New screen is denoted by two newlines in a row         
        if output_cur + output_last == 20:          
            x_pos = 0
            y_pos = 0
            pixels = 0
                
            # Update visualisation
            picture = dict_to_image(screen)
            ax1.clear()
            ax1.imshow(picture)
            fig.canvas.draw()
            
        output_last = output_cur                
    
    return screen, output

def alignment_params(screen):
    """
    Takes a camera screen dictionary as input. Locates all scaffold intersections
    and calculates their alignment parameter (distance from left edge * distance
    from top edge).
    
    Returns the sum of the alignment parameters and an updated screen showing their positions.
    """
    
    intersections = []
    alignment_param = 0
    
    
    moves = {0:(0,1), 1: (0,-1), 2: (1, 0), 3: (-1, 0)}
    
    for tile in screen:
        intersect = True
        pos_x, pos_y = tile
        
        if screen[tile] == 35:
            for i in range(4):
                dx, dy = moves[i]
                test_pos = (pos_x + dx, pos_y + dy)
                if test_pos not in screen or screen[test_pos] != 35:
                    intersect = False
                    break
        
            if intersect:
                intersections.append(tile)
                alignment_param += pos_x * pos_y
    
    for tile in intersections:
        screen[tile] = 48
        
    return screen, alignment_param


def dict_to_image(screen):
    """ Takes a dict of room locations and their block type output by RunGame.
    Renders the current state of the game screen.    
    """     
    
    picture = np.zeros((51, 51))
    
    # Color tiles according to what they represent on screen:.  
    for tile in screen:
        pos_x, pos_y = tile
        if pos_x < 51 and pos_y < 51:
            if screen[tile] == 46:
                picture[pos_y][pos_x] = 0;
            elif screen[tile] == 35:
                picture[pos_y][pos_x] = 240;
            else:
                picture[pos_y][pos_x] = 150

    return picture


def instr_to_intcode(instructions):
    """
    Takes a string of instructions written in ASCII and converts them to integers
    for using as input for the intcode program.
    """
    
    output = []
    
    for char in instructions:
        output.append(ord(char))
        
    output.append(ord('\n'))
    
    return output


program_input = read_data('day17input.txt')
#print(program_input)

# Part 1
print('Calibrating Cameras...')
screen_out, output1 = calibrate_cameras(program_input, text_map = False)
screen, align_val = alignment_params(screen_out)
print('Part 1: Sum of Alignment Parameters: ', align_val)
plt.imshow(dict_to_image(screen))
plt.savefig('day17_scaffold_start.png')
plt.show()
#time.sleep(5)
plt.close()


# Part 2
# Instructions required for Robot were read from the map and decoded by hand
inst_list = instr_to_intcode('A,B,A,C,C,A,B,C,B,B')
inst_A = instr_to_intcode('L,8,R,10,L,8,R,8')
inst_B = instr_to_intcode('L,12,R,8,R,8')
inst_C = instr_to_intcode('L,8,R,6,R,6,R,10,L,8')
camera = [121,10]
no_camera  = [110, 10]

input_inst = inst_list + inst_A + inst_B + inst_C + camera

print('Running Robot over Scaffolding...')
program_input[0] = 2
screen_out2, output2 = calibrate_cameras(program_input, input_inst, text_map = False)
print('Part 2: Dust Collected at end of Scaffold: ', output2)
plt.imshow(dict_to_image(screen_out2))
plt.savefig('day17_scaffold_end.png')
plt.show()


# Maze Path: L,8,R,10,L,8,R,8,L,12,R,8,R,8,L,8,R,10,L,8,R,8,L,8,R,6,R,6,R,10,L,8,L,8,R,6,R,6,R,10,L,8,L,8,R,10,L,8,R,8,L,12,R,8,R,8,L,8,R,6,R,6,R,10,L,8,L,12,R,8,R,8,L,12,R,8,R,8

#A,B,A,C,C,A,B,C,B,B

#A: L,8,R,10,L,8,R,8,L,8
#B: L,12,R,8,R,8
#C: L,8,R,6,R,6,R,10,L,8
