import re

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

file1 = open('input.txt', 'r')
Lines = file1.readlines()
print('\n')
file1.close();
 
count = 0
inst = [["sin", "cos", "tan", "neg"], ["add", "sub", "mul", "protectedDiv"], ["if"]]

file2 = open('output.txt', 'w')

for line in Lines:
    count += 1
    if(line != '\n' and line[0] != '#'):
        print("Line{}: {}".format(count, line.strip()))
        nodes = re.split(r',|\(|\)|\s+', line)
        nodes = list(filter(None, nodes))
        print(nodes)
        tree = form_tree(nodes, inst)
        #print(tree)

        reverse_nodes = tree.post_array()
        print(reverse_nodes)
        First = True
        for item in reverse_nodes:
            if First:
                First = False
            else:
                file2.write(", ")
            file2.write("%s" % item)
        file2.write("\n")
        print("\n")
file2.close()
