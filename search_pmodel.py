# search_pmodel.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search_pmodel.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util_pmodel


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util_pmodel.raiseNotDefined()

    def is_goal_state(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util_pmodel.raiseNotDefined()

    def get_successors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util_pmodel.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util_pmodel.raiseNotDefined()


# BEGIN SOLUTION
class Node:
    """AIMA: A node in a search tree. Contains a pointer 
    to the parent (the node that this is a successor of) 
    and to the actual state for this node. Note that if 
    a state is arrived at by two paths, then there are 
    two nodes with the same state.  Also includes the 
    action that got us to this state, and the total 
    path_cost (also known as g) to reach the node.  
    Other functions may add an f and h value; see 
    best_first_graph_search and astar_search for an 
    explanation of how the f and h values are handled. 
    You will not need to subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        "Create a search tree Node, derived from a parent by an action."
        self.state = state
        self.parent = parent
        self.action = action
        if parent:
            self.path_cost = parent.path_cost + path_cost
            self.depth = parent.depth + 1
        else:
            self.path_cost = path_cost
            self.depth = 0

    def __repr__(self):
        return "<Node %s>" % (self.state,)

    def nodePath(self):
        "Create a list of nodes from the root to this node."
        x, result = self, [self]
        while x.parent:
            result.append(x.parent)
            x = x.parent
        result.reverse()
        return result

    def path(self):
        """
        Create a path of actions from the start to the current state
        """
        actions = []
        currnode = self
        while currnode.parent:
            actions.append(currnode.action)
            currnode = currnode.parent
        actions.reverse()
        return actions

    def expand(self, problem):
        "Return a list of nodes reachable from this node. [Fig. 3.8]"
        return [Node(next, self, act, cost)
                for (next, act, cost) in problem.get_successors(self.state)]


REVERSE_PUSH = False


def graphSearch(problem, fringe):
    """Search through the successors of a problem to find a goal.
    The argument fringe should be an empty queue. [Fig. 3.18]"""
    startstate = problem.get_start_state()
    fringe.push(Node(problem.get_start_state()))
    try:
        startstate.__hash__()
        visited = set()
    except:
        visited = list()

    while not fringe.isEmpty():
        node = fringe.pop()
        if problem.is_goal_state(node.state):
            return node.path()
        try:
            inVisited = node.state in visited
        except:
            visited = list(visited)
            inVisited = node.state in visited

        if not inVisited:
            if isinstance(visited, list):
                visited.append(node.state)
            else:
                visited.add(node.state)
            nextNodes = node.expand(problem)
            if REVERSE_PUSH: nextNodes.reverse()
            for nextnode in nextNodes:
                fringe.push(nextnode)
    return None


# END SOLUTION NO PROMPT


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    # BEGIN SOLUTION METHOD
    return graphSearch(problem, util_pmodel.Stack())
    # END SOLUTION


def breadth_first_search(problem):
    "Search the shallowest nodes in the search tree first. [p 81]"

    # BEGIN SOLUTION METHOD
    return graphSearch(problem, util_pmodel.Queue())
    # END SOLUTION


def uniform_cost_search(problem):
    "Search the node of least total cost first. "

    # BEGIN SOLUTION METHOD
    return graphSearch(problem,
                       util_pmodel.PriorityQueueWithFunction(
                           lambda node: node.path_cost))
    # END SOLUTION


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."

    # BEGIN SOLUTION METHOD
    return graphSearch(problem,
                       util_pmodel.PriorityQueueWithFunction(
                           lambda node: node.path_cost + heuristic(node.state, problem)))
    # END SOLUTION

    # BEGIN SOLUTION


def greedy_search(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest heuristic first."
    return graphSearch(problem, util_pmodel.PriorityQueueWithFunction(
        lambda node: heuristic(node.state, problem)))
    # END SOLUTION NO PROMPT


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
