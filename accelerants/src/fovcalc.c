#include <stdbool.h>
#include <math.h>
#include <stdio.h>

/* 127 - visible
   0 - hidden to range
   1 - hidden to range, adjacent to a 2
   2 - hidden to blocks
*/
#define OOR 0
#define BOR 1
#define HTB 2
#define VISIBLE 127

typedef struct
{
  int numerator;
  int denominator;
} Rational;

typedef enum {North, East, South, West} Cardinal;

typedef struct {
	Cardinal cardinal;
	int ox;
	int oy;
} Quadrant;

typedef struct {
	int x;
	int y;
} vec2;

typedef struct {
	int depth;
	Rational start_slope;
	Rational end_slope;
} Row;

#include "fovcalc.h"

void reduce(Rational *inrat, Rational *outrat) {
  int a, b, rem;

  if (inrat->numerator > inrat->denominator)
  {
    a = inrat->numerator;
    b = inrat->denominator;
  }
  else
  {
    a = inrat->denominator;
    b = inrat->numerator;
  }

  while (b != 0)
  {
    rem = a % b;
    a = b;
    b = rem;
  }

  outrat->numerator = inrat->numerator / a;
  outrat->denominator = inrat->denominator / a;
}

Rational multiply(Rational a, int b) {
	Rational out = {a.numerator * b, a.denominator};
	return (out);
}

int int_larger_than_rational(int b, Rational a) {
	int num = b*a.denominator;
	
	if (num > a.numerator) {
		return 1;
	} else if (num == a.numerator) {
		return 0;
	} else {
		return -1;
	}
}

float numerize(Rational a) {
	return (1.0f * a.numerator/a.denominator);
}

vec2 transform_quadrant(Quadrant q, int depth, int col) {
	vec2 v;
	
	if (q.cardinal == North) {
		v.x = q.ox + col;
		v.y = q.oy - depth;
	} 
	else if (q.cardinal == South) {
		v.x = q.ox - col;
		v.y = q.oy + depth;
	} 
	else if (q.cardinal == East) {
		v.x = q.ox + depth;
		v.y = q.oy + col;
	} 
	else if (q.cardinal == West) {
		v.x = q.ox - depth;
		v.y = q.oy - col;
	}
	
	//printf("in: %d; %d, %d, %d, %d || out: %d, %d\n", q.cardinal, depth, col, q.ox, q.oy, v.x, v.y);
	
	return (v);
}

Rational slope(int depth, int col) {
	Rational s = {2 * col - 1, 2 * depth};
	return (s);
}

bool is_symmetric(Row row, int col) {
	return ((int_larger_than_rational(col, multiply(row.start_slope, row.depth)) >= 0)
		&& (int_larger_than_rational(col, multiply(row.end_slope, row.depth)) <= 0));
}

int round_ties_up(float n) {
	return ((int) n + 0.5f);
}

int round_rational_down(Rational inrat) {
	Rational b;
	
	reduce(&inrat, &b);
	
	// Tie
	if (((b.numerator%2) == 1) && (b.denominator == 2)) {
		return (b.numerator / b.denominator);
	}
	// Above half
	else if (((b.numerator % b.denominator) * 2) > b.denominator) {
		return (b.numerator / b.denominator);
	}
	// Below half
	else if (((b.numerator % b.denominator) * 2) < b.denominator) {
		return (b.numerator / b.denominator);
	}
}

int floorRat(Rational inrat) {
	return (inrat.numerator/inrat.denominator);
}

int round_rational_up(Rational inrat) {
	Rational b;
	
	reduce(&inrat, &b);
	
	// Whole number
	if (b.denominator == 1) {
		return (b.numerator);
	}
	// Tie
	else if (((b.numerator%2) == 1) && (b.denominator == 2)) {
		return (b.numerator / b.denominator)+1;
	}
	// Above half
	else if (((b.numerator % b.denominator) * 2) > b.denominator) {
		return (b.numerator / b.denominator)+1;
	}
	// Below half
	else if (((b.numerator % b.denominator) * 2) < b.denominator) {
		return (b.numerator / b.denominator);
	}
}

