#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <float.h>
#include <limits.h>

typedef struct Node {
	int x, y;
	int f, g, h;
	int px, py;
} Node;

int max(int a, int b) {
	if (a > b) {
		return a;
	}
	return b;
}

int array_index (int col, int row, int max_width) {
	return (row * max_width + col);
}

int isValid(int col, int row, int max_width, int max_height) {
    return (row >= 0) && (row < max_height) && (col >= 0) && (col < max_width);
}

int isUnblocked(int grid[], int col, int row, int max_width) {
    return grid[array_index(col, row, max_width)] == 0;
}

int getUnblocked(int grid[], int col, int row, int max_width) {
    return grid[array_index(col, row, max_width)];
}

int isDestination(int col, int row, int dCol, int dRow) {
    return row == dRow && col == dCol;
}

int square(int n) {
	return n*n;
}

int diagonalDist(int col, int row, int dCol, int dRow) {
	return max(abs(row - dRow), abs(col - dCol));
}

int calculateHValue(int col, int row, int dCol, int dRow) {
    return square(diagonalDist(col, row, dCol, dRow));
}

void tracePath(Node nodes[], int dCol, int dRow, int sCol, int sRow, int max_width) {
	printf("Path is");
	
	Node current = nodes[array_index(dCol, dRow, max_width)];
	
	int i=0;
	
	while (!(current.x == sCol && current.y == sRow) && i<1000) {
		printf(" <- (%d, %d)", current.x, current.y);
		
		current = nodes[array_index(current.px, current.py, max_width)];
		
		i++;
	}
	
	printf(" <- (%d, %d)\n", current.x, current.y);
}

int returnPath(Node nodes[], int sCol, int sRow, int dCol, int dRow, int max_width, int stop_range, int* pathNodesX, int* pathNodesY) {
	int length = 0;
	
	Node current = nodes[array_index(dCol, dRow, max_width)];
	
	int outside_range = 0;
	
	while (!(current.x == sCol && current.y == sRow) && length < 1000) {
		if (diagonalDist(current.x, current.y, dCol, dRow) > stop_range) {
			outside_range = 1;
		}
		// When outside stopping range, add nodes
		if (outside_range) {
			pathNodesX[length] = current.x;
			pathNodesY[length] = current.y;
			
			length ++;
		}
		current = nodes[array_index(current.px, current.py, max_width)];
	}
	
	return (length);
}

int aStarSearch(int* grid, int sCol, int sRow, int dCol, int dRow, int max_width, int max_height, int stop_range, int* pathNodesX, int* pathNodesY) {
	// If the source or destination is out of range
    if (!isValid(sCol, sRow, max_width, max_height) || !isValid(dCol, dRow, max_width, max_height)) {
        return (-2);
    }
    // If the source or destination cell is blocked
    if (!isUnblocked(grid, sCol, sRow, max_width) || !isUnblocked(grid, dCol, dRow, max_width)) {
        return (-3);
    }
    // If the destination cell is the same as source cell
    if (isDestination(sCol, sRow, dCol, dRow)) {
        return (-4);
    }
	
	int map_size = max_height*max_width;
	
	Node* nodes = malloc(map_size * sizeof(Node));
	
	Node* openList = malloc(map_size * sizeof(Node));
	int openListSize = 0;
	
	int* closedList = malloc(map_size * sizeof(int));
	
	// Initialise array
	int index;
	for (int i=0; i<max_width; i++) {
		for (int j=0; j<max_height; j++) {
			index = array_index(i, j, max_width);
			closedList[index] = 0;
			
			nodes[index].x = i;
			nodes[index].y = j;
			
			nodes[index].f = INT_MAX;
			nodes[index].g = INT_MAX;
			nodes[index].h = INT_MAX;
		}
	}
	
	// Start node
	int col = sCol;
	int row = sRow;
	index = array_index(col, row, max_width);
	nodes[index].g = 0;
	nodes[index].h = calculateHValue(col, row, sCol, sRow);
	nodes[index].f = nodes[index].g + nodes[index].h;
	openList[openListSize++] = nodes[index];
	
	// Loop until destination found
	int found = 0;
	while (openListSize > 0) {
		// Get the node with lowest f
		int minF = INT_MAX;
		int minIndex = -1;
		for (int i=0; i<openListSize; i++) {
			if (openList[i].f < minF) {
				minF = openList[i].f;
				minIndex = i;
			}
		}
		
		// Make it the current node and remove it from future checks
		Node current = openList[minIndex];
		col = current.x;
		row = current.y;
		index = array_index(col, row, max_width);
		
		openList[minIndex] = openList[--openListSize];
		closedList[index] = 1;
		
		//if (!(col==sCol && row==sRow)){
		//	printf("Lowest tile is (%d, %d) P (%d, %d)\n", col, row, current.parent -> x, current.parent -> y);
		//}
		
		if (isDestination(col, row, dCol, dRow)) {
			free(openList);
			free(closedList);
			found = 1;
			return returnPath(nodes, sCol, sRow, dCol, dRow, max_width, stop_range, pathNodesX, pathNodesY);
		}
		
		// Loop through all neighbors
		int nbrsX[] = {0, -1, 0, 1, -1, 1, -1, 1};
		int nbrsY[] = {-1, 0, 1, 0, -1, -1, 1, 1};
		int nbrIndex;
		for (int i=0; i<8; i++) {
			int nbrCol = col + nbrsX[i];
			int nbrRow = row + nbrsY[i];
			nbrIndex = array_index(nbrCol, nbrRow, max_width);
			
			//printf("Scanning nbr (%d, %d)\n", nbrCol, nbrRow);
			
			// If tile is on the map
			if (isValid(nbrCol, nbrRow, max_width, max_height)) {				
				if (closedList[nbrIndex] == 0 && isUnblocked(grid, nbrCol, nbrRow, max_width)) {
					int gNew = current.g + 1.0;
					int hNew = calculateHValue(nbrCol, nbrRow, dCol, dRow);
					int fNew = gNew + hNew;
					
					if (fNew < nodes[nbrIndex].f) {
						nodes[nbrIndex].px = col;
						nodes[nbrIndex].py = row;
						nodes[nbrIndex].g = gNew;
						nodes[nbrIndex].h = hNew;
						nodes[nbrIndex].f = fNew;
						openList[openListSize++] = nodes[nbrIndex];
					}
				}
			}
		}
	}
	
	free(nodes);
	free(openList);
	free(closedList);
	
	if (!found) {
		// Not found
		return (-1);
	}
}

int main() {
    // Grid representation where 0 is an unblocked cell and 1 is a blocked cell
    int grid[5*5] =
        {
			0, 0, 0, 0, 0,
			1, 1, 1, 1, 0,
			0, 0, 0, 0, 0,
			0, 0, 0, 0, 0,
			0, 0, 0, 0, 0,
	};
    // Source and destination coordinates
    int sCol = 1, sRow = 0;
    int dCol = 0, dRow = 4;
	
	int pathX[1000];
	int pathY[1000];
	
    int length = aStarSearch(grid, sCol, sRow, dCol, dRow, 5, 5, 1, pathX, pathY);
	
	printf("%d\n", length);
	
	for (int i=0; i<length; i++) {
		printf("(%d, %d)-", pathX[i], pathY[i]);
	}
	printf("\n");
    return 0;
}
