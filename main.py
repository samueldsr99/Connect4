import pygame
from pygame.locals import *
from state import State
from agent import Agent

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
				if self.curState.matrix[i][j] == 1:
					color = (255, 0, 0)
				if self.curState.matrix[i][j] == 2:
					color = (0, 0, 255)
				pygame.draw.circle(self.screen, color, (self.circle[i][j][0], self.circle[i][j][1]), 20, 20)


	def run(self):
		it = 0
		pygame.time.delay(100)

		self.print_screen()
		while self.running and not self.curState.isTerminal():

			self.print_screen()
			pygame.display.update()

			if self.curState.turn == 2:

				from time import time
				initTime = time()

				agent = Agent(self.curState)
				node = agent.findNextAction(1500)
				action = node.state.lastAction
				self.curState.applyAction(action)

				# statistics
				it += 1
				print("move #:", it, " turn:", self.curState.turn)
				for child in agent.root.children:
					print("action:", child.state.lastAction, " wins:", child.wins, " visits:", child.visits)
				print("move chosen:", action, "wins:", node.wins, "simulations:", node.visits, "win rate:", node.wins / node.visits)
				endTime = time()
				print("response time:", endTime - initTime)
				# end statistics

			for event in pygame.event.get():
				if event.type == QUIT:
					self.running = False

				if event.type == MOUSEBUTTONDOWN:
					x = event.pos[0]
					if self.curState.turn == 1:
						for i in range(7):
							if self.circle[0][i][0] - 20 <= x and x <= self.circle[0][i][0] + 20:
								if self.curState.validMove(i):
									it += 1
									print("move #:", it, " turn:", self.curState.turn)
									print(i)
									self.curState.applyAction(i)
		self.print_screen()
		pygame.display.update()
		print("winner: ", self.curState.whoWin())
		
		ed = False

		while True:
			if ed:
				break
			for event in pygame.event.get():
				if event.type == QUIT:
					ed = True
		pygame.quit()


app = App()

app.run()

#funciona bien, pero queda optimizarlo para aumentar las iteraciones.
#es posible vencerle si se juega de 1ro, no le he vencido jugando de 2do.
#para los cambios futuros es recomendable hacer una copia de esta version, pues es bastante estable