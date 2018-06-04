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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

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
        foodList = currentGameState.getFood().asList()

        while (not action is Directions.STOP):
            score = 0
            for ghost in newGhostStates:
                if ghost.scaredTimer < 1 and ghost.getPosition() == newPos:
                    return -99999999999999999

            for food in foodList:
                score = max([(-1 * util.manhattanDistance(newPos, food), food)])
            return score
        return -99999999999999999


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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
        agents = gameState.getNumAgents() - 1
        value = -99999999999999999
        finalAction = gameState.getLegalActions(0)
        for action in finalAction:
            minimum = self.minValue(gameState.generateSuccessor(0, action), self.depth, agents, 1)
            tempValue = value
            value = max(value, minimum)
            if value > tempValue:
                finalAction = action
        if value == -99999999999999999:
            return Directions.STOP
        return finalAction

    def maxValue(self, gameState, depth, agents):
        value = -99999999999999999
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        for action in gameState.getLegalActions(0):
            minimum = self.minValue(gameState.generateSuccessor(0, action), depth, agents, 1)
            value = max(value, minimum)
        return value

    def minValue(self, gameState, depth, agents, agentIndex):
        value = 99999999999999999
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        for action in gameState.getLegalActions(agentIndex):
            if agents == agentIndex:
                value = min(value, self.maxValue(gameState.generateSuccessor(agentIndex, action), depth - 1, agents))
            else:
                value = min(value, self.minValue(gameState.generateSuccessor(agentIndex, action), depth, agents,
                                                 agentIndex + 1))
        return value


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        self.agents = gameState.getNumAgents()
        alpha = -99999999999999999
        beta = 99999999999999999
        finalAction = self.maxvalue(gameState, 0, 0, alpha, beta)
        return finalAction[1]

    def maxvalue(self, gameState, agentIndex, depth, alpha, beta):
        value = (-99999999999999999, Directions.STOP)
        for action in gameState.getLegalActions(agentIndex):
            value = max([value,
                         (self.getValue(gameState.generateSuccessor(agentIndex, action), (depth + 1) % self.agents,
                                               depth + 1, alpha, beta), action)], key=lambda item: item[0])
            if value[0] > beta:
                return value
            alpha = max(alpha, value[0])
        return value

    def minvalue(self, gameState, agentIndex, depth, alpha, beta):
        value = (99999999999999999, Directions.STOP)
        for action in gameState.getLegalActions(agentIndex):
            value = min([value,
                         (self.getValue(gameState.generateSuccessor(agentIndex, action),(depth + 1) % self.agents,
                                               depth + 1, alpha, beta), action)], key=lambda item: item[0])
            if value[0] < alpha:
                return value
            beta = min(beta, value[0])
        return value

    def getValue(self, gameState, agentIndex, depth, alpha, beta):
        if gameState.isLose() or gameState.isWin() or depth >= self.depth * self.agents:
            return self.evaluationFunction(gameState)
        if (agentIndex == 0):
            return self.maxvalue(gameState, agentIndex, depth, alpha, beta)[0]
        else:
            return self.minvalue(gameState, agentIndex, depth, alpha, beta)[0]


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
        agents = gameState.getNumAgents() - 1
        value = -99999999999999999
        finalAction = gameState.getLegalActions(0)
        for action in finalAction:
            expectiMax = self.expectiMaxvalue(gameState.generateSuccessor(0, action), self.depth, agents, 1)
            tempValue = value
            value = max(value, expectiMax)
            if value > tempValue:
                finalAction = action
        if value == -99999999999999999:
            return Directions.STOP
        return finalAction

    def maxValue(self, gameState, depth, agents):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        value = -99999999999999999
        for action in gameState.getLegalActions(0):
            expectiMax = self.expectiMaxvalue(gameState.generateSuccessor(0, action), depth, agents, 1)
            value = max(value, expectiMax)
        return value

    def expectiMaxvalue(self, gameState, depth, agents, agentIndex):
        expectiMaxValue = []
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        for action in gameState.getLegalActions(agentIndex):
            if agents == agentIndex:
                expectiMaxValue.append(
                    self.maxValue(gameState.generateSuccessor(agentIndex, action), depth - 1, agents))
            else:
                expectiMaxValue.append(
                    self.expectiMaxvalue(gameState.generateSuccessor(agentIndex, action), depth, agents,
                                         agentIndex + 1))
        return sum(expectiMaxValue) / len(expectiMaxValue)


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    currentPosition = currentGameState.getPacmanPosition()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    foodPosition = currentGameState.getFood().asList()
    ghostDistance = 0
    score = 0
    distanceToCover = 0
    foodDistance = []

    for ghost in newGhostStates:
        ghostDistance = ghostDistance + util.manhattanDistance(currentPosition,
                                                               ghost.getPosition())

    if ghostDistance <= 2:
        score = -99999999999999999
    else:
        score = score - (10.0 / ghostDistance)

    if currentPosition in foodPosition:
        score = score + 10000


    for food in foodPosition:
        foodDistance.append(util.manhattanDistance(currentPosition, food))

    if foodPosition:
        distanceToCover = min(foodDistance)
        if(len(foodPosition) > 1):
            distanceToCover += max(foodDistance)
        score += 15.5 / (1 + distanceToCover)
    else:
        score += 200

    score -= pow(len(foodPosition), 2)

    score += 1.0 / (1 + (distanceToCover))

    if newScaredTimes[0] >= 20:
        score += 2

    return score

    # util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
