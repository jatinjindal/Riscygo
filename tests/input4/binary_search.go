package main;
import "fmt";

func b_search(ar [10]int,key int,start int,end int) int {
	// printInt ar[0]
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
	// ar[0]=2
	// printInt ar[0]
	var br[1]int
	br[0]=0
	for k := 0; k < 10; k++ {
		ar[k] = k
	}
	 printInt b_search(ar,7,br[0],9)
	// printInt ar[0]
}
