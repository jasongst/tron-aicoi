import sys
import copy

class GameState():
    def __init__(self):
        self._map = [['.' for x in range(30)] for y in range (20)]
        self._myPlayer = 0
        self._playerPositions = []
        self._deadPlayers = []

    def getMap(self):
        return self._map
    
    def getMyPosition(self):
        return self._playerPositions[self._myPlayer]
    
    def getPlayerPosition(self, p):
        return self._playerPositions[p]
    
    def getPositions(self):
        return self._playerPositions
    
    def getMyPlayer(self):
        return self._myPlayer
    
    def setMyPlayer(self, p):
        self._myPlayer = p

    def setPlayerPosition(self, x, y, p):
        self._playerPositions[p] = (x, y)
        self._map[y][x] = str(p + 1)

    def setPlayerPositions(self, list):
        self._playerPositions = list
    
    def addPlayerPosition(self, x, y):
        self._playerPositions.append((x, y))
    
    def showState(self):
        for i in range(len(self._map)):
            print(' '.join(self._map[i]), file=sys.stderr, flush=True)

    def getLegalActions(self, p):
        availableActions = []
        if self._playerPositions[p][0] > 0 and self._map[self._playerPositions[p][1]][self._playerPositions[p][0] - 1] == '.':
            availableActions.append('LEFT')
        if self._playerPositions[p][0] < len(self._map[0]) - 1 and self._map[self._playerPositions[p][1]][self._playerPositions[p][0] + 1] == '.':
            availableActions.append('RIGHT')
        if self._playerPositions[p][1] > 0 and self._map[self._playerPositions[p][1] - 1][self._playerPositions[p][0]] == '.':
            availableActions.append('UP')
        if self._playerPositions[p][1] < len(self._map) - 1 and self._map[self._playerPositions[p][1] + 1][self._playerPositions[p][0]] == '.':
            availableActions.append('DOWN')

        return availableActions
    
    def isValidMove(self, p, action):
        availableActions = []
        if self._playerPositions[p][0] > 0 and self._map[self._playerPositions[p][1]][self._playerPositions[p][0] - 1] == '.':
            availableActions.append('LEFT')
        if self._playerPositions[p][0] < len(self._map[0]) - 1 and self._map[self._playerPositions[p][1]][self._playerPositions[p][0] + 1] == '.':
            availableActions.append('RIGHT')
        if self._playerPositions[p][1] > 0 and self._map[self._playerPositions[p][1] - 1][self._playerPositions[p][0]] == '.':
            availableActions.append('UP')
        if self._playerPositions[p][1] < len(self._map) - 1 and self._map[self._playerPositions[p][1] + 1][self._playerPositions[p][0]] == '.':
            availableActions.append('DOWN')

        return action in availableActions
    
    def haveWinner(self):
        nbPlayersWhoCanMove = 0
        winner = None
        for i in range(len(self._playerPositions)):
            possibleActions = self.getLegalActions(i)
            if len(possibleActions) > 0:
                nbPlayersWhoCanMove += 1
                winner = i
        
        if nbPlayersWhoCanMove <= 1:
            return winner
        else:
            None

    def bestAction(self):
        availableActions = self.getLegalActions(self._myPlayer)

        if len(availableActions) > 0:
            return availableActions[0]

        return 'LEFT'
    
    def move(self, p, action):
        match action:
            case "LEFT":
                self.setPlayerPosition(self._playerPositions[p][0] - 1, self._playerPositions[p][1], p)
            case "RIGHT":
                self.setPlayerPosition(self._playerPositions[p][0] + 1, self._playerPositions[p][1], p)
            case "UP":
                self.setPlayerPosition(self._playerPositions[p][0], self._playerPositions[p][1] - 1, p)
            case "DOWN":
                self.setPlayerPosition(self._playerPositions[p][0], self._playerPositions[p][1] + 1, p)

    def unsetPlayerPosition(self, p):
        self._map = [["." if cell == str(p) else cell for cell in row] for row in self._map]

    def detectDeadPlayers(self):
        for i in range(len(self._playerPositions)):
            if i not in self._deadPlayers:
                possibleActions = self.getLegalActions(i)
                if len(possibleActions) == 0:
                    self._deadPlayers.append(i)
                    self.unsetPlayerPosition(i+1)
        return self._deadPlayers             

