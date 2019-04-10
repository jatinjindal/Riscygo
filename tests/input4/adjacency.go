package main

import "fmt"

type adj struct {
	a int
	b *adj
}

func main() {
	var str [10]*adj
	var ptr *adj

	for i := 0; i < 10; i++ {
		str[i] = malloc(8)
		ptr = str[i]

		for j := 0; j < 10; j++ {
			ptr.a = 10 + i*10 + j
			ptr.b = malloc(8)
			ptr = ptr.b
		}
	}

	for i := 0; i < 10; i++ {
		ptr = str[i]
		for j := 0; j < 10; j++ {
			printInt ptr.a
			printStr " "
			ptr = ptr.b
		}
		printStr "\n"
	}
}