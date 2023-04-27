# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        #print("Current position:", gameState.getPacmanPosition())
        #print("Best score:", bestScore)

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        oldFood = currentGameState.getFood()
        oldGhost = successorGameState.getGhostPositions()
        oldScaredTimes = [ghostState.scaredTimer for ghostState in currentGameState.getGhostStates()]
        initScore = successorGameState.getScore()
        minDistFromGhost = min([manhattanDistance(newPos, ghost) for ghost in oldGhost])
        minDistFromFood = min([manhattanDistance(newPos, food) for food in oldFood.asList()])
        score = initScore
        x, y = newPos
        
        if newPos == currentGameState.getPacmanPosition():
            score -= 1
        
        if oldFood[x][y]: # If there is food in the new position, add 100 points
            score += 99999
        else:
            score -= pow(minDistFromFood, 2)
        
        if newGhostStates:
            if oldScaredTimes[0] > 0: # If the ghost is scared
                if minDistFromGhost < newScaredTimes[0]: # If the ghost is reachable
                    score += 5 * minDistFromGhost # Proceed to eat the ghost
                else:
                    score += 0.1 * minDistFromGhost
            else: # If the ghost is not scared
                if minDistFromGhost < 2:
                    score = -999999
                else:
                    score += 0.1 * minDistFromGhost
        
        return score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        agentsNum = gameState.getNumAgents() # Number of agents
        agentIndex = 0 # Pacman is always agent index 0
        
        def maxValue(gameState, agentIndex, agentsNum, depth):
            if gameState.isWin() or gameState.isLose() or depth == self.depth: # If the game is over or the depth is reached
                return self.evaluationFunction(gameState), None
            
            value, move = -999999, None
            
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                successorValue = minValue(successor, agentIndex + 1, agentsNum, depth)[0]
                
                if successorValue > value: # If the successor value is greater than the current value
                    value, move = successorValue, action
            
            return value, move
        
        def minValue(gameState, agentIndex, agentsNum, depth):
            if gameState.isWin() or gameState.isLose() or depth == self.depth: # If the game is over or the depth is reached
                return self.evaluationFunction(gameState), None
            
            value, move = 999999, None
            
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                
                if agentIndex == agentsNum - 1: # If the agent is the last ghost
                    successorValue = maxValue(successor, 0, agentsNum, depth + 1)[0] # Go to the next depth
                else: # If the agent is not the last ghost
                    successorValue = minValue(successor, agentIndex + 1, agentsNum, depth)[0] # Go to the next ghost
                
                if successorValue < value:
                    value, move = successorValue, action
            
            return value, move
        
        return maxValue(gameState, agentIndex, agentsNum, 0)[1]
        
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        agentsNum = gameState.getNumAgents() # Number of agents
        agentIndex = 0 # Pacman is always agent index 0
        
        def ABmaxValue(gameState, agentIndex, agentsNum, depth, alpha, beta):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState), None
            
            value, move = -999999, None
            
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                successorValue = ABminValue(successor, agentIndex + 1, agentsNum, depth, alpha, beta)[0] 
                
                if successorValue > value:
                    value, move = successorValue, action
                
                if value > beta: # If the value is greater than the beta
                    return value, move 
                
                alpha = max(alpha, value) # Update alpha
            
            return value, move
        
        def ABminValue(gameState, agentIndex, agentsNum, depth, alpha, beta):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState), None
            
            value, move = 999999, None
            
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                
                if agentIndex == agentsNum - 1: # If the agent is the last ghost
                    successorValue = ABmaxValue(successor, 0, agentsNum, depth + 1, alpha, beta)[0] # Go to the next depth
                else: # If the agent is not the last ghost
                    successorValue = ABminValue(successor, agentIndex + 1, agentsNum, depth, alpha, beta)[0] # Go to the next ghost
                
                if successorValue < value:
                    value, move = successorValue, action
                
                if value < alpha: # If the value is less than the alpha
                    return value, move
                
                beta = min(beta, value) # Update beta
            
            return value, move
        
        return ABmaxValue(gameState, agentIndex, agentsNum, 0, -999999, 999999)[1]
        
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        agentNum = gameState.getNumAgents() # Number of agents
        agentIndex = 0 # Pacman is always agent index 0
               
        def expValue(gameState, agentIndex, agentsNum, depth):                    
            if gameState.isWin() or gameState.isLose() or depth == self.depth: # If the game is over or the depth is reached
                return self.evaluationFunction(gameState), None
            
            prob = 1 / len(gameState.getLegalActions(agentIndex)) # Probability of each action
            successors = []
            
            for action in gameState.getLegalActions(agentIndex):
                successors.append(gameState.generateSuccessor(agentIndex, action))
            
            if agentIndex == agentNum - 1: # If finished an iteration over all agents
                return sum([maxValue(successor, 0, agentsNum, depth + 1)[0] * prob for successor in successors]), None # Go to the next depth
            else: # If the agent is a ghost
                return sum([expValue(successor, agentIndex + 1, agentsNum, depth)[0] * prob for successor in successors]), None # Go to the next ghost
        
        def maxValue(gameState, agentIndex, agentsNum, depth):
            if gameState.isWin() or gameState.isLose() or depth == self.depth: # If the game is over or the depth is reached
                return self.evaluationFunction(gameState), None
            
            value, move = -999999, None
            
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                successorValue = expValue(successor, agentIndex + 1, agentsNum, depth)[0]
                
                if successorValue > value: # If the successor value is greater than the current value
                    value, move = successorValue, action
            
            return value, move
        
        return maxValue(gameState, agentIndex, agentNum, 0)[1]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood().asList()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
    score = currentGameState.getScore() # Score for the current state
    ghostScore = 0 # Score for the ghosts
    foodScore = sum([manhattanDistance(newPos, food) for food in newFood]) # Score for the food
    capsulesScore = sum([manhattanDistance(newPos, capsule) for capsule in currentGameState.getCapsules()]) # Score for the capsules
    
    for ghost in newGhostStates:
        ghostDist = manhattanDistance(newPos, ghost.getPosition())
        if newScaredTimes[0] > ghostDist: # If the ghost is scared and can be eaten
            ghostScore += 10 * ghostDist # Add the distance to the ghost score
        else:
            ghostScore += ghostDist # Add the distance to the ghost score
    
    noise = random.uniform(-0.1, 0.1) # Add some noise to the score
    
    score = score + 5 / (foodScore + 1) + 5 / (capsulesScore + 1) - 3 / (ghostScore + 1) + noise # Update the score
    
    return score

# Abbreviation
better = betterEvaluationFunction
