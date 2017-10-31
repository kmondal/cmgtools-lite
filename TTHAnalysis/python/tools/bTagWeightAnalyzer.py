## basically taken from https://github.com/CMSEdge/cmgtools-lite/blob/8020/TTHAnalysis/python/tools/edgeFriends.py

from CMGTools.TTHAnalysis.treeReAnalyzer import *
from ROOT import gSystem
            


## bTagWeightAnalyzer
## ___________________________________________________________________
class bTagWeightAnalyzer():


    ## __init__
    ## _______________________________________________________________
    def __init__(self, csv, eff, algo='CSVv2', wp=1, branchbtag='btagCSV', branchflavor='hadronFlavour', recllabel='Recl', isFastSim=False):

        self.recllabel = "_"+recllabel if recllabel and recllabel[0:1]!="_" else recllabel
        self.algo      = algo
        self.wp        = wp
        self.isFastSim = isFastSim
        self.label     = "FS" if isFastSim else ""

        self.branchflavor = branchflavor
        self.branchbtag   = "btagCSV" if algo in ["CSVv2", "CSV", "csvv2", "csv"] else "btagCMVA"
        self.cutVal       = self.getCutVal()
       
        vector = ROOT.vector('string')()
        vector.push_back("up")
        vector.push_back("down")

        ## load POG stuff
        ## in reader instance: 1 = medium wp
        ## in loading: 0,1,2 = b-jets, c-jets, light-jets
        self.calib    = ROOT.BTagCalibration(self.algo, csv)
        self.reader_b = ROOT.BTagCalibrationReader(1, "central", vector)
        self.reader_b.load(self.calib, 0, "comb" if not isFastSim else "fastsim")
        self.reader_c = ROOT.BTagCalibrationReader(1, "central", vector)
        self.reader_c.load(self.calib, 1, "comb" if not isFastSim else "fastsim")
        self.reader_l = ROOT.BTagCalibrationReader(1, "central", vector)
        self.reader_l.load(self.calib, 2, "incl" if not isFastSim else "fastsim")

        f_eff        = ROOT.TFile.Open(eff, "read")
        self.h_eff_b = f_eff.Get("h2_BTaggingEff_csv_med_Eff_b"   ); self.h_eff_b.SetDirectory(0)
        self.h_eff_c = f_eff.Get("h2_BTaggingEff_csv_med_Eff_c"   ); self.h_eff_c.SetDirectory(0)
        self.h_eff_l = f_eff.Get("h2_BTaggingEff_csv_med_Eff_udsg"); self.h_eff_l.SetDirectory(0)
        f_eff.Close()


	## __call__
    ## _______________________________________________________________
    def __call__(self, event):
        self.event = event
        self.resetMemory()
        self.collectObjects()
        self.computeWeights()
        return self.ret


    ## collectObjects
    ## _______________________________________________________________
    def collectObjects(self):
        goodJets  = [j for j in Collection(self.event, "Jet"    , "nJet"    )]
        discJets  = [j for j in Collection(self.event, "DiscJet", "nDiscJet")]
        if hasattr(self.event, "iJSel" + self.recllabel): 
            self.jets = []
            indices = list(getattr(self.event, "iJSel" + self.recllabel))[0:int(getattr(self.event,"nJetSel"+self.recllabel))]
            for idx in indices:
                if abs(idx)>99: continue
                if   idx >= 0 and idx   <len(goodJets): self.jets.append(goodJets[idx]   )
                elif idx <  0 and -idx-1<len(discJets): self.jets.append(discJets[-idx-1])
        else:
            self.jets = goodJets


    ## computeWeights
    ## _______________________________________________________________
    def computeWeights(self):

        mcTag     = 1.
        mcNoTag   = 1.
        dataTag   = 1.
        dataNoTag = 1.
        sysHFup   = 0
        sysHFdn   = 0
        sysLFup   = 0
        sysLFdn   = 0
    
        for jet in self.jets:
        
            flavor = getattr(jet, self.branchflavor) if hasattr(jet, self.branchflavor) else jet.mcFlavour

            if(abs(jet.eta) > 2.4): continue
            if(abs(jet.pt)  < 25 ): continue

            eff = self.getEff(jet.pt, jet.eta, flavor)
            SF  = self.getSF (jet.pt, jet.eta, flavor)

            istag = getattr(jet, self.branchbtag) > self.cutVal and abs(jet.eta) < 2.4 and jet.pt > 25

            if(istag):
                 mcTag   *= eff
                 dataTag *= eff*SF[0]
                 if flavor in [4, 5]:
                     sysHFup += (SF[1] - SF[0])/SF[0]
                     sysHFdn += (SF[0] - SF[2])/SF[0]
                 else:
                     sysLFup += (SF[1] - SF[0])/SF[0]
                     sysLFdn += (SF[0] - SF[2])/SF[0]
            else: 
                 mcNoTag   *= (1 - eff      )
                 dataNoTag *= (1 - eff*SF[0])
                 if flavor in [4, 5]:
                     sysHFup += -eff*(SF[1] - SF[0])/(1 - SF[0])
                     sysHFdn += -eff*(SF[0] - SF[2])/(1 - SF[0])
                 else: 
                     sysLFup += -eff*(SF[1] - SF[0])/(1 - SF[0])
                     sysLFdn += -eff*(SF[0] - SF[2])/(1 - SF[0])

        central = (dataNoTag * dataTag ) / ( mcNoTag * mcTag )

        self.ret["bTagWeight"+self.label         ] = central
        self.ret["bTagWeight"+self.label+"_HF_Up"] = central * ( 1 - sysHFup )
        self.ret["bTagWeight"+self.label+"_HF_Dn"] = central * ( 1 + sysHFdn )
        self.ret["bTagWeight"+self.label+"_LF_Up"] = central * ( 1 - sysLFup )
        self.ret["bTagWeight"+self.label+"_LF_Dn"] = central * ( 1 + sysLFdn )


    ## getCutVal
    ## _______________________________________________________________
    def getCutVal(self):
        if self.algo in ["CSVv2", "CSV", "csvv2", "csv"]:
            return [0.5426, 0.8484, 0.9535][self.wp]
        return [-0.5884, 0.4432, 0.9432][self.wp]


    ## getEff
    ## _______________________________________________________________
    def getEff(self, pt, eta, mcFlavor):
    
       flavor   = self.pogFlavor(mcFlavor) 
       theHisto = [self.h_eff_b, self.h_eff_c, self.h_eff_l][flavor]

       return theHisto.GetBinContent(max(1, min(theHisto.GetNbinsX(), theHisto.GetXaxis().FindBin(pt      ))), \
                                     max(1, min(theHisto.GetNbinsX(), theHisto.GetXaxis().FindBin(abs(eta)))))
       

    ## getSF
    ## _______________________________________________________________
    def getSF(self, pt, eta, mcFlavor):
        	
       flavor     = self.pogFlavor(mcFlavor) 
       theReader  = [self.reader_b, self.reader_c, self.reader_l][flavor]
    
       SF     = theReader.eval_auto_bounds("central", flavor, eta, pt)  
       SFup   = theReader.eval_auto_bounds("up"     , flavor, eta, pt)  
       SFdn   = theReader.eval_auto_bounds("down"   , flavor, eta, pt)  

       return [SF, SFup, SFdn]


    ## listBranches
    ## _______________________________________________________________
    def listBranches(self):

        biglist = [
            ("bTagWeight"+self.label          , "F"),
            ("bTagWeight"+self.label+"_HF_Up" , "F"),
            ("bTagWeight"+self.label+"_HF_Dn" , "F"),
            ("bTagWeight"+self.label+"_LF_Up" , "F"),
            ("bTagWeight"+self.label+"_LF_Dn" , "F")]
        return biglist


    ## pogFlavor
    ## _______________________________________________________________
    def pogFlavor(self, hadronFlavor):
        match = {5:0, 4:1, 0:2}
        if hadronFlavor in match.keys(): return match[hadronFlavor]
        return 2


	## resetMemory
    ## _______________________________________________________________
    def resetMemory(self):
        self.ret = {}
        self.ret["bTagWeight"+self.label         ] = 0.
        self.ret["bTagWeight"+self.label+"_HF_Up"] = 0.
        self.ret["bTagWeight"+self.label+"_HF_Dn"] = 0.
        self.ret["bTagWeight"+self.label+"_LF_Up"] = 0.
        self.ret["bTagWeight"+self.label+"_LF_Dn"] = 0.





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


