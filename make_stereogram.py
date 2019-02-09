#!/usr/bin/env python3
""" Script to generate an autostereogram.

I want to do this to send stupid messages to my friends.
I have based this code on the blog post at:
https://flothesof.github.io/making-stereograms-Python.html

"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as si
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

    fontsize = 148

    image = Image.new('F', size)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("calibrib.ttf", fontsize)
    w, h = draw.textsize(input_string, font=font)

    draw.text(((size[0] - w)/2.0, (size[1] - h)/2.0),
              input_string, font=font)

    raw_data = image.getdata()
    array_data = np.array(raw_data).reshape(image.size[0],
                                            image.size[1],
                                            order="F")

    # apply a gaussian filter so edges aren't so sharp.
    return si.gaussian_filter(array_data.T, 1.5)


def make_autostereogram(depthmap, pattern, shift_amplitude=0.09):
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

pattern = create_pattern((80, 80), 32)
depth_map = create_depthmap("SPACE\nRACISM!", size=(16*50, 9*50))
stereogram = make_autostereogram(depth_map, pattern)

# save out the stereogram image.
_, ax = plt.subplots(figsize=(16, 9))
ax.imshow(stereogram,
          aspect="equal",
          cmap="viridis",
          interpolation=None)
plt.axis("off")
plt.savefig("autostereogram.png")