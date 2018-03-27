from CMGTools.TTHAnalysis.treeReAnalyzer import *
from CMGTools.TTHAnalysis.tools.leptonJetReCleaner import passMllTLVeto, passTripleMllVeto
from ROOT import TFile,TH1F
import ROOT, copy, os
import array, math

#if "mt2_bisect_cc.so" not in ROOT.gSystem.GetLibraries():
#    if os.path.isdir('/pool/ciencias/' ):
#        ROOT.gROOT.LoadMacro("/pool/ciencias/HeppyTrees/RA7/additionalReferenceCode/mt2_bisect.cpp")
#        print "Loaded from Oviedo"
#    elif os.path.isdir('/mnt/t3nfs01/'):
#        ROOT.gROOT.LoadMacro("/mnt/t3nfs01/data01/shome/cheidegg/s/mT2code/mt2_bisect.cc")
#        print "Loaded from PSI"
#    else:
#        ROOT.gROOT.LoadMacro("/afs/cern.ch/user/c/cheidegg/public/mT2code/mt2_bisect.cc")

#from ROOT import mt2_bisect

# FIXME: additional variables were once written to the LepSel but now commented in order
# to keep the leptonBuilder from becoming too fat


## OSpair
## ___________________________________________________________________
class OSpair:

    ## __init__
    ## _______________________________________________________________
    def __init__(self, l1, l2):
        self.l1   = l1
        self.l2   = l2
        self.load()

    ## debug
    ## _______________________________________________________________
    def debug(self):
        add = "SF" if self.isSF else "OF"
        return "OSpair (%s, %3.1f) made up of (%3.1f, %d) and (%3.1f, %d)" % (add, self.mll, self.l1.pt, self.l1.pdgId, self.l2.pt, self.l2.pdgId)


    ## load
    ## _______________________________________________________________
    def load(self):

        self.isSF = False
        self.isZ = False
        self.wTau = False

        if     self.l1.pdgId  ==          -self.l2.pdgId       : self.isSF = True
        if abs(self.l1.pdgId) == 15 or abs(self.l2.pdgId) == 15: self.wTau = True

        if   self.isSF                                           : self.target = 91.1876
        elif abs(self.l1.pdgId) == 15 or abs(self.l2.pdgId) == 15: self.target = 60
        else                                                     : self.target = 50
  
        self.mll  = (self.l1.p4()               + self.l2.p4()              ).M()
        self.diff = abs(self.target - self.mll)

        if  self.l1.motherId == 23 and self.l2.motherId == 23: self.isZ = True
    ## test
    ## _______________________________________________________________
    def test(self, leps):
        if len(leps) > 3: return False
        ll = [self.l1, self.l2, self.l3]
        return all([l in ll for l in leps])
            


