package main

import "fmt"

func fibo(a int) int {
	if a == 1 {
		return 1
	}
	if a == 2 {
		return 1
	}
	return fibo(a-1)  + fibo(a - 2)
	
}

func main() {
	printInt fibo(32)
}