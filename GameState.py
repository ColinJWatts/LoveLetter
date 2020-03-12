class GameState():
    def __init__(self, numPlayers, deck):
        self.deck = deck
        self.state = "ongoing"
        self.numPlayers = numPlayers
        self.playerTurn = 0

        self.playerCards = []
        self.playerDiscards = []
        self.handMaided = []
        for i in range(numPlayers):
            self.playerCards.append([])
            self.playerDiscards.append([])
            self.handMaided.append(False)

        # This is a space dedicated to the card that is set aside at the beginning of the game
        self.playerCards.append([])

    def setPlayers(self, players):
        self.players = players

    def getCopy(self):
        newState = GameState(self.numPlayers, [])
        newState.state = self.state
        newState.playerTurn = self.playerTurn
        newState.players = self.players

        newState.deck = []
        for i in range(len(self.deck)):
            newState.deck.append(self.deck[i].getCopy())

        for i in range(len(newState.handMaided)):
            newState.handMaided[i] = self.handMaided[i]

        i = 0
        for p in self.playerCards:
            for c in p:
                newState.playerCards[i].append(c.getCopy())
            i += 1

        i = 0
        for d in self.playerDiscards:
            for c in d:
                newState.playerDiscards[i].append(c.getCopy())  
            i += 1     

        return newState

    def getReward(self, player):
        if self.state == "ongoing": 
            return 0
        
        if len(self.playerCards[player]) == 0:
            return 0
        else:
            return self.playerCards[player][0].getValue()

    def isTargetValid(self, player):
        if player < 0 or player >= self.numPlayers:
            return False

        if len(self.playerCards[player]) == 0:
            return False  

        if self.handMaided[player]:
            return False

        return True


    def checkEndConditions(self):
        remainingPlayers = []
        
        for i in range(self.numPlayers):
            if len(self.playerCards[i]) != 0:
                remainingPlayers.append(i)

        if len(remainingPlayers) == 1:
            self.state = f"Player {remainingPlayers[0]} Wins!"
            return

        if len(self.deck) == 0:
            winner = -1
            winVal = 0
            for i in remainingPlayers:
                if self.playerCards[i][0].getValue() > winVal:
                    winVal = self.playerCards[i][0].getValue()
                    winner = i
            self.state = f"Player {winner} Wins with reward {self.getReward(winner)}!"

