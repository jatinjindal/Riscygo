import pickle
import argparse
import random
import re

set_of_activations = []
code = []
current_activation = "global"
reg_map = [[None] * 10, [None] * 8]
reg_map_float = {"$f2":None, "$f4":None,"$f6":None,"$f8":None,"$f10":None,"$f14":None,"$f16":None,"$f18":None,"$f20":None,"$f22":None, "$f24":None,"$f26":None,"$f28":None,"$f30":None}
asm = None
cur_reg = []

label_count = 0
def generate_label():
    global label_count
    label_count += 1
    return "compare_" + str(label_count)


class activation_record:
    def __init__(self, previous=None):
        self.previous = previous
        self.label = "global"
        self.data = {}
        self.total = 0
        self.ret_value_addr = None


def get_name(ind1, ind2):
    if ind1 == 0:
        return "$t" + str(ind2)
    else:
        return "$s" + str(ind2)


def get_empty_register(set_name=None):
    global asm
    global set_of_activations
    global current_activation
    global cur_reg
    # Pick from temporary
    # asm.write("empty_reg\n")
    if set_name =="float" or (get_rec(set_name)!=None and ((get_rec(set_name))["isf"])==1):
        for x in reg_map_float:
            if (reg_map_float[x] == None or reg_map_float=="float") and x not in cur_reg:
                reg_map_float[x] = set_name
                cur_reg.append(x)
                return x
    elif set_name == None or set_name == "int" or get_rec(set_name) == None or (get_rec(set_name))["isf"]==0:    
        for x in range(0, 10):
            if reg_map[0][x] == None and (0, x) not in cur_reg:
                reg_map[0][x] = set_name
                cur_reg.append((0, x))
                return (0, x)
        # Pick from saved
        for x in range(0, 8):
            if reg_map[1][x] == None and (1, x) not in cur_reg:
                reg_map[1][x] = set_name
                cur_reg.append((1, x))
                return (1, x)
    
    
    rec = get_rec(set_name)
    if rec["isf"] == 1:
        reg_f = random.choice(list(reg_map_float.keys()))
        while reg_f in cur_reg:
            reg_f = random.choice(list(reg_map_float.keys()))
        record = get_rec(reg_map_float[reg_f])
        record["isreg"]=-1
        if record["label"] == "global":
            asm.write("s.s " + reg_f + "," +
                  str(-record["func_offset"]) + "($v1)\n")
        else:
            asm.write("s.s " + reg_f + "," +
                      str(-record["func_offset"]) + "($fp)\n")

        reg_map_float[reg_f] = set_name
        rec["isreg"] = reg_f
        cur_reg.append(reg_f)
        return reg_f

    else:
        ind1 = random.randint(0, 1)
        if ind1 == 0:
            ind2 = random.randint(0, 9)
        else:
            ind2 = random.randint(0, 7)

        while (ind1, ind2) in cur_reg:
            ind1 = random.randint(0, 1)
            if ind1 == 0:
                ind2 = random.randint(0, 9)
            else:
                ind2 = random.randint(0, 7)

        record = get_rec(reg_map[ind1][ind2])
        record["isreg"] = -1
        if record["label"] == "global":
            asm.write("sw " + get_name(ind1, ind2) + "," +
                      str(-record["func_offset"]) + "($v1)\n")
        else:
            asm.write("sw " + get_name(ind1, ind2) + "," +
                      str(-record["func_offset"]) + "($fp)\n")

        reg_map[ind1][ind2] = set_name
        cur_reg.append((ind1, ind2))
        return (ind1, ind2)


