package main

func callMyFunc() bool {
	printStr("This should not print\n")
	return 1 == 1
}

func main() {
	a := 0
	if a >= 0 || callMyFunc() {
		printStr("This should print in first line\n")
	}
	if a > 0 && callMyFunc() {
		printStr("This should not print in second line\n")
	} else {
		printStr("This should print in second line\n")
	}
}
