# CMSC 671: Introduction to AI - Fall'18
# Homework 2
# PART 2 - PATH FINDING
# Name: Anushree Desai
# Campus ID: ZO10934

'''****************************************************
Artificial Intelligence: A Modern Approach, 3rd. Edition, Stuart J. Russell and Peter Norvig. Prentice Hall, 2009.
Date: 21st Sep 2018
****************************************************'''

'''****************************************************
Title: HeapQ
Date: 23th Sep 2018
Type: Heapq implementation
Availibility: https://docs.python.org/3.0/library/heapq.html
****************************************************'''

from heapq import heappush, heappop

class ProblemNode:
# Making a class for node, using the class everytime to create a new node

    def __init__(self, costToGoal = 0, state = [], action = None, costTillNow = 0, parent = None ):
        # Called each time object is created and it will assign values to each instance
        self.costToGoal = costToGoal
        self.state = state
        self.parent = parent
        self.action = action
        self.costTillNow = costTillNow

    '''****************************************************
    Title: print function for node
    Date: 24th Sep 2018
    Type: Reference for python __str__ function
    Availability: https://docs.python.org/3/reference/datamodel.html#object.__str__
    ****************************************************'''
    def __str__(self):
        if(self.parent and self.action):
            return ("costToGoal: "+str(self.costToGoal) + ", State Node is in: "+str(self.state)  + ", Node's Action: "+str(self.action) + ", Node's Cost Till Now: "+str(self.costTillNow) +", Node's Parent: "+str(self.parent.state))
        else:
            return ("costToGoal: "+str(self.costToGoal) + ", State Node is in: "+str(self.state) + "Node's Cost Till Now: "+str(self.costTillNow))

    '''****************************************************
    Title: Less than function for node object
    Date: 24th Sep 2018
    Type: Reference for python __lt__ function
    Availability: https://docs.python.org/2/library/operator.html#operator.__lt__
    ****************************************************'''
    def __lt__(self, other):
        # This function will check if one node is greater than other node. It will perform this check based on the costToGoal parameter of the node
        return self.costToGoal < other.costToGoal
    
    '''****************************************************
    Title: Check equal for node object
    Date: 24th Sep 2018
    Type: Reference for python __eq__ function
    Availability: https://docs.python.org/2/library/operator.html#operator.__eq__
    ****************************************************'''   
    def __eq__(self, other):
        # This function will check for equality among two nodes. It will perform this check based on the state tuple stored in the node
        return self.state == other.state

def solve(startCo, goalCo, puzzleMatrix):
    '''
    This is the entry point of the problem Matrix. Function will return the solution in string form.
    parameter 1: startCo - Gives the co-ordinates of the agent start cell
    parameter 2: goalCo - Gives the co-ordinates of the agent goal cell
    parameter 3: puzzleMatrix - Gives the problem in form of a square matrix
    '''

    # Creating initial node with ProblemNode class
    # Since it is a start node, its heuristic cost is 0, initial state is start state, no action,  costTillNow is 0 and it has no parent
    node = ProblemNode(0, startCo, None, 0, None)
    # Creating empty frontier as a list of nodes that will be pushed to frontier, which we will eventually use in form of heapQ
    frontier = []
    # Set explored will store all the nodes that are explored. Currently, no nodes explored thus empty set
    explored = set()
    # Using heappush operation using frontier list initiazed to push initial node to frontier which will store nodes in heapq form
    heappush(frontier, node)
    # Run loop till elements are present in frontier
    while frontier:
        # Generating node from frontier with least cost
        node = heappop(frontier)
        if node.state == goalCo:
        # Return path directly if this is the goal node
            # print(node.costTillNow)
            return getPath(node)
        else:
            # if there is a node with a cost less than or equal to 300 present in frontier, then, return that instead of heading to find a very optimal solution
            for frontierNode in frontier:
                if(goalCo == frontierNode.state and frontierNode.costTillNow <= 300):
                    # print("<300 part: "+str(node.costTillNow))
                    return getPath(frontierNode)
        explored.add(node.state)
        actionsArray = possibleActions(node.state, len(puzzleMatrix))
        for action in actionsArray:
            # Expanding the node and creating its children for legal branches
            child = createChild(puzzleMatrix, node, action, goalCo)
            # print("Child getting created as below************************:")
            # print(child)
            # print('action: '+action)
            if((child.state not in explored) and (child not in frontier)):
                heappush(frontier, child)
            else:
                for frontierNode in frontier:
                    if(child.state == frontierNode.state and child.costToGoal < frontierNode.costToGoal):
                        frontierNode.costToGoal = child.costToGoal

