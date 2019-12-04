# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 10:28:28 2019

@author: Paul
"""

def generate_passwords(start, stop):
    """
    Generates and returns a list strings of all possible passwords in the range 
    start-stop, meeting the following requirements:
        
        - Passwords are six digit numbers
        - In each password two adjacent digits must be the same
        - In each password, going from largest to smallest digit, the size of
        the digit does not decrease:
            111123, 135679, 111111 meet the criteria
            223450 does not (decreasing pair of digits 50)
            123789 does not (no double adjacent digits)  
    """
    
    passwords = []
    
    for i in range(start, stop+1, 1):
        passwords.append(str(i))
        
    return passwords


def valid_passwords_1(passwords):
    """
    Takes a list of password strings, and returns the number of passwords in 
    the list meeting the following criteria:
        
        - Passwords are six digit numbers
        - In each password two adjacent digits must be the same
        - In each password, going from largest to smallest digit, the size of
        the digit does not decrease:
            111123, 135679, 111111 meet the criteria
            223450 does not (decreasing pair of digits 50)
            123789 does not (no double adjacent digits)  
    """
    
    valid = 0
    
    for entry in passwords:
        adjacent = False
        order = True
        
        #Check for adjacent duplicate numbers
        for i in range(len(entry) - 1):
            
            if entry[i] == entry[i+1]:
                adjacent = True
                
        
        for i in range(len(entry) - 1):
            
            if entry[i] > entry[i+1]:
                order = False
                
        if adjacent and order:
            valid += 1
            
    return valid
            

def valid_passwords_2(passwords):
    """
    Takes a list of password strings, and returns the number of passwords in 
    the list meeting the following criteria:
        
        - Passwords are six digit numbers
        - In each password two adjacent digits must be the same
        - The two adjacent digits meeting the above requirement must not be
          part of a larger repeated block ie. 123455 is valid, 123444 is not.
        - In each password, going from largest to smallest digit, the size of
        the digit does not decrease:
            111123, 135679, 111111 meet the criteria
            223450 does not (decreasing pair of digits 50)
            123789 does not (no double adjacent digits)  
    """
    
    valid = 0
    
    for entry in passwords:
        adjacent = False
        order = True
        
        #Check for adjacent duplicate numbers
        for i in range(len(entry) - 1):
            
            if (entry[i] == entry[i+1]):
                test_num = entry[i]
                
                if entry.count(test_num) == 2:
                    adjacent = True
            
        for i in range(len(entry) - 1):
            
            if entry[i] > entry[i+1]:
                order = False
                
        if adjacent and order:
            valid += 1
            
    return valid

#passwords = ["112233", "123444", "111122"] #Test Passwords
passwords = generate_passwords(256310, 732736)
valid_pass_num1 = valid_passwords_1(passwords)

valid_pass_num2 = valid_passwords_2(passwords)
print("Part 1: Number of valid passwords in range: ", valid_pass_num1)
print("Part 2: Number of valid passwords in range: ", valid_pass_num2)