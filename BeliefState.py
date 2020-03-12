import numpy as np
import random as r
import util

class BeliefState():
    def __init__(self, state, numParticles):
        self.n = numParticles
        initialDist = [0,0,0,0,0,0,0,0]
        for c in state.deck:
            initialDist[c.getValue() - 1] += 1
        self.initialDist = initialDist

        self.belief = []
        for i in range(len(state.deck)):
            self.belief.append(initialDist)

        print("generating particles...")
        self.particleSet = []
        for i in range(self.n):
            if i%50 == 0:
                print(f"{i} particles generated")
            self.particleSet.append(self.GenerateParticle())

    def GenerateParticle(self):
        particle = []

        valid = False
        while not valid:
            count = [0,0,0,0,0,0,0,0]
            particle = []
            valid = True
            for i in range(len(self.belief)):
                c = self.GetRandomClass(self.belief[i])
                count[c] += 1
                if count[c] > self.initialDist[c]:
                    valid = False
                particle.append(c)
        
        #print(f"Particle: {particle}")

        return particle

    def GetEstimateForCard(self, id):
        if id < 0 or id >= len(self.belief):
            util.raiseException(f"no card id: {id}")
        
        response = [0,0,0,0,0,0,0,0]

        for p in self.particleSet:
            response[p[id]] += 1
        
        return self.Normalize(response)

    def FilterParticles(self, filter=None):
        if filter is None:
            filter = Filter()
        newSet = []
        for particle in self.particleSet:
            if filter.test(particle):
                newSet.append(particle)

        self.particleSet = newSet
        self.UpdateAndResample()

    def UpdateAndResample(self):
        for i in range(len(self.belief)):
            self.belief[i] = self.GetEstimateForCard(i)

        self.particleSet = []
        for i in range(self.n):
            self.particleSet.append(self.GenerateParticle())

    @staticmethod
    def GetRandomClass(distribution):
        distribution = BeliefState.Normalize(distribution)

        cdf = []
        prev = 0
        for d in distribution:
            cdf.append(prev + d)
            prev += d

        temp = r.random()
        index = 0
        while cdf[index] < temp:
            index += 1
            
        return index

    @staticmethod
    def Normalize(distribution):
        s = sum(distribution)
        result = []
        for i in range(len(distribution)):
            result.append(distribution[i] / s)
        return result


class Filter():
    def __init__(self):
        return

    #default filter filters nothing
    def test(self, particle):
        return True

        