int round_ties_down(float n) {
	if (n <= 0.5f) {
		return ((int) n);
	} else {
		return ((int) n + 1);
	}
}

Row next_row(Row row) {
	Row nr;
	nr.depth = row.depth + 1;
	nr.start_slope = row.start_slope;
	nr.end_slope = row.end_slope;
	return (nr);
}

int min_col(Row row) {
	return (round_rational_down(multiply(row.start_slope, row.depth)));
}
int max_col(Row row) {
	return (round_rational_down(multiply(row.end_slope, row.depth)));
}

int array_index (int x, int y, int max_width) {
	if (x == -1 || y == -1) {
		return (-1);
	}
	return (y * max_width + x);
}

int square(int n) {
	return (n*n);
}

bool tileOOR (int ox, int oy, int x, int y, int max_width, int max_height, int range) {
	if (square(ox - x) + square(oy - y) >= range) {
		return true;
	}
	
	return false;
}

bool tileOOB (Quadrant q, int x, int y, int max_width, int max_height, int range) {
	if (x < 0 || x >= max_width) {
		return true;
	}
	if (y < 0 || y >= max_height) {
		return true;
	}
	
	return false;
}

void calcFOV(int ox, int oy, const bool* obstacles, int max_width, int max_height, char* shown_tiles, int range) {
	size_t i, j, qi;
	int max_index = array_index(max_width-1, max_height-1, max_width);
	Rational a, b;
	Row first_row;
	
	// Hide all
	for (i=0; i<max_height; ++i) {
		for (j=0; j<max_width; ++j) {
			if (tileOOR(ox, oy, j, i, max_width, max_height, range)) {
				shown_tiles[array_index(j, i, max_width)] = OOR;
			} else {
				shown_tiles[array_index(j, i, max_width)] = HTB;
			}
		}
	}

	shown_tiles[array_index(ox, oy, max_width)] = 127;
	
	for (qi=0; qi<4; ++qi) {
		Quadrant quadrant = {qi, ox, oy};
		
		a.numerator = -1;
		a.denominator = 1;
		b.numerator = 1;
		b.denominator = 1;
		
		first_row.depth = 1;
		first_row.start_slope = a;
		first_row.end_slope = b;
		
		scan(quadrant, first_row, obstacles, max_width, max_height, shown_tiles, range);
	}
	
	for (i=0; i<max_height; ++i) {
		for (j=0; j<max_width; ++j) {
			if (shown_tiles[array_index(j, i, max_width)] == OOR && is_adjacent_tile_hidden(j, i, max_width, max_height, shown_tiles)) {
				shown_tiles[array_index(j, i, max_width)] = BOR;
			}
		}
	}
}

bool is_wall(int index, const bool* obstacles) {
	if (index == -1) {
		return false;
	}
	
	return (obstacles[index]);
}

bool is_floor(int index, const bool* obstacles) {
	if (index == -1) {
		return false;
	}
	
	return (!obstacles[index]);
}

char get_tile_value(int x, int y, int max_width, int max_height, char* shown_tiles, char null) {
	if (x<0 || y<0) {
		return null;
	}
	else if (x>=max_width || y>=max_height) {
		return null;
	}
	return shown_tiles[array_index(x, y, max_width)];
}

bool is_adjacent_tile_hidden(int x, int y, int max_width, int max_height, char* shown_tiles) {
	int nbrsX[] = {0, -1, 0, 1, -1, 1, -1, 1};
	int nbrsY[] = {-1, 0, 1, 0, -1, -1, 1, 1};
	
	//printf("Searching tile %d, %d for border special case\n", x, y);
	
	int i, cx, cy;
	char value;
	for (i=0; i<8; i++) {
		cx = x + nbrsX[i];
		cy = y + nbrsY[i];
		
		value = get_tile_value(cx, cy, max_width, max_height, shown_tiles, OOR);
		
		//printf("Scanning (%d, %d), %d - ", cx, cy, value);
		
		if (value == HTB) {
			return true;
		}
		//printf("\n");
	}
	
	return false;
}

