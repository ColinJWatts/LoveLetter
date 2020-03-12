import util
from Action import Action
from Player import Player
from Card import Gaurd
from Card import Priest
from Card import Baron
from Card import Handmaid
from Card import Prince
from Card import King
from Card import Countess
from Card import Princess
from GameState import GameState
import random as r
        
class Game():
    def __init__(self, numHumans, numComps):
        self.players = []
        self.startingDeck = [
           Gaurd(0), Gaurd(1), Gaurd(2), Gaurd(3), Gaurd(4),
           Priest(5), Priest(6),
           Baron(7), Baron(8),
           Handmaid(9), Handmaid(10),
           Prince(11), Prince(12),
           King(13),
           Countess(14),
           Princess(15)]

        # self.startingDeck = [Gaurd(0), Priest(1), Handmaid(2), Princess(3)]

        deck = self.startingDeck.copy()
        r.shuffle(deck)
        
        if numHumans + numComps > 4 or numHumans + numComps < 2: 
            util.raiseException("must have 2 to 4 players")

        for i in range(numHumans):
            self.players.append(Player.createPlayer("human", i))

        for i in range(numComps):
            self.players.append(Player.createPlayer("computer", i + numHumans))

        self.state = GameState(numHumans + numComps, deck)

    def start(self):
        
        for i in range(self.state.numPlayers + 1):
            drawAction = DrawCard(i, setupAction=True)
            self.state = drawAction.execute(self.state)

        self.numTurns = 0
        while self.state.state == "ongoing":
            if len(self.state.playerCards[self.state.playerTurn]) > 0:
                self.state.handMaided[self.state.playerTurn] = False
                drawAction = DrawCard(self.state.playerTurn)
                self.state = drawAction.execute(self.state)
                self.state = self.players[self.state.playerTurn].takeTurn(self.state)
                self.numTurns+=1

            self.state.playerTurn = (self.state.playerTurn + 1) % self.state.numPlayers
                

class DrawCard(Action):
    def __init__(self, player, setupAction = False):
        self.player = player
        self.setupAction = setupAction

    def execute(self, state):
        stateCopy = state.getCopy()
        card = None
        if len(stateCopy.deck) > 0:
            card = stateCopy.deck.pop()
        else:
            card = stateCopy.playerCards[stateCopy.numPlayers].pop()

        stateCopy.playerCards[self.player].append(card)                

        if not self.setupAction:
            stateCopy.checkEndConditions()

        return stateCopy
                