class Node:
    def __init__(self, game, value):
        self.gameState = game
        self.value = value
        self.childrens = []

    def setPossibleChildrens(self):
        actions = self.gameState.getLegalActions(self.gameState.getMyPlayer())
        nextPlayer = (self.gameState.getMyPlayer() + 1) % 2
        for action in actions:
            new_game_state = copy.deepcopy(self.gameState)
            new_game_state.move(new_game_state.getMyPlayer(), action)
            new_game_state.setMyPlayer(nextPlayer)            
            self.childrens.append(Node(new_game_state, 0))
        

def getBestMove(root, depth, max):
    if depth == 0:
        root.value = evaluate(root)
        return root
    
    # Comportement quand noeud terminal à vérifier
    if max:
        bestNode = Node(None, float('-inf'))
        root.setPossibleChildrens()
        for node in root.childrens:
            recNode = getBestMove(node, depth - 1, False)
            node.value = recNode.value
            bestNode = compareNodesMax(bestNode, node)
        return bestNode
    else:
        bestNode = Node(None, float('inf'))
        root.setPossibleChildrens()
        for node in root.childrens:
            recNode = getBestMove(node, depth - 1, True)
            node.value = recNode.value
            bestNode = compareNodesMin(bestNode, node)
        return bestNode
    
def compareNodesMax(node1, node2):
    if node1.value > node2.value:
        return node1
    return node2

def compareNodesMin(node1, node2):
    if node1.value < node2.value:
        return node1
    return node2

def evaluate(node):
    filledBoard = floodFill(node.gameState.getMap(), node.gameState.getPositions())
    my_player = node.gameState.getMyPlayer()
    my_cells = sum(row.count(str(my_player + 4)) for row in filledBoard)
    opponents_cells = sum(1 for row in filledBoard for el in row if el != '.' and int(el) > 4)
    return my_cells * 10000000 + opponents_cells * -100000

def floodFill(board, playerPositions):
    boardTmp = [list(row) for row in board]
    fillPosition = []

    def fill(x, y, val):
        if 0 <= x < len(boardTmp[0]) and 0 <= y < len(boardTmp) and boardTmp[y][x] == '.':
            boardTmp[y][x] = val
            fillPosition.append((x, y))

    for i, (x, y) in enumerate(playerPositions):
        fill(x - 1, y, str(i + 4))
        fill(x + 1, y, str(i + 4))
        fill(x, y - 1, str(i + 4))
        fill(x, y + 1, str(i + 4))

    while fillPosition:
        positionTmp = fillPosition[:]
        fillPosition.clear()
        for x, y in positionTmp:
            fill(x - 1, y, boardTmp[y][x])
            fill(x + 1, y, boardTmp[y][x])
            fill(x, y - 1, boardTmp[y][x])
            fill(x, y + 1, boardTmp[y][x])

    return [''.join(row) for row in boardTmp]

def getMove(xInitial, yInitial, moveNode, p):
    x, y = moveNode.gameState.getPlayerPosition(p)
    if y < yInitial:
        return "UP"
    elif y > yInitial:
        return "DOWN"
    elif x > xInitial:
        return "RIGHT"
    elif x < xInitial:
        return "LEFT"
    
    return ""


game = GameState()
firstTime = True

while True:
    n, p = [int(i) for i in input().split()]
    if firstTime:
        game.setMyPlayer(p)
        game.setPlayerPositions([(0, 0) for i in range(n)])
        firstTime = False
    for i in range(n):
        x0, y0, x1, y1 = [int(j) for j in input().split()]
        game.setPlayerPosition(x1, y1, i)
    game.detectDeadPlayers()
    startNode = Node(game, 0)
    bestMoveNode = getBestMove(startNode, 4, True)
    x, y = game.getMyPosition()
    print(getMove(x, y, bestMoveNode, p))