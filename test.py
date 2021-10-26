import re

class Node:
    def __init__(self, left, right, value, leaf):
        self.value = value
        self.leaf = leaf
        self.left = left
        self.right = right
    def post_array(self, nodes=[]):
        if not self.leaf:
            nodes = [*nodes, *self.left.post_array()]
            nodes = [*nodes, *self.right.post_array()]
            nodes.append(self.value)
            return nodes
        else:
            return [self.value]

    def __repr__(self):
        return self.value

def form_tree(nodes, inst):
    value = nodes.pop(0)
    if value in inst:
        left = form_tree(nodes, inst)
        right = form_tree(nodes, inst)
        newNode = Node(left, right, value, False)
        return newNode
    else:
        newNode = Node(None, None, value, True)
        return newNode

file1 = open('input.txt', 'r')
Lines = file1.readlines()
print('\n')
file1.close();
 
count = 0
inst = ["add", "sub", "mul", "protectedDiv"]

file2 = open('output.txt', 'w')

for line in Lines:
    count += 1
    print("Line{}: {}".format(count, line.strip()))
    nodes = re.split(r',|\(|\)|\s+', line)
    nodes = list(filter(None, nodes))
    print(nodes)
    tree = form_tree(nodes, inst)
    
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
