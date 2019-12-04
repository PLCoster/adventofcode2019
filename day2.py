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


def run_intcode(program):
    """
    Takes data, list of ints to run int_code on.
    Returns list of ints after intcode program has been run.
    
    Running Intcode program looks reads in the integers sequentially in sets of 4:
        data[i]      == Opcode
        data[i+1]    == Index 1
        data[i+2]    == Index 2
        data[i+3]    == Index 3
        
    If Opcode == 1, the entries at index 1 and 2 in the program are summed and
    stored at index 3. 
    If Opcode == 2, the entries at index 1 and 2 are multiplied instead.
    If Opcode == 99, the program is completed and will stop running.
    """
    
    data = program[:]
    
    for i in range(0, len(data), 4):
        
        if data[i] == 99:           
            break
        
        elif data[i] == 1:
            data[data[i+3]] = data[data[i+2]] + data[data[i+1]]
            
        elif data[i] == 2:           
            data[data[i+3]] = data[data[i+2]] * data[data[i+1]]
        
        else:
            print("Problem with the Program")
            break
        
    return data


def run_multiple_intcodes(program, result):
    """
    Takes an intcode program and result, an int which is the desired result
    of running the intcode.
    
    Allows for multiple intcodes to be run, changing the program entries at the
    1st and 2nd index locations, in order to find the intcode program that
    returns the required result at the 0th index position.
    
    Returns the values required at the 1st and 2nd index locations to get the
    desired output.   
    """
    
    for i in range(0, 100):
        for j in range(0, 100):
            program[1] = i
            program[2] = j
            #print(program)
            answer = run_intcode(program)
            #print(answer[0])
        
            if answer[0] == result:
                noun = i
                verb = j
            
                return(noun, verb)

program = read_data("day2input.txt")

program[1] = 12
program[2] = 2

answer = run_intcode(program)
print("Part 1: Answer is: ", answer[0])
                 
print("Part 2: Required inputs are: ", run_multiple_intcodes(program, 19690720))        

