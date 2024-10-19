import ctypes, ctypes.util

# Find the library and load it
def load_lib(lib_name):
    path = ctypes.util.find_library(lib_name)
    if not path:
        return None

    try:
        lib = ctypes.CDLL(path)
    except OSError as err:
        return None

    return lib


