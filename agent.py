from node import Node
from state import State

# Agent that implements Monte Carlo Tree Search

class Agent():
	def __init__(self, state=State(), actionMethod="random"):
		import math
		self.root = Node(state)
		self.c = math.sqrt(2) # constant c
		self.actionMethod = actionMethod

	def calculateValue(self, node):
		import math
		return node.wins / node.visits + self.c * ( math.log(node.parent.visits) / node.visits )

	def findNextAction(self, iterations):
		for _ in range(iterations):
			# 1 selection
			node = self.findChild(self.root)

			# 2 expansion
			if not node.state.IsTerminal() and not node.IsFullyExpanded:
				node = node.expand()

			# 3 playout
			result = self.playout(node)

			# 4 backpropagation
			self.backpropagate(node, result)

		return self.mostVisitedChild(self.root)


	def findChild(self, node):
		while not node.state.IsTerminal() and node.IsFullyExpanded:
			node = self.findBestChild(node)
		return node

	def findBestChild(self, node):
		best = node.children[0]
		for i in node.children:
			if self.calculateValue(i) > self.calculateValue(best):
				best = i
		return best

	def playout(self, node):
		curState = node.state.Copy()

		while not curState.IsTerminal():
			if self.actionMethod == "intelligent":
				action = curState.GetIntelligentAction()
			else:
				action = curState.GetRandomAction()
			curState.ApplyAction(action)
		return curState.WhoWin()

	def backpropagate(self, node, result):
		while node != None:
			if node.state.Turn != result:
				node.wins += 1
			node.visits += 1
			node = node.parent

	def mostVisitedChild(self, node):
		best = node.children[0]
		for i in node.children:
			if i.visits > best.visits:
				best = i
		return best

if __name__ == '__main__':
	# debug
	matrix = [
		[0, 0, 2, 0, 2, 0, 1],
		[0, 0, 1, 0, 1, 0, 2],
		[1, 2, 2, 0, 1, 1, 2],
		[2, 1, 1, 1, 2, 1, 1],
		[2, 1, 1, 2, 2, 1, 2],
		[2, 1, 1, 2, 1, 2, 2],
	]
	state = State(matrix=matrix, lastAction=3, turn=2, FilledCols=3)
