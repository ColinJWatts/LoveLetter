import util
from Action import Action
from Action import DummyAction
from BeliefState import Filter

class Card():
    def __init__(self, id):
        util.raiseNotDefined()

    def getValue(self):
        util.raiseNotDefined()

    def getCopy(self):
        util.raiseNotDefined()

    def getName(self):
        util.raiseNotDefined()

    def doesActionRequireTarget(self):
        return True

    def doesActionRequireArg(self):
        return False

    def getAction(self, player, target=-1, arg=-1):
        return DummyAction()

class Gaurd(Card):
    def __init__(self, id):
        self.id = id
        return

    def getValue(self):
        return 1

    def getCopy(self):
        return Gaurd(self.id)

    def getName(self):
        return "Gaurd"

    def doesActionRequireArg(self):
        return True

    def getAction(self, player, target=-1, arg=-1):
        if arg == -1:
            util.raiseException("No argument given for Gaurd")
        return GaurdAction(player, target, arg)

class GaurdAction(Action):
    def __init__(self, player, target, arg):
        self.player = player
        self.target = target
        self.arg = arg

    def execute(self, state):
        stateCopy = state.getCopy()
        newList = []
        removed = False
        for i in range(len(stateCopy.playerCards[self.player])):
            if stateCopy.playerCards[self.player][i].getValue() == 1 and not removed:
                card = stateCopy.playerCards[self.player][i]
                stateCopy.playerDiscards[self.player].append(card)
                for i in range(len(stateCopy.players)):
                    if i != self.player:
                        stateCopy.players[i].updateBelief(IdentifyCardByID(card.id, card.getValue()))
                removed = True
            else: 
                newList.append(stateCopy.playerCards[self.player][i])

        stateCopy.playerCards[self.player] = newList

        if self.target == -1:
            stateCopy.checkEndConditions()
            return stateCopy
        
        if stateCopy.playerCards[self.target][0].getValue() == self.arg:
            extraAction = PrincessAction(self.target)
            stateCopy = extraAction.execute(stateCopy)

        stateCopy.checkEndConditions()
        return stateCopy

class Priest(Card):
    def __init__(self, id):
        self.id = id
        return

    def getValue(self):
        return 2

    def getCopy(self):
        return Priest(self.id)

    def getName(self):
        return "Priest"

    def getAction(self, player, target=-1, arg=-1):
        if target == -1:
            util.raiseException("No target given for Priest")
        return PriestAction(player, target)

class PriestAction(Action):
    def __init__(self, player, target):
        self.player = player
        self.target = target

    def execute(self, state):
        stateCopy = state.getCopy()
        newList = []
        removed = False
        for i in range(len(stateCopy.playerCards[self.player])):
            if stateCopy.playerCards[self.player][i].getValue() == 2 and not removed:
                card = stateCopy.playerCards[self.player][i]
                stateCopy.playerDiscards[self.player].append(card)
                for i in range(len(stateCopy.players)):
                    if i != self.player:
                        stateCopy.players[i].updateBelief(IdentifyCardByID(card.id, card.getValue()))
                removed = True
            else: 
                newList.append(stateCopy.playerCards[self.player][i])

        stateCopy.playerCards[self.player] = newList
        card = stateCopy.playerCards[self.target][0]
        print(f"You see: {card.getName()}")
        stateCopy.players[self.player].updateBelief(IdentifyCardByID(card.id, card.getValue()))
        stateCopy.checkEndConditions()
        return stateCopy

class IdentifyCardByID(Filter):
    def __init__(self, cardId, value):
        self.id = cardId
        self.val = value - 1

    def test(self, particle):
        return particle[self.id] == self.val

class Baron(Card):
    def __init__(self, id):
        self.id = id
        return

    def getValue(self):
        return 3
    
    def getCopy(self):
        return Baron(self.id)

    def getName(self):
        return "Baron"

    def getAction(self, player, target=-1, arg=-1):
        if target == -1:
            util.raiseException("No target given for Baron")
        return BaronAction(player, target)

