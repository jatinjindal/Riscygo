import pickle
set_of_activations=[]
struct_length={}
code=[]

class activation_record:
    def __init__(self,previous=None):
        self.previous=previous
        self.label="global"
        self.data={}

def getreg(name):
	print "start"



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

	# print "activation records"
	# for cur_activation in set_of_activations:
	# 	print cur_activation.label
	# 	for nam in cur_activation.data:
	# 		print nam,cur_activation.data[nam]["offset"],cur_activation.data[nam]["type"],cur_activation.data[nam]["width"],cur_activation.data[nam]["label"],cur_activation.data[nam]["func_offset"]
	# 	print "\n"
	# print "global_struct_length"
	# for nam in struct_length:
	#     print nam,struct_length[nam]
	for nam in set_of_activations:
		print nam,set_of_activations[nam]
	print "\n"
	print code


if __name__ == '__main__':
    main()
