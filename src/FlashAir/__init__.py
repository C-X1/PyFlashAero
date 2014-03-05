'''
Created on Jan 4, 2014

Licence: GNU AGPL

@author: Christian Holl
'''

import sys
if sys.hexversion < 0x03000000:
    sys.exit("Python 3 or newer is required for running this program.")

__all__ = ['card','ImageViewer']
from FlashAir import card
from FlashAir import ImageViewer