class BaronAction(Action):
    def __init__(self, player, target):
        self.player = player
        self.target = target

    def execute(self, state):
        stateCopy = state.getCopy()
        newList = []
        removed = False
        for i in range(len(stateCopy.playerCards[self.player])):
            if stateCopy.playerCards[self.player][i].getValue() == 3 and not removed:
                card = stateCopy.playerCards[self.player][i]
                stateCopy.playerDiscards[self.player].append(card)
                for i in range(len(stateCopy.players)):
                    if i != self.player:
                        stateCopy.players[i].updateBelief(IdentifyCardByID(card.id, card.getValue()))
                removed = True
            else: 
                newList.append(stateCopy.playerCards[self.player][i])

        stateCopy.playerCards[self.player] = newList
        
        targetCard = stateCopy.playerCards[self.target][0]
        playerCard = stateCopy.playerCards[self.player][0]
        print(f"You see: {targetCard.getName()}")
        if targetCard.getValue() > playerCard.getValue():
            extraAction = PrincessAction(self.player)
            stateCopy = extraAction.execute(stateCopy)
        elif targetCard.getValue() < playerCard.getValue():
            extraAction = PrincessAction(self.target)
            stateCopy = extraAction.execute(stateCopy)

        stateCopy.checkEndConditions()
        return stateCopy

class Handmaid(Card):
    def __init__(self, id):
        self.id = id
        return

    def getValue(self):
        return 4

    def getCopy(self):
        return Handmaid(self.id)

    def getName(self):
        return "Handmaid"

    def doesActionRequireTarget(self):
        return False

    def getAction(self, player, target=-1, arg=-1):
        return HandmaidAction(player)

class HandmaidAction(Action):
    def __init__(self, player):
        self.player = player

    def execute(self, state):
        stateCopy = state.getCopy()
        newList = []
        removed = False
        for i in range(len(stateCopy.playerCards[self.player])):
            if stateCopy.playerCards[self.player][i].getValue() == 4 and not removed:
                card = stateCopy.playerCards[self.player][i]
                stateCopy.playerDiscards[self.player].append(card)
                for i in range(len(stateCopy.players)):
                    if i != self.player:
                        stateCopy.players[i].updateBelief(IdentifyCardByID(card.id, card.getValue()))
                removed = True
            else: 
                newList.append(stateCopy.playerCards[self.player][i])

        stateCopy.playerCards[self.player] = newList

        stateCopy.handMaided[self.player] = True
        
        stateCopy.checkEndConditions()
        return stateCopy

class Prince(Card):
    def __init__(self, id):
        self.id = id
        return

    def getValue(self):
        return 5

    def getCopy(self):
        return Prince(self.id)

    def getName(self):
        return "Prince"
    
    def getAction(self, player, target=-1, arg=-1):
        if target == -1:
            util.raiseException("No target given for prince")
        return PrinceAction(player, target)

class PrinceAction(Action):
    def __init__(self, player, target):
        self.player = player
        self.target = target

    def execute(self, state):
        stateCopy = state.getCopy()
        newList = []
        removed = False
        for i in range(len(stateCopy.playerCards[self.player])):
            if stateCopy.playerCards[self.player][i].getValue() == 5 and not removed:
                card = stateCopy.playerCards[self.player][i]
                stateCopy.playerDiscards[self.player].append(card)
                for i in range(len(stateCopy.players)):
                    if i != self.player:
                        stateCopy.players[i].updateBelief(IdentifyCardByID(card.id, card.getValue()))
                removed = True
            else: 
                newList.append(stateCopy.playerCards[self.player][i])

        stateCopy.playerCards[self.player] = newList
        
        targetCard = stateCopy.playerCards[self.target].pop()
        stateCopy.playerDiscards[self.target].append(targetCard)

        if targetCard.getValue() == 8:
            extraAction = PrincessAction(self.target)
            stateCopy = extraAction.execute(stateCopy)
        else:
            c = None
            if len(stateCopy.deck) > 0:
                c = stateCopy.deck.pop()
            else:
                c = stateCopy.playerCards[stateCopy.numPlayers].pop()
            stateCopy.playerCards[self.target].append(c)

        stateCopy.checkEndConditions()
        return stateCopy

