
# State definition:
# 6x7 matrix (can be optimized)
# 	0 - empty space
# 	1 - player's 1 ball
# 	2 - player's 2 ball
# player's turn
# lastAction: evident

# action is the col of the matrix to put the circle

class State():
	def __init__(self, matrix=None, turn=1, lastAction=None):
		self.matrix = matrix
		if matrix == None:
			self.matrix = []
			for i in range(6):
				self.matrix.append([])
				for j in range(7):
					self.matrix[-1].append(0)
		self.turn = turn
		self.lastAction = lastAction

	# in methods
	
	def copy(self):
		nmatrix = []
		for i in range(6):
			nmatrix.append([])
			for j in range(7):
				nmatrix[i].append(self.matrix[i][j])
		return State(matrix=nmatrix, turn=self.turn, lastAction=self.lastAction)

	def switchToNextPlayer(self):
		self.turn = 3 - self.turn

	def applyAction(self, action):
		self.lastAction = action

		for i in range(5, -1, -1):
			if self.matrix[i][action] == 0:
				self.matrix[i][action] = self.turn
				self.switchToNextPlayer()
				break

	def whoWin(self):
		dr = [0, 1, 1, -1]
		dc = [1, 0, 1, 1]

		for r1 in range(6):
			for c1 in range(7):
				for d in range(4):
					if self.matrix[r1][c1] == 0:
						continue
					r2 = r1 + dr[d]
					c2 = c1 + dc[d]
					r3 = r1 + dr[d] * 2
					c3 = c1 + dc[d] * 2
					r4 = r1 + dr[d] * 3
					c4 = c1 + dc[d] * 3
					if self.IN(r4, c4) and self.IN(r3, c3) and self.IN(r2, c2):
						if (self.matrix[r1][c1] == self.matrix[r2][c2] and self.matrix[r2][c2] == self.matrix[r3][c3]
						and self.matrix[r3][c3] == self.matrix[r4][c4]):
							return self.matrix[r1][c1]
		return 0

	def isTerminal(self):
		return self.whoWin() != 0 or self.isFilled(self.matrix)

	def getRandomAction(self):
		moves = []
		for i in range(7):
			if self.validMove(i):
				moves.append(i)

		from random import random
		it = int( random() * len(moves) )
		return moves[it]

	def getIntelligentAction(self):
		for i in range(7):
			state = self.copy()
			if state.validMove(i):
				state.applyAction(i)
				if state.whoWin() == self.turn:
					return i
		return self.getRandomAction()

	# static methods

	def validMove(self, action):
		return self.matrix[0][action] == 0

	def nextPlayerTurn(self, turn):
		return 3 - turn

	def IN(self, row, col):
		return row >= 0 and row < 6 and col >= 0 and col < 7

	def isFilled(self, matrix):
		for i in range(7):
			if matrix[0][i] == 0:
				return False
		return True