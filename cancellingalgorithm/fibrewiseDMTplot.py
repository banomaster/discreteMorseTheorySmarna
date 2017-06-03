import random
import itertools
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.backends.backend_pdf import PdfPages

# balls
B2 = [(1, 2, 3)]

# spheres
S1 = [(1, 2), (2, 3), (3, 4), (1, 4)]
S2 = [(1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)]
S1VS1 = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]

# torus
T = [(1, 2, 4), (2, 4, 6), (2, 3, 6), (3, 6, 8), (1, 3, 8),
     (1, 4, 8), (4, 5, 6), (5, 6, 7), (6, 7, 8), (7, 8, 9),
     (4, 8, 9), (4, 5, 9), (1, 5, 7), (1, 2, 7), (2, 7, 9),
     (2, 3, 9), (3, 5, 9), (1, 3, 5)]

VcT = {(1, ): [(1, 1), (4, 1), (1, 4), (4, 4)],
       (2, ): [(2, 1), (2, 4)],
       (3, ): [(3, 1), (3, 4)],
       (4, ): [(1, 3), (4, 3)],
       (5, ): [(1, 2), (4, 2)],
       (6, ): [(2, 3)],
       (7, ): [(2, 2)],
       (8, ): [(3, 3)],
       (9, ): [(3, 2)]}

EcT = {(1, 2): [((1, 4), (2, 4)), ((1, 1), (2, 1))],
       (1, 3): [((4, 1), (3, 1)), ((4, 4), (3, 4))],
       (2, 3): [((2, 1), (3, 1)), ((2, 4), (3, 4))],
       (1, 4): [((1, 4), (1, 3)), ((4, 4), (4, 3))],
       (1, 5): [((1, 1), (1, 2)), ((4, 1), (4, 2))],
       (4, 5): [((1, 3), (1, 2)), ((4, 3), (4, 2))],
       (2, 6): [((2, 4), (2, 3))],
       (4, 6): [((1, 3), (2, 3))],
       (3, 8): [((3, 4), (3, 3))],
       (4, 8): [((4, 3), (3, 3))],
       (2, 7): [((2, 1), (2, 2))],
       (5, 7): [((1, 2), (2, 2))],
       (3, 9): [((3, 1), (3, 2))],
       (5, 9): [((4, 2), (3, 2))],
       (6, 7): [((2, 3), (2, 2))],
       (6, 8): [((2, 3), (3, 3))],
       (7, 9): [((2, 2), (3, 2))],
       (8, 9): [((3, 3), (3, 2))],
       (2, 4): [((2, 4), (1, 3))],
       (3, 6): [((3, 4), (2, 3))],
       (1, 8): [((4, 4), (3, 3))],
       (5, 6): [((1, 2), (2, 3))],
       (7, 8): [((2, 2), (3, 3))],
       (4, 9): [((4, 3), (3, 2))],
       (1, 7): [((1, 1), (2, 2))],
       (2, 9): [((2, 1), (3, 2))],
       (3, 5): [((3, 1), (4, 2))]}

FcT = {(1, 2, 4): [(1, 4), (2, 4), (1, 3)], (2, 4, 6): [(2, 4), (1, 3), (2, 3)],
       (2, 3, 6): [(2, 4), (3, 4), (2, 3)], (3, 6, 8): [(3, 4), (2, 3), (3, 3)],
       (1, 3, 8): [(4, 4), (3, 4), (3, 3)], (1, 4, 8): [(4, 4), (4, 3), (3, 3)],
       (4, 5, 6): [(1, 3), (1, 2), (2, 3)], (5, 6, 7): [(1, 2), (2, 3), (2, 2)],
       (6, 7, 8): [(2, 3), (2, 2), (3, 3)], (7, 8, 9): [(2, 2), (3, 3), (3, 2)],
       (4, 8, 9): [(4, 3), (3, 3), (3, 2)], (4, 5, 9): [(4, 3), (4, 2), (3, 2)],
       (1, 5, 7): [(1, 1), (1, 2), (2, 2)], (1, 2, 7): [(1, 1), (2, 1), (2, 2)],
       (2, 7, 9): [(2, 1), (2, 2), (3, 2)], (2, 3, 9): [(2, 1), (3, 1), (3, 2)],
       (3, 5, 9): [(3, 1), (4, 2), (3, 2)], (1, 3, 5): [(4, 1), (3, 1), (4, 2)]}

labelT = {(1, 1): [1, -1, "1", "top", "left"],
          (1, 4): [1, -1, "1", "top", "left"],
          (4, 1): [1, -1, "1", "top", "left"],
          (4, 4): [1, -1, "1", "top", "left"],
          (2, 1): [1, -1, "2", "top", "left"],
          (2, 4): [1, -1, "2", "top", "left"],
          (3, 1): [1, -1, "3", "top", "left"],
          (3, 4): [1, -1, "3", "top", "left"],
          (1, 3): [1, -1, "4", "top", "left"],
          (4, 3): [1, -1, "4", "top", "left"],
          (1, 2): [1, -1, "5", "top", "left"],
          (4, 2): [1, -1, "5", "top", "left"],
          (2, 3): [1, -1, "6", "top", "left"],
          (2, 2): [1, -1, "7", "top", "left"],
          (3, 3): [1, -1, "8", "top", "left"],
          (3, 2): [1, -1, "9", "top", "left"]}

# Klein bottle
K = [(1, 2, 4), (2, 4, 6), (2, 3, 6), (3, 6, 8),
     (1, 3, 8), (1, 5, 8), (4, 5, 6), (5, 6, 7),
     (6, 7, 8), (7, 8, 9), (5, 8, 9), (4, 5, 9),
     (1, 5, 7), (1, 2, 7), (2, 7, 9), (2, 3, 9),
     (3, 4, 9), (1, 3, 4)]

VcK = {(1, ): [(1, 1), (4, 1), (1, 4), (4, 4)],
       (2, ): [(2, 1), (2, 4)],
       (3, ): [(3, 1), (3, 4)],
       (4, ): [(1, 3), (4, 2)],
       (5, ): [(1, 2), (4, 3)],
       (6, ): [(2, 3)],
       (7, ): [(2, 2)],
       (8, ): [(3, 3)],
       (9, ): [(3, 2)]}

