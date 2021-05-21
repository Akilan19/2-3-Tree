
class Node(object):
    def __init__(self, data=[]):
        # items that need to be stored
        self.data = data
        self.left, self.right, self.middle = None, None, None
        self.parent = None
        
    def is_leaf(self):
        if (self.left == None and self.right == None and self.middle == None):
            return True
        assert (self.left == None and self.right == None) or (self.left != None and self.right != None), "Invalid Node"
        return False

    def is_branch(self):
        if (self.is_leaf()) : 
            return False
        elif (len(self.data) == 1):
            assert (self.middle == None), "Invalid Node"
            assert (self.left != None and self.right != None), "Invalid Node"
        elif (len(self.data) == 2):
            assert self.left != None and self.right != None and self.middle != None, "Invalid Node"
        return True

    def insert(self, item):
        if (len(self.data) > 2):
            raise ValueError("Cannot insert more values")
        self.data.append(item)
        self.data.sort() # fast because 3 elements or less in list
        return

class Tree23(object):
    def __init__(self, items=[]):
        self.root = None
        for item in items:
            self.add(item)

        self.length = 0
        self.depth = 0
    
    #### helper functions ####

    # get direction for tree traversal when finding a valid node for adding item
    def getDirection(self, item, node):
        assert node.is_branch(), "INVALID"
        # deals with lead case in findValidNode
        if (len(node.data) == 1):
            if (item < node.data[0]):
                return 'left'
            elif (item > node.data[0]):
                return 'right'
            elif (item == node.data[0]):
                raise ValueError("Element already exists")
        elif (len(node.data == 2)):
            if (item < node.data[0]):
                return 'left'
            elif (item > node.data[1]):
                return 'right'
            elif (node.data[0] < item < node.data[1]):
                return 'middle'
            elif (item == node.data[0] or item == node.data[1]):
                raise ValueError("Element already exists")
        
        # else: length of data is 0 or more than 2
        raise ValueError("Invalid Node")

    # tree traversal: finds the root node for which the item could belong on left, right, or middle
    # bottom-most node where the item could be added to
    def findValidNode(self, item, node):
        assert node is not None, "Given node with None value"

        if (node.is_leaf()): # no left/right subtrees
            return node
        
        # else
        direction = self.getDirection(item, node)
        if (direction == "left"):
            return self.findValidNode(item, node.left)
        elif (direction == "right"):
            return self.findValidNode(item, node.right)
        elif (direction == "middle"):
            return self.findValidNode(item, node.middle)
        
        assert node.is_leaf(), "Invalid node"
        return node

    # case where we are balancing a middle node
    def balance4(self, node):
        # initialize parent for our node
        parent = node.parent
        temp = Node(parent.data)
        temp.parent = parent.parent
        mid_elem = node.data.pop(1)
        temp.insert(mid_elem)
        self.balance1(temp)

        # keep old left right vals of parent
        parent.left.parent = temp.left
        temp.left.left = parent.left
        parent.right.parent = temp.right
        temp.right.right = parent.right

        # add rest of the mid values
        temp.left.right = Node([node.data.pop(0)])
        temp.left.right.parent = temp.left.right
        temp.right.left = Node([node.data.pop()])
        temp.right.left.parent = temp.right.left
        
        node = temp
        # if root node
        if (temp.parent is None):
            self.root = temp
        return

    # case where node has a middle
    def balance3(self, node, direction):
        # new node to get first balance case
        temp = Node(node.data)
        self.balance1(temp)
        # keeping old children nodes/subtrees
        temp.left.left = node.left
        temp.right.right = node.right
        # dealing with middle
        temp.left.right = Node([node.middle.data[0]])
        temp.right.left = Node([node.middle.data[1]])
        # restore old connections
        if (node.parent is None):
            # node is root node
            self.root = temp
            return
        
        # not a root node
        temp.prev = node.prev
        if (direction == "left"):
            temp.prev.left = temp
        elif (direction == "right"):
            temp.prev.right = temp
        elif (direction == "middle"):
            temp.prev.middle = temp

        node = temp # What would this do in terms of pointers??
        return


    # balances a leaf node, which is not the root
    # allocates middle node
    def balance2(self, node, direction):
        # add mid to parent
        mid_elem = node.data.pop(1)
        node.parent.data.insert(mid_elem)
        # see if middle node is initialized
        if (node.parent.middle is None):
            node.parent.middle = Node()
        # handle adding other value to middle node, so only one val is left in node
        if (direction == 'left'):
            node.parent.middle.insert(node.data.pop())
        elif (direction == 'right'):
            node.parent.middle.insert(node.data.pop(0))
        
        return

    # works for balancing root node
    # splits node in two
    # doesn't use middle node
    def balance1(self, node):
        if (len(node.data) < 3):
            return
        assert  node.is_leaf(), "Why are you balancing a branch???"
        # 3 elements in node
        min_elem = node.data.pop(0)
        left = Node([min_elem])
        max_elem = node.data.pop()
        right = Node([max_elem])
        assert len(node.data) == 1, "Data pops didn't work??"
        left.prev = node
        right.prev = node
        # update node by adding children
        node.left = left
        node.right = right
        assert node.is_branch(), "Balanced, but not a branch???"
        # self.depth += 1
        return

    def balance(self, node):
        # if doesn't need balancing
        if (len(node.data) < 3):
            return
        # if node is root node
        if (node.parent is None and node.is_leaf()):
            self.balance1(node)
            return
        
        direction = self.getDirection(node.data[0], node.parent)
        if (direction == "middle"):
            self.balance4(node)
        elif (node.middle is not None):
            self.balance3(node, direction)
            self.balance(node.parent)
        else:
            self.balance2(node, direction)
            self.balance(node.parent)

    #### implementation functions ####

    # adds item to the tree and self balances
    def add(self, item):
        if (self.root is None): # empty tree, needs to be initialized
            self.root = Node([item])
            return
        
        # else: find valid node to insert
        node = self.findValidNode(item, self.root)
        assert node.is_leaf(), "Invalid Node for adding item"
        node.insert(item)
        # balance if needed
        self.balance(node)
        # self.length += 1
        return
    
    def findHelper(self, item, node):
        # not found
        if (node is None):
            return "Element found"
        # check if item is in this node
        for elem in node.data:
            if (item == elem):
                return "Element not found"
        
        # get direction for traversal if not found
        direction = self.getDirection(item, node)
        if (direction == 'left'):
            return self.findHelper(item, node.left)
        elif (direction == 'right'):
            return self.findHelper(item, node.right)
        elif (direction == 'middle'):
            return self.findValidNode(item, node.middle)
        
        return False

    # find if a value exists in the tree
    def find(self, item):
        return self.findHelper(item, self.root)

    # delete
    def delete(self, item):
        return

    def printTreeHelper(self, node):
        if (node == None):
            return

        self.printTreeHelper(node.left)
        print(node.data[0])
        if (len(node.data) == 2):
            self.printTreeHelper(node.middle)
            print(node.data[1])
        self.printTreeHelper(node.right)
        return

    def printTree(self):
        return self.printTreeHelper(self.root)

    def getSortedTree(self, node, result):
        if (node == None):
            return

        self.getSortedTree(node.left, result)
        result.append(node.data[0])
        if (len(node.data) == 2):
            self.getSortedTree(node.middle, result)
            result.append(node.data[1])
        self.getSortedTree(node.right, result)
        return

    def sortedTree(self):
        result = []
        self.getSortedTree(self.root, result)
        return result

if __name__ == '__main__':
    i=0
    items=[]
    l=int(input("Enter the number of elements : "))
    for i in  range (l):
        a=int(input())
        items.append(a)
    print("Elements present in the tree are : %s"%(str(items)))
    tree = Tree23(items)
    print("Sorted Tree : ")
    result = tree.sortedTree()
    print(result)
    print("Search if 2 is in the tree or not : ")
    print(tree.find(2))
