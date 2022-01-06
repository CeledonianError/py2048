# Name:        CeledonianError
# Date:        December 8th, 2021
# Course:      ICS4U
# File name:   py2048.py
# Description: NOTE: This expects you to have the font Atkinson Hyperlegible
#			to be installed. Get the font here: 
#						https://brailleinstitute.org/freefont
#			It also expects a font called "Monospace" to be installed.
#			If you don't want to/can't install the fonts, they are called on 
#		the following lines and can easily be switched to fonts you do have 
#		installed: 173 - Atkinson Hyperlegible
#				   193 - Monospace
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#		The "simple" game of 2048, uses tkinter for GUI.
# 			2048 is a tile-matching game. With each move (up, down, left or 
#		right), every tile on the 4x4 board is moved as far in that 
#		direction as it can go. If it collides with the same valued tile, 
#		they are added together ONCE. If tiles merge and end up beside a tile
# 		of the same, new value, they do not get merged. Merging starts at the 
#		side of the board that corrosponds to the inputted direction.
#	  i.e.: if the board is as follows:  2 0 2 4 
#										 2 0 0 2
#										 4 0 4 0
#		and the player presses RIGHT,	 2 2 2 4
#									- - - - - - - - - 
#		the resulting board should be:	 0 0 4 4 
#										 0 0 0 4
#										 0 0 0 8
#										 0 2 4 4
# 			At the start, 2 tiles (valued either 2 or 4, more likely to be 2)
# 		are randomly placed. After every move, if there are any empty tiles
#		remaining, a random 2, or, less likely, 4, valued tile will be 
#		generated. The game ends if the board is filled and there are no valid
# 		moves left. The player wins if they create a tile with value 2048.
#			The game can continue past 2048, but this program will not react to
# 		the player creating a 4096, or higher, tile. It will only produce a win 
# 		state for a 2048 tile.

from tkinter import *
from tkinter import messagebox
import random
import copy

#   Columns: 0  1  2  3
boardInt = [[0, 0, 0, 0], # Row 0
			[0, 0, 0, 0], # Row 1
			[0, 0, 0, 0], # Row 2
			[0, 0, 0, 0]] # Row 3
# Position = [row][column]

boot = True

def summonRandom(): # Summon new tiles
	global boardInt
	weightedRand = [2, 2, 2, 2, 4]
	boardList = []
	for row in range(4):
		for col in range(4):
			boardList.append(boardInt[row][col])
	if any(boardInt):
		while True:
			randRow = random.randint(0, 3)
			randCol = random.randint(0, 3)
			if boardInt[randRow][randCol] == 0:
				boardInt[randRow][randCol] = random.choice(weightedRand)
				break

def rotateBoard(board, numRot):
	for i in range(numRot):
		board = zip(*board[::-1])
		board = [list(i) for i in board]
	return board

def simMove(boardInt): # Simulate merging tiles
	for row in range(4):
		for col in range(4):
			if boardInt[row][col] != 0:
				try:
					if boardInt[row][col] == boardInt[row + 1][col]:
						return True
				except IndexError:
					pass

def checkWinLose(board):
	# Check if player has won by looking for 2048 tile
	# If no 2048 tile, look to see if there's any valid moves left
	# W = win
	# C = continue
	# L = loss
	for row in range(4):
		for col in range(4):
			if board[row][col] == 2048:
				return "W"
	for row in range(4):
		for col in range(4):
			if board[row][col] == 0:
				return "C"
	# Simulate moves
	#		Up/Down				Left/Right				
	if simMove(board) or simMove(rotateBoard(board, 1)):
		return "C"
	else:
		return "L"

def checkMerge(boardInt): # Check for tiles to merge
	for row in range(4):
		for col in range(4):
			if boardInt[row][col] != 0:
				try:
					if boardInt[row][col] == boardInt[row + 1][col]:
						boardInt[row][col] *= 2
						boardInt[row + 1][col] = 0
				except IndexError:
					pass
	return boardInt

