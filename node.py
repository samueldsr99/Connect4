from state import State

class Node():
	def __init__(self, state=State()):
		self.state = state
		self.children = []
		self.parent = None
		self.wins = 0
		self.visits = 0
		self.actions = []
		for i in range(7):
			if self.state.validMove(i):
				self.actions.append(i)
		self.isFullyExpanded = bool( len(self.actions) == 0 )

	def getRandomChild(self):
		from random import random

		it = int( random() * len(self.actions) )
		return self.actions[it]

	def expand(self):

		action = self.getRandomChild()

		nstate = self.state.copy()
		nstate.applyAction(action)
		
		node = Node(nstate)

		self.actions.remove(action)

		if len(self.actions) == 0:
			self.isFullyExpanded = True

		self.children.append(node)
		node.parent = self

		return node
