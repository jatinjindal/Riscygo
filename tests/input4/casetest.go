package main

import "fmt"

func main() {
	
	var k int
	scanInt k
	switch k{
		case 1:printStr "One\n";break;
		case 2:printStr "Two\n";break;
		case 3:printStr "Three\n";break;
		case 4:printStr "Four\n";break;		
		case 5:printStr "Five\n";break;
		default: printStr "man\n"
	}
	scanInt k
	switch k{
		case 1:printStr "One\n";
		case 2:printStr "Two\n";
		case 3:printStr "Three\n";
		case 4:printStr "Four\n";		
		case 5:printStr "Five\n";
		default: printStr "man\n"
	}

}