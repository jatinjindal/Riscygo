package main

import "fmt"

func hofstaderFemale(a int)int 
func hofstaderMale(a int)int
  
// Female function 
func hofstaderFemale( n int )int{ 
    if (n < 0){
        return 0; 
    }else if n==0{
        return 1  
    }else{
    	return  n - hofstaderMale(hofstaderFemale(n - 1))
    }
} 
  
// Male function 
func hofstaderMale( n int )int{ 
    if (n < 0){
        return 0; 
    }else if n==0{
        return 0
    }else{
    	return  n - hofstaderFemale(hofstaderMale(n - 1))
    }
} 

func main(){
	printStr "F:"
	for k:=0;k<10;k++{
		printInt hofstaderFemale(k)
		printStr " "
	}
	printStr "\n"
	printStr "M:"
	for k:=0;k<10;k++{
		printInt hofstaderMale(k)
		printStr " "
	}
	printStr "\n"
}