EcK = {(1, 2): [((1, 4), (2, 4)), ((1, 1), (2, 1))],
       (1, 3): [((4, 1), (3, 1)), ((4, 4), (3, 4))],
       (2, 3): [((2, 1), (3, 1)), ((2, 4), (3, 4))],
       (1, 4): [((1, 4), (1, 3)), ((4, 1), (4, 2))],
       (1, 5): [((1, 1), (1, 2)), ((4, 4), (4, 3))],
       (4, 5): [((1, 3), (1, 2)), ((4, 2), (4, 3))],
       (2, 6): [((2, 4), (2, 3))],
       (4, 6): [((1, 3), (2, 3))],
       (3, 8): [((3, 4), (3, 3))],
       (5, 8): [((4, 3), (3, 3))],
       (2, 7): [((2, 1), (2, 2))],
       (5, 7): [((1, 2), (2, 2))],
       (3, 9): [((3, 1), (3, 2))],
       (4, 9): [((4, 2), (3, 2))],
       (6, 7): [((2, 3), (2, 2))],
       (6, 8): [((2, 3), (3, 3))],
       (7, 9): [((2, 2), (3, 2))],
       (8, 9): [((3, 3), (3, 2))],
       (2, 4): [((2, 4), (1, 3))], (3, 6): [((3, 4), (2, 3))], (1, 8): [((4, 4), (3, 3))],
       (5, 6): [((1, 2), (2, 3))], (7, 8): [((2, 2), (3, 3))], (5, 9): [((4, 3), (3, 2))],
       (1, 7): [((1, 1), (2, 2))], (2, 9): [((2, 1), (3, 2))], (3, 4): [((3, 1), (4, 2))]}

FcK = {(1, 2, 4): [(1, 4), (2, 4), (1, 3)], (2, 4, 6): [(2, 4), (1, 3), (2, 3)],
       (2, 3, 6): [(2, 4), (3, 4), (2, 3)], (3, 6, 8): [(3, 4), (2, 3), (3, 3)],
       (1, 3, 8): [(4, 4), (3, 4), (3, 3)], (1, 5, 8): [(4, 4), (4, 3), (3, 3)],
       (4, 5, 6): [(1, 3), (1, 2), (2, 3)], (5, 6, 7): [(1, 2), (2, 3), (2, 2)],
       (6, 7, 8): [(2, 3), (2, 2), (3, 3)], (7, 8, 9): [(2, 2), (3, 3), (3, 2)],
       (5, 8, 9): [(4, 3), (3, 3), (3, 2)], (4, 5, 9): [(4, 2), (4, 3), (3, 2)],
       (1, 5, 7): [(1, 1), (1, 2), (2, 2)], (1, 2, 7): [(1, 1), (2, 1), (2, 2)],
       (2, 7, 9): [(2, 1), (2, 2), (3, 2)], (2, 3, 9): [(2, 1), (3, 1), (3, 2)],
       (3, 4, 9): [(3, 1), (4, 2), (3, 2)], (1, 3, 4): [(4, 1), (3, 1), (4, 2)]}

labelK = {(1, 1): [1, -1, "1", "top", "left"],
          (1, 4): [1, -1, "1", "top", "left"],
          (4, 1): [1, -1, "1", "top", "left"],
          (4, 4): [1, -1, "1", "top", "left"],
          (2, 1): [1, -1, "2", "top", "left"],
          (2, 4): [1, -1, "2", "top", "left"],
          (3, 1): [1, -1, "3", "top", "left"],
          (3, 4): [1, -1, "3", "top", "left"],
          (1, 3): [1, -1, "4", "top", "left"],
          (4, 2): [1, -1, "4", "top", "left"],
          (4, 3): [1, -1, "5", "top", "left"],
          (1, 2): [1, -1, "5", "top", "left"],
          (2, 3): [1, -1, "6", "top", "left"],
          (2, 2): [1, -1, "7", "top", "left"],
          (3, 3): [1, -1, "8", "top", "left"],
          (3, 2): [1, -1, "9", "top", "left"]}

# cylinder
C = [(1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6), (1, 5, 6), (1, 2, 6)]

VcC = {(1, ): [(1, 2), (4, 2)],
       (2, ): [(1, 1), (4, 1)],
       (3, ): [(2, 2)],
       (4, ): [(2, 1)],
       (5, ): [(3, 2)],
       (6, ): [(3, 1)]}

EcC = {(1, 2): [((1, 2), (1, 1)), ((4, 2), (4, 1))],
       (3, 4): [((2, 2), (2, 1))],
       (5, 6): [((3, 2), (3, 1))],
       (2, 4): [((1, 1), (2, 1))], (4, 6): [((2, 1), (3, 1))], (2, 6): [((4, 1), (3, 1))],
       (1, 3): [((1, 2), (2, 2))], (3, 5): [((2, 2), (3, 2))], (1, 5): [((4, 2), (3, 2))],
       (2, 3): [((1, 1), (2, 2))], (4, 5): [((2, 1), (3, 2))], (1, 6): [((4, 2), (3, 1))]}

FcC = {(1, 2, 3): [(1, 2), (1, 1), (2, 2)], (2, 3, 4): [(1, 1), (2, 2), (2, 1)],
       (3, 4, 5): [(2, 2), (2, 1), (3, 2)], (4, 5, 6): [(2, 1), (3, 2), (3, 1)],
       (1, 5, 6): [(4, 2), (3, 2), (3, 1)], (1, 2, 6): [(4, 2), (4, 1), (3, 1)]}

labelC = {(1, 1): [0, -1, "2", "top", "center"],
          (2, 1): [0, -1, "4", "top", "center"],
          (3, 1): [0, -1, "6", "top", "center"],
          (4, 1): [0, -1, "2", "top", "center"],
          (1, 2): [0, 1, "1", "bottom", "center"],
          (2, 2): [0, 1, "3", "bottom", "center"],
          (3, 2): [0, 1, "5", "bottom", "center"],
          (4, 2): [0, 1, "1", "bottom", "center"]}

# Moebius band
M = [(1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6), (2, 5, 6), (1, 2, 6)]

