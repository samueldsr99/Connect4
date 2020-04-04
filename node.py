from state import State
from random import choice

class Node():
	def __init__(self, state=State()):
		self.state = state
		self.children = []
		self.parent = None
		self.wins = 0
		self.visits = 0
		self.actions = state.AvailableActions.copy()
		self.IsFullyExpanded = bool( len(self.actions) == 0 )

	def getRandomChild(self):
		return choice(self.actions)

	def expand(self):

		action = self.getRandomChild()

		nstate = self.state.Copy()
		nstate.ApplyAction(action)
		
		node = Node(nstate)

		self.actions.remove(action)

		if len(self.actions) == 0:
			self.IsFullyExpanded = True

		self.children.append(node)
		node.parent = self

		return node
