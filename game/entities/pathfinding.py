from accelerants import aStarSearch
import numpy as np
from queue import SimpleQueue, Empty

MAX_PATH_LENGTH = 400

class PathFinder:
    def __init__(self, map_size, stop_range):
        self.map_size = map_size
        self.stop_range = stop_range

        self.path = SimpleQueue()

        self.tempx = np.empty(MAX_PATH_LENGTH, dtype=np.int32)
        self.tempy = np.empty(MAX_PATH_LENGTH, dtype=np.int32)

    def setOpaques(self, array):
        self.opaques = array

    def genOpaquesFromElevCutoff(self, elevs, cutoff):
        self.setOpaques(elevs > cutoff)

    def extendPath(self, path):
        for node in path:
            self.addPathNode(node)

    def addPathNode(self, node):
        self.path.put(node)

    def clearPath(self):
        self.path = SimpleQueue()

    def getNode(self):
        try:
            return self.path.get(False)
        except Empty:
            return None

    def extendPathFromXY(self, pathx, pathy, x, y, length):
        # Back to front add nodes
        for i in range(length):
            index = length - i - 1
            node = (pathx[index]+x, pathy[index]+y)
            self.addPathNode(node)


    def calcPath(self, start, end):
        left = min(start[0], end[0])
        top = min(start[1], end[1])

        right = max(start[0], end[0]) + 1
        bottom = max(start[1], end[1]) + 1

        if left < 0 or top < 0 or right >= self.map_size[0] or bottom >= self.map_size[1]:
            return

        ops = np.ascontiguousarray(self.opaques[top:bottom, left:right], dtype=np.int32)
        
        length = aStarSearch(ops,
                             start[0]-left, start[1]-top,
                             end[0]-left, end[1]-top,
                             right-left, bottom-top,
                             self.stop_range,
                             self.tempx, self.tempy)

        self.clearPath()
        self.extendPathFromXY(self.tempx, self.tempy, left, top, length)

    
