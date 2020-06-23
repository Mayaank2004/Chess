import random as rand

import numpy as np
import pygame as pg

pg.init()


# def text_objects(text, font, color):
# 	textSurface = font.render(text, True, color)
# 	return textSurface, textSurface.get_rect()
#
#
# def text_display(text, x, y, color):
# 	largeText = pg.font.Font('freesansbold.ttf', 60)
# 	TextSurf, TextRect = text_objects(text, largeText, color)
# 	TextRect.center = (x, y)
# 	self.Display.blit(TextSurf, TextRect)


class Board:

	def __init__(self, state: np.array = None):
		self.START = (20, 20)
		self.SIZE = (70, 70)
		self.PIC_SIZE = (60, 60)
		self.State = State(state, castling=[[1, 1], [1, 1]])

	def addPiece(self, piece, pos):  # adds a piece to a square on the board
		if self.State.state[pos[0]][pos[1]] != 0:
			print('invalid move')
		else:
			self.State.state[pos[0]][pos[1]] = piece

	def set_default(self):  # resets the board to the starting position
		self.State.state = np.zeros((8, 8), dtype=np.int8)
		self.State.state[0] = [-5, -2, -3, -9, -10, -3, -2, -5]
		self.State.state[1] = [-1, -1, -1, -1, -1, -1, -1, -1]

		self.State.state[6] = [1, 1, 1, 1, 1, 1, 1, 1, ]
		self.State.state[7] = [5, 2, 3, 9, 10, 3, 2, 5]

	def show_board(self, super):  # Displays the board only (squares)

		COLORBACK = {
			0: (208, 180, 97),
			1: (147, 117, 26)
		}

		for a in range(8):
			for b in range(8):
				pg.draw.rect(super.Display, COLORBACK[(a + b) % 2],
				             [self.START[0] + a * self.SIZE[0], self.START[1] + b * self.SIZE[1], self.SIZE[0],
				              self.SIZE[1]])

	def show_pieces(self, super):  # displays the pieces
		COLORPIECE = {
			-1: (0, 0, 0),
			0: (255, 255, 255),
			1: (255, 255, 255)
		}
		self.PIECES = {
			-10: super.BKImg,
			-9: super.BQImg,
			-5: super.BRImg,
			-3: super.BBImg,
			-2: super.BNImg,
			-1: super.BPImg,
			0: super.Blank,
			1: super.WPImg,
			2: super.WNImg,
			3: super.WBImg,
			5: super.WRImg,
			9: super.WQImg,
			10: super.WKImg,

		}
		for a in range(8):
			for b in range(8):
				# print(self.state[0,7])
				super.Display.blit(self.PIECES[self.State.state[b][a]], (
					self.START[0] + a * self.SIZE[0] + (self.SIZE[0] - self.PIC_SIZE[0]) / 2,
					self.START[1] + b * self.SIZE[1] + (
							self.SIZE[1] - self.PIC_SIZE[1]) / 2))

	def __str__(self):
		return self.state.__str__()


