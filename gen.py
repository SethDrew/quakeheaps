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
    with open("qh.pickle", 'wb') as f:
        pickle.dump((q, values), f)

def readheap():
    with open("qh.pickle", "r") as f:
        return pickle.load(f)


def create_heap(num):
    q = QuakeHeap()
    values = set()
    for i in random.sample(range(1, 1 + num*10), num):
        q.insert(i)
        values.add(i)
    writeheap(q, values)
   
    return q.dump()

def update_heap(num):
    q, values = readheap()

    #exclude values from random sample
    for i in random.sample(set(range(1, 1+ num + sum(q.levels))) - values, num):
        q.insert(i)
        values.add(i)

    writeheap(q, values)
    print(q.dump())

    return q.dump()

def extract_min():
    q, values = readheap()

    m = q.extract_min()
    values.remove(m)

    writeheap(q, values)

    return m, q.dump()


