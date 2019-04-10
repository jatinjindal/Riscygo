package main


var A [100]int

func partition(p int, r int) int {
    
    var x int 
    x = A[p]
    var i int
    i = p - 1
    var j int
    j = r + 1

    for {
        j--
        var kk int
        kk = A[j]
        for kk < x {
            j--
            kk = A[j]
        }
        i++
        for A[i] > x {
            i++
        }
        if i < j {
            var tmp int
            tmp = A[i]
            A[i] = A[j]
            A[j] = tmp
        } else {
            return j
        }
    }
    return -1
}
func qsort(p int, r int) {
    if p < r {
        var q int
        q = partition(p, r)
        qsort(p, q)
        qsort(q+1, r)
    }
}

func main() {
    var i int 
    for i =0; i < 100; i++ {

        A[i] = i
    }

    
    qsort(0, 99)
    for i =0; i < 100; i++ {
        printInt A[i]
    }

}