package main

type str struct {
	s string
}

func some_function() str {
	var s str
	s.s = malloc(100)
	s.s = "Hello, world!\n"
	return s
}

func main() {
	var s str
	s = some_function()
	printStr s.s
}
