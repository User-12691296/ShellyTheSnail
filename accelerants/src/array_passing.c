int array_index(int col, int row, int width) {
	return (col + row*width);
}

int test_array_reshaping(int* array, int width, int height) {
	int i, j;
	for (i=0; i<height; i++) {
		for (j=0; j<width; j++) {
			// If the array contains anything other than zeroes, return negative
			if (!(array[array_index(j, i, width)] == 0)) {
				return (-1);
			}
		}
	}
	// If the array is clean, return good array
	return (0);
}