VcM = {(1, ): [(1, 2), (4, 1)],
       (2, ): [(1, 1), (4, 2)],
       (3, ): [(2, 2)],
       (4, ): [(2, 1)],
       (5, ): [(3, 2)],
       (6, ): [(3, 1)]}

EcM = {(1, 2): [((1, 2), (1, 1)), ((4, 1), (4, 2))],
       (3, 4): [((2, 2), (2, 1))],
       (5, 6): [((3, 2), (3, 1))],
       (2, 4): [((1, 1), (2, 1))],
       (4, 6): [((2, 1), (3, 1))],
       (1, 6): [((4, 1), (3, 1))],
       (1, 3): [((1, 2), (2, 2))],
       (3, 5): [((2, 2), (3, 2))],
       (2, 5): [((4, 2), (3, 2))],
       (2, 3): [((1, 1), (2, 2))],
       (4, 5): [((2, 1), (3, 2))],
       (2, 6): [((4, 2), (3, 1))]}

FcM = {(1, 2, 3): [(1, 2), (1, 1), (2, 2)], (2, 3, 4): [(1, 1), (2, 2), (2, 1)],
       (3, 4, 5): [(2, 2), (2, 1), (3, 2)], (4, 5, 6): [(2, 1), (3, 2), (3, 1)],
       (2, 5, 6): [(4, 2), (3, 2), (3, 1)], (1, 2, 6): [(4, 1), (4, 2), (3, 1)]}

labelM = {(1, 1): [0, -1, "2", "top", "center"],
          (2, 1): [0, -1, "4", "top", "center"],
          (3, 1): [0, -1, "6", "top", "center"],
          (4, 1): [0, -1, "1", "top", "center"],
          (1, 2): [0, 1, "1", "bottom", "center"],
          (2, 2): [0, 1, "3", "bottom", "center"],
          (3, 2): [0, 1, "5", "bottom", "center"],
          (4, 2): [0, 1, "2", "bottom", "center"]}

# dunce hat (contractible, not collapsible)
D = [(1, 2, 5), (1, 5, 6), (1, 6, 7), (1, 2, 7), (1, 4, 9), (1, 9, 10), (1, 10, 11), (1, 4, 11),
     (1, 2, 13), (1, 13, 14), (1, 14, 15), (1, 4, 15),
     (2, 3, 5), (2, 3, 7), (3, 4, 9), (3, 4, 11), (2, 3, 13), (3, 4, 15),
     (3, 7, 8), (3, 8, 9), (3, 11, 12), (3, 12, 13), (3, 15, 16), (3, 5, 16),
     (5, 6, 17), (5, 16, 17), (6, 7, 17), (7, 8, 17), (8, 9, 17), (9, 10, 17), (10, 11, 17), (11, 12, 17),
     (12, 13, 17), (13, 14, 17), (14, 15, 17), (15, 16, 17)]

VcD = {(1, ): [(0, 0), (10, 0), (5, 8.66)],
       (2, ): [(2.5, 0), (1.25, 2.17), (6.25, 6.5)],
       (3, ): [(5, 0), (2.5, 4.33), (7.5, 4.33)],
       (4, ): [(7.5, 0), (3.75, 6.5), (8.75, 2.17)],
       (5, ): [(2.5, 2.41)],
       (6, ): [(2.5, 1.44)],
       (7, ): [(3.33, 0.96)],
       (8, ): [(5, 1.44)],
       (9, ): [(6.67, 0.96)],
       (10, ): [(7.5, 1.44)],
       (11, ): [(7.5, 2.41)],
       (12, ): [(6.25, 3.61)],
       (13, ): [(5.83, 5.29)],
       (14, ): [(5, 5.77)],
       (15, ): [(4.17, 5.29)],
       (16, ): [(3.75, 3.61)],
       (17, ): [(5, 2.89)]}

EcD = {(1, 2): [((0, 0), (2.5, 0)), ((0, 0), (1.25, 2.17)), ((5, 8.66), (6.25, 6.5))],
       (2, 3): [((2.5, 0), (5, 0)), ((1.25, 2.17), (2.5, 4.33)), ((6.25, 6.5), (7.5, 4.33))],
       (3, 4): [((5, 0), (7.5, 0)), ((2.5, 4.33), (3.75, 6.5)), ((7.5, 4.33), (8.75, 2.17))],
       (1, 4): [((10, 0), (7.5, 0)), ((5, 8.66), (3.75, 6.5)), ((10, 0), (8.75, 2.17))],
       (1, 6): [((0, 0), (2.5, 1.44))],
       (6, 17): [((2.5, 1.44), (5, 2.89))],
       (8, 17): [((5, 1.44), (5, 2.89))],
       (3, 8): [((5, 0), (5, 1.44))],
       (2, 7): [((2.5, 0), (3.33, 0.96))],
       (7, 17): [((3.33, 0.96), (5, 2.89))],
       (3, 7): [((5, 0), (3.33, 0.96))],
       (6, 7): [((2.5, 1.44), (3.33, 0.96))],
       (1, 7): [((0, 0), (3.33, 0.96))],
       (7, 8): [((3.33, 0.96), (5, 1.44))],
       (1, 10): [((10, 0), (7.5, 1.44))],
       (10, 17): [((7.5, 1.44), (5, 2.89))],
       (3, 9): [((5, 0), (6.67, 0.96))],
       (9, 10): [((6.67, 0.96), (7.5, 1.44))],
       (4, 9): [((7.5, 0), (6.67, 0.96))],
       (9, 17): [((6.67, 0.96), (5, 2.89))],
       (1, 9): [((10, 0), (6.67, 0.96))],
       (8, 9): [((5, 1.44), (6.67, 0.96))],
       (1, 11): [((10, 0), (7.5, 2.41))],
       (11, 12): [((7.5, 2.41), (6.25, 3.61))],
       (4, 11): [((8.75, 2.17), (7.5, 2.41))],
       (11, 17): [((7.5, 2.41), (5, 2.89))],
       (10, 11): [((7.5, 1.44), (7.5, 2.41))],
       (3, 11): [((7.5, 4.33), (7.5, 2.41))],
       (3, 12): [((7.5, 4.33), (6.25, 3.61))],
       (12, 17): [((6.25, 3.61), (5, 2.89))],
       (1, 14): [((5, 8.66), (5, 5.77))],
       (14, 17): [((5, 5.77), (5, 2.89))],
       (2, 13): [((6.25, 6.5), (5.83, 5.29))],
       (13, 17): [((5.83, 5.29), (5, 2.89))],
       (1, 13): [((5, 8.66), (5.83, 5.29))],
       (12, 13): [((6.25, 3.61), (5.83, 5.29))],
       (3, 13): [((7.5, 4.33), (5.83, 5.29))],
       (13, 14): [((5.83, 5.29), (5, 5.77))],
       (1, 15): [((5, 8.66), (4.17, 5.29))],
       (15, 16): [((4.17, 5.29), (3.75, 3.61))],
       (3, 16): [((2.5, 4.33), (3.75, 3.61))],
       (16, 17): [((3.75, 3.61), (5, 2.89))],
       (3, 15): [((2.5, 4.33), (4.17, 5.29))],
       (14, 15): [((5, 5.77), (4.17, 5.29))],
       (4, 15): [((3.75, 6.5), (4.17, 5.29))],
       (15, 17): [((4.17, 5.29), (5, 2.89))],
       (1, 5): [((0, 0), (2.5, 2.41))],
       (5, 16): [((2.5, 2.41), (3.75, 3.61))],
       (3, 5): [((2.5, 4.33), (2.5, 2.41))],
       (5, 6): [((2.5, 2.41), (2.5, 1.44))],
       (2, 5): [((1.25, 2.17), (2.5, 2.41))],
       (5, 17): [((2.5, 2.41), (5, 2.89))]}

