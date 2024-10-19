/* typedef struct Node {
	int x, y;
	int g, h, f;
	struct Node *parent
} Node; */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <float.h>
#include <limits.h>

#define ROW 5
#define COL 5

typedef struct {
	int x, y;
	int parent_x, parent_y;
	int f, g, h;
} Node;

int max(int a, int b) {
	if (a > b) {
		return a;
	}
	return b;
}

int isValid(int row, int col) {
    return (row >= 0) && (row < ROW) && (col >= 0) && (col < COL);
}

int isUnBlocked(int grid[][COL], int row, int col) {
    return grid[row][col] == 1;
}

int isDestination(int row, int col, int dest_row, int dest_col) {
    return row == dest_row && col == dest_col;
}

int calculateHValue(int row, int col, int dest_row, int dest_col) {
    return (max(abs(row - dest_row), abs(col - dest_col)));
}
// Function to trace the path from the source to destination
void tracePath(Node nodeDetails[][COL], int dest_row, int dest_col) {
    printf("\nThe path is ");
    int row = dest_row;
    int col = dest_col;
    while (!(nodeDetails[row][col].parent_x == row && nodeDetails[row][col].parent_y == col)) {
        printf("-> (%d,%d) ", row, col);
        int temp_row = nodeDetails[row][col].parent_x;
        int temp_col = nodeDetails[row][col].parent_y;
        row = temp_row;
        col = temp_col;
    }
    printf("-> (%d,%d)\n", row, col);
}
// A* Search Algorithm
void aStarSearch(int grid[][COL], int src_row, int src_col, int dest_row, int dest_col) {
    // If the source or destination is out of range
    if (!isValid(src_row, src_col) || !isValid(dest_row, dest_col)) {
        printf("Source or destination is invalid\n");
        return;
    }
    // If the source or destination cell is blocked
    if (!isUnBlocked(grid, src_row, src_col) || !isUnBlocked(grid, dest_row, dest_col)) {
        printf("Source or destination is blocked\n");
        return;
    }
    // If the destination cell is the same as source cell
    if (isDestination(src_row, src_col, dest_row, dest_col)) {
        printf("We are already at the destination\n");
        return;
    }
    // Initialize closed list and open list
    int closedList[ROW][COL];
    Node nodeDetails[ROW][COL];
    for (int i = 0; i < ROW; i++) {
        for (int j = 0; j < COL; j++) {
            closedList[i][j] = 0;
            nodeDetails[i][j].f = INT_MAX;
            nodeDetails[i][j].g = INT_MAX;
            nodeDetails[i][j].h = INT_MAX;
            nodeDetails[i][j].parent_x = -1;
            nodeDetails[i][j].parent_y = -1;
			nodeDetails[i][j].x = -1;
            nodeDetails[i][j].y = -1;
        }
    }
    // Initialize the start node
    int row = src_row;
    int col = src_col;
    nodeDetails[row][col].f = 0.0;
    nodeDetails[row][col].g = 0.0;
    nodeDetails[row][col].h = 0;
    nodeDetails[row][col].x = col;
    nodeDetails[row][col].y = row;
    // Declare a list to hold open nodes
    // This can be implemented as a priority queue for better performance
    Node openList[ROW * COL];
    int openListSize = 0;
    openList[openListSize++] = nodeDetails[row][col];
    // Loop until the destination is found
    int foundDest = 0;
    while (openListSize > 0) {
        // Find the node with the least f value
        int minF = INT_MAX;
        int minIndex = -1;
        for (int i = 0; i < openListSize; i++) {
            if (openList[i].f < minF) {
                minF = openList[i].f;
                minIndex = i;
            }
        }
        // Remove the node from open list and add to closed list
		Node current = openList[minIndex];
        row = current.y;
        col = current.x;
		printf ("#Scanning node %d, %d, %d, %d, %d\n", col, row, current.f, current.h, current.g);
        openList[minIndex] = openList[--openListSize];
        closedList[row][col] = 1;
        // Generate the 8 successor nodes
        int rowNum[] = {-1, 0, 1, 0, -1, -1, 1, 1};
        int colNum[] = {0, -1, 0, 1, -1, 1, -1, 1};
        for (int i = 0; i < 8; i++) {
            int newRow = row + rowNum[i];
            int newCol = col + colNum[i];
            if (isValid(newRow, newCol)) {
				printf ("Scanning subnode %d, %d, H:%d\n", newCol, newRow, calculateHValue(newRow, newCol, dest_row, dest_col));
                // If the destination cell is reached
                if (isDestination(newRow, newCol, dest_row, dest_col)) {
                    nodeDetails[newRow][newCol].parent_x = col;
                    nodeDetails[newRow][newCol].parent_y = row;
                    printf("The destination cell is found\n");
                    tracePath(nodeDetails, dest_row, dest_col);
                    foundDest = 1;
                    return;
                }
				
                // If the successor is not in closed list and is an unblocked cell
                else if (closedList[newRow][newCol] == 0 && isUnBlocked(grid, newRow, newCol)) {
                    int gNew = current.g + 1.0;
                    int hNew = calculateHValue(newRow, newCol, dest_row, dest_col);
                    int fNew = gNew + hNew;
                    // If it isn't in the open list or has a lower f value
                    if (nodeDetails[newRow][newCol].f == FLT_MAX || nodeDetails[newRow][newCol].f > fNew) {
                        printf("Adding node to open list: F:%d, G:%d, H:%d, X:%d, Y:%d\n", fNew, gNew, hNew, newCol, newRow);
						openList[openListSize++] = nodeDetails[newRow][newCol];
                        nodeDetails[newRow][newCol].f = fNew;
                        nodeDetails[newRow][newCol].g = gNew;
                        nodeDetails[newRow][newCol].h = hNew;
                        nodeDetails[newRow][newCol].parent_x = col;
                        nodeDetails[newRow][newCol].parent_y = row;
						nodeDetails[newRow][newCol].x = newCol;
						nodeDetails[newRow][newCol].y = newRow;
                    }
                }
            }
        }
    }
    if (!foundDest) {
        printf("Failed to find the destination cell\n");
    }
    return;
}
int main() {
    // Grid representation where 1 is an open cell and 0 is a blocked cell
    int grid[ROW][COL] =
        {
            {1, 1, 1, 1, 1},
            {1, 1, 0, 1, 1},
            {1, 1, 1, 0, 1},
            {1, 0, 1, 1, 1},
            {1, 1, 1, 1, 1}};
    // Source and destination coordinates
    int src_row = 0, src_col = 0;
    int dest_row = 2, dest_col = 1;
    aStarSearch(grid, src_row, src_col, dest_row, dest_col);
    return 0;
}