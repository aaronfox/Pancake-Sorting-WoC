// C program to 
// sort array using 
// pancake sort 
#include <stdlib.h> 
#include <stdio.h> 

int flips = 0;
/* Reverses arr[0..i] */
void flip(int arr[], int i) 
{ 
	int temp, start = 0; 
	while (start < i) 
	{ 
		temp = arr[start]; 
		arr[start] = arr[i]; 
		arr[i] = temp; 
		start++; 
		i--; 
	} 
} 

// Returns index of the 
// maximum element in 
// arr[0..n-1] 
int findMax(int arr[], int n) 
{ 
int mi, i; 
for (mi = 0, i = 0; i < n; ++i) 
	if (arr[i] > arr[mi]) 
			mi = i; 
return mi; 
} 

// The main function that 
// sorts given array using 
// flip operations 
int pancakeSort(int *arr, int n) 
{ 
	// Start from the complete 
	// array and one by one 
	// reduce current size 
	// by one 
	for (int curr_size = n; curr_size > 1; --curr_size) 
	{ 
		// Find index of the 
		// maximum element in 
		// arr[0..curr_size-1] 
		int mi = findMax(arr, curr_size); 

		// Move the maximum 
		// element to end of 
		// current array if 
		// it's not already 
		// at the end 
		if (mi != curr_size-1) 
		{ 
			// To move at the end, 
			// first move maximum 
			// number to beginning 
			flip(arr, mi); 
          flips++;

			// Now move the maximum 
			// number to end by 
			// reversing current array 
			flip(arr, curr_size-1); 
          flips++;
		} 
	} 
} 

// A utility function to print 
// n array of size n 
void printArray(int arr[], int n) 
{ 
	for (int i = 0; i < n; ++i) 
		printf("%d ", arr[i]); 
} 

// Driver program to test above function 
int main() 
{ 
	//int arr[] = {23, 10, 20, 11, 12, 6, 7, 3, 12, 16, 38, 51, 52, 66, 71, 72, 76, 79, 85, 56}; 
        int arr[] = {99, 78, 72, 20, 36, 10, 17, 26, 57, 61, 29, 94, 77, 21, 60, 87, 27, 67, 76, 37, 51, 43, 49, 88, 14, 90, 91, 22, 85, 58, 16, 73, 97, 63, 75, 41, 11, 19, 69, 1, 79, 74, 56, 80, 4};
	int n = sizeof(arr)/sizeof(arr[0]); 

	pancakeSort(arr, n); 
  printf("flips == %d\n", flips);
  printf("size of array == %d\n", sizeof(arr)/sizeof(*arr));

	puts("Sorted Array "); 
	printArray(arr, n); 

	return 0; 
} 
