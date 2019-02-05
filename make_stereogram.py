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

def make_pattern(shape, levels):
    """ Create the base repeating pattern. """

    return np.random.randint(0, levels - 1, shape) / levels


def create_depthmap(input_string, size=(800, 600)):
    """ Create the depthmap image to put behind the pattern. 
    
    There might be a another way to do this, but current way
    I'm thinking is create an image, write the text on it with
    PIL, then extract the pixel values.

    I'm using the method descibed here:
    https://stackoverflow.com/questions/16373425/add-text-on-image-using-pil
    
    """

    image = Image.new('RGB', size)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 16)
    draw.text((0, 0),"Sample Text",(255,255,255),font=font)

    return np.array(image.getdata()).reshape((size[0], size[1], 3))

thing = create_depthmap("test", size=(100, 100))
