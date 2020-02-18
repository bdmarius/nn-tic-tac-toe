import os
import random
from model import TicTacToeModel
import copy

PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '
PLAYER_X_VAL = -1
PLAYER_O_VAL = 1
EMPTY_VAL = 0
HORIZONTAL_SEPARATOR = ' | '
VERTICAL_SEPARATOR = '---------------'
GAME_STATE_X = -1
GAME_STATE_O = 1
GAME_STATE_DRAW = 0
GAME_STATE_NOT_ENDED = 2


class Game:

    def __init__(self):
        self.resetBoard()
        self.trainingHistory = []

    def resetBoard(self):
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.boardHistory = []

    def printBoard(self):
        print(VERTICAL_SEPARATOR)
        for i in range(len(self.board)):
            print(' ', end='')
            for j in range(len(self.board[i])):
                if PLAYER_X_VAL == self.board[i][j]:
                    print(PLAYER_X, end='')
                elif PLAYER_O_VAL == self.board[i][j]:
                    print(PLAYER_O, end='')
                elif EMPTY_VAL == self.board[i][j]:
                    print(EMPTY, end='')
                print(HORIZONTAL_SEPARATOR, end='')
            print(os.linesep)
            print(VERTICAL_SEPARATOR)

    def getGameResult(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == EMPTY_VAL:
                    return GAME_STATE_NOT_ENDED

        # Rows
        for i in range(len(self.board)):
            candidate = self.board[i][0]
            for j in range(len(self.board[i])):
                if candidate != self.board[i][j]:
                    candidate = 0
            if candidate != 0:
                return candidate

        # Columns
        for i in range(len(self.board)):
            candidate = self.board[0][i]
            for j in range(len(self.board[i])):
                if candidate != self.board[j][i]:
                    candidate = 0
            if candidate != 0:
                return candidate

        # First diagonal
        candidate = self.board[0][0]
        for i in range(len(self.board)):
            if candidate != self.board[i][i]:
                candidate = 0
        if candidate != 0:
            return candidate

        # Second diagonal
        candidate = self.board[0][2]
        for i in range(len(self.board)):
            if candidate != self.board[i][len(self.board[i]) - i - 1]:
                candidate = 0
        if candidate != 0:
            return candidate

        return GAME_STATE_DRAW


    def getAvailableMoves(self):
        availableMoves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (self.board[i][j]) == EMPTY_VAL:
                    availableMoves.append([i, j])
        return availableMoves

    def addToHistory(self, board):
        self.boardHistory.append(board)

    def printHistory(self):
        print(self.boardHistory)

    def move(self, position, player):
        availableMoves = self.getAvailableMoves()
        for i in range(len(availableMoves)):
            if position[0] == availableMoves[i][0] and position[1] == availableMoves[i][1]:
                self.board[position[0]][position[1]] = player
                self.addToHistory(copy.deepcopy(self.board))


    def simulate(self, playerToMove):
        while (self.getGameResult() == GAME_STATE_NOT_ENDED):
            availableMoves = self.getAvailableMoves()
            selectedMove = availableMoves[random.randrange(0, len(availableMoves))]
            self.move(selectedMove, playerToMove)
            if playerToMove == PLAYER_X_VAL:
                playerToMove = PLAYER_O_VAL
            else:
                playerToMove = PLAYER_X_VAL
        # Get the history and build the training set
        for historyItem in self.boardHistory:
            self.trainingHistory.append((self.getGameResult(), copy.deepcopy(historyItem)))

    def simulateNeuralNetwork(self, nnPlayer, model):
        playerToMove = PLAYER_X_VAL
        while (self.getGameResult() == GAME_STATE_NOT_ENDED):
            availableMoves = self.getAvailableMoves()
            if playerToMove == nnPlayer:
                maxValue = 0
                bestMove = availableMoves[0]
                for availableMove in availableMoves:
                    # get a copy of a board
                    boardCopy = copy.deepcopy(self.board)
                    boardCopy[availableMove[0]][availableMove[1]] = nnPlayer
                    if nnPlayer == PLAYER_X_VAL:
                        value = model.predict(boardCopy, 0)
                    else:
                        value = model.predict(boardCopy, 2)
                    if value > maxValue:
                        maxValue = value
                        bestMove = availableMove
                selectedMove = bestMove
            else:
                selectedMove = availableMoves[random.randrange(0, len(availableMoves))]
            self.move(selectedMove, playerToMove)
            if playerToMove == PLAYER_X_VAL:
                playerToMove = PLAYER_O_VAL
            else:
                playerToMove = PLAYER_X_VAL

    def getTrainingHistory(self):
        return self.trainingHistory

    def simulateManyGames(self, playerToMove, numberOfGames):
        playerXWins = 0
        playerOWins = 0
        draws = 0
        for i in range(numberOfGames):
            self.resetBoard()
            self.simulate(playerToMove)
            if self.getGameResult() == PLAYER_X_VAL:
                playerXWins = playerXWins + 1
            elif self.getGameResult() == PLAYER_O_VAL:
                playerOWins = playerOWins + 1
            else: draws = draws + 1
        totalWins = playerXWins + playerOWins + draws
        print ('X Wins: ' + str(int(playerXWins * 100/totalWins)) + '%')
        print('O Wins: ' + str(int(playerOWins * 100 / totalWins)) + '%')
        print('Draws: ' + str(int(draws * 100 / totalWins)) + '%')


    def simulateManyNeuralNetworkGames(self, nnPlayer, numberOfGames, model):
        nnPlayerWins = 0
        randomPlayerWins = 0
        draws = 0
        print ("NN player")
        print (nnPlayer)
        for i in range(numberOfGames):
            self.resetBoard()
            self.simulateNeuralNetwork(nnPlayer, model)
            if self.getGameResult() == nnPlayer:
                nnPlayerWins = nnPlayerWins + 1
            elif self.getGameResult() == GAME_STATE_DRAW:
                draws = draws + 1
            else: randomPlayerWins = randomPlayerWins + 1
        totalWins = nnPlayerWins + randomPlayerWins + draws
        print ('X Wins: ' + str(int(nnPlayerWins * 100/totalWins)) + '%')
        print('O Wins: ' + str(int(randomPlayerWins * 100 / totalWins)) + '%')
        print('Draws: ' + str(int(draws * 100 / totalWins)) + '%')

if __name__ == "__main__":
    game = Game()
    game.simulateManyGames(1, 10000)
    ticTacToeModel = TicTacToeModel(9, 3, 100, 32)
    ticTacToeModel.train(game.getTrainingHistory())
    print ("Simulating with Neural Network as X Player:")
    game.simulateManyNeuralNetworkGames(PLAYER_X_VAL, 10000, ticTacToeModel)
    print("Simulating with Neural Network as O Player:")
    game.simulateManyNeuralNetworkGames(PLAYER_O_VAL, 10000, ticTacToeModel)

