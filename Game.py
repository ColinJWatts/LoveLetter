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
from BeliefState import Filter
import random as r
        
class Game():
    def __init__(self, numHumans, numComps):
        self.players = []
        cardIds = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        r.shuffle(cardIds)
        self.startingDeck = [
           Gaurd(cardIds[0]), Gaurd(cardIds[1]), Gaurd(cardIds[2]), Gaurd(cardIds[3]), Gaurd(cardIds[4]),
           Priest(cardIds[5]), Priest(cardIds[6]),
           Baron(cardIds[7]), Baron(cardIds[8]),
           Handmaid(cardIds[9]), Handmaid(cardIds[10]),
           Prince(cardIds[11]), Prince(cardIds[12]),
           King(cardIds[13]),
           Countess(cardIds[14]),
           Princess(cardIds[15])]

        # self.startingDeck = [Gaurd(0), Priest(1), Handmaid(2), Princess(3)]

        deck = self.startingDeck.copy()
        r.shuffle(deck)
        self.state = GameState(numHumans + numComps, deck)
        
        if numHumans + numComps > 4 or numHumans + numComps < 2: 
            util.raiseException("must have 2 to 4 players")

        for i in range(numHumans):
            self.players.append(Player.createPlayer("human", i, self.state))

        for i in range(numComps):
            self.players.append(Player.createPlayer("computer", i + numHumans, self.state))

        self.state.setPlayers(self.players)

    def start(self):
        
        for i in range(self.state.numPlayers + 1):
            drawAction = DrawCard(i, setupAction=True)
            self.state = drawAction.execute(self.state)

        print(f"Set card {self.state.playerCards[self.state.numPlayers][0].id} aside")
        self.numTurns = 0
        while self.state.state == "ongoing":
            if len(self.state.playerCards[self.state.playerTurn]) > 0:
                self.state.handMaided[self.state.playerTurn] = False
                drawAction = DrawCard(self.state.playerTurn)
                self.state = drawAction.execute(self.state)
                self.state = self.players[self.state.playerTurn].takeTurn(self.state)
                self.numTurns += 1

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
        if self.player < len(stateCopy.players):
            stateCopy.players[self.player].updateBelief(DrawFilter(card.id, card.getValue()))                

        if not self.setupAction:
            stateCopy.checkEndConditions()

        return stateCopy
                
class DrawFilter(Filter):
    def __init__(self, cardId, value):
        self.id = cardId
        self.val = value - 1
    
    def test(self, particle):
        return particle[self.id] == self.val
