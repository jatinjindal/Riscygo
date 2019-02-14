package main

import "fmt"

func pluscommon(a, b, c int) int {
	return a + b + c
}

func main() {
	res := pluscommon(1, 2, 3)
	fmt.Println("1 + 2 = ", res)
}