## lepgenVarsWZSM
## ___________________________________________________________________
class lepgenVarsWZSM:


    ## __init__
    ## _______________________________________________________________
    def __init__(self, inputlabel):

        self.mt2maker = None
        self.inputlabel = '_' + inputlabel

        self.systsJEC = {0: "", 1: "_jecUp"   , -1: "_jecDown"  }


    ## __call__
    ## _______________________________________________________________
    def __call__(self, event):
        self.resetMemory()
        self.collectObjects(event)
        self.analyzeTopology()
        self.writeLepSel()
        return self.ret


    ## analyzeTopology
    ## _______________________________________________________________
    def analyzeTopology(self):

        #self.passCleverPtCut()
        #if not self.passPtAndMll(): return
        if len(self.genleps)>=3: self.ret["is_3l_gen"] = 1
        if len(self.genleps)>=4: self.ret["is_4l_gen"] = 1
        if len(self.genleps)>=5: self.ret["is_5l_gen"] = 1

        self.collectOSpairs(3, False)
        self.dressLeptons(0.1)
        self.makeMass(3)
        self.makeMt2(3)
        self.findBestOSpair(3)
        self.makeMassMET(3)


        # This in principle is not needed anymore
        #self.collectOSpairs(4, True)
        #self.makeMass(4)
        #self.makeMt2(4)
        #self.findBestOSpair(4)
        #self.findMtMin(4)
        #self.makeMassMET(4)



    ## collectObjects
    ## _______________________________________________________________
    def collectObjects(self, event):

        ## gen leptons
        self.genleps    = [l             for l  in Collection(event, "genLep", "ngenLep")  ]
        
        ## Get Gen leptons
        self.setAttributes(event, self.genleps, event.isData, True)
        self.genleps.sort(key = lambda x: x.pt, reverse=True)

        self.metgen        = {}
        self.metgen[0]     = event.met_genPt if not event.isData else event.met_pt
        self.metgen[1]     = getattr(event, "met_jecUp_genPt"  , event.met_genPt if not event.isData else event.met_pt)
        self.metgen[-1]    = getattr(event, "met_jecDown_genPt", event.met_genPt if not event.isData else event.met_pt)

        self.metgenphi     = {}
        self.metgenphi[0]  = event.met_genPhi if not event.isData else event.met_phi
        self.metgenphi[1]  = getattr(event, "met_jecUp_genPhi"  , event.met_genPhi if not event.isData else event.met_phi)
        self.metgenphi[-1] = getattr(event, "met_jecDown_genPhi", event.met_genPhi if not event.isData else event.met_phi)

        # Gen photons
        self.genphotons = [l for l in Collection(event, "GenPart", "nGenPart") ]
        self.setAttributes(event, self.genphotons, event.isData, True)
        # Not really needed
        self.genphotons.sort(key = lambda x: x.pt, reverse=True)
        
        self.OS = []

    ## dressLeptons
    def dressLeptons(self,delta_r=0.1):
        usedPhoton = [ 0  ] * len(self.genphotons)
        for i in range(min(max, len(self.genleps))):
            for j in range(0,len(self.genphotons)):
                if usedPhoton[j] == 0:
                    if abs(self.genphotons[j].pdgId) == 22 and deltaR(self.genleps[i].p4().Eta(), self.genleps[i].p4().Phi(), self.genphotons[j].p4().Eta(), self.genphotons[j].p4().Phi()) < delta_r:
                        tempLep = self.genleps[i].p4()
                        tempPhot = self.genphotons[j].p4()
                        tempLep += tempPhot
                        self.genleps[i].pt = tempLep.Pt()
                        self.genleps[i].eta = tempLep.Eta()
                        self.genleps[i].phi = tempLep.Phi()
                        self.genleps[i].mass = tempLep.M()
                        usedPhoton[j] = 1
            

    ## collectOSpairs
    ## _______________________________________________________________
    def collectOSpairs(self, max, useBuffer = False):

        self.OS = []
        for i in range(min(max, len(self.genleps))):
            for j in range(i+1,min(max, len(self.genleps))):
                if abs(self.genleps[i].pdgId) == 15 and abs(self.genleps[j].pdgId) == 15: continue # no SF tautau pairs
                if useBuffer and abs(self.genleps[i].pdgId) != abs(self.genleps[j].pdgId): continue # if buffer then SF
                if self.genleps[i].pdgId * self.genleps[j].pdgId < 0: 
                    self.OS.append(OSpair(self.genleps[i], self.genleps[j]))

        ## loop over all pairs, only keep the best OSSF ones, and make sure that they do not overlap
        if useBuffer:
            self.OS.sort(key=lambda x: x.diff)
            buffer = self.OS
            self.OS = []
            used = []
            for os in buffer:
                if not os.l1 in used and not os.l2 in used:
                    self.OS.append(os)
                    used.append(os.l1); used.append(os.l2)

        self.ret["nOSSF_" + str(max) + "l_gen"] = self.countOSSF(max)
        self.ret["nOSTF_" + str(max) + "l_gen"] = self.countOSTF(max)
        self.ret["nOSLF_" + str(max) + "l_gen"] = self.countOSLF(max)


    ## countOSLF
    ## _______________________________________________________________
    def countOSLF(self, max):
        return sum(1 if not os.wTau else 0 for os in self.OS)


    ## countOSSF
    ## _______________________________________________________________
    def countOSSF(self, max):
        return sum(1 if os.isSF else 0 for os in self.OS)


    ## countOSTF
    ## _______________________________________________________________
    def countOSTF(self, max):
        return sum(1 if os.wTau else 0 for os in self.OS)

    ## makeMass
    ## _______________________________________________________________
    def makeMass(self, max):
       
        if len(self.genleps) < 3: return 
        sum = self.genleps[0].p4()
        for i in range(1,min(max,len(self.genleps))):
            sum += self.genleps[i].p4(self.genleps[i].pt)
        self.ret["m" + str(max) + "L_gen"] = sum.M()

        minMllAFAS = 10000
        minMllSFOS = 10000

        for i in range(len(self.genleps)):
          if not(abs(self.genleps[i].motherId) in [23,24]): continue
          for j in range(i,len(self.genleps)):
            if not(abs(self.genleps[j].motherId) in [23,24]): continue
            if i==j: continue
            testMass = (self.genleps[i].p4() + self.genleps[j].p4()).M()
            #if testMass <  5: print testMass, i, j
            if testMass < minMllAFAS:
              minMllAFAS = testMass
            if testMass < minMllSFOS and (self.genleps[i].pdgId + self.genleps[j].pdgId) == 0:
              minMllSFOS = testMass
        self.ret["minmllAFAS_gen"] = minMllAFAS
        self.ret["minmllSFOS_gen"] = minMllSFOS
      

    ## makeMassMET (leptons and MET)
    ## _______________________________________________________________
    def makeMassMET(self, max):
           
        if len(self.genleps) < 3: return 
        sumlep = self.genleps[0].p4()
        metp4 = ROOT.TLorentzVector()
        for i in range(1,min(max,len(self.genleps))):
            sumlep += self.genleps[i].p4(self.genleps[i].pt) 
        for var in self.systsJEC:
            metp4.SetPtEtaPhiM(self.metgen[var],0,self.metgenphi[var],0)
            sumtot = sumlep + metp4
            self.ret["m" + str(max) + "Lmet" + self.systsJEC[var] + "_gen"] = sumtot.M()

    ## makeMt2
    ## _______________________________________________________________
    def makeMt2(self, max):
        ## building two sets of MT2
        ## mT2L = two light flavor leptons from the OS pair (category C, D)
        ## mT2T = hardest light lepton and one tau (category E, F)

        if not self.mt2maker: return False
        #if self.mt2maker: print "I have mT2maker\n"
        anyPairs = []
        for i in range(min(max, len(self.genleps))):
            for j in range(i+1,min(max, len(self.genleps))):
                if abs(self.genleps[i].pdgId) == 15 or abs(self.genleps[j].pdgId) == 15:
                    anyPairs.append(OSpair(self.genleps[i], self.genleps[j]))

        mt2t = []
        mt2l = []
        for os in anyPairs:
            if os.wTau and abs(os.l1.pdgId) != 15 or  abs(os.l2.pdgId) != 15: mt2t.append((os.l1.pt+os.l2.pt, os))
        for os in self.OS:
            if             abs(os.l1.pdgId) != 15 and abs(os.l2.pdgId) != 15: mt2l.append((os.l1.pt+os.l2.pt, os))

        mt2t.sort(reverse=True) # we want the hardest leptons here! 
        mt2l.sort(reverse=True) # we want the hardest leptons here! 
        #if len(mt2l)>0: print "I have os pair for mt2l\n"
        for var in self.systsJEC:
            if len(mt2t)>0: 
                self.ret["mT2T_" + str(max) + "l" + self.systsJEC[var] + "_gen"] = self.mt2(mt2t[0][1].l1, mt2t[0][1].l2, var)
            if len(mt2l)>0: 
                self.ret["mT2L_" + str(max) + "l" + self.systsJEC[var] + "_gen"] = self.mt2(mt2l[0][1].l1, mt2l[0][1].l2, var)
        #if len(mt2l)>0: print self.ret["mT2L_" + str(max) + "l"]

    ## mt  
    ## _______________________________________________________________
    def mt(self, pt1, pt2, phi1, phi2):
        return sqrt(2*pt1*pt2*(1-cos(phi1-phi2)))


    ## mt2
    ## _______________________________________________________________
    def mt2(self, obj1, obj2, var, useGenMet = False):
            
        vector_met     = array.array('d', [0, self.metgen[var]*cos(self.metgenphi[var]), self.metgen[var]*sin(self.metgenphi[var])])
        vector_obj1    = array.array('d', [obj1.mass, obj1.p4(obj1.pt).Px(), obj1.p4(obj1.pt).Py()])
        vector_obj2    = array.array('d', [obj2.mass, obj2.p4(obj2.pt).Px(), obj2.p4(obj2.pt).Py()])

        if useGenMet:
            vector_met = array.array('d', [0, self.metgen[var]*cos(self.metgenphi[var]), self.metgen[var]*sin(self.metgenphi[var])])

        self.mt2maker.set_momenta(vector_obj1, vector_obj2, vector_met)
        self.mt2maker.set_mn(0)

        return self.mt2maker.get_mt2()
    
    
    ## mtW
    ## _______________________________________________________________
    def mtW(self, lep, var, useGenMet = False):
        if useGenMet: return self.mt(lep.pt, self.metgen[var], lep.phi, self.metgenphi[var])
        return self.mt(lep.pt, self.metgen[var], lep.phi, self.metgenphi[var])




    ## findBestOSpair
    ## _______________________________________________________________
    def findBestOSpair(self, max):

        self.bestOSPair = None

        all = []
        for os in self.OS:
            all.append((0 if os.isZ else 1, 0 if os.isSF else 1, os.diff, os)) # priority to SF, then difference to target
            #all.append((0 if os.isSF else 1, 1 if os.wTau else 0, os.diff, os)) # priority to SF, then light, then difference to target

        if all:
            all.sort()
            self.bestOSPair = all[0][3]
            self.ret["mll_" + str(max) + "l_gen"] = self.bestOSPair.mll
            used = [self.bestOSPair.l1, self.bestOSPair.l2] if self.bestOSPair else []
            
            for var in ["pt", "eta", "phi", "mass"]:
                self.ret["genLepZ1_" + var] = getattr(self.bestOSPair.l1, var, 0)
                self.ret["genLepZ2_" + var] = getattr(self.bestOSPair.l2, var, 0)
            for var in ["pdgId", "motherId"]:
                self.ret["genLepZ1_" + var] = int(getattr(self.bestOSPair.l1, var, 0))
                self.ret["genLepZ2_" + var] = int(getattr(self.bestOSPair.l2, var, 0))


            for i in range(min(max,len(self.genleps))):
                if self.genleps[i] in used or not(abs(self.genleps[i].motherId) == 24) : continue
                for var in ["pt", "eta", "phi", "mass"]:
                    self.ret["genLepW_" + var] = getattr(self.genleps[i], var, 0)
                for var in ["pdgId", "motherId"]:
                    self.ret["genLepW_" + var] = int(getattr(self.genleps[i], var, 0))
                #for var in ["pt", "pt"]:
                #    self.ret["wzBalance_" + var] = getattr(self.bestOSPair.l1.p4()+self.bestOSPair.l2.p4()-self.genleps[i].p4(), var, 0)
                balance = self.bestOSPair.l1.p4()
                balance += self.bestOSPair.l2.p4()
                self.ret["deltaR_WZ_gen"] = deltaR(balance.Eta(), balance.Phi(), self.genleps[i].p4().Eta(), self.genleps[i].p4().Phi())
                balance += self.genleps[i].p4()
                metmom = ROOT.TLorentzVector()
                metmom.SetPtEtaPhiM(self.metgen[0],0,self.metgenphi[0],0)
                balance += metmom
                # Later do it with standalone function like makeMassMET
                self.ret["wzBalance_pt_gen"] = balance.Pt()
                balance = self.bestOSPair.l1.p4(self.bestOSPair.l1.pt)
                balance += self.bestOSPair.l2.p4(self.bestOSPair.l2.pt)
                balance += self.genleps[i].p4(self.genleps[i].pt)
                balance += metmom
                self.ret["wzBalance_pt_gen"] = balance.Pt()
            return

        self.ret["mll_" + str(max) + "l_gen"] = -1


    ## listBranches
    ## _______________________________________________________________
    def listBranches(self):

        biglist = [
            ("is_3l_gen"            , "I"),
            ("is_4l_gen"            , "I"),
            ("is_5l_gen"            , "I"),
            ("nOSSF_3l_gen"         , "I"),
            ("nOSLF_3l_gen"         , "I"),
            ("nOSTF_3l_gen"         , "I"),
            ("mll_3l_gen"           , "F"),
            ("m3L_gen"              , "F"),
            ("nOSSF_4l_gen"         , "I"),
            ("nOSLF_4l_gen"         , "I"),
            ("nOSTF_4l_gen"         , "I"),
            ("mll_4l_gen"           , "F"),
            ("m4L_gen"              , "F"),
            ("minDeltaR_3l_gen"     , "F"),
            ("minDeltaR_4l_gen"     , "F"),
            ("minDeltaR_3l_mumu_gen", "F"),
            ("minDeltaR_4l_mumu_gen", "F"),
            ("minmllAFAS_gen"       , "F"),
            ("minmllSFOS_gen"       , "F")]
            
        biglist.append(("nOS_gen"   , "I"))
        #biglist.append(("mll_gen"   , "F", 20, "nOS"))
        #biglist.append(("mll_i1_gen", "I", 20, "nOS"))
        #biglist.append(("mll_i2_gen", "I", 20, "nOS"))
        biglist.append(("deltaR_WZ_gen", "F"))

        biglist.append(("nLepGen_gen"   , "I"))
        for var in ["pt", "eta", "phi", "mass"]:
            biglist.append(("LepGen_" + var, "F", 4))
            biglist.append(("genLepZ1_"  + var, "F"))
            biglist.append(("genLepZ2_"  + var, "F"))
            biglist.append(("genLepW_"   + var, "F"))
        for var in ["pdgId", "motherId"]:
            biglist.append(("LepGen_" + var, "I", 4))
            biglist.append(("genLepZ1_"  + var, "I"))
            biglist.append(("genLepZ2_"  + var, "I"))
            biglist.append(("genLepW_"   + var, "I"))

        for var in ["pt"]:
            biglist.append(("wzBalance_" + var + "_gen", "F"))
  
        for var in self.systsJEC:
            biglist.append(("mT_3l"       + self.systsJEC[var] + "_gen", "F"))
            biglist.append(("mT2L_3l"     + self.systsJEC[var] + "_gen", "F"))
            biglist.append(("mT2T_3l"     + self.systsJEC[var] + "_gen", "F"))
            biglist.append(("mT_4l"       + self.systsJEC[var] + "_gen", "F"))
            biglist.append(("mT2L_4l"     + self.systsJEC[var] + "_gen", "F"))
            biglist.append(("mT2T_4l"     + self.systsJEC[var] + "_gen", "F"))
            biglist.append(("m3Lmet"      + self.systsJEC[var] + "_gen", "F"))
            biglist.append(("m4Lmet"      + self.systsJEC[var] + "_gen", "F"))
        return biglist


    ## resetMemory
    ## _______________________________________________________________
    def resetMemory(self):

        self.ret = {};

        self.ret["is_3l_gen"                ] = 0
        self.ret["is_4l_gen"                ] = 0
        self.ret["is_5l_gen"                ] = 0
        self.ret["nOSSF_3l_gen"             ] = 0
        self.ret["nOSLF_3l_gen"             ] = 0
        self.ret["nOSTF_3l_gen"             ] = 0
        self.ret["mll_3l_gen"               ] = 0
        self.ret["m3L_gen"                  ] = 0
        self.ret["nOSSF_4l_gen"             ] = 0
        self.ret["nOSLF_4l_gen"             ] = 0
        self.ret["nOSTF_4l_gen"             ] = 0
        self.ret["mll_4l_gen"               ] = 0
        self.ret["m4L_gen"                  ] = 0
        self.ret["minDeltaR_3l_gen"         ] = -1
        self.ret["minDeltaR_4l_gen"         ] = -1
        self.ret["minDeltaR_3l_mumu_gen"    ] = -1
        self.ret["minDeltaR_4l_mumu_gen"    ] = -1
        self.ret["deltaR_WZ_gen"            ] = 0

        self.ret["nOS_gen"   ] = 0
        #self.ret["mll_gen"   ] = [0.]*20
        #self.ret["mll_i1_gen"] = [-1]*20
        #self.ret["mll_i2_gen"] = [-1]*20

        self.ret["nLepGen_gen"] = 0
        for var in ["pt", "eta", "phi", "mass"]:
            self.ret["LepGen_" + var] = [0.]*20
            self.ret["genLepZ1_"  + var] = 0.
            self.ret["genLepZ2_"  + var] = 0.
            self.ret["genLepW_"   + var] = 0.
        for var in ["pdgId", "motherId"]:
            self.ret["LepGen_" + var] = [0]*20
            self.ret["genLepZ1_"  + var] = 0
            self.ret["genLepZ2_"  + var] = 0
            self.ret["genLepW_"   + var] = 0

        for var in ["pt", "pt"]:
            self.ret["wzBalance_" + var + "_gen"] = 0

        for var in self.systsJEC:
            self.ret["mT_3l"       + self.systsJEC[var] + "_gen"] = 0.
            self.ret["mT2L_3l"     + self.systsJEC[var] + "_gen"] = 0.  
            self.ret["mT2T_3l"     + self.systsJEC[var] + "_gen"] = 0. 
            self.ret["mT_4l"       + self.systsJEC[var] + "_gen"] = 0.
            self.ret["mT2L_4l"     + self.systsJEC[var] + "_gen"] = 0.  
            self.ret["mT2T_4l"     + self.systsJEC[var] + "_gen"] = 0. 
            self.ret["m3Lmet"      + self.systsJEC[var] + "_gen"] = 0. 
            self.ret["m4Lmet"      + self.systsJEC[var] + "_gen"] = 0. 


    ## setAttributes 
    ## _______________________________________________________________
    def setAttributes(self, event, lepSel, isData = False,  isGen = True):

        for i, l in enumerate(lepSel): 
            if  isGen:
                setattr(l, "motherId"     , l.motherId                          )
                setattr(l, "grandmotherId"     , l.grandmotherId                     )

                





    ## writeLepSel
    ## _______________________________________________________________
    def writeLepSel(self):

        self.ret["nLepGen_gen"] = len(self.genleps)
        for i, l in enumerate(self.genleps):
            if i == 4: break # only keep the first 4 entries
            for var in ["pt", "eta", "phi", "mass"]:
                self.ret["LepGen_" + var][i] = getattr(l, var, 0)
            for var in ["pdgId"]:
                self.ret["LepGen_" + var][i] = int(getattr(l, var, 0))


        all = []
        for os in self.OS:
            all.append((0 if os.isSF else 1, 1 if os.wTau else 0, os.diff, os)) # priority to SF, then light, then difference to target
        if all:
            all.sort()
            self.ret["nOS_gen"] = len(all)
            #for i,os in enumerate(all):
            #    self.ret["mll_gen"][i] = os[3].mll
            #    self.ret["mll_i1_gen"][i] = self.genleps.index(os[3].l1)
            #    self.ret["mll_i2_gen"][i] = self.genleps.index(os[3].l2)





