class Archetype:

    archetypeList = []


    def __init__(self, name: str, coreMinions: list, tier: int, availabilityFunc, description = "", optionalMinions = []):
        self.name = name
        self.description = description
        self.coreMinions = coreMinions
        self.optionalMinions = optionalMinions
        self.tier = tier
        self.availabilityFunc = availabilityFunc
        Archetype.archetypeList.append(self)


    def printArchetypeInfo(self):
        print(f'{self.name}\n{self.description}')
        minionsByTier = {}
        allMinions = self.coreMinions + self.optionalMinions
        allMinions.sort(key=lambda minion: minion.tier)
        for minion in allMinions:
            if minion.tier in minionsByTier:
                minionsByTier[minion.tier].append(minion)
            else:
                minionsByTier[minion.tier] = [minion]
        for i in minionsByTier:
            coreList = []
            optionalList = []
            for minion in minionsByTier[i]:
                if minion in self.coreMinions:
                    coreList.append(minion)
                elif minion in self.optionalMinions:
                    optionalList.append(minion)
            if len(coreList) + len(optionalList) > 0:
                print(f'level {i}')
                if len(coreList) > 0:
                    print (f'core minions: {', '.join([minion.name for minion in coreList])}')
                if len(optionalList) > 0:
                    print (f'optional minions: {', '.join([minion.name for minion in optionalList])}')

    def getValidArchetypes(currentTribes: list):
        validArchetypeList = []
        for archetype in Archetype.archetypeList:
            if archetype.availabilityFunc(currentTribes):
                validArchetypeList.append(archetype)
        return validArchetypeList
    
    def getMinionsArchetypes(minion):
        coreArchetypes = []
        optionalArchetypes = []
        for archetype in Archetype.archetypeList:
            if minion in archetype.coreMinions:
                coreArchetypes.append(archetype)
            elif minion in archetype.optionalMinions:
                optionalArchetypes.append(archetype)           
        return (coreArchetypes,optionalArchetypes)

