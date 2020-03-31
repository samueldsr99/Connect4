from node import Node
from state import State

# Agent that implements Monte Carlo Tree Search

class Agent():
	def __init__(self, state=State()):
		import math
		self.root = Node(state)
		self.c = math.sqrt(2) # constant c

	def calculateValue(self, node):
		import math
		return node.wins / node.visits + self.c * ( math.log(node.parent.visits) / node.visits )

	def findNextAction(self, iterations):
		for i in range(iterations):
			# 1 selection
			node = self.findChild(self.root)

			# 2 expansion
			if not node.state.isTerminal() and not node.isFullyExpanded:
				node = node.expand()

			# 3 playout
			result = self.playout(node)

			# 4 backpropagation
			self.backpropagate(node, result)

		return self.mostVisitedChild(self.root)


	def findChild(self, node):
		while not node.state.isTerminal() and node.isFullyExpanded:
			node = self.findBestChild(node)
		return node

	def findBestChild(self, node):
		best = node.children[0]
		for i in node.children:
			if self.calculateValue(i) > self.calculateValue(best):
				best = i
		return best

	def playout(self, node):
		curState = node.state.copy()

		while not curState.isTerminal():
			action = curState.getIntelligentAction()
			curState.applyAction(action)
		return curState.whoWin()

	def backpropagate(self, node, result):
		while node != None:
			if node.state.turn != result:
				node.wins += 1
			node.visits += 1
			node = node.parent

	def mostVisitedChild(self, node):
		best = node.children[0]
		for i in node.children:
			if i.visits > best.visits:
				best = i
		return best

# debug
matrix = [
	[0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 2, 1, 0, 0],
	[1, 0, 0, 1, 0, 1, 0],
	[2, 2, 0, 2, 1, 0, 1],
	[1, 2, 2, 1, 0, 0, 1],
]
state = State(matrix=matrix)

print(state.getIntelligentAction())

#agent = Agent(state)

#node = agent.findNextAction(200)
#action = node.state.lastAction

#for child in agent.root.children:
#	print("action:", child.state.lastAction, " wins:", child.wins, " visits:", child.visits)
#print(action)
#end debug