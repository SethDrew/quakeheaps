""" This function is O(N), must be O(1). Rethink tree repr to allow cut in const time
"""

#needs to be an object so that it can be copied
class Value():
    def __init__(self, value, ancestors):
        self.value = value
        self.ancestors = ancestors #IMPORTANT IMPL DETAIL: this goes here so it can be copied and changed on o(1) after every merge for the whole path.

    def __lt__(self, other):
        return self.value < other.value
    def set(self, value):
        self.value = value

class Node():

    
    def __init__(self, value, children, ancestors = [], levels = []):
        if isinstance(value, Value):
            self.value = value
        else:
            self.value = Value(value, ancestors)

        self.children = children #array to support one or two children
        self.height = -1         #tree height. Only used at root.
    def __lt__(self, other):
        return self.value < other.value

    def get_ancestors(self):
        return self.value.ancestors
        #array of copies as far as it's copied up the tree. arr is maintained from bottom to top. 
        #Last entry is the next node that is not a copy.
    def get_children(self):
        return self.children
    #debug function, gets all descendents incuding the original parent
    def all_descendents(self):
        children = [self]

        path = [self]
        while len(path) > 0:
            cur = path.pop(0)
            for n in cur.children:
                children.append(n)
                path.append(n)

        return children

    def copy_child(self):
        for child in self.children:
            if child.value is self.value:
                return child
        return None
    def off_child(self):
        for child in self.children:
            if child.value is not self.value:
                return child
        return None
    def remove_child(self, node): 
        self.children.remove(node)
        return node
    def remove_ancestor(self, node):
        self.value.ancestors.remove(node)  

    def __str__(self):
        return "<Node {}> {}".format(id(self), self.value.value)
    def __repr__(self):
        return self.__str__()

"""
Notes: node.remove_child() deletes all neccessary pointers from top of tree to children
       node.remove_ancestor() deletes all pointers back up the tree

       When cutting a node out of a tree, both of these must be used to give the node a clean slate for it's new home
            - must call remove_child() and remove_ancestors() when creating a new tree

"""


