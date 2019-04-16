package main

func main()

type point struct{
	x int
	y int
}
 
type rectange struct{
	v1 point
	v2 point
}
 

func main() {
	var rec1 rectange
	// rec1.v1.x=0
	// rec1.v1.y=0
	// rec1.v2.x=4
	// rec1.v2.y=4
	printStr "enter left bottom x"
	scanInt rec1.v1.x
	printStr "enter left bottom y"
	scanInt rec1.v1.y
	printStr "enter right top x"
	scanInt rec1.v2.x
	printStr "enter right top y"
	scanInt rec1.v2.y
	var i int
	var j int
	for i=rec1.v2.y;i>rec1.v1.y;i--{
		for j=rec1.v1.x;j<rec1.v2.x;j++{
			printStr "*"
		
	}
	printStr "\n"	
	}

}