class King(Card):
    def __init__(self, id):
        self.id = id
        return

    def getValue(self):
        return 6

    def getCopy(self):
        return King(self.id)

    def getName(self):
        return "King"

    def getAction(self, player, target=-1, arg=-1):
        if target == -1:
            util.raiseException("No target given for king")
        return KingAction(player, target)

class KingAction(Action):
    def __init__(self, player, target):
        self.player = player
        self.target = target

    def execute(self, state):
        stateCopy = state.getCopy()
        newList = []

        for i in range(len(stateCopy.playerCards[self.player])):
            if stateCopy.playerCards[self.player][i].getValue() == 6:
                card = stateCopy.playerCards[self.player][i]
                stateCopy.playerDiscards[self.player].append(card)
                for i in range(len(stateCopy.players)):
                    if i != self.player:
                        stateCopy.players[i].updateBelief(IdentifyCardByID(card.id, card.getValue()))
            else: 
                newList.append(stateCopy.playerCards[self.player][i])

        stateCopy.playerCards[self.player] = newList

        if self.player == self.target: 
            stateCopy.checkEndConditions()
            return stateCopy

        playerCard = stateCopy.playerCards[self.player].pop()
        targetCard = stateCopy.playerCards[self.target].pop()
        stateCopy.playerCards[self.target].append(playerCard)
        stateCopy.playerCards[self.player].append(targetCard)

        stateCopy.checkEndConditions()
        return stateCopy

class Countess(Card):
    def __init__(self, id):
        self.id = id
        return

    def getValue(self):
        return 7

    def getCopy(self):
        return Countess(self.id)

    def getName(self):
        return "Countess"

    def doesActionRequireTarget(self):
        return False

    def getAction(self, player, target=-1, arg=-1):
        return CountessAction(player)

class CountessAction(Action):
    def __init__(self, player):
        self.player = player

    def execute(self, state):
        stateCopy = state.getCopy()
        newList = []

        for i in range(len(stateCopy.playerCards[self.player])):
            if stateCopy.playerCards[self.player][i].getValue() == 7:
                card = stateCopy.playerCards[self.player][i]
                stateCopy.playerDiscards[self.player].append(card)
                for i in range(len(stateCopy.players)):
                    if i != self.player:
                        stateCopy.players[i].updateBelief(IdentifyCardByID(card.id, card.getValue()))
            else: 
                newList.append(stateCopy.playerCards[self.player][i])

        stateCopy.playerCards[self.player] = newList
        stateCopy.checkEndConditions()
        return stateCopy


class Princess(Card):
    def __init__(self, id):
        self.id = id
        return

    def getValue(self):
        return 8

    def getCopy(self):
        return Princess(self.id)

    def getName(self):
        return "Princess"

    def doesActionRequireTarget(self):
        return False

    def getAction(self, player, target=-1, arg=-1):
        return PrincessAction(player)

class PrincessAction(Action):
    def __init__(self, player):
        self.player = player
       
    def execute(self, state):
        stateCopy = state.getCopy()
        while len(stateCopy.playerCards[self.player]) > 0:
            card = stateCopy.playerCards[self.player].pop()
            for i in range(len(stateCopy.players)):
                    if i != self.player:
                        stateCopy.players[i].updateBelief(IdentifyCardByID(card.id, card.getValue()))
            stateCopy.playerDiscards[self.player].append(card)             

        stateCopy.checkEndConditions()

        return stateCopy

        