FcD = {(1, 2, 5): [(0.00, 0.00), (1.25, 2.17), (2.50, 2.41)],
       (1, 5, 6): [(0.00, 0.00), (2.50, 2.41), (2.50, 1.44)],
       (1, 6, 7): [(0.00, 0.00), (2.50, 1.44), (3.33, 0.96)],
       (1, 2, 7): [(0.00, 0.00), (2.50, 0.00), (3.33, 0.96)],
       (1, 4, 9): [(10.0, 0.00), (7.50, 0.00), (6.67, 0.96)],
       (2, 3, 5): [(1.25, 2.17), (2.50, 4.33), (2.50, 2.41)],
       (2, 3, 7): [(2.50, 0.00), (5.00, 0.00), (3.33, 0.96)],
       (3, 4, 9): [(5.00, 0.00), (7.50, 0.00), (6.67, 0.96)],
       (3, 7, 8): [(5.00, 0.00), (3.33, 0.96), (5.00, 1.44)],
       (3, 8, 9): [(5.00, 0.00), (5.00, 1.44), (6.67, 0.96)],
       (1, 9, 10): [(10.0, 0.00), (6.67, 0.96), (7.50, 1.44)],
       (1, 4, 11): [(10.0, 0.00), (8.75, 2.17), (7.50, 2.41)],
       (1, 2, 13): [(5.00, 8.66), (6.25, 6.50), (5.83, 5.29)],
       (1, 4, 15): [(5.00, 8.66), (3.75, 6.50), (4.17, 5.29)],
       (3, 4, 11): [(7.50, 4.33), (8.75, 2.17), (7.50, 2.41)],
       (2, 3, 13): [(6.25, 6.50), (7.50, 4.33), (5.83, 5.29)],
       (3, 4, 15): [(2.50, 4.33), (3.75, 6.50), (4.17, 5.29)],
       (3, 5, 16): [(2.50, 4.33), (2.50, 2.41), (3.75, 3.61)],
       (5, 6, 17): [(2.50, 2.41), (2.50, 1.44), (5.00, 2.89)],
       (6, 7, 17): [(2.50, 1.44), (3.33, 0.96), (5.00, 2.89)],
       (7, 8, 17): [(3.33, 0.96), (5.00, 1.44), (5.00, 2.89)],
       (8, 9, 17): [(5.00, 1.44), (6.67, 0.96), (5.00, 2.89)],
       (5, 16, 17): [(2.50, 2.41), (3.75, 3.61), (5.00, 2.89)],
       (1, 13, 14): [(5.00, 8.66), (5.83, 5.29), (5.00, 5.77)],
       (1, 14, 15): [(5.00, 8.66), (5.00, 5.77), (4.17, 5.29)],
       (1, 10, 11): [(10.0, 0.00), (7.50, 1.44), (7.50, 2.41)],
       (3, 11, 12): [(7.50, 4.33), (7.50, 2.41), (6.25, 3.61)],
       (3, 12, 13): [(7.50, 4.33), (6.25, 3.61), (5.83, 5.29)],
       (3, 15, 16): [(2.50, 4.33), (4.17, 5.29), (3.75, 3.61)],
       (9, 10, 17): [(6.67, 0.96), (7.50, 1.44), (5.00, 2.89)],
       (10, 11, 17): [(7.50, 1.44), (7.50, 2.41), (5.00, 2.89)],
       (11, 12, 17): [(7.50, 2.41), (6.25, 3.61), (5.00, 2.89)],
       (12, 13, 17): [(6.25, 3.61), (5.83, 5.29), (5.00, 2.89)],
       (13, 14, 17): [(5.83, 5.29), (5.00, 5.77), (5.00, 2.89)],
       (14, 15, 17): [(5.00, 5.77), (4.17, 5.29), (5.00, 2.89)],
       (15, 16, 17): [(4.17, 5.29), (3.75, 3.61), (5.00, 2.89)]}

