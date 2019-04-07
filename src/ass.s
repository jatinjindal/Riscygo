.text
mov $v1,$sp
mov $fp,$sp
addi $sp,$sp,-28
li $t1,5
sw $t1,0($v1)
sw $t2,-4($v1)
addi $sp,$sp,-4
sw $ra,0($sp)
jal main
goto end
li $t4,1
sw $t4,0($fp)
sw $t5,-4($v1)
li $t7,0
sw $t7,-4($fp)
end:
lw $ra,0($sp)
addi $sp,$sp,4
addi $sp,$sp,28
jr $ra