def get_reg(name):
    global set_of_activations
    global current_activation
    global cur_reg

    if type(name) == int:
        reg = get_empty_register()
        reg_name = get_name(reg[0], reg[1])
        asm.write("li " + reg_name + "," + str(name) + "\n")
        return reg_name

    if type(name) == float:
        reg_name = get_empty_register("float")
        asm.write("li.s " + reg_name + "," + str(name) + "\n" )
        return reg_name

    rec = get_rec(name)
    if rec["isf"] == 1:
        assert (name[:3] == 'var')
        if rec['isreg'] != -1:
            cur_reg.append(rec['isreg'])
            return rec['isreg']
        else:
            reg = get_empty_register(name)
            off = rec['func_offset']
            rec['isreg'] = reg
            asm.write('l.s ' + reg + ',' + str(-off))
            if rec['label'] == 'global':
                asm.write('($v1)\n')
            else:
                asm.write('($fp)\n')
            return reg
    else:
        if name[0] == '*':
            # Deferencing a var
            name = name[1:]
            assert (name[:3] == 'var')
            off = rec['func_offset']
            reg = get_reg(name)
            regt = get_name(*get_empty_register())
            asm.write('lw ' + regt + ',0(' + reg + ')\n')
            return regt
        elif name[0] == '&':
            # Getting an address of var
            name = name[1:]
            assert (name[:3] == 'var')
            rec = get_rec(name)
            off = rec['func_offset']
            reg = get_empty_register()
            asm.write('addi ' + get_name(*reg))
            if rec['label'] == 'global':
                asm.write(',$v1,')
            else:
                asm.write(',$fp,')
            asm.write(str(-rec['func_offset']) + '\n')
            return get_name(*reg)
        elif len(name.split('.')) != 1:
            # Getting member of a struct
            member = name.split('.')[1]
            name = name.split('.')[0]
            assert (name[:3] == 'var')
            rec = get_rec(name)
            off = rec['func_offset']
            if rec['width'] == 0:
                reg = get_name(*get_empty_register())
                asm.write('lw ' + reg + ',' + str(-off - int(member)))
                if rec['label'] == 'global':
                    asm.write('($v1)\n')
                else:
                    asm.write('($fp)\n')
                return reg
            else:
                reg = get_reg(name)
                regt = get_name(*get_empty_register())
                asm.write('lw ' + regt + ',-' + str(member) + '(' + reg + ')\n')
                return regt
        elif len(name.split('[')) != 1:
            # Getting array member
            index = name.split('[')[1].split(']')[0]
            name = name.split('[')[0]
            assert (name[:3] == 'var' and index[:3] == 'var')
            # Load the value of index

            regi = get_reg(index)
            rec = get_rec(name)
            off = rec['func_offset']
            reg = get_name(*get_empty_register())
            if rec['width'] == 0:
                asm.write('sub ' + reg + ',')
                if rec['label'] == 'global':
                    asm.write('$v1,' + regi + '\n')
                else:
                    asm.write('$fp,' + regi + '\n')
                asm.write('lw ' + reg + ',' + str(-off) + '(' + reg + ')\n')
            else:
                asm.write('lw ' + reg + ',' + str(-off))
                if rec['label'] == 'global':
                    asm.write('($v1)\n')
                else:
                    asm.write('($fp)\n')
                asm.write('sub ' + reg + ',' + reg + ',' + regi + '\n')
                asm.write('lw ' + reg + ',0(' + reg + ')\n')
            return reg
        else:
            # A normal var
            assert (name[:3] == 'var')
            rec = get_rec(name)
            if rec['isreg'] != -1:
                cur_reg.append(rec['isreg'])
                return get_name(*rec['isreg'])
            else:
                reg = get_empty_register(name)
                off = rec['func_offset']
                rec['isreg'] = reg
                asm.write('lw ' + get_name(*reg) + ',' + str(-off))
                if rec['label'] == 'global':
                    asm.write('($v1)\n')
                else:
                    asm.write('($fp)\n')
                return get_name(*reg)







def get_rec(name):
    global set_of_activations
    global current_activation

    if name in set_of_activations[current_activation].data:
        return set_of_activations[current_activation].data[name]
    elif name in set_of_activations["global"].data:
        return set_of_activations["global"].data[name]
    else:
        return None

