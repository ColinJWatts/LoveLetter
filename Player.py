import util
import random
from BeliefState import BeliefState

numParticles = 1000

class Player():
    """description of class"""

    @staticmethod
    def createPlayer(playerType,  id, initalState):
        if playerType == "human":
            return HumanPlayer(id, initalState)
        elif playerType == "computer":
            return ComputerPlayer(id, initalState)

    def __init__(self):
        self.belief = None
        util.raiseNotDefined()

    def takeTurn(self, state):
        util.raiseNotDefined()

    def observe(self, player, actionInfo):
        util.raiseNotDefined()

    def updateBelief(self, filter):
        self.belief.FilterParticles(filter)

class HumanPlayer(Player):
    def __init__(self, playerNumber, initalState):
        self.id = playerNumber
        self.belief = BeliefState(initalState, numParticles)
        print(f"Belief State for card 0: {self.belief.GetEstimateForCard(0)}")
        return 

    def takeTurn(self, state):
        print(f"\nPlayer {self.id}'s turn. Press enter to continue...")
        input()
        print(f"Player {self.id} has cards: ")
        
        hasCountess = False

        for c in state.playerCards[self.id]:
            print(f"  {c.getName()}")
            if c.getName().lower() == "countess":
                hasCountess = True

        print("BELIEF STATE")
        i = 0
        for b in self.belief.belief:
            print(f"{i}: {b}")
            i += 1

        print("Type the name of the card you wish to play")
        cardName = ""
        card = None
        flag = True
        while flag:
            cardName = input()
            for c in state.playerCards[self.id]:
                if cardName.lower() == c.getName().lower():
                    if not (hasCountess and (c.getValue() == 6 or c.getValue() == 5)):
                        print("Okay!")
                        flag = False
                        card = c
                        break
            if flag:    
                print(f"{cardName} is not a valid card")

        target = -1
        if card.doesActionRequireTarget(): 
            valid = False
            while not valid:
                print("card action requires a target. Input target now")
                target = int(input())
                valid = state.isTargetValid(target)
                    
        arg = -1
        if card.doesActionRequireArg():
            valid = False
            while not valid:
                print("card action requires an argument. Input argument now")
                arg = int(input())
                if arg > 1 and arg <= 8:
                    valid = True

        action = card.getAction(self.id, target, arg)

        return action.execute(state)

class ComputerPlayer(Player):
    
    def __init__(self, player, initalState):
        self.id = player
        self.belief = BeliefState(initalState, numParticles)
        return    

    def takeTurn(self, state):
        print(f"Player {self.id} takes their turn...")
        print(f"Player {self.id} has cards: ")
        
        print("BELIEF STATE")
        i = 0
        for b in self.belief.belief:
            print(f"{i}: {b}")
            i += 1
        hasCountess = False

        for c in state.playerCards[self.id]:
            print(f"  {c.getName()}")
            if c.getName().lower() == "countess":
                hasCountess = True
        
        # Choose an action
        action = random.randint(0, len(state.playerCards[self.id]) - 1)

        if (state.playerCards[self.id][action].getValue() >= 5 and state.playerCards[self.id][action].getValue() != 7 and hasCountess):
            action = (action + 1) % 2

        card = state.playerCards[self.id][action]

        target = -1
        valid = False
        while not valid:
            target = random.randint(0, state.numPlayers - 1)
            valid = state.isTargetValid(target)

        argument = random.randint(2, 8)

        print(f"Player {self.id} chooses to play {card.getName()} with target {target} and argument {argument}")
        
        a = card.getAction(self.id, target=target, arg=argument)

        return a.execute(state)