def moveUp(boardInt):
	oldBoard = copy.deepcopy(boardInt) # why has python forsaken me
	def move():
		for _ in range(6): # Move tiles
			for row in range(3, -1, -1):
				for col in range(3, -1, -1):
					checkRow = row - 1
					try:
						for _ in range(3):
							if boardInt[checkRow][col] == 0 and checkRow != -1:
								boardInt[checkRow][col] = boardInt[row][col]
								for i in range(1,4): # Move the rest of the rows
									boardInt[row][col] = boardInt[row + i][col]
								boardInt[row][col] = 0
					except IndexError:
						boardInt[row][col] = 0
	move()
	boardInt = checkMerge(boardInt)
	move()
	if boardInt != oldBoard:
		summonRandom()

def moveDown(boardInt): # Move tiles down by flipping then moving up
	def flipBoard(board):
		global boardInt
		board = boardInt
		for _ in range(3):
			upsideDownBoard = []
			for row in range(3, -1, -1):
				upsideDownBoard.append(board[row])
		return upsideDownBoard
	flipBoard(moveUp(flipBoard(boardInt)))

def moveLeft(board): # Move tiles left
	global boardInt
	boardInt = rotateBoard(boardInt, 1)
	moveUp(boardInt)
	boardInt = rotateBoard(boardInt, 3)

def moveRight(board): # Move tiles right
	global boardInt
	boardInt = rotateBoard(boardInt, 1)
	moveDown(boardInt)
	boardInt = rotateBoard(boardInt, 3)



def main():
	global boardInt
	global boot

	if boot: # Summon first 2 random tiles
		summonRandom()
		summonRandom()
		boot = False

	atkinsonInput = ("Atkinson Hyperlegible", 12)

	guiBoard = Tk() # Window
	guiBoard.title("2048")
	guiBoard.configure(bg="#112233")
	guiBoard.resizable(False, False)

	def updateBoard(board): # Force update board
		# Destroy old buttons (makes everything flash, but looks a lot nicer)
		for widget in guiBoard.grid_slaves():
			widget.destroy()
		inputButtons()
		# Create grid out of buttons for the board
		for row in range(0, 4):
			for col in range(0, 4):
				if board[row][col] != 0: # Generate colour by doing uhhhhhh this
					colour = ("#" + str(hex(board[row][col] ** 3))[2:].zfill(2)\
						.replace("0", "C") + "FFFF")[:7]
					tile = Button(guiBoard, text = board[row][col], bg = colour,\
						activebackground=colour, borderwidth=3,\
						highlightbackground="#556677", font=("Monospace", 15))
					tile.grid(row = row, column = col, sticky="NEWS")
				else:
					tile = Button(guiBoard, text = " ", bg="#112233",\
						activebackground="#112233", relief="flat",\
						highlightbackground="#334455")
					tile.grid(row = row, column = col, sticky="NEWS")
		# Check if the player has won or lost after updating the board
		if checkWinLose(boardInt) == "W":
			messagebox.showinfo(title = "2048", message = "Congrats! \nYou won!")
		elif checkWinLose(boardInt) == "L":
			messagebox.showinfo(title = "2048", message = "No valid moves left!")
			guiBoard.destroy()

	def inputButtons(): # Controls
		spacer = Button(guiBoard, text = " ", bg="#112233",\
			activebackground="#112233", relief="flat",\
			highlightbackground="#112233")
		spacer.grid(row = 0, column = 4)
		buttonUp = Button(guiBoard, text = "Up", command=lambda:[moveUp\
			(boardInt), updateBoard(boardInt)], bg="#334455", fg="white",\
			font=atkinsonInput)
		buttonUp.grid(row = 0, column = 6)
		buttonLeft = Button(guiBoard, text = "Left", command=lambda:[moveLeft\
			(boardInt), updateBoard(boardInt)], bg="#334455", fg="white",\
			font=atkinsonInput)
		buttonLeft.grid(row = 1, column = 5)
		buttonRight = Button(guiBoard, text = "Right", command=lambda:[moveRight\
			(boardInt), updateBoard(boardInt)], bg="#334455", fg="white",\
			font=atkinsonInput)
		buttonRight.grid(row = 1, column = 7)
		buttonDown = Button(guiBoard, text = "Down", command=lambda:[moveDown\
			(boardInt), updateBoard(boardInt)], bg="#334455", fg= "white",\
			font=atkinsonInput)
		buttonDown.grid(row = 2, column = 6)

	updateBoard(boardInt)
	guiBoard.mainloop()

if __name__ == "__main__":
	main()