labelD = {(0.00, 0.00): [-1, -1, "1", "top", "right"],
          (10.0, 0.00): [1, -1, "1", "top", "left"],
          (5.00, 8.66): [0, 1, "1", "bottom", "center"],
          
          (2.50, 0.00): [0, -1, "2", "top", "center"],
          (1.25, 2.17): [-1, 0, "2", "center", "right"],
          (6.25, 6.50): [1, 0, "2", "center", "left"],
          
          (5.00, 0.00): [0, -1, "3", "top", "center"],
          (2.50, 4.33): [-1, 0, "3", "center", "right"],
          (7.50, 4.33): [1, 0, "3", "center", "left"],
          
          (7.50, 0.00): [0, -1, "4", "top", "center"],
          (3.75, 6.50): [-1, 0, "4", "center", "right"],
          (8.75, 2.17): [1, 0, "4", "center", "left"],
          
          (2.50, 2.41):  [-1, 1, "5", "bottom", "right"],
          (2.50, 1.44):  [-1.5, 0, "6", "bottom", "right"],
          (3.33, 0.96):  [0, -1.5, "7", "top", "center"],
          (5.00, 1.44):  [1, -1, "8", "top", "left"],
          (6.67, 0.96):  [0, -1.5, "9", "top", "center"],
          (7.50, 1.44):  [1.5, 0, "10", "bottom", "left"],
          (7.50, 2.41):  [1, 1, "11", "bottom", "left"],
          (6.25, 3.61):  [2, 0.5, "12", "top", "left"],
          (5.83, 5.29):  [1.5, 0, "13", "bottom", "left"],
          (5.00, 5.77):  [1, 1, "14", "bottom", "left"],
          (4.17, 5.29):  [-1.5, 0, "15", "bottom", "right"],
          (3.75, 3.61):  [-2, 0.5, "16", "top", "right"],
          (5.00, 2.89):  [1.8, 2.2, "17", "bottom", "left"]}

# projective plane
RP2 = [(1, 3, 5), (1, 2, 6), (1, 5, 6), (1, 2, 4), (1, 3, 4),
       (2, 3, 5), (2, 3, 6), (2, 4, 5), (3, 4, 6), (4, 5, 6)]

VcRP2 = {(1, ): [(0, 5.73), (0, 0.27)],
         (2, ): [(-2, 2.27), (2.73, 5)],
         (3, ): [(-2.73, 5), (2, 2.27)],
         (4, ): [(0, 2.27)],
         (5, ): [(-1, 4)],
         (6, ): [(1, 4)]}

EcRP2 = {(1, 2): [((0, 5.73), (2.73, 5)), ((0, 0.27), (-2, 2.27))],
         (1, 3): [((0, 0.27), (2, 2.27)), ((0, 5.73), (-2.73, 5))],
         (2, 3): [((-2, 2.27), (-2.73, 5)), ((2.73, 5), (2, 2.27))],
         (1, 6): [((0, 5.73), (1, 4))],
         (2, 6): [((2.73, 5), (1, 4))],
         (3, 6): [((2, 2.27), (1, 4))],
         (1, 4): [((0, 0.27), (0, 2.27))],
         (2, 4): [((-2, 2.27), (0, 2.27))],
         (3, 4): [((2, 2.27), (0, 2.27))],
         (1, 5): [((0, 5.73), (-1, 4))],
         (2, 5): [((-2, 2.27), (-1, 4))],
         (3, 5): [((-2.73, 5), (-1, 4))],
         (4, 6): [((0, 2.27), (1, 4))],
         (4, 5): [((0, 2.27), (-1, 4))],
         (5, 6): [((-1, 4), (1, 4))]}

FcRP2 = {(3, 4, 6): [(2, 2.27), (0, 2.27), (1, 4)],
         (2, 3, 5): [(-2, 2.27), (-2.73, 5), (-1, 4)],
         (2, 3, 6): [(2.73, 5), (2, 2.27), (1, 4)],
         (2, 4, 5): [(-2, 2.27), (0, 2.27), (-1, 4)],
         (1, 2, 4): [(0, 0.27), (-2, 2.27), (0, 2.27)],
         (4, 5, 6): [(0, 2.27), (-1, 4), (1, 4)],
         (1, 2, 6): [(0, 5.73), (2.73, 5), (1, 4)],
         (1, 5, 6): [(0, 5.73), (-1, 4), (1, 4)],
         (1, 3, 5): [(0, 5.73), (-2.73, 5), (-1, 4)],
         (1, 3, 4): [(0, 0.27), (2, 2.27), (0, 2.27)]}

labelRP2 = {(0, 5.73): [0, 1, "1", "bottom", "center"],
            (0, 0.27): [0, -1, "1", "top", "center"],
            (-2, 2.27): [0, -1, "2", "top", "center"],
            (2.73, 5): [0, 1, "2", "bottom", "center"],
            (-2.73, 5): [0, 1, "3", "bottom", "center"],
            (2, 2.27): [0, -1, "3", "top", "center"],
            (0, 2.27): [0, 1, "4", "bottom", "center"],
            (-1, 4): [0, -1.5, "5", "top", "center"],
            (1, 4): [0, -1.5, "6", "top", "center"]}


# hypercubes
Q4 = [( 1,  4, 14, 15), ( 1,  6, 12, 15), ( 1,  7, 12, 14), ( 1,  8, 10, 15), ( 1,  8, 11, 14), ( 1,  8, 12, 13),
     ( 2,  3, 13, 16), ( 2,  5, 11, 16), ( 2,  7,  9, 16), ( 2,  7, 11, 14), ( 2,  7, 12, 13), ( 2,  8, 11, 13),
     ( 3,  5, 10, 16), ( 3,  6,  9, 16), ( 3,  6, 10, 15), ( 3,  6, 12, 13), ( 3,  8, 10, 13), ( 4,  5,  9, 16),
     ( 4,  5, 10, 15), ( 4,  5, 11, 14), ( 4,  6,  9, 15), ( 4,  7,  9, 14), ( 5,  8, 10, 11), ( 6,  7,  9, 12),
     ( 1,  4,  6, 10, 15), ( 1,  4,  7, 11, 14), ( 1,  6,  7, 12, 13), ( 1,  8, 10, 11, 13), ( 1,  8, 12, 14, 15),
     ( 2,  3,  5,  9, 16), ( 2,  3,  8, 12, 13), ( 2,  5,  8, 11, 14), ( 2,  7,  9, 12, 14), ( 2,  7, 11, 13, 16),
     ( 3,  5,  8, 10, 15), ( 3,  6,  9, 12, 15), ( 3,  6, 10, 13, 16), ( 4,  5,  9, 14, 15), ( 4,  5, 10, 11, 16),
     ( 4,  6,  7,  9, 16), ( 1,  4,  6,  7, 10, 11, 13, 16), ( 2,  3,  5,  8,  9, 12, 14, 15)]