def off_load():
    for x in range(0, 10):
        if reg_map[0][x] != None:
            record = get_rec(reg_map[0][x])
            record["isreg"] = -1
            if record["label"] == "global":
                asm.write("sw " + get_name(0, x) + "," +
                          str(-record["func_offset"]) + "($v1)\n")
            else:
                asm.write("sw " + get_name(0, x) + "," +
                          str(-record["func_offset"]) + "($fp)\n")
            reg_map[0][x] = None
    for x in range(0, 8):
        if reg_map[1][x] != None:
            record = get_rec(reg_map[1][x])
            record["isreg"] = -1
            if record["label"] == "global":
                asm.write("sw " + get_name(1, x) + "," +
                          str(-record["func_offset"]) + "($v1)\n")
            else:
                asm.write("sw " + get_name(1, x) + "," +
                          str(-record["func_offset"]) + "($fp)\n")
            reg_map[1][x] = None


def handle_assign(dst, reg):
    global asm
    # TODO: Handle floating point registers
    rec_dst = get_rec(dst)
    if reg[1] =="f":
        assert (dst[:3] == 'var')
        rec = get_rec(dst)
        if rec['isreg'] != -1:
            reg2 = rec['isreg']
        else:
            rec["isf"]=1
            reg2 = get_empty_register(dst)
            # asm.write("check\n")
            rec['isreg'] = reg2
        # asm.write("check1\n")
        asm.write('mov.s '+ reg2+','+reg+'\n')
        asm.write('s.s '+reg+','+str(-rec["func_offset"]) )
        if rec['label'] == 'global':
            asm.write('($v1)\n')
        else:
            asm.write('($fp)\n')
    else:   
        if dst[-1] == "]":
            dst_nam = dst.split('[')[0]
            index = dst.split('[')[1].split(']')[0]
            assert (dst_nam[:3] == 'var' and index[:3] == 'var')
            regi = get_reg(index)
            rec = get_rec(dst_nam)
            off = rec['func_offset']
            reg_emp = get_name(*get_empty_register())
            if rec["width"] == 0:
                asm.write('sub ' + reg_emp + ',')
                if rec['label'] == 'global':
                    asm.write('$v1,' + regi + '\n')
                else:
                    asm.write('$fp,' + regi + '\n')
                asm.write('sw ' + reg + ',' + str(-off) + '(' + reg_emp + ')\n')
            else:
                reg2 = get_reg(dst_nam)
                asm.write('sub ' + reg2 + ',' + reg2 + ',' + regi + '\n')
                asm.write('sw ' + reg + ',0(' + reg2 + ')\n')
        elif dst[0] == "*":
            dst = dst[1:]
            assert (dst[:3] == 'var')
            reg2 = get_reg(dst)
            asm.write("sw " + reg + ",0(" + reg2 + ")\n")
        elif len(dst.split('.')) != 1:
            # Getting member of a struct
            member = dst.split('.')[1]
            name = dst.split('.')[0]
            assert (name[:3] == 'var')
            rec = get_rec(name)
            off = rec['func_offset']
            if rec['width'] == 0:
                asm.write('sw ' + reg + ',' + str(-off - int(member)))
                if rec['label'] == 'global':
                    asm.write('($v1)\n')
                else:
                    asm.write('($fp)\n')
            else:
                reg2 = get_reg(name)
                asm.write('sw ' + reg + ',-' + member + '(' + reg2 + ')\n')
        else:
            assert (dst[:3] == 'var')
            rec = get_rec(dst)
            if rec['isreg'] != -1:
                reg2 = rec['isreg']
            else:
                reg2 = get_empty_register(dst)
                rec['isreg'] = reg2
            asm.write('move '+ get_name(*reg2)+','+reg+'\n')
            asm.write('sw '+reg+','+str(-rec["func_offset"]) )
            if rec['label'] == 'global':
                asm.write('($v1)\n')
            else:
                asm.write('($fp)\n')