class State:

	def __init__(self, state, castling):
		self.state = state
		self.castling = castling
		self.N_MOVES = self.set_N_MOVES()
		self.B_MOVES = self.set_B_MOVES()
		self.R_MOVES = self.set_R_MOVES()
		self.Q_MOVES = self.set_Q_MOVES()
		self.K_MOVES = self.set_K_MOVES()

	def verify_bishop(self, pos, total, blocks, opp, capture=False):  # finds valid moves for bishop

		final = []
		# quadrants
		q = [
			[n for n in total if (n[0] < pos[0] and n[1] > pos[1])],
			[n for n in total if (n[0] < pos[0] and n[1] < pos[1])],
			[n for n in total if (n[0] > pos[0] and n[1] < pos[1])],
			[n for n in total if (n[0] > pos[0] and n[1] > pos[1])],
		]

		qb = [
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in blocks if (n[0] < pos[0] and n[1] > pos[1])],
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in blocks if (n[0] < pos[0] and n[1] < pos[1])],
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in blocks if (n[0] > pos[0] and n[1] < pos[1])],
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in blocks if (n[0] > pos[0] and n[1] > pos[1])]
		]
		qob = [
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in opp if (n[0] < pos[0] and n[1] > pos[1])],
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in opp if (n[0] < pos[0] and n[1] < pos[1])],
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in opp if (n[0] > pos[0] and n[1] < pos[1])],
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in opp if (n[0] > pos[0] and n[1] > pos[1])]
		]
		# print(qb1, '\n', qb2, '\n', qb3, '\n', qb4)
		minB = [0] * 4
		minOB = [0] * 4

		for i in range(4):
			if len(qb[i]) > 0:
				minB[i] = min(qb[i])
			else:
				minB[i] = 100

			if len(qob[i]) > 0:
				minOB[i] = min(qob[i])
			else:
				minOB[i] = 101

		if not capture:

			for i in range(4):
				if minOB[i] < minB[i]:
					for x in q[i]:
						if np.abs(x[0] - pos[0]) + np.abs(x[1] - pos[1]) <= minOB[i]:
							final.append(x)
				else:
					for x in q[i]:
						if np.abs(x[0] - pos[0]) + np.abs(x[1] - pos[1]) < minB[i]:
							final.append(x)
		else:
			for i in range(4):
				if minOB[i] < minB[i]:
					for x in q[i]:
						if np.abs(x[0] - pos[0]) + np.abs(x[1] - pos[1]) <= minOB[i]:
							final.append(x)
				else:
					for x in q[i]:
						if np.abs(x[0] - pos[0]) + np.abs(x[1] - pos[1]) <= minB[i]:
							final.append(x)

		return final

	def verify_bishop2(self,pos,turn,capture= False):
		dirs = [(1,1),(1,-1),(1,-1),(-1,-1)]
		final =[]
		for dir in dirs:
			for len in range(1,8):
				moveX = len* dir[1] + pos[1]
				moveY = len * dir[0] + pos[0]

				if moveX >=0 and moveX <=7 and moveY >=0 and moveY <=7:
					if self.state[moveY,moveX] == 0:
						final.append((moveY,moveX))

					if self.state[moveY,moveX] *turn> 0:
						if capture:
							final.append((moveY, moveX))
						break
					if self.state[moveY, moveX] * turn < 0:
						final.append((moveY, moveX))
						break

		return final


	def verify_rook2(self,pos,turn,capture= False):
		dirs = [(0,1),(1,0),(0,-1),(-1,0)]
		final =[]
		for dir in dirs:
			for len in range(1,8):
				moveX = len* dir[1] + pos[1]
				moveY = len * dir[0] + pos[0]

				if moveX >=0 and moveX <=7 and moveY >=0 and moveY <=7:
					if self.state[moveY,moveX] == 0:
						final.append((moveY,moveX))

					if self.state[moveY,moveX] *turn> 0:
						if capture:
							final.append((moveY, moveX))
						break
					if self.state[moveY, moveX] * turn < 0:
						final.append((moveY, moveX))
						break

		return final
	def verify_queen(self, pos, total, blocks, opp, capture=False):  # finds valid moves for queen
		final = []
		# quadrants
		q = [
			[n for n in total if (n[0] < pos[0] and n[1] > pos[1])],
			[n for n in total if (n[0] < pos[0] and n[1] < pos[1])],
			[n for n in total if (n[0] > pos[0] and n[1] < pos[1])],
			[n for n in total if (n[0] > pos[0] and n[1] > pos[1])],
			[n for n in total if (n[0] == pos[0] and n[1] > pos[1])],
			[n for n in total if (n[0] < pos[0] and n[1] == pos[1])],
			[n for n in total if (n[0] == pos[0] and n[1] < pos[1])],
			[n for n in total if (n[0] > pos[0] and n[1] == pos[1])],
		]

		qb = [
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in blocks if (n[0] < pos[0] and n[1] > pos[1])],
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in blocks if (n[0] < pos[0] and n[1] < pos[1])],
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in blocks if (n[0] > pos[0] and n[1] < pos[1])],
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in blocks if (n[0] > pos[0] and n[1] > pos[1])],
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in blocks if (n[0] == pos[0] and n[1] > pos[1])],
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in blocks if (n[0] < pos[0] and n[1] == pos[1])],
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in blocks if (n[0] == pos[0] and n[1] < pos[1])],
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in blocks if (n[0] > pos[0] and n[1] == pos[1])]
		]

		qob = [
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in opp if (n[0] < pos[0] and n[1] > pos[1])],
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in opp if (n[0] < pos[0] and n[1] < pos[1])],
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in opp if (n[0] > pos[0] and n[1] < pos[1])],
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in opp if (n[0] > pos[0] and n[1] > pos[1])],
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in opp if (n[0] == pos[0] and n[1] > pos[1])],
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in opp if (n[0] < pos[0] and n[1] == pos[1])],
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in opp if (n[0] == pos[0] and n[1] < pos[1])],
			[np.abs(n[0] - pos[0]) + np.abs(n[1] - pos[1]) for n in opp if (n[0] > pos[0] and n[1] == pos[1])]
		]

		# print(qb1, '\n', qb2, '\n', qb3, '\n', qb4)
		minB = [0] * 8
		minOB = [0] * 8

		for i in range(8):
			if len(qb[i]) > 0:
				minB[i] = min(qb[i])
			else:
				minB[i] = 100

			if len(qob[i]) > 0:
				minOB[i] = min(qob[i])
			else:
				minOB[i] = 101

		if not capture:

			for i in range(8):
				if minOB[i] < minB[i]:
					for x in q[i]:
						if np.abs(x[0] - pos[0]) + np.abs(x[1] - pos[1]) <= minOB[i]:
							final.append(x)
				else:
					for x in q[i]:
						if np.abs(x[0] - pos[0]) + np.abs(x[1] - pos[1]) < minB[i]:
							final.append(x)
		else:

			for i in range(8):
				if minOB[i] < minB[i]:
					for x in q[i]:
						if np.abs(x[0] - pos[0]) + np.abs(x[1] - pos[1]) <= minOB[i]:
							final.append(x)
				else:
					for x in q[i]:
						if np.abs(x[0] - pos[0]) + np.abs(x[1] - pos[1]) <= minB[i]:
							final.append(x)
		return final

	def valid_capture(self, piece, pos, state=[]):  # finds the squares a piece controls (can  capture)
		# pos := (y downwards, x rightwards)
		if state == []:
			state = self.state
		turn = np.sign(piece)
		piece = np.abs(piece)
		if piece == 0:
			return []
		if piece == 1:
			tempMoves = []
			# print('pos = ', pos)
			if (turn == 1 and pos[0] != 0) or (turn == -1 and pos[0] != 7):
				if pos[1] > 0:
					tempMoves += [(pos[0] - turn, pos[1] - 1)]
				if pos[1] < 7:
					tempMoves += [(pos[0] - turn, pos[1] + 1)]

			return tempMoves

		if piece == 2:
			temp_moves = self.N_MOVES[pos[0]][pos[1]]
			return temp_moves

		if piece == 3:
			temp_moves = self.B_MOVES[pos[0]][pos[1]]
			blocks = []
			opp_blocks = []
			for n in temp_moves:
				if state[n[0]][n[1]] * turn > 0:
					blocks.append(n)
				if state[n[0]][n[1]] * turn < 0 and state[n[0]][n[1]] != -turn * 10:
					opp_blocks.append(n)

			final_moves = self.verify_bishop2(pos, turn, capture=True)
			return final_moves

		if piece == 5:
			temp_moves = self.R_MOVES[pos[0]][pos[1]]
			blocks = []
			opp_blocks = []
			for n in temp_moves:
				if state[n[0]][n[1]] * turn > 0:
					blocks.append(n)
				if state[n[0]][n[1]] * turn < 0 and state[n[0]][n[1]] != -turn * 10:
					opp_blocks.append(n)

			final_moves = self.verify_rook2(pos,turn, capture=True)
			return final_moves

		if piece == 9:
			temp_moves = self.Q_MOVES[pos[0]][pos[1]]
			# print('yeeeeeee', temp_moves)
			blocks = []
			opp_blocks = []
			for n in temp_moves:
				if state[n[0]][n[1]] * turn > 0:
					blocks.append(n)
				if state[n[0]][n[1]] * turn < 0 and state[n[0]][n[1]] != -turn * 10:
					opp_blocks.append(n)
			# print('blocks',blocks)

			final_moves = self.verify_queen(pos, temp_moves, blocks, opp_blocks, capture=True)
			# print('yeeeeeeeee',final_moves)
			return final_moves

		if piece == 10:
			final_moves = self.K_MOVES[pos[0]][pos[1]]

			return final_moves

	def detect_check(self, turn, king, move=None):  # finds if king is under check when a a move is made
		if move != None:
			temp_state = self.state.copy()
			temp_state[move[0]], temp_state[move[1]] = 0, temp_state[move[0]]

			opp_pieces = []
			for a in range(8):
				for b in range(8):
					if temp_state[a, b] * turn < 0:
						opp_pieces.append((temp_state[a, b], a, b))
			opp_moves = [self.valid_capture(piece, (pos0, pos1), temp_state) for piece, pos0, pos1 in opp_pieces]

			if any([king in blocks for blocks in opp_moves]):
				return True
			else:
				return False



		else:
			opp_pieces = []
			for a in range(8):
				for b in range(8):
					if self.state[a, b] * turn < 0:
						opp_pieces.append((self.state[a, b], a, b))
			opp_moves = [self.valid_capture(piece, (pos0, pos1)) for piece, pos0, pos1 in opp_pieces]

			if any([king in blocks for blocks in opp_moves]):
				return True
			else:
				return False

	def valid_moves(self, piece, pos):  # lists all the validmoves for a piece
		# pos := (y downwards, x rightwards)
		turn = np.sign(piece)
		piece = np.abs(piece)
		pos_King = ()
		for a in range(8):
			for b in range(8):
				if self.state[a, b] == turn * 10:
					pos_King = (a, b)

		if piece == 0:
			return []

		if piece == 1:
			tempMoves = []
			# print('pos = ', pos)
			if (turn == 1 and pos[0] != 0) or (turn == -1 and pos[0] != 7):
				if pos[1] > 0:
					if self.state[pos[0] - turn][pos[1] - 1] * turn < 0:
						# print('yes')
						tempMoves += [(pos[0] - turn, pos[1] - 1)]
				if pos[1] < 7:
					if self.state[pos[0] - turn][pos[1] + 1] * turn < 0:
						tempMoves += [(pos[0] - turn, pos[1] + 1)]

			if pos[0] == 3.5 + 2.5 * turn:

				if self.state[pos[0] - turn][pos[1]] != 0:
					tempMoves += []
				elif self.state[pos[0] - 2 * turn][pos[1]] != 0:
					tempMoves += [(pos[0] - turn, pos[1])]
				else:
					tempMoves += [(pos[0] - turn, pos[1]), (pos[0] - 2 * turn, pos[1])]
			elif (turn == 1 and pos[0] != 0) or (turn == -1 and pos[0] != 7):
				if self.state[pos[0] - turn][pos[1]] != 0:
					tempMoves += []
				else:
					tempMoves += [(pos[0] - turn, pos[1])]
			else:
				return []

			final_moves = [move for move in tempMoves if not self.detect_check(turn, pos_King, (pos, move))]
			return final_moves

		if piece == 2:
			temp_moves = self.N_MOVES[pos[0]][pos[1]]
			final_moves = []
			for n in temp_moves:
				if self.state[n[0]][n[1]] * turn <= 0:
					final_moves.append(n)

			final_moves = [move for move in final_moves if not self.detect_check(turn, pos_King, (pos, move))]
			return final_moves

		if piece == 3:
			temp_moves = self.B_MOVES[pos[0]][pos[1]]
			blocks = []
			opp_blocks = []
			for n in temp_moves:
				if self.state[n[0]][n[1]] * turn > 0:
					blocks.append(n)
				if self.state[n[0]][n[1]] * turn < 0:
					opp_blocks.append(n)

			final_moves = self.verify_bishop2(pos, turn)
			final_moves = [move for move in final_moves if not self.detect_check(turn, pos_King, (pos, move))]
			return final_moves

		if piece == 5:
			temp_moves = self.R_MOVES[pos[0]][pos[1]]
			blocks = []
			opp_blocks = []
			for n in temp_moves:
				if self.state[n[0]][n[1]] * turn > 0:
					blocks.append(n)
				if self.state[n[0]][n[1]] * turn < 0:
					opp_blocks.append(n)

			final_moves = self.verify_rook2(pos,turn)
			final_moves = [move for move in final_moves if not self.detect_check(turn, pos_King, (pos, move))]
			return final_moves

		if piece == 9:
			temp_moves = self.Q_MOVES[pos[0]][pos[1]]
			# print('yeeeeeee',temp_moves)
			blocks = []
			opp_blocks = []
			for n in temp_moves:
				if self.state[n[0]][n[1]] * turn > 0:
					blocks.append(n)
				if self.state[n[0]][n[1]] * turn < 0:
					opp_blocks.append(n)
			# print('blocks',blocks)

			final_moves = self.verify_queen(pos, temp_moves, blocks, opp_blocks)
			final_moves = [move for move in final_moves if not self.detect_check(turn, pos_King, (pos, move))]
			# print('yeeeeeeeee',final_moves)
			return final_moves

		if piece == 10:
			temp_moves = self.K_MOVES[pos[0]][pos[1]]
			final_moves = []
			for n in temp_moves:
				if self.state[n[0]][n[1]] * turn <= 0:
					final_moves.append(n)

			final_moves = [move for move in final_moves if not self.detect_check(turn, move)]

			if turn == 1 and pos == (7, 4):
				if self.castling[0][0] == 1:

					if not self.detect_check(turn, (7, 4)) and not self.detect_check(turn, (7, 5)) \
							and not self.detect_check(turn, (7, 6)) and self.state[7, 5] == self.state[7, 6] == 0:
						final_moves.append((7, 6))
				if self.castling[0][1] == 1:
					if not self.detect_check(turn, (7, 4)) and not self.detect_check(turn, (7, 3)) \
							and not self.detect_check(turn, (7, 2)) \
							and self.state[7, 3] == self.state[7, 2] == self.state[7, 1] == 0:
						final_moves.append((7, 2))

			if turn == -1 and pos == (0, 4):
				if self.castling[1][0] == 1:

					if not self.detect_check(turn, (0, 4)) and not self.detect_check(turn, (0, 5)) \
							and not self.detect_check(turn, (0, 6)) and self.state[0, 5] == self.state[0, 6] == 0:
						final_moves.append((0, 6))
				if self.castling[1][1] == 1:
					if not self.detect_check(turn, (0, 4)) and not self.detect_check(turn, (0, 3)) \
							and not self.detect_check(turn, (0, 2)) \
							and self.state[0, 3] == self.state[0, 2] == self.state[0, 1] == 0:
						final_moves.append((0, 2))

			return final_moves

	@classmethod
	def set_N_MOVES(cls):  # create movement pattern for Knight "L - shaped"
		N_MOVES = np.empty((8, 8), dtype=list)
		for a in range(8):
			for b in range(8):
				N_MOVES[a][b] = []
		for x1 in range(8):
			for y1 in range(8):
				for x2 in range(8):
					for y2 in range(8):
						if (y2 - y1)**2 + (x2 - x1)**2 == 5:
							N_MOVES[y1][x1].append((y2, x2))

		return N_MOVES

	@staticmethod
	def set_B_MOVES():  # create movement pattern for Bishop
		B_MOVES = np.empty((8, 8), dtype=list)
		for a in range(8):
			for b in range(8):
				B_MOVES[a][b] = []

		for x1 in range(8):
			for y1 in range(8):
				for x2 in range(8):
					for y2 in range(8):
						if np.abs(y2 - y1) == np.abs((x2 - x1)):
							B_MOVES[y1][x1].append((y2, x2))

		return B_MOVES

	@staticmethod
	def set_R_MOVES():  # create movement pattern for Rook
		R_MOVES = np.empty((8, 8), dtype=list)
		for a in range(8):
			for b in range(8):
				R_MOVES[a][b] = []

		for x1 in range(8):
			for y1 in range(8):
				for x2 in range(8):
					for y2 in range(8):
						if y2 - y1 == 0 or x2 - x1 == 0:
							R_MOVES[y1][x1].append((y2, x2))

		return R_MOVES

	@staticmethod
	def set_Q_MOVES():  # create movement pattern for Queen
		Q_MOVES = np.empty((8, 8), dtype=list)
		for a in range(8):
			for b in range(8):
				Q_MOVES[a][b] = []

		for x1 in range(8):
			for y1 in range(8):
				for x2 in range(8):
					for y2 in range(8):
						if y2 - y1 == 0 or x2 - x1 == 0 or np.abs(y2 - y1) == np.abs(x2 - x1):
							Q_MOVES[y1][x1].append((y2, x2))

		return Q_MOVES

	@staticmethod
	def set_K_MOVES():  # create movement pattern for King
		K_MOVES = np.empty((8, 8), dtype=list)
		for a in range(8):
			for b in range(8):
				K_MOVES[a][b] = []
		for x1 in range(8):
			for y1 in range(8):
				for x2 in range(8):
					for y2 in range(8):
						if (y2 - y1)**2 + (x2 - x1)**2 < 3:
							K_MOVES[y1][x1].append((y2, x2))

		return K_MOVES