# ==============================================================================


# from a list of maximal simplices construct a list of all simplices sorted by length
def allsc(X):
    A = set(X)
    for s in X:
        n = len(s)
        for i in range(1, n):
            for p in itertools.combinations(s, i):
                A.add(p)
    A = list(A)
    A.sort(key=len)
    return A


# construct a product of two copies of X
def pr(X):
    A = []
    simp = allsc(X)
    for a in simp:
        for b in simp:
            A.append((a, b))
    A.sort()
    return A


# given a cube in the product, find its dimension
def dimcub(s, t):
    return len(s)+len(t)-2


# returns the dimension of a given simplex
def dim(s):
    return len(s)-1


# construct the cubical diagonal
def ddiag(X):
    A = []
    All = allsc(X)
    for a in All:
        A.append((a, a))
    A.sort(key=len)
    return A


# get the boundary of s
def boundary(s):
    if len(s) == 1:
        return []
    B = set()
    for b in itertools.combinations(s, len(s)-1):
        B.add(b)
    return B


# returns an open star of a given simplex s, S can be a list of all simplices
# or a list of maximal simplices
def star(s, S):
    A = allsc(S)
    st = [s]
    for a in A:
        B = boundary(a)
        B = allsc(B)
        if s in B:
            st.append(a)
    return st


def euler(Crit):
    chi = {}
    for c in Crit:
        dim = len(c)-1
        if dim in chi:
            chi[dim] += 1
        else:
            chi[dim] = 1
      
    txtfile.write("Critical simplices count by dimension:\n")
    txtfile.write(str(chi))
    txtfile.write("\n\n")

    x = 0
    for c in chi:
        if c % 2 == 0:
            x += chi[c]
        else:
            x -= chi[c]
      
    txtfile.write("Euler characteristic:\n")
    txtfile.write(str(x))


# ==============================================================================


# test if adding an arrow to the vector field creates a closed loop
def makes_loop(alpha, beta, Paths):
    p = dim(alpha)
    B = boundary(beta)
    for A in Paths:
        if dim(A[0][0]) == p:
            is_face_of = []
            is_coface_of = []
            for i in range(len(A)):
                if alpha in boundary(A[i][1]):
                    is_face_of.append(i)
                if A[i][0] in B:
                    is_coface_of.append(i)
            if is_face_of != [] and is_coface_of != [] and is_face_of[0] > is_coface_of[0]:
                return True
    return False


# ==============================================================================


# update the list of maximal paths after adding an arrow from alpha to beta
def path_update(alpha, beta, Paths):
    P = [path for path in Paths]
    p = dim(alpha)
    Bbeta = boundary(beta)
    is_face_of = []
    is_coface_of = []
  
    # go through all paths and check if the given pair fits in somewhere
    for A in Paths:
        if dim(A[0][0]) == p:
            j = Paths.index(A)
            for i in range(len(A)):
                if alpha in boundary(A[i][1]):
                    is_face_of.append((j, i))
                if A[i][0] in Bbeta:
                    is_coface_of.append((j, i))

    # if it did not, add the pair as the start of a new path
    if is_face_of == [] and is_coface_of == []:
        P.append([(alpha, beta)])
 
    if is_face_of == [] and is_coface_of != []:
        for m in range(len(is_coface_of)):
            (j, i) = is_coface_of[m]
            A = Paths[j]
            new_path = [(alpha, beta)]
            new_path += A[i:]
            if new_path not in P:
                P.append(new_path)
            if i == 0:
                P.remove(A)
             
    if is_face_of != [] and is_coface_of == []:
        for m in range(len(is_face_of)):
            (j, i) = is_face_of[m]
            A = Paths[j]
            new_path = A[:i+1]
            new_path.append((alpha, beta))
            if new_path not in P:
                P.append(new_path)
            if i == len(A)-1:
                P.remove(A)
        
    if is_face_of != [] and is_coface_of != []:
        for m in range(len(is_face_of)):
            (j, i) = is_face_of[m]
            for o in range(len(is_coface_of)):
                (k, l) = is_coface_of[o]
                A = Paths[j]
                B = Paths[k]
                new_path = A[:i+1]
                new_path.append((alpha, beta))
                new_path += B[l:]
                if new_path not in P:
                    P.append(new_path)
        
                if i == len(A)-1 and A in P:
                    P.remove(A)
                if l == 0 and B in P:
                    P.remove(B)
          
    return P


# ==============================================================================


# to print the results
# any of the variables can be set to "N/A"
def printout(Crit, Field, Paths, new=False):

    if Field != "N/A":
        if new:
            # txtfile.write("Vector field:\n")
            print "Vector field:\n"
        else:
            # txtfile.write("Updated vector field:\n")
            print "Updated vector field:\n"
        for v in Field:
            # txtfile.write(str(v)+"\n")
            print str(v)+"\n"
        # txtfile.write("\n")
        print "\n"
  
    if Paths != "N/A":
        if new:
            # txtfile.write("Paths:\n")
            print "Paths:\n"
        else:
            # txtfile.write("Updated paths:\n")
            print "Updated paths:\n"
        for p in Paths:
            # txtfile.write(str(p)+"\n")
            print str(p)+"\n"
        # txtfile.write("\n")
        print "\n"

    if Crit != "N/A":
        if new:
            # txtfile.write("Critical simplices:\n")
            print "Critical simplices:\n"
        else:
            # txtfile.write("Critical simplices after cancelling:\n")
            print "Critical simplices after cancelling:\n"
        # txtfile.write(str(Crit)+"\n\n")
        print str(Crit)+"\n\n"

# ==============================================================================


