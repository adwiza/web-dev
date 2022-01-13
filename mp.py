import objgraph
# from guppy import hpy
#
# h = hpy()
#
# print(h.heap())

x = []
y = [x, [x], dict(x=x)]
objgraph.show_refs([y], filename='sample-graph.png')
