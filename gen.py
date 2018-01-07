from quakeheaps import *
import sys

if len(sys.argv) < 2:
    print("Usage: python gen.py [number_of_nodes]")
    sys.exit(0);
q = QuakeHeap()
for i in range(int(sys.argv[1])):
    q.insert(i)

q.extract_min()

q.dump("tree_data.json")

