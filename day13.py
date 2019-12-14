# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 11:58:23 2019

@author: Paul
"""

import numpy as np
import matplotlib.pyplot as plt
import time


def read_data(filename):
    """
    Reads csv file into a list, and converts string entries to ints, then turns 
    the list into a dictionary of memory locations and their values for the intcode.
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


def RunGame (program):
    """ 
    Runs intcode game program to generate a screen image.
    
    Returns a dictionary containing screen coordinates and their values:
        0 is an empty tile (No game object)
        1 is a wall tile (indestructible barrier)
        2 is a block tile - can be broken by the ball
        3 is a horizontal paddle tile - the paddle is indestructible
        4 is a ball tile - it moves diagonally and bounces off objects.
        
    Also returns the score at the end of the game.
    """
    # Initialise image to show game state
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)       
    fig.show()
    
    # Initialise Intcode program arguments        
    data = program.copy()
    prog_pos = 0
    phase = 0
    output = 0
    init = True
    out_code = -1
    rel_base_mem = 0
    input_num = 0
    
    # Initialise gameplay parameters
    pix_drawn = 0   
    ball_pos = 0
    paddle_pos = 0
    score = 0  
    screen = {} 
        
    print("Game program running")
    # Repeat steps until end of program halt code received
    while out_code != 99:
    # Run intcode program twice to get the x, y coord of pixel being drawn
        data, output, out_code, prog_pos, rel_base_mem = run_intcode(data, phase, input_num, prog_pos, output, rel_base_mem, init)
        pix_x = output         
        data, output, out_code, prog_pos, rel_base_mem = run_intcode(data, phase, input_num, prog_pos, output, rel_base_mem, init)
        pix_y = output         
        # Run program again to get the pixel type to draw:
        data, output, out_code, prog_pos, rel_base_mem = run_intcode(data, phase, input_num, prog_pos, output, rel_base_mem, init)
        block = output
        
        # Get the ball and paddle positions
        if block == 4:
            ball_pos = pix_x
            
        if block == 3:
            paddle_pos = pix_x
        
        # Apply input to intcode to move the paddle towards the ball position  
        if ball_pos > paddle_pos:
            input_num = 1
        elif ball_pos < paddle_pos:
            input_num = -1
        else:
            input_num = 0
        
        # Add pixel coords and type to screen, or set score of pos_x = -1
        if pix_x != -1:
            screen[(pix_x, pix_y)] = block
        else:
            score = block
            print('Current Score: ', score)       
        
        # Refresh screen every 5 pixels after one full screen rendered.
        if pix_drawn > 990 and pix_drawn % 5 == 0:
            picture = dict_to_image(screen)
            ax1.clear()
            ax1.imshow(picture)
            fig.canvas.draw()

        pix_drawn += 1
            
    print("Game Complete!")
    plt.close()
    #print("Pixels Created: ", pix_drawn)
        
    return screen, score

def dict_to_image(screen):
    """ Takes a dict of game screen locations and their block type output by RunGame.
    Renders the current state of the game screen.    
    """     
    
    picture = np.zeros((24, 45))
    
    # Color tiles according to what they represent on screen:.  
    for tile in screen:
        pos_x, pos_y = tile
        if screen[tile] == 1:
            picture[pos_y][pos_x+1] = 255
        if screen[tile] == 2:
            picture[pos_y][pos_x+1] = 140
        if screen[tile] == 3:
            picture[pos_y][pos_x+1] = 50
        if screen[tile] == 4:
            picture[pos_y][pos_x+1] = 200            
    
    return picture


program_input = read_data("day13input.txt") 

# Part 1
screen_end, score = RunGame(program_input)
blocks = 0;

for entry in screen_end:
    if screen_end[entry] == 2:
        blocks += 1
        
print("Part 1: Remaining Blocks after running program: ", blocks)
print("Starting game in 5 seconds")
time.sleep(5)    


# Part 2  
program_input[0] = 2 # Free Play
screen_end, score = RunGame(program_input)

print("Part 2: Game over! Final Score: ", score)
time.sleep(10)

