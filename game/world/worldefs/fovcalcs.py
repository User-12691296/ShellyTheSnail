from fractions import Fraction
import numpy as np

import accelerants as ACCEL

def slope(tile):
    row_depth, col = tile
    return Fraction(2 * col - 1, 2 * row_depth)


def is_symmetric(row, tile):
    return (tile[1] >= row.depth * row.start_slope
            and tile[1] <= row.depth * row.end_slope)


def round_ties_up(n):
    return int(n+0.5)


def round_ties_down(n):
    return int(-((n-0.5)//-1))


class Quadrant:
    north = 0
    east = 1
    south = 2
    west = 3
    def __init__(self, cardinal, origin):
        self.cardinal = cardinal
        self.ox, self.oy = origin

    def transform(self, tile):
        row, col = tile
        if self.cardinal == self.north:
            return (self.ox + col, self.oy - row)

        if self.cardinal == self.south:
            return (self.ox - col, self.oy + row)

        if self.cardinal == self.east:
            return (self.ox + row, self.oy + col)

        if self.cardinal == self.west:
            return (self.ox - row, self.oy - col)
        

class Row:
    def __init__(self, depth, start_slope, end_slope):
        self.depth = depth
        self.start_slope = start_slope
        self.end_slope = end_slope

    def tiles(self):
        min_col = round_ties_down(self.depth * self.start_slope)
        max_col = round_ties_down(self.depth * self.end_slope)

        for col in range(min_col, max_col+1):
            yield (self.depth, col)


    def next(self):
        return Row(
            self.depth + 1,
            self.start_slope,
            self.end_slope)

# 127 - shown
# 1 - hidden to tiles
# 0 - hidden to range

class FOVCalculator:
    def __init__(self, map_size, shown_tiles, range=12):
        self.map_size = map_size
        self.shown_tiles = shown_tiles
        self.range = range**2

    def setOpaques(self, array):
        self.opaques = array

    def setRange(self, range):
        self.range = range**2

    def genOpaquesFromElevCutoff(self, elevs, cutoff):
        self.setOpaques(elevs > cutoff)

    def showTile(self, tile):
        self.shown_tiles[tile[1]][tile[0]] = 127

    def hideAllTiles(self):
        self.shown_tiles.fill(0)

    def isTileOpaque(self, tile):
        return self.opaques[tile[1]][tile[0]]

    def calcFOV(self, origin):
        if ACCEL.calcFOV:
            self.calcFOVaccel(origin)

        else:
            self.calcFOVstd(origin)

    def calcFOVaccel(self, origin):
        ACCEL.calcFOV(origin[0], origin[1], self.opaques, self.map_size[0], self.map_size[1], self.shown_tiles, self.range)

    def calcFOVstd(self, origin):
        self.hideAllTiles()

        for i in range(4):
            quadrant = Quadrant(i, origin)

            def isTileOutOfBounds(tile):
                x, y = quadrant.transform(tile)

                if (origin[0]-x)**2 + (origin[1]-y)**2 >= self.range:
                    return True
                
                if x < 0 or x >= self.map_size[0]:
                    return True
                if y < 0 or y >= self.map_size[1]:
                    return True
                
                return False
            
            def reveal(tile):
                x, y = quadrant.transform(tile)
                self.showTile((x, y))

            def is_wall(tile):
                if tile is None:
                    return False

                x, y = quadrant.transform(tile)
                return self.isTileOpaque((x, y))

            def is_floor(tile):
                if tile is None:
                    return False

                x, y = quadrant.transform(tile)
                return not self.isTileOpaque((x, y))
            
            def scan(row):
                rows = [row]
                while rows:
                    row = rows.pop()
                    prev_tile = None
                    for tile in row.tiles():
                        if isTileOutOfBounds(tile):
                            continue
                        
                        if is_wall(tile) or is_symmetric(row, tile):
                            reveal(tile)

                        if is_wall(prev_tile) and is_floor(tile):
                            row.start_slope = slope(tile)

                        if is_floor(prev_tile) and is_wall(tile):
                            next_row = row.next()
                            next_row.end_slope = slope(tile)
                            rows.append(next_row)

                        prev_tile = tile

                    if is_floor(prev_tile):
                        rows.append(row.next())

            first_row = Row(1, Fraction(-1), Fraction(1))
            scan(first_row)