def path_flip(alpha, beta, my_path, Crit, V, name, step):

    # my_path has for q a list [(p, ib, ia, b, a),...]
    # q is a slice p[ib:ia+1] (equal for all p)

    # there should only be one q in Q
    Q = my_path.keys()
    q = Q[0]
    k = len(q)
  
    # revese the path q
    qbar = [(alpha, q[k-1][1])]
    for i in range(k-1, 0, -1):
        qbar.append((q[i][0], q[i-1][1]))
    qbar.append((q[0][0], beta))

    # keep a list of newly added arrows for plotting purposes
    NewV = []
  
    # remove old pairs from the vector field
    for pair in q:
        V.remove(pair)
    # add new pairs to the vector field
    for pair in qbar:
        V.append(pair)
        NewV.append(pair)

    # rebuild a list of maximal paths
    Paths = []
    for pair in V:
        a = pair[0]
        b = pair[1]
        Paths = path_update(a, b, Paths)

    for p in Paths:
        for pair in p:
            for e in pair:
                if e in Crit:
                    Crit.remove(e)
  
    # printout("N/A", "N/A", Paths)
  
    if name == "RP2":
        plotV(VcRP2, EcRP2, FcRP2, labelRP2, V, Crit, NewV, name, step)
    if name == "T":
        plotV(VcT, EcT, FcT, labelT, V, Crit, NewV, name, step)
    if name == "K":
        plotV(VcK, EcK, FcK, labelK, V, Crit, NewV, name, step)
    if name == "D":
        plotV(VcD, EcD, FcD, labelD, V, Crit, NewV, name, step)
    if name == "C":
        plotV(VcC, EcC, FcC, labelC, V, Crit, NewV, name, step)
    if name == "M":
        plotV(VcM, EcM, FcM, labelM, V, Crit, NewV, name, step)

    return Crit, V, Paths


# ==============================================================================


# construct a DGVF on X which is critical on the open star of s
def DGVF(X, s, name):

    random.seed(0)
    S = allsc(X)
    St = star(s, X)
  
    # all simplices in the star should be critical and will not be paired up
    Crit = St
    for c in Crit:
        S.remove(c)
    
    V = []
    Paths = []
    AllPairs = []

    # create a list of all possible pairs
    for beta in S:
        for alpha in boundary(beta):
            if alpha not in Crit:
                AllPairs.append((alpha, beta))

    # while there are any pairs left
    while AllPairs:

        # choose one remaining pair at random
        n = len(AllPairs)
        i = random.randint(0, n-1)
        (alpha, beta) = AllPairs[i]

        # if it makes a loop, remove it and try again
        if makes_loop(alpha, beta, Paths):
            AllPairs.remove((alpha, beta))

        # else, add it to the vector field and
        # remove all pairs that have a simplex in common from the list of possible pairs and
        # update the list of maximal paths
        else:
            R = set()
            for pair in AllPairs:
                if alpha == pair[0] or alpha == pair[1]:
                    R.add(pair)
            for pair in AllPairs:
                if beta == pair[0] or beta == pair[1]:
                    R.add(pair)
            for pair in R:
                AllPairs.remove(pair)

            V.append((alpha, beta))
            S.remove(alpha)
            S.remove(beta)
            Paths = path_update(alpha, beta, Paths)

    # add all simplices that did not get paired up to the list of critical simplices
    for sx in S:
        Crit.append(sx)

    printout(Crit, V, Paths, new=True)

    if name == "RP2":
        plotV(VcRP2, EcRP2, FcRP2, labelRP2, V, Crit, [], name, 0)
    if name == "T":
        plotV(VcT, EcT, FcT, labelT, V, Crit, [], name, 0)
    if name == "K":
        plotV(VcK, EcK, FcK, labelK, V, Crit, [], name, 0)
    if name == "D":
        plotV(VcD, EcD, FcD, labelD, V, Crit, [], name, 0)
    if name == "C":
        plotV(VcC, EcC, FcC, labelC, V, Crit, [], name, 0)
    if name == "M":
        plotV(VcM, EcM, FcM, labelM, V, Crit, [], name, 0)

    return Crit, V, Paths


# ==============================================================================


# given a vector field, try cancelling pairs of critical simplices to
# obtain a vector field with fewer critical cells
def cancel(X, s, V, Crit, Paths, name):

    step = 1

    # create a graded list (dictionary) of critical simplices
    GradCrit = {}
    for c in Crit:
        d = dim(c)
        if d not in GradCrit:
            GradCrit[d] = [c]
        else:
            GradCrit[d].append(c)

    # for each critical simplex find all faces and cofaces
    S = allsc(X)
    FaceCrit = {}
    CofaceCrit = {}
    for c in Crit:
        FaceCrit[c] = list(boundary(c))
        CofaceCrit[c] = []
        n = dim(c)
        for sx in S:
            if dim(sx) == n+1 and c in boundary(sx):
                CofaceCrit[c].append(sx)

    # build a list of pairs of critical simplices
    # with neighbouring dimensions (candidates for cancelling)
    # only consider pairs not contained in the star of s
    dims = GradCrit.keys()
    dims.sort()
    pairs_to_cancel = []
    St = star(s, X)
    if len(GradCrit[0]) == 1:
        dims.remove(0)
    for d in dims:
        if d+1 in dims:
            new_pairs = [(a, b) for a in GradCrit[d] for b in GradCrit[d+1] if ((a not in St and b not in St) and (a not in boundary(b)))]
            for pair in new_pairs:
                pairs_to_cancel.append(pair)

    random.seed(2)
  
    # while there are pairs to cancel left, choose one at random
    while pairs_to_cancel:
    
        m = len(pairs_to_cancel)
        i = random.randint(0, m-1)
        pair = pairs_to_cancel[i]

        # dim(alpha) = d, dim(beta) = d+1
        alpha = pair[0]
        beta = pair[1]
    
        # look at all faces and cofaces
        B = FaceCrit[beta]
        A = CofaceCrit[alpha]
    
        my_path = {}
        unique = True
    
        for b in B:
            for a in A:
                for p in Paths:
                    # if there is a path starting at b and ending in a, remember it
                    p0 = [arrow[0] for arrow in p]    # starts of arrows
                    p1 = [arrow[1] for arrow in p]    # ends of arrows
                    if b in p0 and a in p1:
                        ib = p0.index(b)
                        ia = p1.index(a)
                        if ib <= ia:
                            q = tuple(p[ib:ia+1])
                            Q = my_path.keys()
                            if Q != [] and q not in Q:
                                unique = False
                            if q in Q:
                                my_path[q].append((p, ib, ia, b, a))
                            elif my_path == {}:
                                my_path[q] = [(p, ib, ia, b, a)]
                            else:
                                unique = False
                            # if there is more than one pair, the pair cannot be cancelled, so skip it
                            if not unique:
                                break    # for p in Paths
                if not unique:
                    break    # for a in A
        
            if not unique:
                # print "removing: ", pair, "(more than one path)"
                break    # for b in B
        if my_path == {}:
            unique = False
            # print "removing: ", pair, "(no paths)"
        pairs_to_cancel.remove(pair)
        if unique:
            Crit, V, Paths = path_flip(alpha, beta, my_path, Crit, V, name, step)
            step += 1
            toRemove = []
            for p in pairs_to_cancel:
                if p[0] == alpha or p[1] == beta:
                    toRemove.append(p)
            for p in toRemove:
                pairs_to_cancel.remove(p)

        printout(Crit, "N/A", "N/A")
        print len(Crit)
    # while ends here

    txtfile.write("\nCancelling complete.\n\n")

    printout(Crit, V, Paths)

    # finally, update the list of critical simplices after cancelling
    # and the new vector field after cancelling
  
    # if name in ["RP2", "T", "K","D", "C", "M"]:
    # plt.show()

    return Crit, V, Paths
    

