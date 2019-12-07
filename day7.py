# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 11:06:59 2019

@author: Paul
"""

import itertools

def read_data(filename):
    """
    Reads csv file into a list, and converts to ints
    """
    
    data = []
    
    f = open(filename, 'r')
    for line in f:
        data += line.strip('\n').split(',')
    
    int_data = [int(i) for i in data]
    f.close()   
    
    return int_data


def run_intcode(program, phase_input, power_input, position, mem_state, initialised):
    """
    Takes data, list of ints to run int_code on.
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
    
    If Opcode == 7 and entry 1 = entry 2, store 1 in position given by third param,
    otherwise store 0 at position given by third param.
       
    If Opcode == 99, the program is completed and will stop running.
    
    Parameters are digits to the left of the opcode, read left to right:
        Parameter 0 -> Position mode - the entry is treated as an index location
        Parameter 1 -> Immediate mode - the entry is treated as a value
    """
    
    data = program[:]
    answer = mem_state
    params = [0, 0, 0]
    param_modes = ['', '', '']
   
    input_num = 1
    out_code = 0    
    
    # If the amplifier has not been initialised, use phase and input, otherwise just inpuf
    if not initialised:
        input_num = 1
    else:
        input_num = 2
       
    i = position
    
    while (i < len(program)):
        
        #print("i = ", i)
        
        # Determine Opcode and parameter codes:       
        opcode_str = "{:0>5d}".format(data[i])
        
        opcode = int(opcode_str[3:])
        param_modes[0] = opcode_str[2]
        param_modes[1] = opcode_str[1]
        param_modes[2] = opcode_str[0]
        
        #print(opcode_str)
        
        for j in range(2):
            if param_modes[j] == '0':
                try:
                    params[j] = data[data[i+j+1]]
                except IndexError:
                    continue
            else:
                try:
                    params[j] = data[i+j+1]
                except IndexError:
                    continue
                
        #print(params, param_modes)
            
        # If opcode is 1, add relevant entries:
        if opcode == 1:
            data[data[i+3]] = params[0] + params[1]
            i += 4;
        # If opcode is 2, multiply the relevant entries:    
        elif opcode == 2:
            data[data[i+3]] = params[0] * params[1]
            i += 4;
        # If opcode is 3, store input value at required location.
        elif opcode == 3:
            if input_num == 1:
                data[data[i+1]] = phase_input
                input_num += 1
            elif input_num == 2:
                data[data[i+1]] = power_input
                input_num += 1
            else:
                print("Problem with the Program: Too many inputs needed")
                out_code = -1
                break
            i += 2;
        # If opcode is 4, print out the input stored at specified location.
        elif opcode == 4:
            answer = data[data[i+1]]
            #print("Amplifier output: ", data[data[i+1]])
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
                data[data[i+3]] = 1
            else:
                data[data[i+3]] = 0                
            i += 4               
        # If the opcode is 8, carry out equality comparison and store 1/0 at loc 3        
        elif opcode == 8:
            if params[0] == params[1]:
                data[data[i+3]] = 1
            else:
                data[data[i+3]] = 0              
            i += 4
        # If the opcode is 99, halt the intcode    
        elif opcode == 99:
            #print("Program ended by halt code")
            out_code = 99
            break
        # If opcode is anything else something has gone wrong!
        else:
            print("Problem with the Program: Incorrect Intcode")
            outcode = -1
            break       
      
    return data, answer, out_code, i

def tune_amplifiers(program, start_input, start_phase, end_phase):
    """
    Takes intcode program, the starting input to the first amplifier, and the 
    number of phases to consider when tuning the amplifier.
    
    Runs the intcode program through each amplifier in turn (5 total), with every 
    permutation of phases, in order to find the permutation that gives the 
    highest output. The output of each amplifier is fed into the next one, along
    with its phase.
    
    Returns the phase sequence that gives the highest output, and the output value.
    """
    
    best_result = 0
    best_phases = []
    phase_list = []
        
    # Generate list of possible phases
    for i in range(start_phase, end_phase + 1, 1):
        phase_list.append(i)
    
    # Generate all possible permutations of the phases
    phase_perms = list(itertools.permutations(phase_list))
    print('Part1: Testing Phase Permutations of: ', phase_list)
    
    # Run amplifier sequence through all phase permutations
    for phase in phase_perms:
        amp_input = start_input
        
        # Run each phase through amplifier and put output into input:
        for i in range(5):
            run_prog = program[:]
            amp_data, amp_out, out_code, code_pos = run_intcode(run_prog, phase[i], amp_input, 0, 0, False)
            amp_input = amp_out
            
        if amp_out > best_result:
            best_result = amp_out
            best_phases = phase
            
    return best_result, best_phases

def tune_amplifiers_feedback(program, start_input, start_phase, end_phase):
    """
    Takes intcode program, the starting input to the first amplifier, and the 
    number of phases to consider when tuning the amplifier.
    
    Runs the intcode program through each amplifier in turn (5 total), with every 
    permutation of phases, in order to find the permutation that gives the 
    highest output. The output of each amplifier is fed into the next one, along
    with its phase.
    
    Returns the phase sequence that gives the highest output, and the output value.
    """
    
    best_result = 0
    best_phases = []
    phase_list = []
        
    # Generate list of possible phases
    for i in range(start_phase, end_phase + 1, 1):
        phase_list.append(i)
    
    # Generate all possible permutations of the phases
    phase_perms = list(itertools.permutations(phase_list))
    print('Part2: Testing Phase Permutations of: ', phase_list)
    
    # Run amplifier sequence through all phase permutations
    for phase in phase_perms:
        amp_input = start_input
        
        # Create list of programs and program positions for each amplifier, and if the amplifiers have been initialised.
        prog_list = [program[:]] * 5
        code_pos_list = [0] * 5
        init_list = [False] * 5
        prog_mem = [0] * 5
        
        out_code = 0
        
        # Run until end signal has been received at e
        while out_code == 0:
                        
            # Run through each amplifier in turn
            for i in range(5):
                #Run intcode on each amp, store ouput code and program position
                amp_data, amp_out, out_code, code_pos = run_intcode(prog_list[i], phase[i], amp_input, code_pos_list[i], prog_mem[i], init_list[i])
                amp_input = amp_out
                prog_list[i] = amp_data
                code_pos_list[i] = code_pos
                prog_mem[i] = amp_out
                init_list[i] = True
                               
            # If program complete signal received from amp E, move to next phase perm
            if out_code == 99:
                # If the output of this permutation is the best yet, store results.
                if amp_out > best_result:
                    best_result = amp_out
                    best_phases = phase

            
    return best_result, best_phases
    

program = read_data("day7input.txt")
#print(program)

#test_program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
#test_program2= [3,23,3,24,1002,24,10,24,1002,23,-1,23,
#101,5,23,23,1,24,23,23,4,23,99,0,0]
#test_program3= [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
#1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]

#Pt 2 test programs
#test_program4 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
#27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
#test_program5 = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
#-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
#53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]


best_output, best_phases = tune_amplifiers(program, 0, 0, 4)
print(best_output, best_phases)
print("Part 1: Answer is: ", best_output)

best_output2, best_phases2 = tune_amplifiers_feedback(program, 0, 5, 9)
print(best_output2, best_phases2)
print("Part 2: Answer is: ", best_output2)

               
       

