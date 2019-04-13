package main

func main() {
	var str string
	str = "testfile.txt"
	var data string = "This is test data!"
	var readdata string
	readdata = malloc(22)
	var fd int
	fd = openFile(str, 0x41, 0x1FF)
	printStr "Opened file with fd: "
	printInt fd
	printStr "\n"
	writeFile(fd, data, 18)
	closeFile(fd)

	fd = openFile(str, 0x40, 0)
	printStr "Opened file with fd: "
	printInt fd
	printStr "\n"
	readFile(fd, readdata, 11)
	printStr readdata
	printStr "\n"
	closeFile(fd)
	printStr readdata
	printStr "\n"
}
