package main

import "fmt"

type ll struct {
	a    int
	next *ll
}

func main() {
	var a1 ll
	var a2 ll
	var a3 ll
	var a4 ll
	var head *ll

	a1.a = 1
	a2.a = 2
	a3.a = 3
	a4.a = 4

	a1.next = &a2
	a2.next = &a3
	a3.next = &a4
	a4.next = null

	head = &a1
	var n int
	scanInt n

	var found int= 0
	for ;;{
		if head == null {
			break
		}
		if head.a == n {
			found = 1
			break
		}
		head = head.next
	}

	if found==1 {
		printStr "Found\n"
	} else {
		printStr "Not Found\n"
	}
}