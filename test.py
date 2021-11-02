import re
import math
import copy
import os

class Node:
    """Node class defines one node in a program tree. Node can either be a 
    function or terminal value. This class is used to point to a full tree."""
    def __init__(self, children, value, leaf):
        """Node Arguments:
        children -- variable length array containing this nodes children. 
            length of array corresponds with this node's arity. If this node is a 
            leaf, this array is empty.
        value -- string referring to the node's value. Can be a function 
            or terminal
        leaf -- boolean value referring to whether node is a leaf/terminal"""
        self.value = value
        self.leaf = leaf
        self.children = children
    def reverse_notation(self, nodes=[]):
        """Returns postfix node order from specified node"""
        if not self.leaf:
            for i in range(len(self.children)):
                nodes = [*nodes, *self.children[i].reverse_notation()]
            nodes.append(self.value)
            return nodes
        else:
            return [self.value]

    def __repr__(self):
        return self.value

def form_program_tree(nodes, function_arity_map):
    """Takes prefix node array and arity map as arguments and returns a node
    that is the root of a program tree"""
    value = nodes.pop(0)
    for i in range(len(function_arity_map)):
        if value in function_arity_map[i]:
            children = [None] * (i+1)
            for j in range(i+1):
                children[j] = form_program_tree(nodes, function_arity_map)
            newNode = Node(children, value, False)
            return newNode
    else:
        newNode = Node(None, value, True)
        return newNode

def write_reverse_notation(program_trees):
    postfix_file = open('postfix.txt', 'w')
    """Takes a list of program trees as input and writes values in
    postfix order to the file"""
    for program_tree in program_trees:
        reverse_nodes = program_tree.reverse_notation()
        First = True
        for item in reverse_nodes:
            if First:
                First = False
            else:
                postfix_file.write(", ")
            postfix_file.write("%s" % item)
        postfix_file.write("\n")
    postfix_file.close()

def create_opcodes(function_set, terminal_set, opcode_width):
    """Takes arrays containing the function and terminal sets as well the
    opcode length and returns an opcode set. This opcode set is a map where
    a string of a function or terminal name is the key, and the value is an
    opcode."""
    get_bin = lambda x: format(x, 'b').zfill(opcode_width)
    opcodes = list(range(0, 2**opcode_width))
    opcodes = list(map(get_bin, opcodes))
    values = ["NULL", *function_set, *terminal_set]
    pad = [0]*(len(opcodes) - len(values))
    values = [*values, *pad]
    zip_iterator = zip(values, opcodes)
    opcodes = dict(zip_iterator)
    return opcodes

def write_mif(opcodes, prefix_programs, opcode_width, max_length, file_name):
    """Takes an opcode map, an array of prefix program arrays, the opcode 
    width, the max length of a mif file, and the name of the mif file to be
    created. This function writes all of the programs in prefix_programs to
    a .mif file located in the mifs directory. The mif file has hex addresses
    and data values. Programs are separated by a zero (NULL value). Unused
    space is padded with NULLs"""
    mif_file = open(file_name, 'w')
    mif_file.write("WIDTH = " + str(opcode_width) + ";\n")
    mif_file.write("DEPTH = " + str(max_length) + ";\n\n")
    mif_file.write("ADDRESS_RADIX = HEX;\n")
    mif_file.write("DATA_RADIX = HEX;\n\nCONTENT BEGIN\n")
    address = 0
    data_digits = math.ceil(opcode_width/4)
    addr_digits = math.ceil(math.log2(max_length)/4)
    for nodes in prefix_programs:
        for i in range(len(nodes)):
            mif_file.write("{0:0{1}X}".format(address, addr_digits) + " : ")
            mif_file.write("{0:0{1}X}".format(int(opcodes[nodes[i]],2), \
                data_digits) + ";\n")
            address = address + 1
        mif_file.write("{0:0{1}X}".format(address, addr_digits) + " : " + \
            "{0:0{1}X}".format(0, data_digits) + ";\n")
        address = address + 1
    if (address < max_length - 1):
        mif_file.write("[" + "{0:0{1}X}".format(address, addr_digits) + ", ")
        mif_file.write("{0:0{1}X}".format(max_length-1, addr_digits) + \
             "] : " + "{0:0{1}X}".format(0, data_digits) + ";\n")
    elif (address == max_length - 1):
        mif_file.write("{0:0{1}X}".format(address, addr_digits) + " : " + \
            "{0:0{1}X}".format(0, data_digits) + ";\n")
    mif_file.write("END;")
    mif_file.close()



# create mifs directory if it doesn't exist
if not os.path.exists('./mifs'):
    os.makedirs('./mifs')

# retrieve test equations from input file
input_file = open('input.txt', 'r')
lines = input_file.readlines()
input_file.close()
 

#define function set and arities
function_set = ["add", "cos", "protectedDiv", "if", "mul", \
                "neg", "sin", "sub", "tan"]
function_arity_map = [["sin", "cos", "tan", "neg"], \
                      ["add", "sub", "mul", "protectedDiv"], ["if"]]


#Retrieve terminal set from appropriate text file
terminal_set_file = open('terminal_set.txt', 'r')
terminal_set_line = terminal_set_file.readlines()
terminal_set = re.split(r',|\(|\)|\s+', terminal_set_line[0])
terminal_set = list(filter(None, terminal_set))
terminal_set_file.close()

#Calculate opcode width
opcode_width = math.ceil(math.log2(len(terminal_set) + len(function_set) + 1))

#Define how many nodes a program can have and how many can be in a mif file
max_program_size = 63
population_size = 8
max_length = (max_program_size + 1) * population_size

#Generate opcode map
opcodes = create_opcodes(function_set, terminal_set, opcode_width)

#Parse through input equations and write to prefix_programs list
prefix_programs = []
program_tree_list = []
for line in lines:
    if(line != '\n' and line[0] != '#'):
        #obtain prefix nodes from lines
        nodes = re.split(r',|\(|\)|\s+', line)
        nodes = list(filter(None, nodes))
        nodes2 = copy.deepcopy(nodes, memo=None, _nil=[])

        #add nodes to prefix programs
        prefix_programs.append(nodes2)

        #generate prorgam tree and add to list
        program_tree = form_program_tree(nodes, function_arity_map)
        program_tree_list.append(program_tree)
        

write_reverse_notation(program_tree_list)
write_mif(opcodes, prefix_programs, opcode_width, max_length, \
                  "./mifs/test_cases.mif")


