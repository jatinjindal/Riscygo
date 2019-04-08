package main

import "fmt"

func fibo_iter(n int) int{
	a := 0
	b := 1
	var tmp int
	for i := 0; i < n; i++ {
		
		tmp = a + b
		a = b
		b = tmp
	}
	return a
}

func main() {
	
	printInt fibo_iter(32)
}