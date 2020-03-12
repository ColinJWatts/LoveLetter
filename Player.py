import util
import random

class Player():
    """description of class"""

    @staticmethod
    def createPlayer(playerType,  id):
        if playerType == "human":
            return HumanPlayer(id)
        elif playerType == "computer":
            return ComputerPlayer(id)

    def __init__(self):
        util.raiseNotDefined()

    def takeTurn(self, state):
        util.raiseNotDefined()

    def observe(self, player, actionInfo):
        util.raiseNotDefined()

class HumanPlayer(Player):
    def __init__(self, playerNumber):
        self.id = playerNumber
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
    
    def __init__(self, player):
        self.id = player
        return    

    def takeTurn(self, state):
        print(f"Player {self.id} takes their turn...")
        print(f"Player {self.id} has cards: ")
        
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