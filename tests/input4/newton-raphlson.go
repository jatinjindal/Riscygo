package main

var DELTA float32 = 0.0001
var INITIAL_Z float32 = 100.0

func step(x float32, z float32) float32 {
	return z - (z * z - x) / (2 * z)
}

func kabs(x float32) float32 {
	if x > 0 {
		return x
	} else {
		return -x
	}
}

func Sqrt(x float32) float32 {
	var z float32 = INITIAL_Z
	var zz float32

	for zz = step(x, z); kabs(zz-z) > DELTA; {
		z = zz
		zz = step(x, z)
	}
	return z
}

func main() {
	printFloat Sqrt(500.00)
}
