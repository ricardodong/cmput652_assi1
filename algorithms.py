import numpy as np
import math

def swap(a,b):
    return b,a

class node:
    def __init__(self, index):
        self.neighbours = []
        self.heuristic = 99999
        self.gcost = 99999
        self.hash = index

    def print(self):
        print(self.hash)

    def getNeigh(self):
        return self.neighbours

    def printneigh(self):
        for i in self.neighbours:
            print(i.hash)

class spnode(node):
    def __init__(self, a):
        self.state = np.zeros(16)
        self.state = a
        self.zeroPosi = 0
        for i in range(16):
            if self.state[i] == 0:
                self.zeroPosi = i
                break
        self.neighbours = []
        #only get neighbour when we want
        self.hash = self.getHash(self.state)

        self.path = []
        #things in path are also spnode.
        #only used in A-star, record the path to get current g-cost
        self.heuristic = self.getHeuristic(self.state)
        self.gcost = 999999
        #should be assigned in algorithm, start node is 0

    def getHash(self, state):
        hashvalue = 0
        for i in range(16):
            currhash = state[i]
            hashvalue = hashvalue + currhash
            hashvalue = hashvalue<<4
        return hashvalue

    def getHeuristic(self, state):
        heur = 0
        for i in range(16):
            currslid = state[i]
            if currslid == 0:
                continue
            #we don't take the blank to calculate heuristic
            (currx, curry) = np.divmod(currslid,4)#行，列，从0开始
            (targx, targy) = np.divmod(i,4) #these should be replaced by constant
            heur = heur + abs(currx-targx) + abs(curry-targy)
        return heur

    def print(self):
        for i in range(4):
            for j in range(4):
                print(str(self.state[j + 4 * i]) + " ", end="")
            print("\n")
        print("----------------------")

    def switch_left(self):
        ##move 0 to left
        mod_0posi_4 = divmod(self.zeroPosi, 4)[1]
        if mod_0posi_4 == 0:
            #print("can't move left")
            return -1
        else:
            i = self.zeroPosi
            generatedNode = spnode(self.state)
            (generatedNode.state[i], generatedNode.state[i - 1]) = swap(generatedNode.state[i],
                                                                        generatedNode.state[i - 1])
            return generatedNode

    def switch_right(self):
        ##move 0 to right
        mod_0posi_4 = divmod(self.zeroPosi, 4)[1]
        if mod_0posi_4 == 3:
            #print("can't move right")
            return -1
        else:
            i = self.zeroPosi
            generatedNode = spnode(self.state)
            (generatedNode.state[i], generatedNode.state[i + 1]) = swap(generatedNode.state[i],
                                                                        generatedNode.state[i + 1])
            return generatedNode

    def switch_up(self):
        ##move 0 to up
        if self.zeroPosi <= 3:
            #print("can't move up")
            return -1
        else:
            i = self.zeroPosi
            generatedNode = spnode(self.state)
            (generatedNode.state[i], generatedNode.state[i - 4]) = swap(generatedNode.state[i],
                                                                        generatedNode.state[i - 4])
            return generatedNode

    def switch_down(self):
        ##move 0 to up
        if self.zeroPosi >= 12:
            #print("can't move down")
            return -1
        else:
            i = self.zeroPosi
            generatedNode = spnode(self.state)
            generatedNode.state[i], generatedNode.state[i + 4] = swap(generatedNode.state[i],
                                                                      generatedNode.state[i + 4])
            return generatedNode

    def setNeigh(self):
        numofneigh = 4
        zero_left = self.switch_left()
        if zero_left == -1:
            numofneigh = numofneigh - 1
        else:
            self.neighbours.append(zero_left)
        zero_right = self.switch_right()
        if zero_right == -1:
            numofneigh = numofneigh - 1
        else:
            self.neighbours.append(zero_right)
        zero_up = self.switch_up()
        if zero_up == -1:
            numofneigh = numofneigh - 1
        else:
            self.neighbours.append(zero_up)
        zero_down = self.switch_down()
        if zero_down == -1:
            numofneigh = numofneigh - 1
        else:
            self.neighbours.append(zero_down)
        return numofneigh

