import pygame
from pygame.locals import *
from state import State
from agent import Agent
from time import time
from logs import Log

class App:
	def __init__(self):
		pygame.init()
		flags = RESIZABLE
		self.screen = pygame.display.set_mode((640, 480), flags)
		self.running = True
		pygame.display.set_caption("Connect 4")

		# editable options
		self.bgcolor = (200, 200, 200)
		self.curState = State()

		# circle coords:
		self.circle = []

		for i in range(6):
			self.circle.append([])

			for j in range(7):
				if i == 0 and j == 0:
					self.circle[i].append([160, 100])
				elif j == 0:
					self.circle[i].append(self.circle[i - 1][j].copy())
					self.circle[i][j][1] += 55
				else:
					self.circle[i].append(self.circle[i][j - 1].copy())
					self.circle[i][j][0] += 55


	def print_screen(self):
		self.screen.fill(self.bgcolor)

		for i in range(len(self.circle)):
			for j in range(len(self.circle[i])):
				color = (100, 100, 100)
				if self.curState.Matrix[i][j] == 1:
					color = (255, 0, 0)
				if self.curState.Matrix[i][j] == 2:
					color = (0, 0, 255)
				pygame.draw.circle(self.screen, color, (self.circle[i][j][0], self.circle[i][j][1]), 20, 20)


	def run(self, verbose=False, iterations=3000):
		logs = Log()
		logs.log("Iterations: " + str(iterations))
		logs.log("Action Method: random")

		pygame.time.delay(100)

		self.print_screen()
		while self.running and not self.curState.IsTerminal():

			self.print_screen()
			pygame.display.update()

			# Agent's Turn
			if self.curState.Turn == 2:
				
				initTime = time()

				agent = Agent(self.curState, actionMethod="random")
				node = agent.findNextAction(3000)
				action = node.state.LastAction
				self.curState.ApplyAction(action)

				endTime = time()

				logs.RegisterLastAction(State.NextPlayerTurn(self.curState.Turn), action, node.wins, node.visits, endTime-initTime)
				if verbose:
					print(logs.LastActionStatistics())

			# Player's Turn
			for event in pygame.event.get():
				if event.type == QUIT:
					self.running = False

				if event.type == MOUSEBUTTONDOWN:
					x = event.pos[0]
					if self.curState.Turn == 1:
						for i in range(7):
							if self.circle[0][i][0] - 20 <= x and x <= self.circle[0][i][0] + 20:
								if self.curState.ValidMove(i):
									self.curState.ApplyAction(i)
									logs.RegisterLastAction(State.NextPlayerTurn(self.curState.Turn), i, 0, 0, 0)
		self.print_screen()
		pygame.display.update()
		winner = self.curState.WhoWin()

		if verbose:
			print("winner: ", winner)
		logs.log("Winner: " + str(winner))

		font = pygame.font.Font(None, 48)
		text = font.render("Winner: " + str(winner), False, (0, 0, 0))
		self.screen.blit(text, (20, 20))
		pygame.display.update()

		logs.SaveData()

		ed = False

		while True:
			if ed:
				break
			for event in pygame.event.get():
				if event.type == QUIT:
					ed = True
		pygame.quit()


app = App()

app.run(verbose=False, iterations=5000)
