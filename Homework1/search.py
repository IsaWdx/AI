# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    # from game import Directions
    # s = Directions.SOUTH
    # w = Directions.WEST
    # e = Directions.EAST
    # n = Directions.NORTH
    # options = {"South": s,
    #            "West": w,
    #            "East": e,
    #            "North": n
    #            }
    route = []
    dfs_stack = util.Stack()
    start_state = problem.getStartState()
    dfs_stack.push(start_state)
    visited = []
    succ = {}
    while not dfs_stack.isEmpty():
        current = dfs_stack.pop()
        if current in visited:
            successors = succ[current]
        elif current[0] in visited:
            successors = succ[current[0]]
        else:
            if len(current) < 3:
                successors = problem.getSuccessors(current)
                succ[current] = successors
                visited.append(current)
            else:
                successors = problem.getSuccessors(current[0])
                succ[current[0]] = successors
                visited.append(current[0])
        reach_goal = False
        for state in reversed(successors):
            if state[0] in visited:
                continue
            else:
                if problem.isGoalState(state[0]):
                    dfs_stack.push(current)
                    dfs_stack.push(state)
                    reach_goal = True
                    break
                else:
                    dfs_stack.push(current)
                    dfs_stack.push(state)
                    break
        if reach_goal:
            break


    while not dfs_stack.isEmpty():
        current = dfs_stack.pop()
        if len(current) == 3:
            route.insert(0, current[1])
    return route
    #util.raiseNotDefined()



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH

    succ = {}
    bfs_queue = util.Queue()
    pre_dic = {}
    bfs_queue.push(problem.getStartState())
    route = []
    visited = []
    inqueue = []
    start_state = problem.getStartState()
    result = None
    found_goal = False
    while not bfs_queue.isEmpty():

        v = bfs_queue.pop()
        if v in visited:
            successors = succ[v]
        elif v[0] in visited:
            successors = succ[v[0]]
        else:
            if v != start_state:
                successors = problem.getSuccessors(v[0])
                succ[v[0]] = successors
                visited.append(v[0])
            else:
                successors = problem.getSuccessors(v)
                visited.append(v)
                succ[v] = successors
        if found_goal:
            break
        for vertex in successors:
            if (vertex[0] in visited) or (vertex[0] in inqueue):
                continue
            else:

                if problem.isGoalState(vertex[0]):
                    pre_dic[vertex[0]] = v
                    result = vertex
                    found_goal = True
                    inqueue.append(vertex[0])
                else:
                    pre_dic[vertex[0]] = v
                    bfs_queue.push(vertex)
                    inqueue.append(vertex[0])


    while hasattr(result, '__len__') and pre_dic.get(result[0], None) is not None:

        route.insert(0, result[1])
        result = pre_dic[result[0]]
    return route




    # util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    bfs_queue = util.PriorityQueue()
    pre_dic = {}
    bfs_queue.push(problem.getStartState(), 0)
    route = []
    visited = []
    cost = {}
    succ = {}
    start_state = problem.getStartState()
    result = None
    cost[start_state] = 0
    while not bfs_queue.isEmpty():
        v = bfs_queue.pop()

        if v != start_state:
            if problem.isGoalState(v[0]):
                result = v
                break
            if v[0] in succ:
                successors = succ[v[0]]
            else:
                successors = problem.getSuccessors(v[0])
                succ[v[0]] = successors
            visited.append(v[0])
        else:
            successors = problem.getSuccessors(v)
            succ[v] = successors
            visited.append(v)
            cost[v] = 0
            pre_dic[v] = None
        for vertex in successors:
            if vertex[0] in visited:
                continue
            else:

                if v != start_state:
                    if cost.get(vertex[0], -1) == -1 or cost[v[0]] + vertex[2] < cost[vertex[0]]:
                        cost[vertex[0]] = cost[v[0]] + vertex[2]
                        pre_dic[vertex[0]] = v
                        bfs_queue.update(vertex, cost[vertex[0]])
                else:
                    cost[vertex[0]] = cost[v] + vertex[2]
                    pre_dic[vertex[0]] = v
                    bfs_queue.update(vertex, cost[vertex[0]])


    while True:
        print "result", result
        route.insert(0, result[1])
        result = pre_dic[result[0]]
        if result == start_state:
            break
    return route


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    def priorityFunction(v):
        if len(v) < 3:
            return 0
        else:
            return v[2] + heuristic(v[0], problem)
    bfs_queue = util.PriorityQueueWithFunction(priorityFunction)
    start_state = problem.getStartState()
    visited = {}
    cost = {}
    succ = {}
    cost[start_state] = 0
    bfs_queue.push((start_state, list(), 0))
    while not bfs_queue.isEmpty():
        v, path, cost = bfs_queue.pop()

        if problem.isGoalState(v):
            return path
        if v in visited:
            successors = visited[v]
        else:
            successors = problem.getSuccessors(v)
            visited[v] = successors

        for vertex in successors:
            if vertex[0] in visited:
                continue
            else:
                bfs_queue.push((vertex[0], path + [vertex[1]], cost + vertex[2]))





# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
