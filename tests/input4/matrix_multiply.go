
package main;
import "fmt";


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

