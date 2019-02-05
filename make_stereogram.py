#!/usr/bin/env python3
""" Script to generate an autostereogram.

I want to do this to send stupid messages to my friends.
I have based this code on the blog post at:
https://flothesof.github.io/making-stereograms-Python.html

"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def create_pattern(shape, levels):
    """ Create the base repeating pattern. """

    return np.random.randint(0, levels - 1, shape) / levels


def create_depthmap(input_string, size):
    """ Create the depthmap image to put behind the pattern. 
    
    There might be a another way to do this, but current way
    I'm thinking is create an image, write the text on it with
    PIL, then extract the pixel values.

    I'm using the method descibed here:
    https://stackoverflow.com/questions/16373425/add-text-on-image-using-pil

    Returns a depth map, normalised from 0 - 1
    
    """

    fontsize = 140

    image = Image.new('F', size)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("ariblk.ttf", fontsize)

    # fix width and height offset
    # TB TODO: Get the automatic placement of the text correct.
    offset_width = 0.10 * size[0]
    offset_height = 0.10 * size[1]

    offset = (offset_width, offset_height)
    draw.text(offset, input_string, 1.0, font=font)

    raw_data = image.getdata()
    array_data = np.array(raw_data).reshape(image.size[0],
                                            image.size[1],
                                            order="F")

    print(array_data.shape)
    print("expected pixels are: {}".format(size[0]*size[1]))

    return array_data.T


def make_autostereogram(depthmap, pattern, shift_amplitude=0.15):
    "Creates an autostereogram from depthmap and pattern."
    
    autostereogram = np.zeros_like(depthmap, dtype=pattern.dtype)

    for r in np.arange(autostereogram.shape[0]):
        for c in np.arange(autostereogram.shape[1]):
            # TB NOTE: I don't quite understand this bit yet.
            if c < pattern.shape[1]:
                autostereogram[r, c] = pattern[r % pattern.shape[0], c]
            else:
                shift = int(depthmap[r, c] * shift_amplitude * pattern.shape[1])
                autostereogram[r, c] = autostereogram[r, c - pattern.shape[1] + shift]
    return autostereogram

pattern = create_pattern((100, 100), 8)
depth_map = create_depthmap("SPACE\nRACIST", size=(800, 600))
stereogram = make_autostereogram(depth_map, pattern)