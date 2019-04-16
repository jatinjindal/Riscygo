package main

type t1 int
type t2 t1
type person struct{
	a t2
	b t2
	c *person
}
type new_person person
 

func main() {
	var a new_person
	var b new_person
	a.c=&b
	a.a=1
	b.a=3
	var c *new_person
	c=&a
	printInt c.a
	printStr "\n"
	c=c.c
	printInt c.a
}



