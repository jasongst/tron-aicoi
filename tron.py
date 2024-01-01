import sys
import math

gameState = [['.' for x in range(30)] for y in range (20)]

def showGraph(graph):
    for i in range(len(graph)):
        print(' '.join(graph[i]), file=sys.stderr, flush=True)

def bestAction(x, y):
    availableActions = []
    if x > 0 and gameState[y][x - 1] == '.':
        availableActions.append('LEFT')
    if x < len(gameState[0]) - 1 and gameState[y][x + 1] == '.':
        availableActions.append('RIGHT')
    if y > 0 and gameState[y - 1][x] == '.':
        availableActions.append('UP')
    if y < len(gameState) - 1 and gameState[y + 1][x] == '.':
        availableActions.append('DOWN')

    if len(availableActions) > 0:
        return availableActions[0]

    return 'LEFT'

# game loop
while True:
    # n: total number of players (2 to 4).
    # p: your player number (0 to 3).
    n, p = [int(i) for i in input().split()]
    x = 0
    y = 0
    for i in range(n):
        # x0: starting X coordinate of lightcycle (or -1)
        # y0: starting Y coordinate of lightcycle (or -1)
        # x1: starting X coordinate of lightcycle (can be the same as X0 if you play before this player)
        # y1: starting Y coordinate of lightcycle (can be the same as Y0 if you play before this player)
        x0, y0, x1, y1 = [int(j) for j in input().split()]
        gameState[y1][x1] = str(i + 1)
        if i == p:
            x = x1
            y = y1

    print(str(x) + ', ' + str(y), file=sys.stderr, flush=True)
    showGraph(gameState)
    print(bestAction(x, y))

    