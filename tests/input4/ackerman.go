package main;
import "fmt";


func ackerman(a int,b int)int{

	if a==0{
		return b+1
	}
	if a>0 && b==0{
		var c int=ackerman(a-1,1)
		// printInt c 
		return c
	}
	if a>0 && b>0{
		var e int=ackerman(a-1,ackerman(a,b-1))
		// printInt e
		return e
	}
}

func main(){
	var a int=3
	var b int=4
	printInt ackerman(a,b)
}