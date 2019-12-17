# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 10:53:42 2019

@author: Paul
"""

# Advent of Code Day 16: Flawed Frequency Transmission

def read_data(filename):
    """
    Reads data file into a list of ints.
    """
    
    int_data = []
    
    f = open(filename, 'r')
    for line in f:
        data = line.strip('\n')
        int_data += [int(char) for char in data]
    
    f.close() 
         
    return int_data


def fft(signal, num_phases, offset):
    """
    Runs fft  algorithm on signal for specified number of phases
    
    At each phase, it multiplies each element of the signal by the repeating pattern
    [0, 1, 0, -1], sums the result, and takes the smallest digit. When calculating the result
    for each element the repeated pattern is extended i.e. [0,0,-1,-1,0,0,1,1] for the second element.
    
    The final result for each phase is then used as the signal input for the next phase.
    
    offset determines the point in the signal code you are interested in. When calculating
    the digits at this point all previous elements will be multiplied by repeat pattern [0],
    and so will not affect the result.
    
    Returns the processed signal.
    """
    
    signal_in = signal
    
    print('Running FFT...')
    # Run process for required number of phases
    for i in range(num_phases):
        
        #print('Calculating phase:', i)
        output_str = ''
        
        # Iterate over each digit of ouput
        for j in range(offset, len(signal_in), 1):
            
            #print('Calculating digit: ', j)
            
            repeat_pattern = [0] * (j+1) + [1] * (j+1) + [0] * (j+1) + [-1] * (j+1)    
            result = 0
            
            # Iterate over all signal elements, multiply and sum to get digit of output
            for k in range (offset, len(signal_in), 1):
                
                pattern = repeat_pattern[(k+1) % len(repeat_pattern)]
                #print('k: ', k)
                #print(pattern)
                #print(signal_in[k])
                result += pattern * signal_in[k]
            
            # Get output digit and out to the output string
            output_str += str(abs(result) % 10)
            
        
        # Output signal used as input signal for next phase
        signal_in = signal[0:offset] + [int(x) for x in output_str]
        
    return output_str


def fft_offset(signal, num_phases, offset):
    """
    Runs fft  algorithm on signal for specified number of phases, where the offset
    is bigger than half the signal length.
    
    Where the offset is > 1/2 the signal length, all the repeated pattern parameters
    are 0 or 1. To calculate each digit, the sum of all values in the signal from the 
    offset point is calculated - This gives the result for digit 0. The result for
    digit 1 can then be calculated by subtracting the first signal value fromthe offset point.
    
    Returns the processed signal, starting from the offset point.
    """
    
    signal_in = signal[offset:]
    
    print('Running Optimised FFT with offset > 1/2 signal length...')
    # Run process for required number of phases
    for i in range(num_phases):
        
        #print('Calculating phase:', i)
        output_str = ''
        
        # Get the first result
        results = []
        results.append(sum(signal_in))
        output_str += str(results[0] % 10)
        # Next result is previous result minus first signal digit, etc:               
        for k in range(0, len(signal_in)-1):

            results.append(results[k] - signal_in[k])
                                                            
            output_str += str(results[k+1] % 10)
            
        # Output signal used as input signal for next phase
        signal_in = [int(x) for x in output_str]
        
    return output_str
                

signal = read_data('day16input.txt')
#print(signal)

# Test for part 1
#test = fft([1,2,3,4,5,6,7,8], 4, 1) # 01029498
#print(test)

# Part 1:
result1 = fft(signal, 100, 0)
print('Part 1: First 8 digits output after 100 phases FFT: ', result1[0:8])


# Test for part 2
#test2 = fft_offset([1,2,3,4,5,6,7,8], 4, 4) # 9498
#print(test2)

# Part2:
result2 = fft_offset(signal*10000,100, 5972351) # 5972351
print('Part2: 8 Digits at offset location (5972351): ', result2[0:8])

