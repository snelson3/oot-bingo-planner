import sys, json

class Card:
    def __init__(self):
        self.card = [[],[],[],[],[]]
        pass

    def parseSlot(self,line):
        # Slot should be in the following form
        # <td class="row1 col1 tlbr" id="slot1">Get to the end of Fire Trial</td>
        try:
            l = line.split(">")
            s = l[1].split("<")
            return s[0]
        except:
            raise Exception("Slot not formatted correctly: " + line)
        pass

    def parseHTML(self,fn):
        'TODO catch & symbol'
        lines = []
        with open(fn,"r") as f:
            for line in f:
                lines.append(line.strip())
        if len(lines) < 34:
            raise Exception("Card file does not have enough lines")
        # PARSE ROW 1
        self.card[0].append(self.parseSlot(lines[1]))
        self.card[1].append(self.parseSlot(lines[2]))
        self.card[2].append(self.parseSlot(lines[3]))
        self.card[3].append(self.parseSlot(lines[4]))
        self.card[4].append(self.parseSlot(lines[5]))
        # PARSE ROW 2
        self.card[0].append(self.parseSlot(lines[8]))
        self.card[1].append(self.parseSlot(lines[9]))
        self.card[2].append(self.parseSlot(lines[10]))
        self.card[3].append(self.parseSlot(lines[11]))
        self.card[4].append(self.parseSlot(lines[12]))
        # PARSE ROW 3
        self.card[0].append(self.parseSlot(lines[15]))
        self.card[1].append(self.parseSlot(lines[16]))
        self.card[2].append(self.parseSlot(lines[17]))
        self.card[3].append(self.parseSlot(lines[18]))
        self.card[4].append(self.parseSlot(lines[19]))
        # PARSE ROW 4
        self.card[0].append(self.parseSlot(lines[22]))
        self.card[1].append(self.parseSlot(lines[23]))
        self.card[2].append(self.parseSlot(lines[24]))
        self.card[3].append(self.parseSlot(lines[25]))
        self.card[4].append(self.parseSlot(lines[26]))
        # PARSE ROW 5
        self.card[0].append(self.parseSlot(lines[29]))
        self.card[1].append(self.parseSlot(lines[30]))
        self.card[2].append(self.parseSlot(lines[31]))
        self.card[3].append(self.parseSlot(lines[32]))
        self.card[4].append(self.parseSlot(lines[33]))

    def printCard(self):
        for col in self.card:
            if len(col) != 5:
                raise Exception("Col is not correct length: " + str(col))
        print "#########################################################################"
        for i in range(5):
            st = "## "
            for j in range(5):
                st += self.card[j][i]
                st += " ## "
            print st
            print "#########################################################################"

class Optimizer:
    def __init__(self,goalsfn):
        self.card = None
        with open(goalsfn,"r") as f:
            self.goals = json.load(f)

    def assignCard(self,card):
        self.card = card.card
        self.verifyCard(card)

    def verifyCard(self,card):
        'TODO this method should be in the Card class somehow, I think I will need to rearchitect this'
        if self.card is None:
            raise Exception("No card assigned!")
        '''verify all the goals in the card are in the goals, otherwise add it and make a warning'''
        for i in range(5):
            for j in range(5):
                try:
                    self.goals[self.card[j][i]]
                except KeyError:
                    print('WARNING: Goal not found - ' + self.card[j][i])
                    self.goals[self.card[j][i]] = {"time": 0}

    def getLength(self,route):
        time = 0
        for goal in route:
            time += self.goals[goal]["time"]
        return time

    def optimize(self):
        routes = []
        # find the length of all 12 possible routes
         # rows
        for i in range(5):
            r = map(lambda j: self.card[j][i],range(5))
            t = self.getLength(r)
            routes.append(('Row ' + str(i+1),r, t))
         # cols
        for i in range(5):
            r = map(lambda j: self.card[i][j], range(5))
            t = self.getLength(r)
            routes.append(('Col ' + str(i+1),r, t))
         # tl-br
        r = map(lambda i: self.card[i][i], range(5))
        t = self.getLength(r)
        routes.append(('TL-BR ', r, t))
         # bl-tr
        r = map(lambda i: self.card[i][4-i], range(5))
        t = self.getLength(r)
        routes.append(('BL-TR ', r, t))
        # sort by length
        routes.sort(key=lambda x: x[2])
        # post them sorted by length
        for route in routes:
            print route[0] + ' - ' + str(route[2]) + ': ' + str(route[1])

card = Card()
card.parseHTML(sys.argv[1])
opt = Optimizer(sys.argv[2])
opt.assignCard(card)
opt.optimize()
