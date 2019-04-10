package main

import "fmt"

type bst struct {
	a    int
	left *bst
	right *bst
}

func bst_insert(head *bst,val int)*bst{
	if head==null{
		head=malloc(12)
		head.a=val
		return head
	}else{
		if head.a<=val{
			head.right=bst_insert(head.right,val)
		}else{
			head.left=bst_insert(head.left,val)
		}
		return head

	}

}
func main() {
	var n int
	var head *bst
	head=null

	for k:=0;k<5;k++{
		scanInt n
		head=bst_insert(head,n)
	}
	head=head.right
	printInt head.a
	
	
}
