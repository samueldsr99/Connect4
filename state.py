from random import choice

# State definition:
# 6x7 matrix (can be optimized)
# 	0 - empty space
# 	1 - player's 1 ball
# 	2 - player's 2 ball
# player's turn
# lastAction: evident
# FilledCols: number of cols filled by circles

# action is the col of the matrix to put the circle

class State():
	def __init__(self, matrix=None, turn=1, lastAction=None, FilledCols=0, AvailableActions=[0,1,2,3,4,5,6]):
		self.matrix = matrix
		if matrix == None:
			self.matrix = []
			for i in range(6):
				self.matrix.append([])
				for j in range(7):
					self.matrix[-1].append(0)
		self.turn = turn
		self.AvailableActions = AvailableActions
		self.lastAction = lastAction
		self.FilledCols = FilledCols
	
	def copy(self):
		nmatrix = []
		for i in range(6):
			nmatrix.append([])
			for j in range(7):
				nmatrix[i].append(self.matrix[i][j])
		return State(matrix=nmatrix, turn=self.turn, lastAction=self.lastAction, FilledCols=self.FilledCols, AvailableActions=self.AvailableActions.copy())

	# Fast
	def switchToNextPlayer(self):
		self.turn = 3 - self.turn

	def applyAction(self, action):
		self.lastAction = action

		for i in range(5, -1, -1):
			if self.matrix[i][action] == 0:
				if i == 0:
					self.FilledCols += 1
					self.AvailableActions.remove(action)
				self.matrix[i][action] = self.turn
				self.switchToNextPlayer()
				break

	# Who Win based on the last action
	def whoWin(self):
		if self.lastAction == None:
			return 0
		
		pWinner = self.nextPlayerTurn(self.turn)
		# Vertical
		p = 0
		col = self.lastAction
		row = 0
		for i in range(5, -1, -1):
			p = p + 1 if self.matrix[i][col] == pWinner else 0
			
			if p == 4:
				return pWinner

			if self.matrix[i][col] == 0 and row == 0:
				row = i + 1

		# Horizontal
		left, right = col, col
		while left - 1 >= 0 and self.matrix[row][left - 1] == pWinner:
			left -= 1
			if right - left + 1 == 4:
				return pWinner
		
		while right + 1 < 7 and self.matrix[row][right + 1] == pWinner:
			right += 1
			if right - left + 1 == 4:
				return pWinner
		
		# Diagonal 1
		left, right = [row, col], [row, col]
		while self.IN(left[0] - 1, left[1] - 1) and self.matrix[left[0] - 1][left[1] - 1] == pWinner:
			left[0] -= 1; left[1] -= 1
			if right[1] - left[1] + 1 == 4:
				return pWinner
		
		while self.IN(right[0] + 1, right[1] + 1) and self.matrix[right[0] + 1][right[1] + 1] == pWinner:
			right[0] += 1; right[1] += 1
			if right[1] - left[1] + 1 == 4:
				return pWinner

		# Diagonal 2
		left, right = [row, col], [row, col]
		while self.IN(left[0] + 1, left[1] - 1) and self.matrix[left[0] + 1][left[1] - 1] == pWinner:
			left[0] += 1; left[1] -= 1
			if right[1] - left[1] + 1 == 4:
				return pWinner
		
		while self.IN(right[0] - 1, right[1] + 1) and self.matrix[right[0] - 1][right[1] + 1] == pWinner:
			right[0] -= 1; right[1] += 1
			if right[1] - left[1] + 1 == 4:
				return pWinner

		# Tie
		return 0

	def isTerminal(self):
		return self.whoWin() != 0 or self.isFilled(self.matrix)

	def getRandomAction(self):
		action = choice(self.AvailableActions)
		return action

	def getIntelligentAction(self):
		for i in range(7):
			state = self.copy()
			if state.validMove(i):
				state.applyAction(i)
				if state.whoWin() == self.turn:
					return i
		return self.getRandomAction()

	# Fast
	def validMove(self, action):
		return self.matrix[0][action] == 0

	# Fast
	def nextPlayerTurn(self, turn):
		return 3 - turn

	# Fast
	def IN(self, row, col):
		return row >= 0 and row < 6 and col >= 0 and col < 7

	# Fast
	def isFilled(self, matrix):
		return self.FilledCols == 7