class QuakeHeap():
    alpha = .75
    def __init__(self):
        self.trees = []
        self.levels = [0]
    def insert(self, x):
        self.levels[0] += 1
        return self._add_tree(Node(x, [], [], [1]), 1)

    def decrease_key(self, node, k): # Spawns one new tree. No need to adjust levels because we just cut and update.
        ancestors = node.get_ancestors()
        height = len(ancestors)
        if height > 0:
            parent = ancestors[0]
            if parent.value is not node.value: #if the node is not a root of a tree
                newroot = parent.off_child()
                parent.remove_child(newroot)
                newroot.remove_ancestor(parent) 
                self._add_tree(newroot, len(newroot.get_ancestors()) + 1)  #we're cutting: we need to change height param
                newroot.value.set(k)  #node is lowest value in tree, just set it to the value we want
                return newroot

        node.value.set(k)  #node is lowest value in tree, just set it to the value we want
        return node

    def extract_min(self):
        #Cut along the path
        min_node = self._find_min_node()
        for i in range(min_node.height):
            self.levels[i] -= 1

        return self._delete(min_node)

    def min(self):
        return min(self.trees).value.value
    
    def _delete(self, node): # Spawns h new trees where h is the height to the bottom from the node we are deleting. We also use this time to link the trees 
        self.trees.remove(node) #IMPL DETAIL: Delete never called on something that's not a root. Delete_min is only delete op that QH support
        ancestors = node.get_ancestors()
        for i in range(len(ancestors)-1, -1, -1):
            newroot = ancestors[i].off_child() #get child that is not a copy and make a new tree from it
            if(newroot):
                ancestors[i].remove_child(newroot)
                newroot.remove_ancestor(ancestors[i])
                self._add_tree(newroot, len(newroot.get_ancestors()) + 1) #adjust tree height based on what level removed from node
                # print("After delete of {}: Making new tree with root: {} and height: {}".format(node, newroot, newroot.height))
        #self.run_quake()
        self._link_trees()
        return node.value.value
    
    def _cut_above(self, level, node, curlevel, newtrees):
        if curlevel == level: #at l1 nodes
            newtrees.append(node)

        elif curlevel > level: #still above l1, recurse lower
            for child in node.children:

                child.remove_ancestor(node)
                self._cut_above(level, child, curlevel - 1, newtrees)

    def run_quake(self): #this is for vis to have control over quake
        self._quake(self.quake_test()) 

    def quake_test(self):
        for i in range(len(self.levels) - 1):
            l1 = self.levels[i]
            l2 = self.levels[i+1]
            if l1 * self.alpha < l2 and l2 != 0: #quake condition 
                print("Quake condition on levels = {}".format(self.levels))
                return i+1

        return -1

    def _quake(self, chop_level):
        if chop_level > -1: 
            newtrees = []
            print("QUAAAAKEEEE on level {}".format(chop_level))
            self.levels = self.levels[:chop_level]
            print "new levels after slice: {}".format(self.levels)
            for tree in self.trees:
                print("considering root of tree {} with height {}".format(tree.value.value, tree.height)) 
                if tree.height > chop_level: 
                    self._cut_above(chop_level - 1, tree, tree.height -1, newtrees) #put its children back
            self.trees = newtrees
        else:
            pass

    def _link_trees(self):
        # height_table = [None] * self.levels[-1] #number of nodes at leaf level should be big enough. improvement todo
        height_table = [None] * 1000
        to_link = [t for t in self.trees]

        while len(to_link) > 0:
            tree = to_link.pop()
            # print ("looking at {} with height {}".format(tree, tree.height))
            # print("self.trees = {}".format(self.trees))
            # print([(x, x.height) for x in height_table if x is not None])
            if height_table[tree.height] is not None:
                to_link.append(self._merge(height_table[tree.height], tree)) #appends merged to the end of the list
                height_table[tree.height] = None
            else:
                height_table[tree.height] = tree

    def _find_min_node(self):
        assert len(self.trees) > 0
        return min(self.trees)

    def _add_tree(self, node, height):
        self.trees.append(node)
        node.height = height
        return node

    #return the merge of two trees with the same height
    def _merge(self, t1, t2):
        # print ("merging {}, {}".format(t1, t2))
        assert t1.height == t2.height 
        
        winner = t2
        loser = t1
        if t1.value < t2.value:
            winner = t1
            loser = t2
            #t1 root wins, so put a copy of value at root

        newroot = Node(winner.value, [winner, loser]) #value copy of winner, children of both competitors

        newroot.height = winner.height+1

        if len(self.levels) + 1 == newroot.height:
            self.levels.append(0);
        self.levels[newroot.height-1] += 1

        #height left undefined for non roots
        

        winner.get_ancestors().insert(0,newroot) 
        loser.get_ancestors().insert(0,newroot) #last entry is next node not a copy, so we need to include this

        self.trees.remove(loser)
        self.trees.remove(winner)
        self.trees.append(newroot)


        return newroot

    def show(self):
        print("------BEGIN QH---------")
        for tree in self.trees:
            print("-------------------")
            # print("({}, {}, {}) --> {}".format(tree, tree.get_children(), tree.get_ancestors(), 0))
            # print("{} --> {}".format(tree, 0))
            print("{} --> {}, height = {}".format(tree, 0,tree.height))
            self._rec_print(tree, 1)

        print("--------END QH--------")

    def _rec_print(self, node, level):
        for child in node.get_children():
            # print("({}, {}, {}) --> {}".format(child, child.get_children(), child.get_ancestors(), level))
            # print("{} --> {}".format(child, level))
            print("{} --> {}".format(child, level,child.height))
        for child in node.get_children():
            self._rec_print(child, level+1)

    def _tree_print(self):
        for tree in self.trees:
            print("-------------------")
            for node in tree.all_descendents():
                print(node, node.value.value)
    def dumpf(self,file):
        import json
        qh = self.dump()
        with open(file, 'w') as f:
            f.write(json.dumps(qh, indent=2))
    def dump(self):
        qh = []
        for tree in self.trees:
            qh.append({
                    "name":tree.value.value,
                    "height":tree.height,
                    "children":self._rec_dump(tree)  #recurse on that node to finish all it's children
                    }) 
        return {"all":qh}
                    

    def _rec_dump(self, parent):
        nodes = []
        for child in parent.get_children():
            nodes.append({
                "name":child.value.value,
                "children":self._rec_dump(child)
                })
        return nodes





# q = QuakeHeap()
# for i in range(10):
#     q.insert(i)

# q.extract_min()
# q.show()

# # q._merge(q.trees[0], q.trees[1])
# # q._merge(q.trees[0], q.trees[1])
# # q._merge(q.trees[0], q.trees[1])


# # q.show()
# # q.decrease_key(to_cut, 2)

# while len(q.trees) > 0:
#     print("Extracted min: {}".format(q.extract_min()))
