package main

import "fmt"

func num(k int)string{
	switch k{
	case 0:return "Zero";break
	case 1:return "One";break
	case 2:return "Two";break
	case 3:return "Three";break
	case 4:return "Four";break
	case 5:return "Five";break
	case 6:return "Six";break
	case 7:return "Seven";break
	case 8:return "Eight";break
	case 9:return "Nine";break
	default: return "error"
	}
}

func main() {
	var str string
	var concat string=""
	var num1 int

	printStr "Enter Your Name:\n"
	scanStr str
	printStr "Welcome "+str+"!\n"	
	printStr "Write any number:\n"
	scanInt num1

	for ;num1>0;{
		concat=num(num1%10)+" "+concat
		num1=num1/10
	}
	printStr concat


}