import re
import math
import copy
import os

class Node:
    def __init__(self, children, value, leaf):
        self.value = value
        self.leaf = leaf
        self.children = children
    def post_array(self, nodes=[]):
        if not self.leaf:
            for i in range(len(self.children)):
                nodes = [*nodes, *self.children[i].post_array()]
            nodes.append(self.value)
            return nodes
        else:
            return [self.value]

    def __repr__(self):
        return self.value

def form_tree(nodes, inst):
    value = nodes.pop(0)
    for i in range(len(inst)):
        if value in inst[i]:
            children = [None] * (i+1)
            for j in range(i+1):
                children[j] = form_tree(nodes, inst)
            newNode = Node(children, value, False)
            return newNode
    else:
        newNode = Node(None, value, True)
        return newNode

def write_post_line(file, tree):
    reverse_nodes = tree.post_array()
    print(reverse_nodes)
    First = True
    for item in reverse_nodes:
        if First:
            First = False
        else:
            file.write(", ")
        file.write("%s" % item)
    file.write("\n")
    print("\n")

def create_opcode_set(instorder, args, constants, datasize):
    get_bin = lambda x: format(x, 'b').zfill(datasize)
    opcodes = list(range(0, 2**datasize))
    opcodes = list(map(get_bin, opcodes))
    values = ["NULL", *instorder, *args, *constants]
    pad = [0]*(len(opcodes) - len(values))
    values = [*values, *pad]
    zip_iterator = zip(values, opcodes)
    opcode_set = dict(zip_iterator)
    return opcode_set
    
def write_mif(opcode_set, nodes, datasize, maxlength, title):
    mif_file = open(title, 'w')
    mif_file.write("WIDTH = " + str(datasize) + ";\n")
    mif_file.write("DEPTH = " + str(maxlength) + ";\n\n")
    mif_file.write("ADDRESS_RADIX = HEX;\nDATA_RADIX = HEX;\n\nCONTENT BEGIN\n")
    for i in range(maxlength):
        if i < len(nodes):
            #print(nodes[i] + "\n")
            #print(opcode_set[nodes[i]] + "\n")
            mif_file.write(hex(i)[2:].upper() + ": " + hex(int(opcode_set[nodes[i]],2))[2:].upper() + ";\n")
        else:
            mif_file.write(hex(i)[2:].upper() + ": " + "0;\n")
    mif_file.close()



if not os.path.exists('./mifs'):
    os.makedirs('./mifs')
file1 = open('input.txt', 'r')
Lines = file1.readlines()
print('\n')
file1.close()
 
count = 0
inst = [["sin", "cos", "tan", "neg"], ["add", "sub", "mul", "protectedDiv"], ["if"]]
instorder = ["add", "cos", "protectedDiv", "if", "mul", "neg", "sin", "sub", "tan"]
args = ["ARG0", "ARG1", "ARG2"]
constants = ["1", "2", "3", "-4", "7", "-1", "5"]
datasize = math.ceil(math.log2(len(instorder) + len(args) + len(constants) + 1))
#print(datasize)
maxlength = 256
opcode_set = create_opcode_set(instorder, args, constants, datasize)
#print(opcode_set)

file2 = open('output.txt', 'w')

for line in Lines:
    if(line != '\n' and line[0] != '#'):
        #print("Line{}: {}".format(count, line.strip()))
        nodes = re.split(r',|\(|\)|\s+', line)
        nodes = list(filter(None, nodes))
        nodes2 = copy.deepcopy(nodes, memo=None, _nil=[])
        #print(nodes)
        tree = form_tree(nodes, inst)
        #print(tree)
        write_mif(opcode_set, nodes2, datasize, maxlength, "./mifs/test_case" + str(count) + ".mif")
        #write_post_line(file2, tree)
        count += 1
        

        
file2.close()


