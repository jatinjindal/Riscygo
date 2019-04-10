
package main

import "fmt"

func arglist(a int, b int, c int, d int, e int, f int, g int, h int) {
	printInt a
	printStr "\n"
	printInt b
	printStr "\n"
	printInt c
	printStr "\n"
	printInt d
	printStr "\n"
	printInt e
	printStr "\n"
	printInt f
	printStr "\n"
	printInt g
	printStr "\n"
	printInt h
	printStr "\n"
}

func main() {
	arglist(1, 2, 3, 4, 5, 6, 7, 8)
}