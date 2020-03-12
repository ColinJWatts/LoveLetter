from Game import Game

numPlayers = 3
sumOfTurns = 0
numGames = 10000

for i in range(numGames):
    print(f"Starting game {i} with {numPlayers} players")

    loveLetterGame = Game(0, numPlayers)
    loveLetterGame.start()
    sumOfTurns += loveLetterGame.numTurns

    print(f"Game Ended with status: {loveLetterGame.state.state}\n\n")

print(f"Average Number of Turns Taken is: {sumOfTurns/numGames}")