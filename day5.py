# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 11:06:59 2019

@author: Paul
"""

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


def run_intcode(program, input_int):
    """
    Takes data, list of ints to run int_code on.
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
    answer = -1
    params = [0, 0, 0]
    param_modes = ['', '', '']
   
    i = 0
    
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
            data[data[i+1]] = input_int
            i += 2;
        # If opcode is 4, print out the input stored at specified location.
        elif opcode == 4:
            answer = data[data[i+1]]
            print("Program output: ", data[data[i+1]])
            i += 2;
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
            print("Program ended by halt code")
            break
        # If opcode is anything else something has gone wrong!
        else:
            print("Problem with the Program")
            break       
        
    return data, answer

program = read_data("day5input.txt")
#print(program)

result1, answer1 = run_intcode(program, 1)
#print(result1)
print("Part 1: Answer is: ", answer1)

result2, answer2 = run_intcode(program, 5)
#print(result2)
print("Part 2: Answer is: ", answer2)

#test_program = [1002,4,3,4,33]
#test_program2 = [3,0,4,0,99]
#test_program3 = [1101,100,-1,4,0]

#test_program4 = [3,9,8,9,10,9,4,9,99,-1,8] # 1 if input = 8, 0 otherwise
#test_program5 = [3,9,7,9,10,9,4,9,99,-1,8] # 1 if input < 8, 0 otherwise
#test_program6 = [3,3,1108,-1,8,3,4,3,99]   # 1 if input = 8, 0 otherwise
#test_program7 = [3,3,1107,-1,8,3,4,3,99]   # 1 if input < 8, 0 otherwise
#test_program8 = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]  # 0 if input = 0, 1 otherwise
#test_program9 = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]       # 0 if input = 0, 1 otherwise

#test_program10 = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,
#36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,
#1105,1,46,98,99] # 999 if input < 8, 1000 if input = 8, 1001 if input > 8                 
       

