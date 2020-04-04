from random import choice

# State definition:
# 6x7 Matrix
# 	0 - empty space
# 	1 - player's 1 ball
# 	2 - player's 2 ball
# player's turn
# LastAction: last action
# FilledCols: number of cols filled by circles

# action is the col of the Matrix to put the circle

class State():
	def __init__(self, matrix=None, turn=1, lastAction=None, filledCols=0, availableActions=[0,1,2,3,4,5,6]):
		self.Matrix = matrix
		if matrix == None:
			self.Matrix = []
			for i in range(6):
				self.Matrix.append([])
				for j in range(7):
					self.Matrix[-1].append(0)
		self.Turn = turn
		self.AvailableActions = availableActions
		self.LastAction = lastAction
		self.FilledCols = filledCols
	
	def Copy(self):
		nmatrix = []
		for i in range(6):
			nmatrix.append([])
			for j in range(7):
				nmatrix[i].append(self.Matrix[i][j])
		return State(matrix=nmatrix, turn=self.Turn, lastAction=self.LastAction, filledCols=self.FilledCols, availableActions=self.AvailableActions.copy())

	# Fast
	def SwitchToNextPlayer(self):
		self.Turn = 3 - self.Turn

	def ApplyAction(self, action):
		self.LastAction = action

		for i in range(5, -1, -1):
			if self.Matrix[i][action] == 0:
				if i == 0:
					self.FilledCols += 1
					self.AvailableActions.remove(action)
				self.Matrix[i][action] = self.Turn
				self.SwitchToNextPlayer()
				break

	# Who Win based on the last action
	def WhoWin(self):
		if self.LastAction == None:
			return 0
		
		pWinner = State.NextPlayerTurn(self.Turn)
		# Vertical
		p = 0
		col = self.LastAction
		row = 0
		for i in range(5, -1, -1):
			p = p + 1 if self.Matrix[i][col] == pWinner else 0
			
			if p == 4:
				return pWinner

			if self.Matrix[i][col] == 0 and row == 0:
				row = i + 1

		# Horizontal
		left, right = col, col
		while left - 1 >= 0 and self.Matrix[row][left - 1] == pWinner:
			left -= 1
			if right - left + 1 == 4:
				return pWinner
		
		while right + 1 < 7 and self.Matrix[row][right + 1] == pWinner:
			right += 1
			if right - left + 1 == 4:
				return pWinner
		
		# Diagonal 1
		left, right = [row, col], [row, col]
		while self.In(left[0] - 1, left[1] - 1) and self.Matrix[left[0] - 1][left[1] - 1] == pWinner:
			left[0] -= 1; left[1] -= 1
			if right[1] - left[1] + 1 == 4:
				return pWinner
		
		while self.In(right[0] + 1, right[1] + 1) and self.Matrix[right[0] + 1][right[1] + 1] == pWinner:
			right[0] += 1; right[1] += 1
			if right[1] - left[1] + 1 == 4:
				return pWinner

		# Diagonal 2
		left, right = [row, col], [row, col]
		while self.In(left[0] + 1, left[1] - 1) and self.Matrix[left[0] + 1][left[1] - 1] == pWinner:
			left[0] += 1; left[1] -= 1
			if right[1] - left[1] + 1 == 4:
				return pWinner
		
		while self.In(right[0] - 1, right[1] + 1) and self.Matrix[right[0] - 1][right[1] + 1] == pWinner:
			right[0] -= 1; right[1] += 1
			if right[1] - left[1] + 1 == 4:
				return pWinner

		# Tie
		return 0

	def IsTerminal(self):
		return self.WhoWin() != 0 or self.IsFilled(self.Matrix)

	def GetRandomAction(self):
		action = choice(self.AvailableActions)
		return action

	def GetIntelligentAction(self):
		for i in range(7):
			state = self.Copy()
			if self.ValidMove(i):
				state.ApplyAction(i)
				if state.WhoWin() == self.Turn:
					return i
		return self.GetRandomAction()

	# Fast
	def IsFilled(self, Matrix):
		return self.FilledCols == 7
	# Fast
	def ValidMove(self, action):
		return self.Matrix[0][action] == 0

	# Fast
	@staticmethod
	def NextPlayerTurn(turn):
		return 3 - turn

	# Fast
	@staticmethod
	def In(row, col):
		return row >= 0 and row < 6 and col >= 0 and col < 7