def generate_code(ins):
    global first_func
    global set_of_activations
    global current_activation

    if ins[0] == "=":
        assert (len(ins) == 3)
        reg = get_reg(ins[2])
        # asm.write("check\n")
        handle_assign(ins[1], reg)
    elif ins[0] == "returnm":
        if len(ins) == 1:
            off_load()
            asm.write("addi $sp,$sp," + str(set_of_activations["main"].total) +
                      "\n")
            asm.write("lw $fp,0($sp)\n")
            asm.write("addi $sp,$sp,4\n")
            asm.write("addi $sp,$sp," +
                      str(set_of_activations["global"].total) + "\n")
            asm.write("jr $ra\n")

        else:
            reg = get_reg(ins[1])
            ret_off = set_of_activations[current_activation].ret_value_addr
            asm.write("sw " + reg + "," + str(-ret_off) + "($fp)\n")
            off_load()
            asm.write("addi $sp,$sp," +
                      str(set_of_activations[current_activation].total) + "\n")
            asm.write("lw $fp,0($sp)\n")
            asm.write("addi $sp,$sp,4\n")
            asm.write("jr $ra\n")

    elif ins[0] == "return":
        if len(ins) == 2:
            reg = get_reg(ins[1])
            ret_off = set_of_activations[current_activation].ret_value_addr
            asm.write("sw " + reg + "," + str(-ret_off) + "($fp)\n")
        off_load()
        asm.write("addi $sp,$sp," +
                  str(set_of_activations[current_activation].total) + "\n")
        asm.write("lw $fp,0($sp)\n")
        asm.write("addi $sp,$sp,4\n")
        asm.write("jr $ra\n")

    elif ins[0] == "malloc":
        reg2 = get_reg(ins[2])
        asm.write("move $a0," + reg2 + "\n")
        asm.write("li $v0, 9\n")
        asm.write("syscall\n")
        handle_assign(ins[1],"$v0")

    elif len(ins) == 1 and ins[0] == "push":
        asm.write("addi $sp,$sp,-4\n")

    elif len(ins) == 2 and ins[0] == "push":
        if ins[1][:3] == "var":
            rec = get_rec(ins[1])
            if rec["width"] == 0:
                reg_emp = get_empty_register()
                reg2 = get_name(reg_emp[0], reg_emp[1])
                asm.write("li " + reg2 + "," + str(rec["func_offset"]) + "\n")
                if rec["label"] == "global":
                    asm.write("sub " + reg2 + ",$v1," + reg2 + "\n")
                else:
                    asm.write("sub " + reg2 + ",$fp," + reg2 + "\n")
                asm.write("addi $sp,$sp,-4\n")
                asm.write("sw " + reg2 + ",0($sp)\n")

            else:
                reg = get_reg(ins[1])
                asm.write("addi $sp,$sp,-4\n")
                asm.write("sw " + reg + ",0($sp)\n")
        else:
            reg = get_reg(ins[1])
            asm.write("addi $sp,$sp,-4\n")
            asm.write("sw " + reg + ",0($sp)\n")

    elif len(ins) == 3 and ins[0] == "call":
        asm.write("addi $sp,$sp,-4\n")
        asm.write("sw $ra,0($sp)\n")
        off_load()
        asm.write("jal " + ins[1] + "\n")
        asm.write("lw $ra,0($sp)\n")
        asm.write("addi $sp,$sp,4\n")

    elif len(ins) == 1 and ins[0] == "pop":
        asm.write("addi $sp,$sp,4\n")

    elif len(ins) == 2 and ins[0] == "pop":
        # rec = get_rec(ins[1])
        reg_emp = get_empty_register(None)
        reg_name = get_name(reg_emp[0], reg_emp[1])
        asm.write("lw " + reg_name + ",0($sp)\n")
        handle_assign(ins[1],reg_name)
        # asm.write("sw " + reg_name + "," + str(-rec["func_offset"]))
        # if rec["label"] == "global":
        #     asm.write("($v1)\n")
        # else:
        #     asm.write("($fp)\n")
        asm.write("addi $sp,$sp,4\n")

    elif len(ins) == 2 and ins[0] == "printInt":
        reg = get_reg(ins[1])
        asm.write("move $a0" + "," + reg + "\n")
        asm.write("li $v0,1\n")
        asm.write("syscall\n")

    elif len(ins) == 2 and ins[0] == "printFloat":
        reg = get_reg(ins[1])
        asm.write("mov.s $f12" + "," + reg + "\n")
        asm.write("li $v0,2\n")
        asm.write("syscall\n")

    elif len(ins)==3 and ins[0]=="cast-float":
        rec = get_rec(ins[1])
        rec["isf"]=1
        rec["isreg"] = -1
        reg1 = get_reg(ins[1])
        reg2 = get_reg(ins[2])
        asm.write("mtc1 "+reg2+","+reg1+"\n")
        asm.write("cvt.s.w " + reg1 + "," + reg1 + "\n")
        rec["isreg"] = reg1

    elif len(ins) == 2 and ins[0] == "ScanInt":
        asm.write("li $v0,5\n")
        asm.write("syscall\n")
        handle_assign(ins[1],"$v0")

    elif len(ins) == 2 and ins[0] in set_of_activations and ins[0] == "main":
        off_load()
        asm.write("main:")
        asm.write("move $v1,$sp\n")
        asm.write("move $fp,$sp\n")
        current_activation = "global"
        asm.write("addi $sp,$sp," + str(-set_of_activations["global"].total) +
                  "\n")

    elif len(ins) == 2 and ins[0] == "EndOfDecl":
        #do a function call to save current registers
        asm.write("addi $sp,$sp,-4\n")
        asm.write("sw $fp,0($sp)\n")
        asm.write("move $fp,$sp\n")
        current_activation = "main"
        asm.write("addi $sp,$sp," +
                  str(-set_of_activations[current_activation].total) + "\n")

    elif len(ins) == 2 and ins[0] in set_of_activations:
        off_load()
        asm.write(ins[0] + ins[1] + "\n")
        asm.write("addi $sp,$sp,-4\n")
        asm.write("sw $fp,0($sp)\n")
        asm.write("move $fp,$sp\n")
        current_activation = ins[0]
        asm.write("addi $sp,$sp," +
                  str(-set_of_activations[current_activation].total) + "\n")

    elif len(ins) == 2 and ins[1] == ":":
        off_load()
        asm.write(ins[0] + ins[1] + "\n")

    elif len(ins) == 2 and ins[0] == "goto":
        off_load()
        asm.write("j " + ins[1] + "\n")

    elif len(ins) == 4 and (ins[0] == "<" or ins[0] == "<int"):
        reg1 = get_reg(ins[2])
        reg2 = get_reg(ins[3])
        reg3 = get_empty_register(None)
        reg_name = get_name(reg3[0], reg3[1])
        asm.write("slt " + reg_name + "," + reg1 + "," + reg2 + "\n")
        handle_assign(ins[1],reg_name)
        #CALL A GENERIC FUNCTION HERE
        # if ins[1][:3] == "var":
        #     rec = get_rec(ins[1])
        #     asm.write("sw " + reg_name + "," + str(-rec["func_offset"]))
        #     if rec["label"] == "global":
        #         asm.write("($v1)\n")
        #     else:
        #         asm.write("($fp)\n")
    elif len(ins) == 4 and (ins[0] == "<float"):
        reg1 = get_reg(ins[2])
        reg2 = get_reg(ins[3])
        reg3 = get_reg(1)
        asm.write("c.lt.s " + reg1 + "," + reg2 + "\n")
        lab = generate_label()
        asm.write("bc1t "+lab + "\n")
        asm.write("li "+reg3 +",0\n")
        asm.write(lab +":")
        handle_assign(ins[1],reg3)
    elif len(ins) == 4 and (ins[0] == ">" or ins[0] == ">int"):
        reg1 = get_reg(ins[2])
        reg2 = get_reg(ins[3])
        reg3 = get_empty_register(None)
        reg_name = get_name(reg3[0], reg3[1])
        asm.write("slt " + reg_name + "," + reg2 + "," + reg1 + "\n")
        handle_assign(ins[1],reg_name)
        #CALL A GENERIC FUNCTION HERE
        # if ins[1][:3] == "var":
        #     rec = get_rec(ins[1])
        #     asm.write("sw " + reg_name + "," + str(-rec["func_offset"]))
        #     if rec["label"] == "global":
        #         asm.write("($v1)\n")
        #     else:
        #         asm.write("($fp)\n")
    elif len(ins) == 4 and (ins[0] == ">float"):
        reg1 = get_reg(ins[2])
        reg2 = get_reg(ins[3])
        reg3 = get_reg(1)
        asm.write("c.lt.s " + reg2 + "," + reg1 + "\n")
        lab = generate_label()
        asm.write("bc1t "+lab + "\n")
        asm.write("li "+reg3 +",0\n")
        asm.write(lab +":")
        handle_assign(ins[1],reg3)

    elif len(ins) == 4 and (ins[0] == "<=" or ins[0] == "<=int"):
        reg1 = get_reg(ins[2])
        reg2 = get_reg(ins[3])
        reg3 = get_empty_register(None)
        reg_name = get_name(reg3[0], reg3[1])
        asm.write("slt " + reg_name + "," + reg2 + "," + reg1 + "\n")
        asm.write("xor " + reg_name + "," + reg_name + ",1" + "\n")
        handle_assign(ins[1],reg_name)
        #CALL A GENERIC FUNCTION HERE
        # if ins[1][:3] == "var":
        #     rec = get_rec(ins[1])
        #     asm.write("sw " + reg_name + "," + str(-rec["func_offset"]))
        #     if rec["label"] == "global":
        #         asm.write("($v1)\n")
        #     else:
        #         asm.write("($fp)\n")
    elif len(ins) == 4 and (ins[0] == "<=float"):
        reg1 = get_reg(ins[2])
        reg2 = get_reg(ins[3])
        reg3 = get_reg(1)
        asm.write("c.le.s " + reg1 + "," + reg2 + "\n")
        lab = generate_label()
        asm.write("bc1t "+lab + "\n")
        asm.write("li "+reg3 +",0\n")
        asm.write(lab +":")
        handle_assign(ins[1],reg3)

    elif len(ins) == 4 and (ins[0] == ">=" or ins[0] == ">=int"):
        reg1 = get_reg(ins[2])
        reg2 = get_reg(ins[3])
        reg3 = get_empty_register(None)
        reg_name = get_name(reg3[0], reg3[1])
        asm.write("slt " + reg_name + "," + reg1 + "," + reg2 + "\n")
        asm.write("xor " + reg_name + "," + reg_name + ",1" + "\n")
        handle_assign(ins[1],reg_name)
        #CALL A GENERIC FUNCTION HERE
        # if ins[1][:3] == "var":
        #     rec = get_rec(ins[1])
        #     asm.write("sw " + reg_name + "," + str(-rec["func_offset"]))
        #     if rec["label"] == "global":
        #         asm.write("($v1)\n")
        #     else:
        #         asm.write("($fp)\n")
    elif len(ins) == 4 and (ins[0] == ">=float"):
        reg1 = get_reg(ins[2])
        reg2 = get_reg(ins[3])
        reg3 = get_reg(0)
        asm.write("c.lt.s " + reg1 + "," + reg2 + "\n")
        lab = generate_label()
        asm.write("bc1t  "+lab + "\n")
        asm.write("li "+reg3 +",1\n")
        asm.write(lab +":")
        handle_assign(ins[1],reg3)

    elif len(ins) == 4 and (ins[0] == "==" or ins[0] == "==int"):

        reg1 = get_reg(ins[2])
        reg2 = get_reg(ins[3])
        reg3 = get_empty_register(None)
        reg4 = get_empty_register(None)
        reg_name1 = get_name(reg3[0], reg3[1])
        reg_name2 = get_name(reg4[0], reg4[1])
        asm.write("slt " + reg_name1 + "," + reg1 + "," + reg2 + "\n")
        asm.write("slt " + reg_name2 + "," + reg2 + "," + reg1 + "\n")
        asm.write("or " + reg_name2 + "," + reg_name1 + "," + reg_name2 + "\n")
        asm.write("xor " + reg_name2 + "," + reg_name2 + ",1" + "\n")
        handle_assign(ins[1],reg_name2)
        #CALL A GENERIC FUNCTION HERE
        # if ins[1][:3] == "var":
        #     rec = get_rec(ins[1])
        #     asm.write("sw " + reg_name2 + "," + str(-rec["func_offset"]))
        #     if rec["label"] == "global":
        #         asm.write("($v1)\n")
        #     else:
        #         asm.write("($fp)\n")
    elif len(ins) == 4 and (ins[0] == "==float"):
        reg1 = get_reg(ins[2])
        reg2 = get_reg(ins[3])
        reg3 = get_reg(1)
        asm.write("c.eq.s " + reg1 + "," + reg2 + "\n")
        lab = generate_label()
        asm.write("bc1t "+lab + "\n")
        asm.write("li "+reg3 +",0\n")
        asm.write(lab +":")
        handle_assign(ins[1],reg3)

    elif len(ins) == 4 and (ins[0] == "!=" or ins[0] == "!=int"):
        reg1 = get_reg(ins[2])
        reg2 = get_reg(ins[3])
        reg3 = get_empty_register(None)
        reg4 = get_empty_register(None)
        reg_name1 = get_name(reg3[0], reg3[1])
        reg_name2 = get_name(reg4[0], reg4[1])
        asm.write("slt " + reg_name1 + "," + reg1 + "," + reg2 + "\n")
        asm.write("slt " + reg_name2 + "," + reg2 + "," + reg1 + "\n")
        asm.write("or " + reg_name2 + "," + reg_name1 + "," + reg_name2 + "\n")
        handle_assign(ins[1],reg_name2)
        #CALL A GENERIC FUNCTION HERE
        # if ins[1][:3] == "var":
        #     rec = get_rec(ins[1])
        #     asm.write("sw " + reg_name2 + "," + str(-rec["func_offset"]))
        #     if rec["label"] == "global":
        #         asm.write("($v1)\n")
        #     else:
        #         asm.write("($fp)\n")
    elif len(ins) == 4 and (ins[0] == "!=float"):
        reg1 = get_reg(ins[2])
        reg2 = get_reg(ins[3])
        reg3 = get_reg(0)
        asm.write("c.eq.s " + reg1 + "," + reg2 + "\n")
        lab = generate_label()
        asm.write("bc1t "+lab + "\n")
        asm.write("li "+reg3 +",1\n")
        asm.write(lab +":")
        handle_assign(ins[1],reg3)

    elif len(ins) == 4 and (ins[0] == "+" or ins[0] == "+int"):
        reg1 = get_reg(ins[2])
        reg2 = get_reg(ins[3])
        reg_emp = get_name(*get_empty_register())
        asm.write("add " + reg_emp + "," + reg1 + "," + reg2 + "\n")
        handle_assign(ins[1],reg_emp)
    elif len(ins) == 4 and (ins[0] == "+float"):
        reg1 = get_reg(ins[2])
        reg2 = get_reg(ins[3])
        reg_emp = get_empty_register("float")
        asm.write("add.s " + reg_emp + "," + reg1 + "," + reg2 + "\n")
        handle_assign(ins[1],reg_emp)
    elif len(ins) == 4 and (ins[0] == "-" or ins[0] == "-int"):
        reg1 = get_reg(ins[2])
        reg2 = get_reg(ins[3])
        reg_emp = get_name(*get_empty_register())
        asm.write("sub " + reg_emp + "," + reg1 + "," + reg2 + "\n")
        handle_assign(ins[1],reg_emp)
    elif len(ins) == 4 and (ins[0] == "-float"):
        reg1 = get_reg(ins[2])
        reg2 = get_reg(ins[3])
        reg_emp = get_empty_register("float")
        asm.write("sub.s " + reg_emp + "," + reg1 + "," + reg2 + "\n")
        handle_assign(ins[1],reg_emp)
    elif len(ins) == 4 and (ins[0] == "*" or ins[0] == "*int"):
        reg1 = get_reg(ins[2])
        reg2 = get_reg(ins[3])
        reg_emp = get_name(*get_empty_register())
        asm.write("mul " + reg_emp + "," + reg1 + "," + reg2 + "\n")
        handle_assign(ins[1],reg_emp)
    elif len(ins) == 4 and (ins[0] == "*float"):
        reg1 = get_reg(ins[2])
        reg2 = get_reg(ins[3])
        reg_emp = get_empty_register("float")
        asm.write("mul.s " + reg_emp + "," + reg1 + "," + reg2 + "\n")
        handle_assign(ins[1],reg_emp)
    elif len(ins) == 4 and (ins[0] == "/" or ins[0] == "/int"):
        reg1 = get_reg(ins[2])
        reg2 = get_reg(ins[3])
        reg_emp = get_name(*get_empty_register())
        asm.write("div "+ reg1 + "," + reg2 + "\n")
        asm.write("mflo "+reg_emp+"\n")
        handle_assign(ins[1],reg_emp)
    elif len(ins) == 4 and (ins[0] == "/float"):
        reg1 = get_reg(ins[2])
        reg2 = get_reg(ins[3])
        reg_emp = get_empty_register("float")
        asm.write("div.s " + reg_emp + "," + reg1 + "," + reg2 + "\n")
        handle_assign(ins[1],reg_emp)
    elif len(ins) == 4 and ins[0] == "&&":
        reg1 = get_reg(ins[2])
        reg2 = get_reg(ins[3])
        reg_emp = get_name(*get_empty_register())
        asm.write("and " + reg_emp + "," + reg1 + "," + reg2 + "\n")
        handle_assign(ins[1],reg_emp)
        
    elif len(ins) == 4 and ins[0] == "||":
        reg1 = get_reg(ins[2])
        reg2 = get_reg(ins[3])
        reg_emp = get_name(*get_empty_register())
        asm.write("or " + reg_emp + "," + reg1 + "," + reg2 + "\n")
        handle_assign(ins[1],reg_emp)
    # elif len(ins)==4 and (ins[0]=="/" or ins[0]=="/int"):
    #     reg1=get_reg(ins[2])
    #     reg2=get_reg(ins[3])
    #     reg3=get_reg(ins[1])
    #     asm.write("sub " + reg3 + "," +reg1+","+reg2+"\n")

    elif len(ins) == 4 and ins[0] == "iffalse":
        reg = get_reg(ins[1])
        off_load()
        asm.write("beq " + reg + ",$0," + ins[3] + "\n")


