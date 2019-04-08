package main;
import "fmt";

// type f struct{
// 	a int
// 	b *f
// }

var a int=5

func ar_print(ar [5]int){
	for k:=0;k<5;k++{
		printInt ar[k]
	}
}


func main()int{
	// f();
	// var r f
	// r.a=1
	// var c int=5
	// var e float32=12.0
	var ar [5] int
	for k:=0;k<5;k++{
		ar[k]=k
	}
	ar_print(ar)	

}

