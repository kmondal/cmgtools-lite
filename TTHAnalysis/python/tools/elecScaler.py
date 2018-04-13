class correction(object):
    def __init__(self, line):
        words = line.split("\t")
        items = []
        for w in words:
            w = w.replace("\n", "")
            if not (w == ""):
                items.append(w)
        self.catText = items[0]
        self.rMin    = int(items[2])
        self.rMax    = int(items[3])
        self.ptMin   = -1
        self.ptMax   = 9999999
        self.etaMin  = -1
        self.etaMax  =  5
        self.r9Min    = -1
        self.r9Max    = 9999999
        self.corr    = float(items[4])
        #Quadratic sum of variations
        self.totVar  = (sum([float(k)**2 for k in items[5:]]))**0.5 
        self.getCatCuts()
    def getCatCuts(self):
        steps = self.catText.split("-")
        for s in steps:
            if "absEta" in s:
                self.etaMin = float(s.split("_")[1])
                self.etaMax = float(s.split("_")[2])
            elif "Et" in s:
                self.ptMin = float(s.split("_")[1])
                self.ptMax = float(s.split("_")[2])
            else:
                if s == "bad":
                    self.r9min = -1.
                    self.r9min = 0.94
                if s == "gold":
                    self.r9min = 0.94
                    self.r9max = 99999999999.

    def isIn(self, pt, eta, r9, run):
        return (pt > self.ptMin) and (pt < self.ptMax) and (eta > self.etaMin) and (eta < self.etaMax) and (r9 > self.r9Min) and (r9 < self.r9Max) and (run > self.rMin) and (run < self.rMax)

class elecScaler_MODES(object):
    def __init__(self, corrFile, isData):
        if isData:
            self.cFile = open(corrFile + "_data.dat", "r")
        else:
            self.cFile = open(corrFile + "_MC.dat", "r")
        print "LOADING"
        self.loadCorrections()
    def loadCorrections(self):
        self.corrections = [ correction(line) for line in self.cFile.readlines()]
    def getCorrection(self, lep, run):
        pt = lep.pt
        eta = abs(lep.eta)
        r9  = lep.r9
        run =  run
        for c in self.corrections:
            if c.isIn(pt,eta,r9,run):
                #print lep.pt*c.corr, c.totVar
                return lep.pt*c.corr, c.totVar
        print "NO CATEGORY FOUND!!!!", pt, eta, r9, run

class elecScalerCORRECTOR(object):
    def __init__(self, corrFile):
        print "DEFINE MC"
        self.corrMC = elecScaler_MODES(corrFile, False)
        print "DEFINE Data"
        self.corrData = elecScaler_MODES(corrFile, True)

    def getCorrection(self, lep, run, isData):
        if isData:
            return self.corrData.getCorrection(lep, run)
        else:
            return self.corrMC.getCorrection(lep, run)
