.data
.text
.globl main
bst_insert:
addi $sp,$sp,-4
sw $fp,0($sp)
move $fp,$sp
addi $sp,$sp,-20
lw $t0,12($fp)
li $t1,0
slt $t2,$t0,$t1
slt $t3,$t1,$t0
or $t3,$t2,$t3
xor $t3,$t3,1
move $t4,$t3
sw $t3,-4($fp)
beq $t4,$0,if_1.false
li $t0,12
move $t1,$t0
sw $t0,-8($fp)
move $a0,$t1
li $v0, 9
syscall
move $t0,$v0
sw $v0,12($fp)
lw $t2,8($fp)
sw $t2,-0($t0)
sw $t0,16($fp)
addi $sp,$sp,20
lw $fp,0($sp)
addi $sp,$sp,4
jr $ra
j if_1.next
if_1.false:
lw $t0,12($fp)
lw $t1,-0($t0)
lw $t2,8($fp)
slt $t3,$t2,$t1
xor $t3,$t3,1
move $t4,$t3
sw $t3,-12($fp)
beq $t4,$0,if_2.false
addi $sp,$sp,-4
lw $t0,12($fp)
lw $t1,-8($t0)
addi $sp,$sp,-4
sw $t1,0($sp)
lw $t1,8($fp)
addi $sp,$sp,-4
sw $t1,0($sp)
addi $sp,$sp,-4
sw $ra,0($sp)
jal bst_insert
lw $ra,0($sp)
addi $sp,$sp,4
addi $sp,$sp,4
addi $sp,$sp,4
lw $t0,0($sp)
move $t1,$t0
sw $t0,-16($fp)
addi $sp,$sp,4
lw $t0,12($fp)
sw $t1,-8($t0)
j if_2.next
if_2.false:
addi $sp,$sp,-4
lw $t0,12($fp)
lw $t1,-4($t0)
addi $sp,$sp,-4
sw $t1,0($sp)
lw $t1,8($fp)
addi $sp,$sp,-4
sw $t1,0($sp)
addi $sp,$sp,-4
sw $ra,0($sp)
jal bst_insert
lw $ra,0($sp)
addi $sp,$sp,4
addi $sp,$sp,4
addi $sp,$sp,4
lw $t0,0($sp)
move $t1,$t0
sw $t0,-20($fp)
addi $sp,$sp,4
lw $t0,12($fp)
sw $t1,-4($t0)
if_2.next:
lw $t0,12($fp)
sw $t0,16($fp)
addi $sp,$sp,20
lw $fp,0($sp)
addi $sp,$sp,4
jr $ra
if_1.next:
addi $sp,$sp,20
lw $fp,0($sp)
addi $sp,$sp,4
jr $ra
main:move $v1,$sp
move $fp,$sp
addi $sp,$sp,0
addi $sp,$sp,-4
sw $fp,0($sp)
move $fp,$sp
addi $sp,$sp,-32
li $t0,0
move $t1,$t0
sw $t0,-8($fp)
li $t0,0
move $t2,$t0
sw $t0,-12($fp)
move $t0,$t2
sw $t2,-16($fp)
for_1:
li $t0,5
move $t1,$t0
sw $t0,-20($fp)
lw $t0,-16($fp)
slt $t2,$t0,$t1
move $t3,$t2
sw $t2,-24($fp)
beq $t3,$0,for_1.next
li $v0,5
syscall
move $t0,$v0
sw $v0,-4($fp)
addi $sp,$sp,-4
lw $t1,-8($fp)
addi $sp,$sp,-4
sw $t1,0($sp)
addi $sp,$sp,-4
sw $t0,0($sp)
addi $sp,$sp,-4
sw $ra,0($sp)
jal bst_insert
lw $ra,0($sp)
addi $sp,$sp,4
addi $sp,$sp,4
addi $sp,$sp,4
lw $t0,0($sp)
move $t1,$t0
sw $t0,-32($fp)
addi $sp,$sp,4
move $t0,$t1
sw $t1,-8($fp)
for_1.post:
li $t0,1
move $t1,$t0
sw $t0,-28($fp)
lw $t0,-16($fp)
add $t2,$t0,$t1
move $t0,$t2
sw $t2,-16($fp)
j for_1
for_1.next:
lw $t0,-8($fp)
lw $t1,-8($t0)
move $t0,$t1
sw $t1,-8($fp)
lw $t1,-0($t0)
move $a0,$t1
li $v0,1
syscall
addi $sp,$sp,32
lw $fp,0($sp)
addi $sp,$sp,4
addi $sp,$sp,0
jr $ra

#String copy code
strcpy:
li $t8 10 #store newline in $t8
sCopyFirst:
    lb   $t0 0($a0)
    beq  $t0 $zero sCopySecond 
    beq  $t0 $t8 sCopySecond   
    sb   $t0 0($a2)
    addi $a0 $a0 1
    addi $a2 $a2 1
    b sCopyFirst

sCopySecond:
    lb   $t0 0($a1)
    beq  $t0 $zero sDone 
    beq  $t0 $t8 sDone   
    sb   $t0 0($a2)
    addi $a1 $a1 1
    addi $a2 $a2 1
    b sCopySecond

sDone:
    sb $zero 0($a2) 
    jr $ra
        