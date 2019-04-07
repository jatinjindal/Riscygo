import pickle
import argparse
import random
import re

set_of_activations = []
struct_length = {}
code = []
current_activation = "global"
reg_map = [[None] * 10, [None] * 8]
asm = None
cur_reg=[]
first_func=0


class activation_record:
    def __init__(self, previous=None):
        self.previous = previous
        self.label = "global"
        self.data = {}


def get_name(ind1, ind2):
    if ind1 == 0:
        return "$t" + str(ind2)
    else:
        return "$s" + str(ind2)


def get_empty_register(set_name=None):
    global asm
    global set_of_activations
    global current_activation
    # Pick from temporary
    for x in range(0, 10):
        if reg_map[0][x] == None and (0,x) not in cur_reg:
            reg_map[0][x] = set_name
            cur_reg.append((0,x))
            return (0, x)
    # Pick from saved
    for x in range(0, 8):
        if reg_map[1][x] == None and (0,x) not in cur_reg:
            reg_map[1][x] = set_name
            cur_reg.append((1,x))
            return (1, x)

    ind1 = random.randint(0, 1)
    if ind1 == 0:
        ind2 = random.randint(0, 9)
    else:
        ind2 = random.randint(0, 7)
    
    while((ind1,ind2) in cur_reg):
        ind1 = random.randint(0, 1)
        if ind1 == 0:
            ind2 = random.randint(0, 9)
        else:
            ind2 = random.randint(0, 7)
        

    record = set_of_activations[current_activation].data[reg_map[ind1][ind2]]
    set_of_activations[current_activation].data[reg_map[ind1][ind2]]["isreg"] = -1
    if record["label"] == "global":
        asm.write("sw " + get_name(ind1, ind2) + "," +
                   str(-record["func_offset"]) + "($v1)\n")
    else:
        asm.write("sw " + get_name(ind1, ind2) + "," +
                   str(-record["func_offset"]) + "($fp)\n")

    reg_map[ind1][ind2] = set_name
    cur_reg.append((ind1,ind2))
    return (ind1, ind2)


def get_reg(name):
    global set_of_activations
    global current_activation

    if name in set_of_activations[current_activation].data:
        record = set_of_activations[current_activation].data[name]
        if record["isreg"] != -1:
            cur_reg.append(record["isreg"])
            return get_name(record["isreg"][0], record["isreg"][1])
        else:
            reg = get_empty_register(name)
            set_of_activations[current_activation].data[name]["isreg"] = reg
            return get_name(reg[0], reg[1])
    else:
        reg = get_empty_register()
        return get_name(reg[0],reg[1])

def get_rec(name):
    global set_of_activations
    global current_activation
    print name
    print len(name)
    if name in set_of_activations[current_activation].data:
        return set_of_activations[current_activation].data[name]
    else:
        return set_of_activations["global"].data[name] 


def handle_assign(dst, src):
    global asm
    # TODO: Handle floating point registers
    assert(dst[:3] == "var")
    if type(src) == str:
        assert(src[:3] == "var")
        reg = get_reg(src)
        # rec1, rec2 = get_rec(dst), get_rec(src)
        # width = 0
        # while rec1['width'] - width > 0:
        #     asm.write("lw " + reg + "," + str(-(rec2["func_offset"] + width)))
        #     if record["label"] == "global":
        #         asm.write("($v1)\n")
        #     else:
        #         asm.write("($fp)\n")
        #     asm.write("sw " + reg + "," + str(-(rec1["func_offset"] + width)))
        #     if record["label"] == "global":
        #         asm.write("($v1)\n")
        #     else:
        #         asm.write("($fp)\n")
        #     width += 4
    elif type(src) == int or type(src) == float:
        reg = get_name(get_empty_register()[0],get_empty_register()[1])
        asm.write("li " + reg+","+str(src)+"\n")
        

    if dst[:3] == "var":
        rec = get_rec(dst)
        asm.write("sw " + reg + "," + str(-rec["func_offset"]))
        if rec["label"] == "global":
            asm.write("($v1)\n")
        else:
            asm.write("($fp)\n")
    elif dst[0] == "*":
        reg2 = get_name(get_empty_register()[0],get_empty_register()[1])
        rec = get_rec(dst[1:])
        asm.write("lw " + reg2 + "," + str(-rec["func_offset"]))
        if rec["label"] == "global":
            asm.write("($v1)\n")
        else:
            asm.write("($fp)\n")
        asm.write("sw " + reg + ",0("+reg2+")\n")
    elif dst[-1] == "]":
        dst_nam = dst.split("[")[0]
        index = dst.split("[")[1][:-1]
        rec = get_rec(dst_nam)
        if rec["width"]==0:
            reg2 = get_name(get_empty_register()[0],get_empty_register()[1])
            reg_index = get_reg(index)
            asm.write("addi " + reg2 + ","+reg_index+","+str(-rec["func_offset"])+"\n")
            if rec["label"] == "global":
                asm.write("sub "+reg2+",$v1,"+reg2+"\n")
            else:
                asm.write("sub "+reg2+",$fp,"+reg2+"\n")
            asm.write("sw " + reg + ",0("+reg2+")\n")
            




def generate_code(ins):
    global first_func
    global set_of_activations
    global current_activation

    if ins[0] == "=":
        assert(len(ins) == 3)
        handle_assign(ins[1], ins[2])
    elif len(ins) == 2 and first_func == 0:
        first_func = 1
        #do a function call to save current registers
        current_activation=ins[0]
        asm.write("addi $sp,$sp,-4\n")
        asm.write("sw $ra,0($sp)\n")
        asm.write("jal main\n")
        asm.write("goto end\n")
    elif len(ins)==2 and ins[0] in set_of_activations:
        asm.write(ins[0]+ins[1]+"\n")
        current_activation=ins[0]
        asm.write("mov $fp,$sp\n")
        asm.write("addi $sp,$sp,"+str(-set_of_activations[current_activation].total)+"\n")


def main():
    global set_of_activations
    global struct_length
    global code
    global asm

    with open('activation.pickle', 'rb') as handle:
        set_of_activations = pickle.load(handle)
    with open('struct.pickle', 'rb') as handle:
        struct_length = pickle.load(handle)
    with open('code.pickle', 'rb') as handle:
        code = pickle.load(handle)
    parser = argparse.ArgumentParser(description='A Parser for Golang')
    parser.add_argument(
        '--output', required=True, help='Output file for 3 Address Code')
    args = parser.parse_args()
    asm = open(args.output, 'w+')


    print "global_struct_length"
    for nam in struct_length:
        print nam,struct_length[nam]
    for nam in set_of_activations:
        print nam
        for item in set_of_activations[nam].data:
            print item,set_of_activations[nam].data[item]["func_offset"],set_of_activations[nam].data[item]["label"],set_of_activations[nam].data[item]["width"]
        print set_of_activations[nam].total
    print "\n"
    print code

    asm.write(".text\n")
    asm.write("mov $v1,$sp\n")
    asm.write("mov $fp,$sp\n")
    asm.write("addi $sp,$sp,"+str(-set_of_activations["global"].total)+"\n")
    for ins in code:
        generate_code(ins)
        cur_reg=[]

    asm.write("end:\n")
    asm.write("lw $ra,0($sp)\n")
    asm.write("addi $sp,$sp,4\n")
    asm.write("addi $sp,$sp,"+str(set_of_activations["global"].total)+"\n")
    asm.write("jr $ra\n")



if __name__ == '__main__':
    main()