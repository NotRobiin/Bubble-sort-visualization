import pygame
import random
import time

class Config:
	def __init__(self):
		self.windowSize = (1280, 720)
		self.windowTitle = "Bubble sort visualization"

		self.arrayItems = 25
		self.arrayRange = (0, 50)

		self.fps = 20

		self.minimumHeight = 0
		self.maximumHeight = self.windowSize[1] - round(self.windowSize[1] / 10)

		self.offsetX = 5
		self.offsetY = 5
		self.offsetYtop = 0

		self.closeAfterSort = False

		self.fontRender = True

		if self.fontRender:
			self.renderIterationsOnly = False
			self.fontVertical = False
			self.fontType = "Arial"
			self.fontBold = True
			self.fontSize = 14
			self.font = None
			self.offsetYtop = round(self.fontSize * 3)

		self.color = {
			"background" : (140, 140, 140),
			"neutralLine" : (220, 220, 220),
			"higherLine" : (20, 200, 20),
			"backgroundIterations" : (40, 40, 40),
			"numbers" : (160, 0, 0),
			"highlightNumbers" : (20, 200, 20),
			"errorMessage" : (200, 0, 0)
		}

class Visualization:
	def __init__(self, config):
		self.config = config
		self.array = []
		self.arrayIndex = 0
		self.arrayLength = 0
		self.arraySorted = False
		self.sortCount = 0
		self.highlight = 0
		self.iterations = 0
		self.startTime = 0
		self.endTime = 0

		self.createArray()
		self.setup()
		self.loop()

	def setup(self):
		pygame.init()

		self.window = pygame.display.set_mode(self.config.windowSize)

		pygame.display.set_caption(self.config.windowTitle)

		self.clock = pygame.time.Clock()

		self.setupFont()

	def setupFont(self):
		if not self.config.fontRender:
			return

		self.config.font = pygame.font.SysFont(self.config.font, self.config.fontSize)
		self.config.font.set_bold(self.config.fontBold)

	def createArray(self):
		self.array = [
			random.randint(self.config.arrayRange[0], self.config.arrayRange[1]) for _ in range(self.config.arrayItems)
		]

		self.arrayLength = len(self.array)

	def getLineWidth(self):
		return round((self.config.windowSize[0] / self.arrayLength) / 2)

	def getLineX(self, lineIndex, width):
		return round((self.config.windowSize[0] / self.arrayLength) * lineIndex) + self.config.offsetX + round(width / 2)

	def getLineY(self):
		return self.config.windowSize[1] - self.config.offsetY

	def getLineColor(self, lineIndex):
		if(lineIndex == self.highlight):
			return self.config.color["higherLine"]

		return self.config.color["neutralLine"]

	def getLineEndY(self, lineIndex):
		if(self.array[lineIndex]):
			return self.config.maximumHeight - (self.config.maximumHeight * (self.array[lineIndex] / self.config.arrayRange[1])) + self.config.offsetYtop
		
		else:
			return self.config.windowSize[1] - self.config.minimumHeight - self.config.offsetYtop

	def drawBackground(self):
		self.window.fill(self.config.color["background"])

	def drawIterations(self):
		text = self.config.font.render(f"Iterations: {self.iterations}", True, self.config.color["backgroundIterations"])
		self.drawText(text, round(self.config.windowSize[0] / 2) + self.config.offsetX - round(text.get_width() / 2), round(self.config.windowSize[1] / 2))

	def drawHorizontalNumbers(self, lineIndex, x):
		text = self.config.font.render(str(self.array[lineIndex]), True, self.highlight == lineIndex and self.config.color["highlightNumbers"] or self.config.color["numbers"])
		self.drawText(text, x - round(text.get_width() / 2), text.get_height())

	def drawVerticalNumbers(self, lineIndex, x):
		plainText = str(self.array[lineIndex])
		text = self.config.font.render(str(self.array[lineIndex]), True, self.highlight == lineIndex and self.config.color["highlightNumbers"] or self.config.color["numbers"])
		self.drawText(text, x, 0, True, plainText)

	def drawTimeElapsed(self):
		text = self.config.font.render("Time elapsed: %0.2f" %(self.arraySorted and self.endTime - self.startTime or time.time() - self.startTime), True, self.config.color["backgroundIterations"])
		self.drawText(text, round(self.config.windowSize[0] / 2) + self.config.offsetX - round(text.get_width() / 2), round(self.config.windowSize[1] / 2) + text.get_height())

	def drawError(self, message):
		text = self.config.font.render(f"ERROR: {message}", True, self.config.color["errorMessage"])
		self.drawText(text, 0, 0)

	def loop(self):
		self.startTime = time.time()

		while True:
			self.clock.tick(self.config.fps)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()

			if not self.arraySorted:
				if self.arrayIndex == self.arrayLength - 1:
					self.arrayIndex = 0

				if self.sortCount > self.arrayLength:
					self.finish()

					if self.config.closeAfterSort:
						break

				self.sort()

			self.draw()

			pygame.display.update()

	def draw(self):
		self.drawBackground()

		for iterator in range(self.arrayLength):
			w = self.getLineWidth()
			x = self.getLineX(iterator, w)
			y = self.getLineY()
			c = self.getLineColor(iterator)
			endY = self.getLineEndY(iterator)

			self.drawLine(x, y, endY, w, c)

			if not self.config.fontRender:
				continue

			self.drawIterations()

			if not self.config.renderIterationsOnly:
				if self.config.fontVertical:
					self.drawVerticalNumbers(iterator, x)

				else:
					self.drawHorizontalNumbers(iterator, x)

				self.drawTimeElapsed()

	def drawLine(self, x, y, endY, w, c):
			pygame.draw.line(self.window, c, (x, y), (x, endY), w)

	def drawText(self, text, x, y, vertical = False, plainText = ""):
		if vertical:
			for i, char in enumerate(plainText):
				temporaryText = self.config.font.render(char, True, self.config.color["numbers"])
				self.window.blit(temporaryText, (x, y + (text.get_height() * i)))

		else:
			self.window.blit(text, (x, y))


	def sort(self):
		if(self.arrayLength <= 1):
			self.drawError(f"Invalid array length ({len(self.array)})")

			self.quit()

		self.highlight = self.arrayIndex + 1

		if self.array[self.arrayIndex] > self.array[self.arrayIndex + 1]:
			self.array[self.arrayIndex], self.array[self.arrayIndex + 1] = self.array[self.arrayIndex + 1], self.array[self.arrayIndex]

			self.sortCount = 0
		else:
			self.sortCount += 1

		self.arrayIndex += 1
		self.iterations += 1

	def quit(self):
		pygame.quit()
		quit()

	def finish(self):
		self.arraySorted = True
		self.endTime = time.time()

		print(f"Finished in {self.iterations + 1} iterations.\nTime elapsed: {int(self.endTime - self.startTime)}")

if __name__ == "__main__":
	config = Config()
	visual = Visualization(config)