def possibleActions(coordinate, puzzleMatrixLen):
    '''
    This function will return all the legal and possible actions for state in the node
    parameter 1: coordinate - Gives state coordinate of the node that is currently generated
    parameter 2: puzzleMatrixLen - gives length of square matrix to check the bounds and constraints of actions

    It will allow Left move to the agent only if agent is not at left most position.
    It will allow Up move to the agent only if agent is not at the North most position.
    Similarly for Right and Down moves
    '''
    actionsArray = []
    if(coordinate[0] > 0): actionsArray.append('N')
    if(coordinate[0] < puzzleMatrixLen-1): actionsArray.append('S')
    if(coordinate[1] > 0): actionsArray.append('W')
    if(coordinate[1] < puzzleMatrixLen-1): actionsArray.append('E')
    return actionsArray

def createChild(puzzleMatrix, node, action, goalCo):
    '''
    This function will return child node for node after applying action
    parameter 1: puzzleMatrix - given problem matrix
    parameter 2: node - current node under expansion
    parameter 3: action: action to be applied to node
    parameter 4: goal coordinates to calculate heuristic and actual costs
    '''
    state = []
    if(action == 'N'):
        state = (node.state[0] - 1, node.state[1])
    elif(action == 'S'):
        state = (node.state[0] + 1, node.state[1])
    elif(action == 'W'):
        state = (node.state[0], node.state[1] - 1)
    else:
        state = (node.state[0], node.state[1] + 1)

    #f(n) = g(n) + h(n)

    costTillNow =  calculateCostTillNow(puzzleMatrix, node, state) #g(n) = actual cost of the node n = from start state to n
    costToGoal = costTillNow + calculateHeuristicCost(puzzleMatrix, state, goalCo) #h(n) = heuristic cost of the node n = from n to goal state
    return ProblemNode(costToGoal, state, action, costTillNow, node)

def calculateCostTillNow(puzzleMatrix, node, state):
    '''
    This function will calculate the actual cost to reach from start to node n via that path
    parameter 1: puzzleMatrix - given problem matrix
    parameter 2: node - current node under expansion
    parameter 3: state: new formed state passed from calling function

    Add parent's cost and its own cost depending on whether it is path, mountain or sand
    '''
    cell = puzzleMatrix[state[0]][state[1]]
    # if(node.parent):
    if(cell == 'm'): return (node.costTillNow + 100)
    elif(cell == 's'): return (node.costTillNow + 30)
    else: return (node.costTillNow + 10)
    # else:
    #     return 0

def calculateHeuristicCost(puzzleMatrix, state, goalCo):
    '''
    This function will calculate the heuristic cost to reach from node n to goal state
    parameter 1: puzzleMatrix - given problem matrix
    parameter 2: state: new formed state passed from calling function
    parameter 3: goalCo: goal coordiantes
    parameter 4: state: new formed state passed from calling function
    '''
    # cell = puzzleMatrix[state[0]][state[1]]
    manhattanDistance = manhattanDist(state, goalCo)
    return manhattanDistance * 10
    # if (cell == 'm'): return (100 + (manhattanDistance * 10))
    # elif (cell == 's'): return (30 + (manhattanDistance * 10))
    # else: return (10 + (manhattanDistance * 10))
    # if (cell == 'm'): return (100 + (manhattanDistance))
    # elif (cell == 's'): return (30 + (manhattanDistance))
    # else: return (10 + (manhattanDistance))

def manhattanDist(currentState, goalState):
    '''
    This function will calculate the manhattan distance between two cells of the square matrix
    parameter 1: currentState - cell 1
    parameter 2: goalState: cell 2
    '''
    try:
        return abs(currentState[0] - goalState[0]) + abs(currentState[1] - goalState[1])
    except Exception:
        return "Manhattan Distance exception thrown"

def getPath(node):
    if(not node.parent): return ""
    return getPath(node.parent) + node.action

startCo = (1,0)
goalCo = (2,2)
puzzleMatrix = [
['p','p','p'],
['p','m','p'],
['s','s','s']]
#NEESS

# startCo = (0,0)
# goalCo = (2,2)
# puzzleMatrix = [
# ['m','m','m','s'],
# ['m','m','m','s'],
# ['m','m','m','s'],
# ['p','p','p','p']]
#SSSEEN

resultPath = solve(startCo, goalCo, puzzleMatrix)
print("Result Path: "+resultPath)