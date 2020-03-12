from Game import Game
from matplotlib import pyplot as plt

numPlayers = 2
turnCounts = []
numGames = 10000

for i in range(numGames):
    print(f"Starting game {i} with {numPlayers} players")

    loveLetterGame = Game(1, numPlayers)
    loveLetterGame.start()
    turnCounts.append(loveLetterGame.numTurns)


    print(f"Game Ended with status: {loveLetterGame.state.state}\n\n")

plt.hist(turnCounts, 15, [0,15])
plt.show()