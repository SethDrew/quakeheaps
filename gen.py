from quakeheaps import *
from quakeheaps import Node
import sys
import random
import cPickle as pickle

# if len(sys.argv) < 2:
#     print("Usage: python gen.py [number_of_nodes]")
#     sys.exit(0);
# q = QuakeHeap()
# num = int(sys.argv[1])
# for i in random.sample(range(1, num*10), num):
#     q.insert(i)

# with open("curvals.txt", 'w') as f:
#     pickle.dump(q, f)


# q.extract_min() #triggers merging the heaps so they are merged in the viz

# q.dumpf("tree_data.json")


def writeheap(q, values):
    try:
        with open("qh.pickle", "r") as f1:
            with open("qh_old.pickle", "wb") as f2:
                for line in f1:
                    f2.write(line)
    except FileNotFoundError:
        pass

    with open("qh.pickle", 'wb') as f:
        pickle.dump((q, values), f)

def readheap():
    with open("qh.pickle", "r") as f:
        return pickle.load(f)

def read_oldheap():
    with open("qh_old.pickle", "r") as f:
        return pickle.load(f)



def create_heap(num):
    q = QuakeHeap()
    values = {}
    for i in random.sample(range(1, 1 + num*10), num):
        node = q.insert(i)
        values.setdefault(i, node)
    writeheap(q, values)
   
    return q.dump()

def update_heap(num):
    q, values = readheap()

    insert_range = set(range(10 * (1+ num + q.levels[0]))) 
        # (number of new nodes to add + total leaves in qh) (* 10 for good large range)
    used_keys = set(values.keys()) 
    sample_range = insert_range - used_keys #set minus

    for i in random.sample(sample_range, num):
        node = q.insert(i)
        values.setdefault(i, node)

    writeheap(q, values)

    return q.dump()

def revert_heap():
    q, values = read_oldheap()

    writeheap(q, values)

    return q.dump()

def decrease_key(node_val):
    q, values = readheap()

    #for now just choose smallest possible key we can.
    used_keys = set(values.keys())
    keyrange = set(range(node_val)) - used_keys
    k = random.sample(keyrange, 1)[0] 

    q.decrease_key(values[node_val], k)
    values[k] = values.pop(node_val) #change dict key pointing to this node
    writeheap(q, values)

    return k, q.dump()


def extract_min():
    q, values = readheap()

    m = q.extract_min()
    values.pop('m', None)

    writeheap(q, values)

    return m, q.dump(), q.quake_test()
def run_quake():
    q, values = readheap()
    quake_level = q.quake_test()
    assert quake_level > -1

    q.run_quake()

    writeheap(q, values)
    return q.dump(), quake_level




