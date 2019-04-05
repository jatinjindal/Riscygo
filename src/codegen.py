import pickle
import argparse
import random
import re


set_of_activations=[]
struct_length={}
code=[]
current_activation="global"
reg_map=[[None,None,None,None,None,None,None,None,None,None],[None,None,None,None,None,None,None,None]]


class activation_record:
    def __init__(self,previous=None):
        self.previous=previous
        self.label="global"
        self.data={}

def get_name(ind1,ind2):
	if ind1==0:
		return "$t"+str(ind2)
	else:
		return "$s"+str(ind2)

def get_empty_register(file,set_name=None):
	for x in range(0,10):
		if reg_map[0][x]==None:
			reg_map[0][x]=set_name
			return (0,x)
	for x in range(0,8):
		if reg_map[0][x]==None:
			reg_map[0][x]=set_name
			return (1,x)
	ind1=random.randint(0,1)
	if ind1==0:
		ind2=random.randint(0,9)
	else:
		ind2=random.randint(0,7)
	record=set_of_activations[current_activation].data[reg_map[ind1][ind2]]
	record["isreg"]=-1
	if record["label"]=="global":
		file.write("sw "+get_name(ind1,ind2)+","+str(record["func_offset"])+"($v1)\n")
	else:
		file.write("sw "+get_name(ind1,ind2)+","+str(record["func_offset"])+"($fp)\n")

	reg_map[ind1][ind2]=set_name
	return (ind1,ind2)




def getreg(file,name):
	record=set_of_activations[current_activation].data[name]
	if record["isreg"]!=-1:
		return get_name(record["isreg"][0],record["isreg"][1])
	else:
		reg=get_empty_register(file,name)
		set_of_activations[current_activation].data[name]["isreg"]=reg
		return get_name(reg[0],reg[1])




def generate_code(file):
	for ins in code[]:
		if len(ins) == 3:
			if ins[0][0] == "=":
				if ins[1][0]=="t" and ins[2][0]=="t":
					reg1=getreg(file,ins[1])
					reg2=getreg(file,ins[2])
					file.write("mov "+str(ins[1])+","+str(ins[2]))
				elif ins[1][0]=="v" and ins[2][0]=="t":
					reg1=getreg(file,ins[2])
					record=set_of_activations[current_activation].data[ins[1]]
					if record["label"]=="global":
						file.write("sw "+reg1+","+str(record["func_offset"])+"($v1)\n")
					else:
						file.write("sw "+reg1+","+str(record["func_offset"])+"($fp)\n")
				elif ins[1][0]=="v" and ins[2][0]=="v":
					record1=set_of_activations[current_activation].data[ins[1]]
					record2=set_of_activations[current_activation].data[ins[2]]
					width=record1["width"]
					reg_ind=get_empty_register(file,None)
					reg=get_name(reg_ind[0],reg_ind[1])
					while width>0:
						if record2["label"]=="global":
							file.write("lw "+reg+","+str(record2["func_offset"])+"($v1)\n")
						else:
							file.write("lw "+reg+","+str(record2["func_offset"])+"($fp)\n")

						if record1["label"]=="global":
							file.write("lw "+reg+","+str(record1["func_offset"])+"($v1)\n")
						else:
							file.write("lw "+reg+","+str(record1["func_offset"])+"($fp)\n")
						width=width/4
				elif ins[1][0]=="t" and re.match("^\d+?\.\d+?$", ins[2]) is  None:
					reg=getreg(file,ins[1])
					file.write("li "+reg+","+ins[2])











def main():
	global set_of_activations
	global struct_length
	global code

	with open('activation.pickle', 'rb') as handle:
		set_of_activations=pickle.load(handle)
	with open('struct.pickle', 'rb') as handle:
		struct_length=pickle.load(handle)
	with open('code.pickle', 'rb') as handle:
		code=pickle.load(handle)
	parser = argparse.ArgumentParser(description='A Parser for Golang')
	parser.add_argument('--output', required=True, help='Output file for 3 Address Code')
	args = parser.parse_args()
	ass = open(args.output, 'w+')
	ass.write(".text\n")
	ass.write("mov $v1,$sp\n")
	ass.write("mov $fp,$sp\n")
	generate_code(ass)

	# print "global_struct_length"
	# for nam in struct_length:
	#     print nam,struct_length[nam]
	# for nam in set_of_activations:
	# 	print nam
	# 	for item in set_of_activations[nam].data:
	# 		print item,set_of_activations[nam].data[item]["func_offset"],set_of_activations[nam].data[item]["type"],set_of_activations[nam].data[item]["label"]
	# print "\n"
	# print code


if __name__ == '__main__':
    main()
