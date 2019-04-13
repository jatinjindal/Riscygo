package main

func main() {
	var a float32
	a = 1.22
	var b float32
	b = sin(a)
	printFloat b
	printStr "\n"
	b = cos(a)
	printFloat b
	printStr "\n"
}