# ==============================================================================


def plotV(Vc, Ec, Fc, Label, V, Crit, NewV, name, step):

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    # ax.get_xaxis().set_visible(False)
    # ax.get_yaxis().set_visible(False)
    plt.axis('off')

    # plot critical triangles
    patches = []
    for f in Fc:
        if f in Crit:
            [A, B, C] = Fc[f]
            poly = Polygon(np.array([[A[0], A[1]], [B[0], B[1]], [C[0], C[1]]]), True)
            patches.append(poly)

    p = PatchCollection(patches, facecolors='#c03240', alpha=0.4)
    ax.add_collection(p)

    # plot non-critical triangles
    patches = []
    for f in Fc:
        if f not in Crit:
            [A, B, C] = Fc[f]
            poly = Polygon(np.array([[A[0], A[1]], [B[0], B[1]], [C[0], C[1]]]), True)
            patches.append(poly)

    p = PatchCollection(patches, facecolors='#ffffff', alpha=0.4)
    ax.add_collection(p)
 
    # plot edges
    for e in Ec:
        if e in Crit:
            for i in Ec[e]:
                plt.plot([i[0][0], i[1][0]], [i[0][1], i[1][1]], color='#c03240', linewidth=1.5)
        else:
            for i in Ec[e]:
                plt.plot([i[0][0], i[1][0]], [i[0][1], i[1][1]], color='#000000', linewidth=0.7)

    # plot arrows in V
    for arrow in V:
        # edge-face arrows
        if len(arrow[0]) == 2:
            f = arrow[1]
            e = arrow[0]
            ia = f.index(e[0])
            ib = f.index(e[1])
            I = [0, 1, 2]
            I.remove(ia)
            I.remove(ib)
            ic = I[0]
            coords = Fc[f]
            A = coords[ia]
            B = coords[ib]
            C = coords[ic]
            sx = (A[0]+B[0]+0.0)/2
            sy = (A[1]+B[1]+0.0)/2
            cx = C[0]
            cy = C[1]
            norm = math.sqrt((cx-sx)**2+(cy-sy)**2)
            norm *= 4
            if arrow in NewV:
                plt.arrow(sx, sy, (cx-sx)/norm, (cy-sy)/norm, width=0.002, fc='#5354a3', ec='#5354a3')
            else:
                plt.arrow(sx, sy, (cx-sx)/norm, (cy-sy)/norm, width=0.002, fc='#000000', ec='#000000')
        # vertex-edge arrows
        if len(arrow[0]) == 1:
            e = arrow[1]
            v = arrow[0]
            ia = e.index(v[0])
            I = [0, 1]
            I.remove(ia)
            ib = I[0]
            coords = Ec[e]
            for c in coords:
                A = c[ia]
                B = c[ib]
                norm = math.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2)
                norm *= 3
                if arrow in NewV:
                    plt.arrow(A[0], A[1], (B[0]-A[0])/norm, (B[1]-A[1])/norm, width=0.002, fc='#5354a3', ec='#5354a3')
                else:
                    plt.arrow(A[0], A[1], (B[0]-A[0])/norm, (B[1]-A[1])/norm, width=0.002, fc='#000000', ec='#000000')

    # plot the vertices
    for v in Vc:
        if v in Crit:
            for i in Vc[v]:
                plt.plot([i[0]], [i[1]], color='#c03240', marker='o', ms=4)
        else:
            for i in Vc[v]:
                plt.plot([i[0]], [i[1]], color='#000000', marker='o', ms=3)

    if name == "D":
        fs = 7
        delta = 0.1
    else:
        fs = 8
        delta = 0.08
      
    # plot vertex labels
    for n in Label:
        p = Label[n]
        plt.text(n[0]+p[0]*delta, n[1]+p[1]*delta, p[2], fontsize=fs, verticalalignment=p[3], horizontalalignment=p[4])

    # set the size of the plot
    if name == "K" or name == "T":
        plt.axis([0.5, 4.5, 0.5, 4.5])
    if name == "RP2":
        plt.axis([-3, 3, -0.2, 6.2])
    if name == "D":
        plt.axis([-0.5, 10.5, -0.5, 9.2])
    if name == "M" or name == "C":
        plt.axis([0, 5, 0, 3])

    myplot[step] = fig


# ==============================================================================


# for saving outputs
myplot = {}
pp = PdfPages('morse.pdf')
txtfile = open('morse.txt', 'w')

# choose the space here
X = K
name = "K"
# s = ( 2,  3,  5,  8,  9, 12, 14, 15)
s = (4, 5, 6)

Crit, V, Paths = DGVF(X, s, name)
Crit, V, Paths = cancel(X, s, V, Crit, Paths, name)
euler(Crit)

# write generated images to pdf
for i in myplot:
    pp.savefig(myplot[i], bbox_inches='tight', transparent=True, pad_inches=0)
pp.close()
txtfile.close()
print "Done."
