import sys


def make_graph(g, p, verbose=False):
    #print("Size of p: {}".format(len(p)))
    nodes = set()
    nodes.add( next(iter(p) ))
    #print("First: {}".format(str(nodes)))

    while nodes:
        _nodes = set()
        for n in nodes:
            if n in p:
                g.add(n)
                [ _nodes.add(x) for x in p[n] ]
                p.pop(n)
        nodes = set()
        for n in _nodes:
            if n not in g:
                nodes.add(n)
    if verbose: print("Len of graph: {}".format( len(g))
            
)


if __name__ == "__main__":
    if len(sys.argv) == 2 or len(sys.argv) == 3:
        p = dict()
        [ p.update( { x.split(" <-> ")[0]: list( x.split(" <-> ")[1].split('\n')[0].split(', ')  ) } ) for x in open(sys.argv[1]).readlines() ]
        graph = set()
        make_graph(graph, p, verbose=True)

        if len(sys.argv) == 3:
            c = 1
            while len(p) > 0:
                graph = set()
                make_graph(graph, p)
                c+= 1
            print("## Groups: {}".format(c))
    else:
        print("Use:\n\t'python l12.py file_name' for PART I\n\t'python l12.py file_name 1' for PART II")