def main():
    global set_of_activations
    global code
    global asm
    global cur_reg

    with open('activation.pickle', 'rb') as handle:
        set_of_activations = pickle.load(handle)
    with open('code.pickle', 'rb') as handle:
        code = pickle.load(handle)
    parser = argparse.ArgumentParser(description='A Parser for Golang')
    parser.add_argument(
        '--output', required=True, help='Output file for 3 Address Code')
    args = parser.parse_args()
    asm = open(args.output, 'w+')

    for nam in set_of_activations:
        print nam
        for item in set_of_activations[nam].data:
            print item, set_of_activations[nam].data[item][
                "func_offset"], set_of_activations[nam].data[item][
                    "label"], set_of_activations[nam].data[item]["width"]
        print set_of_activations[nam].total
        print set_of_activations[nam].ret_value_addr
    print "\n"
    global_decl = []
    leng = 0
    for decl in code:
        if len(decl) == 2 and decl[0] in set_of_activations:
            break
        else:
            global_decl.append(decl)
            leng += 1
    for i in range(leng):
        del code[0]

    for ind in range(len(code)):
        if len(code[ind]) == 2 and code[ind][0] == 'main':
            code = code[:ind + 1] + global_decl + [["EndOfDecl", ":"]
                                                   ] + code[ind + 1:]
            break

    for i in range(len(code)):
        for j in range(len(code[i])):
            if type(code[i][j]) == str:
                code[i][j] = code[i][j].strip()

    asm.write(".text\n")
    asm.write(".globl main\n")
    print code

    for ins in code:
        generate_code(ins)
        cur_reg = []


if __name__ == '__main__':
    main()