class Main:
	def __init__(self, mode='computer'):

		pg.init()
		clock = pg.time.Clock()

		self.mode = mode

		WIDTH = 600
		HEIGHT = 600
		WHITE = 255, 255, 255
		BLACK = 0, 0, 0

		self.Display = pg.display.set_mode((WIDTH, HEIGHT))
		self.Display.fill(WHITE)
		pg.display.set_caption('Chess')

		self.board = Board(None)
		self.board.set_default()
		self.load_assets()

		if mode == 'sandbox':
			close = False
			self.pick_active = False
			self.picked_piece = 0

			while not close:
				for event in pg.event.get():

					if event.type == pg.QUIT:
						close = True

					if event.type == pg.MOUSEBUTTONDOWN and self.pick_active == False:
						self.pos = pg.mouse.get_pos()
						# print(self.pos)
						self.pick_piece()
						self.pick_active = True

					if event.type == pg.MOUSEBUTTONUP and self.pick_active == True:
						self.pos = pg.mouse.get_pos()
						# print(self.pos)
						self.drop_piece()

				self.Display.fill(WHITE)

				self.board.show_board(self)
				self.board.show_pieces(self)

				if self.pick_active == True:
					self.pos = pg.mouse.get_pos()
					self.follow_piece()

				pg.display.update()

		if mode == 'computer':
			self.comp_turn = -1
			self.chance = True
			close = False
			self.pick_active = False
			self.picked_piece = 0

			comp = Comp(self, self.comp_turn)
			while not close:
				clock.tick(30)
				if self.chance:
					for event in pg.event.get():

						if event.type == pg.QUIT:
							close = True

						if event.type == pg.MOUSEBUTTONDOWN and self.pick_active == False:
							self.pos = pg.mouse.get_pos()
							# print(self.pos)
							self.pick_piece()
							self.pick_active = True

						if event.type == pg.MOUSEBUTTONUP and self.pick_active == True:
							self.pos = pg.mouse.get_pos()
							# print(self.pos)
							temp = self.drop_piece()
							self.chance = not temp
					self.Display.fill(WHITE)

					self.board.show_board(self)
					self.board.show_pieces(self)

					if self.pick_active == True:
						self.pos = pg.mouse.get_pos()
						self.follow_piece()
					pg.display.update()

				else:
					for event in pg.event.get():
						if event.type == pg.QUIT:
							close = True
					# print('-------------------------------------')
					# print(self.board.state)
					piece, pos0, posFin, self.board.State,_ = comp.eval_depth(self.board.State,self.comp_turn,0)
					print(type(self.board.State.state))
					self.board.State.state[pos0[1], pos0[0]] = 0

					self.make_move(piece, pos0, posFin)
					# print((posFin[1],posFin[0]),'\n',self.board.state)
					self.chance = True

					self.Display.fill(WHITE)

					self.board.show_board(self)
					self.board.show_pieces(self)

					if self.pick_active == True:
						self.pos = pg.mouse.get_pos()
						self.follow_piece()
					pg.display.update()

	def load_assets(self):
		self.Blank = pg.image.load(r"C:\Users\Ashok\Mayaank\Programming\Python\Python 3.7\Chess\Assets\Blank.png")
		self.WPImg = pg.image.load(r"C:\Users\Ashok\Mayaank\Programming\Python\Python 3.7\Chess\Assets\WPImg.png")
		self.BPImg = pg.image.load(r"C:\Users\Ashok\Mayaank\Programming\Python\Python 3.7\Chess\Assets\BPImg.png")

		self.WNImg = pg.image.load(r"C:\Users\Ashok\Mayaank\Programming\Python\Python 3.7\Chess\Assets\WNImg.png")
		self.BNImg = pg.image.load(r"C:\Users\Ashok\Mayaank\Programming\Python\Python 3.7\Chess\Assets\BNImg.png")

		self.WBImg = pg.image.load(r"C:\Users\Ashok\Mayaank\Programming\Python\Python 3.7\Chess\Assets\WBImg.png")
		self.BBImg = pg.image.load(r"C:\Users\Ashok\Mayaank\Programming\Python\Python 3.7\Chess\Assets\BBImg.png")

		self.WRImg = pg.image.load(r"C:\Users\Ashok\Mayaank\Programming\Python\Python 3.7\Chess\Assets\WRImg.png")
		self.BRImg = pg.image.load(r"C:\Users\Ashok\Mayaank\Programming\Python\Python 3.7\Chess\Assets\BRImg.png")

		self.WQImg = pg.image.load(r"C:\Users\Ashok\Mayaank\Programming\Python\Python 3.7\Chess\Assets\WQImg.png")
		self.BQImg = pg.image.load(r"C:\Users\Ashok\Mayaank\Programming\Python\Python 3.7\Chess\Assets\BQImg.png")

		self.WKImg = pg.image.load(r"C:\Users\Ashok\Mayaank\Programming\Python\Python 3.7\Chess\Assets\WKImg.png")
		self.BKImg = pg.image.load(r"C:\Users\Ashok\Mayaank\Programming\Python\Python 3.7\Chess\Assets\BKImg.png")

	def pick_piece(self):
		self.square_sel_old = ((self.pos[0] - self.board.START[0]) // self.board.SIZE[0],
		                       (self.pos[1] - self.board.START[1]) // self.board.SIZE[1])
		if self.square_sel_old[0] < 8 and self.square_sel_old[1] < 8:
			if self.board.State.state[self.square_sel_old[1]][self.square_sel_old[0]] != 0:
				self.picked_piece = self.board.State.state[self.square_sel_old[1]][self.square_sel_old[0]]
				self.moves_valid = self.board.State.valid_moves(self.picked_piece,
				                                                (self.square_sel_old[1], self.square_sel_old[0]))
				print('moves valid = ', self.moves_valid)
				# print('piece ', self.picked_piece)
				self.board.State.state[self.square_sel_old[1]][self.square_sel_old[0]] = 0
			else:
				self.moves_valid = []
				self.pick_active = False

	def follow_piece(self):
		self.Display.blit(self.board.PIECES[self.picked_piece],
		                  (self.pos[0] - self.board.PIC_SIZE[0] / 2, self.pos[1] - self.board.PIC_SIZE[1] / 2))

	def drop_piece(self):
		ret_val = False
		self.square_sel = ((self.pos[0] - self.board.START[0]) // self.board.SIZE[0],
		                   (self.pos[1] - self.board.START[1]) // self.board.SIZE[1])
		if self.square_sel[0] < 8 and self.square_sel[1] < 8 and self.square_sel_old[0] < 8 and self.square_sel_old[
			1] < 8:  # if the cursor is within the board
			if (
			self.square_sel[1], self.square_sel[0]) in self.moves_valid:  # the piece is being moved to a valid square

				return self.make_move()


			else:  # invalid move has been made
				self.board.State.state[self.square_sel_old[1]][self.square_sel_old[0]] = self.picked_piece
				self.picked_piece = 0
				self.pick_active = False
				print('invalid move')
				return False
		else:  # invalid move has been made
			if self.picked_piece != 0:
				self.board.State.state[self.square_sel_old[1]][self.square_sel_old[0]] = self.picked_piece
			self.picked_piece = 0
			self.pick_active = False
			print('invalid move')
			return False

	def make_move(self, piece=None, pos0=None, posFin=None):
		# pos0,posFin := (x- right wards,y- downwards)
		if piece == None:
			piece = self.picked_piece

		if pos0 == None:
			pos0 = self.square_sel_old
		if posFin == None:
			posFin = self.square_sel

		if piece == 10:
			self.board.State.castling[0] = [0, 0]
		elif piece == -10:
			self.board.State.castling[1] = [0, 0]

		elif piece == 5:
			if pos0 == (0, 7):
				self.board.State.castling[0][1] = 0
			if pos0 == (7, 7):
				self.board.State.castling[0][0] = 0

		elif piece == -5:
			if pos0 == (0, 0):
				self.board.State.castling[1][1] = 0
			if pos0 == (7, 0):
				self.board.State.castling[1][0] = 0

		if piece in [1, -1]:  # if a pawn is picked
			if piece == 1 and posFin[1] == 0:  # pawn is on the last rank for white? promote to queen
				print('fageshdghfgdsfsgsdhdffghd')
				self.board.State.state[posFin[1]][posFin[0]] = 9
				# print(self.board.state)
				ret_val = True
			elif piece == -1 and posFin[1] == 7:  # pawn is on the last rank for black ? promote to queen
				self.board.State.state[posFin[1]][posFin[0]] = -9
				ret_val = True
			else:
				self.board.State.state[posFin[1]][posFin[0]] = piece
				ret_val = True

		elif piece in [10, -10]:
			if pos0 == (4, 7) and posFin == (6, 7) and piece == 10:
				self.board.State.state[posFin[1]][posFin[0]] = 10
				self.board.State.state[7][5] = 5
				self.board.State.state[7][7] = 0
				ret_val = True
			if pos0 == (4, 7) and posFin == (2, 7) and piece == 10:
				self.board.State.state[posFin[1]][posFin[0]] = 10
				self.board.State.state[7][3] = 5
				self.board.State.state[7][0] = 0
				ret_val = True
			if pos0 == (4, 0) and posFin == (6, 0) and piece == -10:
				self.board.State.state[posFin[1]][posFin[0]] = 10
				self.board.State.state[0][5] = -5
				self.board.State.state[0][7] = 0
				ret_val = True
			if pos0 == (4, 0) and posFin == (2, 0) and piece == -10:
				self.board.State.state[posFin[1]][posFin[0]] = -10
				self.board.State.state[0][3] = -5
				self.board.State.state[0][0] = 0
				ret_val = True
			else:
				self.board.State.state[posFin[1]][posFin[0]] = piece
				ret_val = True


		else:
			self.board.State.state[posFin[1]][posFin[0]] = piece
			ret_val = True

		self.picked_piece = 0
		self.pick_active = False
		return ret_val


class Comp:
	def __init__(self, Super: Main, turn):
		self.State = Super.board.State
		self.turn = turn
		self.pieces = []
		self.update_pieces(self.State, self.turn)
		self.piece_vals = {
			-10: 1000,
			-9: 90,
			-5: 50,
			-3: 30,
			-2: 30,
			-1: 10,
			1: 10,
			2: 30,
			3: 30,
			5: 50,
			9: 90,
			10: 1000

		}

	def evaluate_state(self, board: Board, turn=-1):
		state0 = board.State
		moves, own_pieces, opp_pieces = self.list_moves(state0,turn)

		move_state = {move: self.make_move(State(state0.state.copy(),state0.castling.copy()), move[0], (move[2], move[1]), (move[4], move[3])) for move in
		              moves}
		move_val = {move:self.give_score(move_state[move],turn)  for move in moves}

		if turn ==1:
			max_val = max(list(move_val.values()))
		else:
			max_val = min(list(move_val.values()))
		# print(min_val)

		final_moves = [move for move in move_val.keys() if move_val[move] == max_val]
		final_move = rand.sample(final_moves,1)[0]
		print(final_move)

		return final_move[0],final_move[1:3][::-1],final_move[3:5][::-1],move_state[final_move]

	def eval_depth(self,state:State,turn,depth):
		state0 = state
		print(type(state0))
		moves, own_pieces, opp_pieces = self.list_moves(state0, turn)
		move_state = {
			move: self.make_move(State(state0.state.copy(), state0.castling.copy()), move[0], (move[2], move[1]),
			                     (move[4], move[3])) for move in
			moves}
		if depth == 0:
			move_val = {move: self.give_score(move_state[move], turn) for move in moves}

			if turn == 1:
				max_val = max(list(move_val.values()))
			else:
				max_val = min(list(move_val.values()))
			# print(min_val)

			final_moves = [move for move in move_val.keys() if move_val[move] == max_val]
			final_move = rand.sample(final_moves, 1)[0]

			print(final_move)

			return final_move[0], final_move[1:3][::-1], final_move[3:5][::-1], move_state[final_move],max_val

		if depth>0:
			move_val = {move: self.eval_depth(move_state[move], turn*-1,depth-1)[4] for move in moves}
			if turn == 1:
				max_val = max(list(move_val.values()))
			else:
				max_val = min(list(move_val.values()))
			# print(min_val)

			final_moves = [move for move in move_val.keys() if move_val[move] == max_val]
			final_move = rand.sample(final_moves, 1)[0]
			print(final_move)

			return final_move[0], final_move[1:3][::-1], final_move[3:5][::-1], move_state[final_move],max_val


	def give_score(self, state,turn):
		own_pieces = []
		opp_pieces = []
		state = state.state
		for a in range(8):
			for b in range(8):
				if state[a, b] <0:
					opp_pieces.append((state[a, b], a, b))
				if state[a, b]  > 0:
					own_pieces.append((state[a, b], a, b))
		opp_score = np.sum([self.piece_vals[x[0]] for x in opp_pieces])
		own_score = np.sum([self.piece_vals[x[0]] for x in own_pieces])
		# print(own_score - opp_score)
		return own_score - opp_score

	def update_pieces(self, state, turn):

		own_pieces = []
		opp_pieces = []
		for a in range(8):
			for b in range(8):
				if state.state[a, b] * turn > 0:
					own_pieces.append((state.state[a, b], a, b))
				if state.state[a, b] * turn < 0:
					opp_pieces.append((state.state[a, b], a, b))
		return own_pieces, opp_pieces

	def list_moves(self, state, turn):
		own_pieces, opp_pieces = self.update_pieces(state, turn)
		moves = []
		for piece in own_pieces:
			move_list = state.valid_moves(piece[0], (piece[1], piece[2]))
			for move in move_list:
				moves.append(piece + move)
		return moves, own_pieces, opp_pieces

	def make_move(self, state: State, piece=None, pos0=None, posFin=None):
		# pos0,posFin := (x- right wards,y- downwards)
		state.state[pos0[1],pos0[0]] =0
		if piece == 10:
			state.castling[0] = [0, 0]
		elif piece == -10:
			state.castling[1] = [0, 0]

		elif piece == 5:
			if pos0 == (0, 7):
				state.castling[0][1] = 0
			if pos0 == (7, 7):
				state.castling[0][0] = 0

		elif piece == -5:
			if pos0 == (0, 0):
				state.castling[1][1] = 0
			if pos0 == (7, 0):
				state.castling[1][0] = 0

		if piece in [1, -1]:  # if a pawn is picked
			if piece == 1 and posFin[1] == 0:  # pawn is on the last rank for white? promote to queen
				print('fageshdghfgdsfsgsdhdffghd')
				state.state[posFin[1]][posFin[0]] = 9
				# print(self.board.state)
				ret_val = True
			elif piece == -1 and posFin[1] == 7:  # pawn is on the last rank for black ? promote to queen
				state.state[posFin[1]][posFin[0]] = -9
				ret_val = True
			else:
				state.state[posFin[1]][posFin[0]] = piece
				ret_val = True

		elif piece in [10, -10]:
			if pos0 == (4, 7) and posFin == (6, 7) and piece == 10:
				state.state[posFin[1]][posFin[0]] = 10
				state.state[7][5] = 5
				state.state[7][7] = 0
				ret_val = True
			if pos0 == (4, 7) and posFin == (2, 7) and piece == 10:
				state.state[posFin[1]][posFin[0]] = 10
				state.state[7][3] = 5
				state.state[7][0] = 0
				ret_val = True
			if pos0 == (4, 0) and posFin == (6, 0) and piece == -10:
				state.state[posFin[1]][posFin[0]] = 10
				state.state[0][5] = -5
				state.state[0][7] = 0
				ret_val = True
			if pos0 == (4, 0) and posFin == (2, 0) and piece == -10:
				state.state[posFin[1]][posFin[0]] = -10
				state.state[0][3] = -5
				state.state[0][0] = 0
				ret_val = True
			else:
				state.state[posFin[1]][posFin[0]] = piece
				ret_val = True


		else:
			# print(posFin)
			state.state[posFin[1]][posFin[0]] = piece
			ret_val = True

		return state

	def rand_turn(self, state):
		self.State.state = state

		moves, _, _ = self.list_moves(self.State, self.turn)
		# print(self.pieces)
		done = False
		if len(moves) != 0:
			move = rand.sample(moves, 1)[0]

			return move[0], move[1:3][::-1], move[3:5][::-1], self.State.state


if __name__ == '__main__':
	setup = Main('sandbox')
