
package main

import "fmt"

func is_even(a int)int
func is_odd(a int)int

func is_even(n int)int {
    if n == 0{
        return 1;
    }else{
        return is_odd(n - 1);
    }
}

func is_odd(n int)int {
    if n == 0{
        return 0;
    }else{
        return is_even(n - 1);
    }
}

 func main() {

 	var  n int
 	scanInt n
 	if is_even(n)==1{
 		printStr "Given number is even\n"
 	}
 	if is_odd(n)==1{
 		printStr "Given number is odd\n"
 	}
}