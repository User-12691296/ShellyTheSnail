from load import load_lib
import numpy as np
from numpy.ctypeslib import ndpointer
import ctypes

# Load the C function - this code works
LIB = load_lib("./ap")

test = LIB.test_array_reshaping
test.restype = ctypes.c_int
test.argtypes = [ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"),
                 ctypes.c_int,
                 ctypes.c_int]

# Create an array
og_array = np.zeros((100, 100), dtype=np.int32)

# Splice it and make it contiguous
splice = np.ascontiguousarray(og_array[10:20, 10:20])

# Test to make sure only zeroes were passed
print("Test for zeroes:", test(splice, 10, 10))
