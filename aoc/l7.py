import sys


class Node():

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

        self.depth = None
        self.height = None
        self.sum_weight = None
        self.children = list()
        self.parent = None
        self.bug = False


    def __str__(self):
        _c = ""
        _parent_name = self.parent.name if self.parent != None else "None"
        for c in self.children:
            _c += c.name + ' '
        s = "{name}: w:{w}, sw: {sw}, h:{h}, parent:{pname}, children:{children}".format(
        name=self.name, w=self.weight, sw=self.sum_weight, h=self.height,
          pname=_parent_name, children=_c
        )
        return s

class Tree():

    def __init__(self, nodes, leafs):
        self.nodes = nodes
        self.leafs = leafs

        self.root = None
        self.bug_nodes = set()
        self.__fill()


    def __calc_depth(self, node, depth):
        node.depth = depth
        for c in node.children:
            self.__calc_depth(c, depth+1)


    def __fill_level(self, level, height):
        next_level = set()

        _count = 0
        for _l in level:
            _l.height = height
            _all_children_ok = True
            if _l.parent != None:
                for c in _l.parent.children:
                    if c.sum_weight == None:
                        _all_children_ok = False
                        break
            if _all_children_ok:
                _count += 1
                _parent = _l.parent
                if _parent: # Not root
                    _sum_weight = 0
                    for c in _parent.children:
                        _sum_weight += c.sum_weight
                    _sum_weight += _parent.weight

                    _parent.sum_weight = _sum_weight
                    next_level.add(_parent)
                else:
                    if not self.root:
                        print("[-] Root found: {}".format(str(_l)) )
                        self.root = _l

        print("\tLevel count: {}/{}".format(_count, len(level)))

        return next_level


    def __fill(self):
        level = self.leafs
        #print("### LEAFS:")
        for leaf in self.leafs:
            leaf.sum_weight = leaf.weight
            #print(str(leaf))

        _heigh = 1
        _next_level = self.__fill_level(level, _heigh)

        while(_next_level != set()):
            _heigh += 1
            _next_level = self.__fill_level(_next_level, _heigh)

        self.__calc_depth(self.root, 0)


    def __print_level(self, nodes, level_name):
        print("### {}".format(level_name))
        _next_level = list()

        for _n in nodes:
            print( str(_n) )
            _next_level.extend(_n.children)

        return _next_level

    def print_tree(self):
        _level = [self.root]
        _lv = self.root.depth
        _level_name = "Depth {}".format(_lv)

        while _level != list():
            _level_name = "Depth {}".format(_lv)
            _level = self.__print_level(_level, _level_name)
            _lv += 1


    def __is_bug_in_node(self, node):
        found_bug = False

        if len(node.children) == 1:
            print("[only child] Debug of: ".format(node.children[0]))
        elif len(node.children) == 2:
            if node.children[0].sum_weight != node.children[1].sum_weight:
                self.__print_level(node.children, "([2 children] Debug of '{}".format(node.name))
                found_bug = True
        else:
            _differents = set()

            for i in range( len(node.children)):
                _dif = False
                _dc = 0
                for j in range(len(node.children)):
                    _w1 = node.children[i].sum_weight
                    _w2 = node.children[j].sum_weight
                    if _w1 != _w2:
                        _dc += 1
                    if _dc > 1:
                        _dif = True
                        break
                if _dif == True:
                    _differents.add(node.children[i])
                    found_bug = True
            for d in _differents:
                if d.bug == False:
                    self.bug_nodes.add(d)
                    self.__print_level(_differents, "[Bug found] Debug of '{}'".format(d.name))
                    d.bug = True

        return found_bug


    def __debug_level(self, level):
        next_level = set()

        for node in level:
            if node.parent != None:
                if not self.__is_bug_in_node(node.parent):
                    next_level.add(node.parent)

        return next_level

    def find_bugs(self):
        _next_level = self.leafs

        while _next_level != set():
            _next_level = self.__debug_level(_next_level)

        _min_h = 999
        _low_bug = None
        for bn in self.bug_nodes:
            if bn.height < _min_h:
                _min_h = bn.height
                _low_bug = bn

        # _low_bug
        print("\n# Lowest bug node:\n\t{}".format(str(_low_bug)))
        # parents
        print("# Parent:\n\t{}".format(str(_low_bug.parent)))
        # brothers
        print("# Brothers:")
        _brothers_value = 0
        for b in _low_bug.parent.children:
            if b.name != _low_bug.name:
                print("\t" + str(b))
                _brothers_value = b.sum_weight
        # children
        _children_sum = 0
        print("# Children:")
        for c in _low_bug.children:
            print("\t" + str(c))
            _children_sum += c.sum_weight

        _correct_value = _brothers_value - _children_sum
        print("# Bug correction:")
        print("\tActual: {}. Correct: {} ({} - {})".format(_low_bug.weight, _correct_value, _brothers_value, _children_sum) )

        return list(self.bug_nodes)


def make_tree(file_name):
    nodes = list()
    leafs = list()

    _nodes = [ l.split('\n')[0] for l in tuple(open(file_name)) ]

    for n in _nodes:
        _name = n.split(' ')[0]
        _weight = int(n[n.find('(')+1 : n.find(')')])
        _node = Node(_name, _weight)
        nodes.append(_node)

    for n in _nodes:
        _name = n.split(' ')[0]
        _parts = n.split(' -> ')
        if len(_parts) == 2:
            _children = _parts[1].split(', ')
            _l_children = list()
            _parent_node = None

            # Found nodes children and parent
            for c in _children:
                for _node in nodes:
                    if _node.name == c:
                        _l_children.append(_node)
                    if _node.name == _name:
                        _parent_node = _node
            # Register parent in children nodes
            for c in _l_children:
                if c.parent != None:
                    if c.parent.name != _parent_node.name:
                        print("Two parents")
                    else:
                        print(".")
                c.parent = _parent_node
            # Register children in parent node
            _parent_node.children = _l_children

        else:   # leaf
            node = None
            for _node in nodes:
                if _node.name == _name:
                    node = _node
            leafs.append(node)

    tree = Tree(nodes = nodes, leafs = leafs)

    return tree



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Use: python3 l7.py file_name")
    else:
        tree = make_tree(sys.argv[1])
        tree.find_bugs()
