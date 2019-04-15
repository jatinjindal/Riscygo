package main;
import "fmt";

func b_search(ar [10]int, key int, start int, end int) int {
	if end >= start {
		var mid int
		mid = (start + end) / 2
		if ar[mid] == key {
			return mid
		}
		if ar[mid] > key {
			return b_search(ar, key, start, mid - 1)
		}
		return b_search(ar, key, mid + 1, end)
	}
	return -1
}

func main(){
	var ar [10]int

	for k := 0; k < 10; k++ {
		ar[k] = k
	}
	printInt b_search(ar, 7, 0, 9)
}
