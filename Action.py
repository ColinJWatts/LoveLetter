import util

class Action():
    def __init__(self):
        return
    
    def execute(self, gameState):
        util.raiseNotDefined()
        return
    
class DummyAction(Action):
    def __init__(self):
        return
    
    def execute(self, gameState):
        print("Dummy happened")
        return gameState