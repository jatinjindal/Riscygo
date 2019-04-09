
package main;
import "fmt";
// var a f
// var a int=5
// var c float32=10.0

// func test(a int,b [3]int){

// }


// func main()int{
// 	// var r f
// 	// r.a=1
// 	// var c int=5
// 	// var e float32=12.0
// 	// var c [3]int
// 	// test(2,c)
// 	// var ar [3]int
// 	// var c int=5+6+7+ar[0]
// 	return 0;
// };
// func del(c int,e int){
// 	c=1

// }

// func fibo(n int)int{
	
// 	if n== 1{
// 		return 1
// 	}
// 	if n== 2{
// 		return 1
// 	}
// 	return fibo(n-1)+fibo(n-2)

// }

// // var a int=0

// func ackerman(a int,b int)int{

// 	if a==0{
// 		return b+1
// 	}
// 	if a>0 && b==0{
// 		var c int=ackerman(a-1,1)
// 		// printInt c 
// 		return c
// 	}
// 	if a>0 && b>0{
// 		var e int=ackerman(a-1,ackerman(a,b-1))
// 		// printInt e
// 		return e
// 	}
// }


// func sum( num int)int{
//     if num!=0{
//         return num + sum(num-1); // sum() function calls itself
//     }else{
//         return num;
//     }
// }

// type f struct{
// 	a int
// 	b *f
// }

// var a int=5

// func ar_print(ar [5]int){
// 	for k:=0;k<5;k++{
// 		printInt ar[k]
// 	}
// }


func main()int{
	var ar[3][3]int
	var br[3][3]int
	var res[3][3]int

	for i:=0;i<3;i++{
		for j:=0;j<3;j++{
			if i==j{
				ar[i][j]=i+1
			}else{
				ar[i][j]=0
			}
		}

	}
	for i:=0;i<3;i++{
		for j:=0;j<3;j++{
			if i==j{
				br[i][j]=i+1
			}else{
				br[i][j]=0
			}
		}

	}
	for i:=0;i<3;i++{
		for j:=0;j<3;j++{
			sum:=0
			for k:=0;k<3;k++{
				sum+=ar[i][k]*br[k][j]
			}
			res[i][j]=sum
		}	
	}
	for i:=0;i<3;i++{
		for j:=0;j<3;j++{
			printInt res[i][j]
			printStr " "
		}
		printStr "\n"
	}

}

