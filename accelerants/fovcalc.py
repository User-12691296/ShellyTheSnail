import ctypes
from .load import load_lib
from numpy.ctypeslib import ndpointer
import os

LIB = load_lib(os.path.join(os.path.dirname(__file__), "fovcalc"))

if LIB != None:
    calcFOV = LIB.calcFOV
    calcFOV.restype = None
    calcFOV.argtypes = [ctypes.c_int,
                           ctypes.c_int,
                           ndpointer(ctypes.c_bool, flags="C_CONTIGUOUS"),
                           ctypes.c_int,
                           ctypes.c_int,
                           ndpointer(ctypes.c_int8, flags="C_CONTIGUOUS"),
                           ctypes.c_int]
else:
    calcFOV = None
