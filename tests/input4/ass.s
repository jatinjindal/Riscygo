.data
msg_6: .asciiz "\n"
msg_5: .asciiz " "
msg_4: .asciiz "M:"
msg_3: .asciiz "\n"
msg_2: .asciiz " "
msg_1: .asciiz "F:"
.text
.globl main
hofstaderFemale:
addi $sp,$sp,-4
sw $fp,0($sp)
move $fp,$sp
addi $sp,$sp,-44
li $t0,0
move $t1,$t0
sw $t0,-4($fp)
lw $t0,8($fp)
slt $t2,$t0,$t1
move $t3,$t2
sw $t2,-8($fp)
beq $t3,$0,if_1.false
li $t0,0
move $t1,$t0
sw $t0,-12($fp)
sw $t1,12($fp)
addi $sp,$sp,44
lw $fp,0($sp)
addi $sp,$sp,4
jr $ra
j if_1.next
if_1.false:
li $t0,0
move $t1,$t0
sw $t0,-16($fp)
lw $t0,8($fp)
slt $t2,$t0,$t1
slt $t3,$t1,$t0
or $t3,$t2,$t3
xor $t3,$t3,1
move $t4,$t3
sw $t3,-20($fp)
beq $t4,$0,if_2.false
li $t0,1
move $t1,$t0
sw $t0,-24($fp)
sw $t1,12($fp)
addi $sp,$sp,44
lw $fp,0($sp)
addi $sp,$sp,4
jr $ra
j if_1.next
if_2.false:
li $t0,1
move $t1,$t0
sw $t0,-28($fp)
lw $t0,8($fp)
sub $t2,$t0,$t1
move $t3,$t2
sw $t2,-32($fp)
addi $sp,$sp,-4
addi $sp,$sp,-4
sw $t3,0($sp)
addi $sp,$sp,-4
sw $ra,0($sp)
jal hofstaderFemale
lw $ra,0($sp)
addi $sp,$sp,4
addi $sp,$sp,4
lw $t0,0($sp)
move $t1,$t0
sw $t0,-36($fp)
addi $sp,$sp,4
addi $sp,$sp,-4
addi $sp,$sp,-4
sw $t1,0($sp)
addi $sp,$sp,-4
sw $ra,0($sp)
jal hofstaderMale
lw $ra,0($sp)
addi $sp,$sp,4
addi $sp,$sp,4
lw $t0,0($sp)
move $t1,$t0
sw $t0,-40($fp)
addi $sp,$sp,4
lw $t0,8($fp)
sub $t2,$t0,$t1
move $t3,$t2
sw $t2,-44($fp)
sw $t3,12($fp)
addi $sp,$sp,44
lw $fp,0($sp)
addi $sp,$sp,4
jr $ra
if_1.next:
addi $sp,$sp,44
lw $fp,0($sp)
addi $sp,$sp,4
jr $ra
hofstaderMale:
addi $sp,$sp,-4
sw $fp,0($sp)
move $fp,$sp
addi $sp,$sp,-44
li $t0,0
move $t1,$t0
sw $t0,-4($fp)
lw $t0,8($fp)
slt $t2,$t0,$t1
move $t3,$t2
sw $t2,-8($fp)
beq $t3,$0,if_3.false
li $t0,0
move $t1,$t0
sw $t0,-12($fp)
sw $t1,12($fp)
addi $sp,$sp,44
lw $fp,0($sp)
addi $sp,$sp,4
jr $ra
j if_3.next
if_3.false:
li $t0,0
move $t1,$t0
sw $t0,-16($fp)
lw $t0,8($fp)
slt $t2,$t0,$t1
slt $t3,$t1,$t0
or $t3,$t2,$t3
xor $t3,$t3,1
move $t4,$t3
sw $t3,-20($fp)
beq $t4,$0,if_4.false
li $t0,0
move $t1,$t0
sw $t0,-24($fp)
sw $t1,12($fp)
addi $sp,$sp,44
lw $fp,0($sp)
addi $sp,$sp,4
jr $ra
j if_3.next
if_4.false:
li $t0,1
move $t1,$t0
sw $t0,-28($fp)
lw $t0,8($fp)
sub $t2,$t0,$t1
move $t3,$t2
sw $t2,-32($fp)
addi $sp,$sp,-4
addi $sp,$sp,-4
sw $t3,0($sp)
addi $sp,$sp,-4
sw $ra,0($sp)
jal hofstaderMale
lw $ra,0($sp)
addi $sp,$sp,4
addi $sp,$sp,4
lw $t0,0($sp)
move $t1,$t0
sw $t0,-36($fp)
addi $sp,$sp,4
addi $sp,$sp,-4
addi $sp,$sp,-4
sw $t1,0($sp)
addi $sp,$sp,-4
sw $ra,0($sp)
jal hofstaderFemale
lw $ra,0($sp)
addi $sp,$sp,4
addi $sp,$sp,4
lw $t0,0($sp)
move $t1,$t0
sw $t0,-40($fp)
addi $sp,$sp,4
lw $t0,8($fp)
sub $t2,$t0,$t1
move $t3,$t2
sw $t2,-44($fp)
sw $t3,12($fp)
addi $sp,$sp,44
lw $fp,0($sp)
addi $sp,$sp,4
jr $ra
if_3.next:
addi $sp,$sp,44
lw $fp,0($sp)
addi $sp,$sp,4
jr $ra
main:move $v1,$sp
move $fp,$sp
addi $sp,$sp,0
addi $sp,$sp,-4
sw $fp,0($sp)
move $fp,$sp
addi $sp,$sp,-72
la $t0,msg_1
move $t1,$t0
sw $t0,-4($fp)
move $a0,$t1
li $v0,4
syscall
li $t0,0
move $t2,$t0
sw $t0,-8($fp)
move $t0,$t2
sw $t2,-12($fp)
for_1:
li $t0,10
move $t1,$t0
sw $t0,-16($fp)
lw $t0,-12($fp)
slt $t2,$t0,$t1
move $t3,$t2
sw $t2,-20($fp)
beq $t3,$0,for_1.next
addi $sp,$sp,-4
lw $t0,-12($fp)
addi $sp,$sp,-4
sw $t0,0($sp)
addi $sp,$sp,-4
sw $ra,0($sp)
jal hofstaderFemale
lw $ra,0($sp)
addi $sp,$sp,4
addi $sp,$sp,4
lw $t0,0($sp)
move $t1,$t0
sw $t0,-28($fp)
addi $sp,$sp,4
move $a0,$t1
li $v0,1
syscall
la $t0,msg_2
move $t2,$t0
sw $t0,-32($fp)
move $a0,$t2
li $v0,4
syscall
for_1.post:
li $t0,1
move $t1,$t0
sw $t0,-24($fp)
lw $t0,-12($fp)
add $t2,$t0,$t1
move $t0,$t2
sw $t2,-12($fp)
j for_1
for_1.next:
la $t0,msg_3
move $t1,$t0
sw $t0,-36($fp)
move $a0,$t1
li $v0,4
syscall
la $t0,msg_4
move $t2,$t0
sw $t0,-40($fp)
move $a0,$t2
li $v0,4
syscall
li $t0,0
move $t3,$t0
sw $t0,-44($fp)
move $t0,$t3
sw $t3,-48($fp)
for_2:
li $t0,10
move $t1,$t0
sw $t0,-52($fp)
lw $t0,-48($fp)
slt $t2,$t0,$t1
move $t3,$t2
sw $t2,-56($fp)
beq $t3,$0,for_2.next
addi $sp,$sp,-4
lw $t0,-48($fp)
addi $sp,$sp,-4
sw $t0,0($sp)
addi $sp,$sp,-4
sw $ra,0($sp)
jal hofstaderMale
lw $ra,0($sp)
addi $sp,$sp,4
addi $sp,$sp,4
lw $t0,0($sp)
move $t1,$t0
sw $t0,-64($fp)
addi $sp,$sp,4
move $a0,$t1
li $v0,1
syscall
la $t0,msg_5
move $t2,$t0
sw $t0,-68($fp)
move $a0,$t2
li $v0,4
syscall
for_2.post:
li $t0,1
move $t1,$t0
sw $t0,-60($fp)
lw $t0,-48($fp)
add $t2,$t0,$t1
move $t0,$t2
sw $t2,-48($fp)
j for_2
for_2.next:
la $t0,msg_6
move $t1,$t0
sw $t0,-72($fp)
move $a0,$t1
li $v0,4
syscall
addi $sp,$sp,72
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
        