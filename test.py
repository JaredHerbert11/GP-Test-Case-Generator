import re
import math
import copy
import os

class Node:
    def __init__(self, children, value, leaf):
        self.value = value
        self.leaf = leaf
        self.children = children
    def reverse_notation(self, nodes=[]):
        if not self.leaf:
            for i in range(len(self.children)):
                nodes = [*nodes, *self.children[i].reverse_notation()]
            nodes.append(self.value)
            return nodes
        else:
            return [self.value]

    def __repr__(self):
        return self.value

def form_program(nodes, function_arity_map):
    value = nodes.pop(0)
    for i in range(len(function_arity_map)):
        if value in function_arity_map[i]:
            children = [None] * (i+1)
            for j in range(i+1):
                children[j] = form_program(nodes, function_arity_map)
            newNode = Node(children, value, False)
            return newNode
    else:
        newNode = Node(None, value, True)
        return newNode

def write_reverse_notation(file, program):
    reverse_nodes = program.reverse_notation()
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

def create_opcodes(function_set, variable_terminals, \
                   constant_terminals, opcode_width):
    get_bin = lambda x: format(x, 'b').zfill(opcode_width)
    opcodes = list(range(0, 2**opcode_width))
    opcodes = list(map(get_bin, opcodes))
    values = ["NULL", *function_set, *variable_terminals, *constant_terminals]
    pad = [0]*(len(opcodes) - len(values))
    values = [*values, *pad]
    zip_iterator = zip(values, opcodes)
    opcodes = dict(zip_iterator)
    return opcodes
    
def write_mif(opcodes, nodes, opcode_width, maxlength, file_name):
    mif_file = open(file_name, 'w')
    mif_file.write("WIDTH = " + str(opcode_width) + ";\n")
    mif_file.write("DEPTH = " + str(maxlength) + ";\n\n")
    mif_file.write("ADDRESS_RADIX = HEX;\n")
    mif_file.write("DATA_RADIX = HEX;\n\nCONTENT BEGIN\n")
    for i in range(len(nodes)):
        #print(nodes[i] + "\n")
        #print(opcodes[nodes[i]] + "\n")
        mif_file.write(hex(i)[2:].upper() + " : ")
        mif_file.write(hex(int(opcodes[nodes[i]],2))[2:].upper() + ";\n")
    mif_file.write("[" + hex(len(nodes))[2:].upper() + ", ")
    mif_file.write(hex(maxlength-1)[2:].upper() + "] : 0\n")
    mif_file.write("END;")
    mif_file.close()



if not os.path.exists('./mifs'):
    os.makedirs('./mifs')
input_file = open('input.txt', 'r')
lines = input_file.readlines()
print('\n')
input_file.close()
 
program_count = 0
function_set = ["add", "cos", "protectedDiv", "if", "mul", \
                "neg", "sin", "sub", "tan"]
function_arity_map = [["sin", "cos", "tan", "neg"], \
                      ["add", "sub", "mul", "protectedDiv"], ["if"]]
variable_terminals = ["v0", "v1", "v2"]
constant_terminals = ["1", "2", "3", "-4", "7", "-1", "5"]
terminal_set = [*variable_terminals, *constant_terminals]
opcode_width = math.ceil(math.log2(len(function_set) + \
                                   len(variable_terminals) + \
                                   len(constant_terminals) + 1))
#print(opcode_width)
maxlength = 256
opcodes = create_opcodes(function_set, variable_terminals, \
                         constant_terminals, opcode_width)
#print(opcodes)

output_file = open('output.txt', 'w')
for line in lines:
    if(line != '\n' and line[0] != '#'):
        #print("Line{}: {}".format(program_count, line.strip()))
        nodes = re.split(r',|\(|\)|\s+', line)
        nodes = list(filter(None, nodes))
        nodes2 = copy.deepcopy(nodes, memo=None, _nil=[])
        #print(nodes)
        program = form_program(nodes, function_arity_map)
        #print(program)
        write_mif(opcodes, nodes2, opcode_width, maxlength, \
                  "./mifs/test_case" + str(program_count) + ".mif")
        #write_reverse_notation(output_file, program)
        program_count += 1
        

        
output_file.close()


