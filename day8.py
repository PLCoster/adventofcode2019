# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 22:23:19 2019

@author: Paul
"""

import numpy as np
from PIL import Image

def read_data(filename):
    """
    Reads raw space image format data file into a string
    """
    
    data = ''
    
    f = open(filename, 'r')
    for line in f:
        data += line.strip('\n')    
    f.close()   
    
    return data


def get_layers(data_raw, width, height):
    """
    Takes raw input data string and splits it into layers, based
    on the width and height of the image received.
    
    Returns a list with each entry being a single layer of the
    image.
    """
    
    layer_list = []
    image_size = width * height
    
    
    for i in range(0, len(data_raw), image_size):
        layer_list.append(data_raw[i:i+image_size])
        
    return layer_list


def validate_image(layer_list):
    """ 
    Takes list of image layer strings.
    
    Validates image layer data by finding the layer with the fewest 0 digits,
    and then determines and returns the number of 1 digits multiplied by the number
    of 2 digits in that layer.
    """
    
    min_count = 150
    best_layer = -1
    
    for i in range(len(layer_list)):
        zeroes = layer_list[i].count('0')
        if zeroes < min_count:
            min_count = zeroes
            best_layer = i
            
    return layer_list[best_layer].count('1') * layer_list[best_layer].count('2')


def decode_image(layer_list):
    """
    Takes list of image layer strings as input.
    
    Produces an output by looking through each layer until the following:
    If a digit is 0 that means that pixel is black.
    If a digit is 1 that means the pixel is white.
    If a digit is 2 that means the pixel is transparent.
    
    The first layer with a 0 or 1 pixel will dictate the color of that pixel.
    """

    decoded = []
    
    for i in range(len(layer_list[0])):
        
        layer = 0
              
        while True:
            if layer_list[layer][i] == '0':
                decoded.append('0')
                break
            elif layer_list[layer][i] == '1':
                decoded.append('1')
                break
            
            layer += 1
   
    return decoded
                


raw_data = read_data('day8input.txt')
#print(raw_data)

layer_list = get_layers(raw_data, 25, 6)
#print(layer_list)

validation = validate_image(layer_list)
print("Part1: Answer is: ", validation)

decoded = decode_image(layer_list)
#print(decoded)

#Turn decoded image into 2D array and then display
picture = np.array(decoded).reshape(-1,25).astype(np.int)
#print(picture)
img = Image.fromarray(picture*255)
img.show() #'CEKUA'