## deltaPhi
## _______________________________________________________________
def deltaPhi(phi1, phi2):
    res = phi1 - phi2
    while res >   math.pi: res -= 2*math.pi
    while res <= -math.pi: res += 2*math.pi
    return res

## deltaR
## _______________________________________________________________
def deltaR(eta1, phi1, eta2, phi2):
    dEta = abs(eta1-eta2)
    dPhi = deltaPhi(phi1, phi2)
    return math.sqrt(dEta*dEta + dPhi*dPhi)



if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf1 = LeptonChoiceEWK("Old", 
                lambda lep : lep.relIso03 < 0.5, 
                lambda lep : lep.relIso03 < 0.1 and lep.sip3d < 4 and _susy2lss_lepId_CB(lep),
                cleanJet = lambda lep,jet,dr : (lep.pt > 10 and dr < 0.4))
            self.sf2 = LeptonChoiceEWK("PtRel", 
                lambda lep : lep.relIso03 < 0.4 or lep.jetPtRel > 5, 
                lambda lep : (lep.relIso03 < 0.1 or lep.jetPtRel > 14) and lep.sip3d < 4 and _susy2lss_lepId_CB(lep),
                cleanJet = lambda lep,jet,dr : (lep.pt > 10 and dr < 0.4))
            self.sf3 = LeptonChoiceEWK("MiniIso", 
                lambda lep : lep.miniRelIso < 0.4, 
                lambda lep : lep.miniRelIso < 0.05 and lep.sip3d < 4 and _susy2lss_lepId_CB(lep),
                cleanJet = lambda lep,jet,dr : (lep.pt > 10 and dr < 0.4))
            self.sf4 = LeptonChoiceEWK("PtRelJC", 
                lambda lep : lep.relIso03 < 0.4 or lep.jetPtRel > 5, 
                lambda lep : (lep.relIso03 < 0.1 or lep.jetPtRel > 14) and lep.sip3d < 4 and _susy2lss_lepId_CB(lep),
                cleanJet = lambda lep,jet,dr : (lep.pt > 10 and dr < 0.4 and not (lep.jetPtRel > 5 and lep.pt*(1/lep.jetPtRatio-1) > 25)))
            self.sf5 = LeptonChoiceEWK("MiniIsoJC", 
                lambda lep : lep.miniRelIso < 0.4, 
                lambda lep : lep.miniRelIso < 0.05 and lep.sip3d < 4 and _susy2lss_lepId_CB(lep),
                cleanJet = lambda lep,jet,dr : (lep.pt > 10 and dr < 0.4 and not (lep.jetDR > 0.5*10/min(50,max(lep.pt,200)) and lep.pt*(1/lep.jetPtRatio-1) > 25)))
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf1(ev)
            print self.sf2(ev)
            print self.sf3(ev)
            print self.sf4(ev)
            print self.sf5(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)