class graph:
    def __init__(self):
        ##for test, create a binary tree
        depth = 10
        bf = 2 ##branching factor
        ##initial the first node
        self.nodes = []
        firstnode  = node(0)
        self.nodes.append(firstnode)
        ##create tree
        k=1
        for i in range(depth):
            #indicate which level are we in
            numOfPCurrNodes = bf**i
            numOfPTotalNodes = len(self.nodes)
            for m in range(numOfPCurrNodes):
                #indicate the current level
                indexOfCurrNode = numOfPTotalNodes-(numOfPCurrNodes-m)
                for n in range(bf):
                    ##create bf 个 nodes
                    createdNode = node(k)
                    k=k+1
                    self.nodes[indexOfCurrNode].neighbours.append(createdNode)
                    createdNode.neighbours.append(self.nodes[indexOfCurrNode])
                    self.nodes.append(createdNode)

class DFS_limit:

    def __init__(self):
        self.path = []
        self.safe = False
        #indicate whether we have reach the limitation of level,
        # if it is, then it means we cannot find result because of limitation,
        # else because of no goal find
        self.respath = []

    def GetPath(self, start, goal, level, lelimit):
        start.setNeigh()
        neigh = start.neighbours
        self.path.append(start)
        #print(start.hash)
        if start.hash == goal.hash:
            print("asdasdasdasdasd")
            self.respath = self.path
            return 1
        elif level < lelimit:
            nextlevel = level+1
            for i in neigh:
                if self.isInPath(i):
                    #print("same")
                    continue
                j = self.GetPath(i, goal, nextlevel, lelimit)
                if j == 1:
                    return 1
            self.path.remove(start)
            return -1
        else:
            self.safe = True
            return -1

    def isInPath(self, neighNode):
        for i in self.path:
            if neighNode.hash == i.hash:
                return True
        return False

class DFID:
    def __init__(self):
        self.path = []
        self.respath = []
        self.findlevel = 99999

    def search(self,start, goal):
        lelimit = 0
        while True:
            newdfs = DFS_limit()
            found  = newdfs.GetPath(start, goal, 0, lelimit)
            if found == 1:
                self.respath = newdfs.respath
                self.findlevel = lelimit
                return 1
            else:
                if newdfs.safe == False:
                    break
                else:
                    lelimit = lelimit + 1
                    print(lelimit)

        return -1

class A_star:
    def __init__(self):
        self.path = []
        self.closelist = []
        self.openlist  = []
        self.stpaction = 1
        #this is for the gcost change of nodes, in sliding tile puzzle, it's 1

    def search(self, start, goal):

        if start.hash == goal.hash:
            #should also generate path
            return 1

        #init of close and open list
        self.closelist.append(start)
        nodeaddtoclose = start

        #interative adding
        while True:
            #generate openlist (update the f-cost)
            #fast
            nodeaddtoclose.setNeigh()
            ineigh = nodeaddtoclose.neighbours
            for j in ineigh:
                # should update gcost here.
                newgcost = self.stpaction + nodeaddtoclose.gcost
                if j.gcost > newgcost:
                    # update path and gcost
                    j.gcost = newgcost
                    j.path = nodeaddtoclose.path
                    j.path.append(nodeaddtoclose)
                #decide whether should add the node to openlist
                AlreadyInOpen = False
                for k in self.openlist:
                    if k.hash == j.hash:
                        AlreadyInOpen = True
                        break
                if not AlreadyInOpen:
                    self.openlist.append(j)

            #select one from openlist to close list
            minfcost = self.openlist[0].gcost + self.openlist[0].heuristic
            minnode  = self.openlist[0]
            for m in self.openlist:
                mfcost = m.gcost+m.heuristic
                if mfcost < minfcost:
                    minfcost = mfcost
                    minnode  = m

            #if the selected is the goal, then end search, else add it to close list
            if minnode.hash == goal.hash:
                #found goal
                self.path = minnode.path
                return 1
            else:
                self.openlist.remove(minnode)
                self.closelist.append(minnode)
                nodeaddtoclose = minnode
                minnode.print()

if __name__ == '__main__':

    #newgraph = graph()

    #newsearch = DFS_limit()
    #find = newsearch.GetPath(newgraph.nodes[0],newgraph.nodes[100], 0, 10)
    #for i in newsearch.respath:
    #    print(i.hash, end=" ")

    a = [15 , 1 , 8, 10, 7, 11, 14, 2, 12 , 5 , 9, 13 , 4 , 6 , 3 , 0]
    firstnode = spnode(a)
    firstnode.gcost = 0
    goalstate = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    goalnode = spnode(goalstate)

    newsearch = A_star()
    find = newsearch.search(firstnode,goalnode)
    for i in newsearch.path:
        i.print()