void scan(Quadrant quadrant, Row row, const bool* obstacles, int max_width, int max_height, char* shown_tiles, int range) {	
	int pretx = -1;
	int prety = -1;
	
	int minc = min_col(row);
	int maxc = max_col(row);
	
	int index, pindex;
	vec2 cur;
	
	//printf("\nScanning Q%d MN%d to MX%d with depth %d\n", quadrant.cardinal, minc, maxc, row.depth);
	//printf("Slopes start %d/%d - end %d/%d\n", row.start_slope.numerator, row.start_slope.denominator, row.end_slope.numerator, row.end_slope.denominator);
	Row nr;
	for (int col=minc; col <= maxc; col++) {
		cur = transform_quadrant(quadrant, row.depth, col);
		index = array_index(cur.x, cur.y, max_width);
		pindex = array_index(pretx, prety, max_width);
		
		//printf("Pos %d, %d\n", cur.x, cur.y);
		//printf("Scanning q%d, row%d, col%d\n", quadrant.cardinal, row.depth, col);
		//printf("Slope to current: %d/%d\n", slope(row.depth, col).numerator, slope(row.depth, col).denominator);
		
		if (tileOOB(quadrant, cur.x, cur.y, max_width, max_height, range)) {
			continue;
		}
		if (tileOOR(quadrant.ox, quadrant.oy, cur.x, cur.y, max_width, max_height, range)) {
			continue;
		}
		
		if (is_wall(index, obstacles) || is_symmetric(row, col)) {
			shown_tiles[index] = VISIBLE;
		}
		
		if (is_wall(pindex, obstacles) && is_floor(index, obstacles)) {
			//printf("Hit wall at col, %d", col);
			row.start_slope = slope(row.depth, col);
		}
		
		if (is_floor(pindex, obstacles) && is_wall(index, obstacles)) {
			nr = next_row(row);
			nr.end_slope = slope(row.depth, col);
			scan(quadrant, nr, obstacles, max_width, max_height, shown_tiles, range);
		}
		
		pretx = cur.x;
		prety = cur.y;
	}
	
	pindex = array_index(pretx, prety, max_width);
	if (is_floor (pindex, obstacles)) {
		scan(quadrant, next_row(row), obstacles, max_width, max_height, shown_tiles, range);
	}
}

void print_array(const char* shown_tiles, bool*obstacles, int max_width, int max_height, int x, int y) {
	for (int row=0; row<max_height; row++) {
		for (int col=0; col<max_width; col++) {
			int tile_val = shown_tiles[array_index(col, row, max_width)];
			
			if ((col == x) && (row == y)) {
				printf("O");
			} else if (tile_val == VISIBLE) {
				if (is_wall(array_index(col, row, max_width), obstacles)) {
					printf("#");
				}
				else {
					printf("+");
				}
			} else if (tile_val == HTB) {
				printf("H");
			} else if (tile_val == BOR) {
				printf("B");
			} else if (tile_val == OOR) {
				printf("R");
			}
			
			printf(", ");
		}
		printf("\n");
	}
}

void main() {
	int max_width = 10, max_height = 10;
	int length = max_width*max_height;
	bool obstacles[length];
	char shown_tiles[length];
	
	for (int i=0; i<length; i++) {
		obstacles[i] = 0;
	}
	/* obstacles[10] = true;
	obstacles[20] = true;
	obstacles[30] = true;
	obstacles[40] = true;
	obstacles[50] = true;
	obstacles[60] = true;
	obstacles[70] = true;
	obstacles[80] = true;
	obstacles[90] = true; */
	
	/* obstacles[26] = true;
	obstacles[36] = true;
	obstacles[46] = true;
	obstacles[56] = true;
	obstacles[66] = true;
	obstacles[76] = true;
	obstacles[86] = true;
	obstacles[96] = true; */
	
	int ox = 8, oy = 3;
	
	calcFOV(ox, oy, obstacles, max_width, max_height, shown_tiles, 144);
	
	print_array(shown_tiles, obstacles, max_width, max_height, ox, oy);
}