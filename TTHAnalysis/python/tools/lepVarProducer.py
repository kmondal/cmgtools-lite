import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True
from math import*

from PhysicsTools.HeppyCore.utils.deltar import deltaR

#Code adapted from @emanueledimarco's https://github.com/WMass/cmgtools-lite/blob/80X/WMass/python/postprocessing/examples/lepVarProducer.py#L102-L160
class lepCalibratedEnergyProducer():
    def __init__(self,correctionFile,seed=0,synchronization=False):
        self.corrFile = correctionFile
        self.seed = seed
        self.synchronization = synchronization
        if "/EnergyScaleCorrection_class_cc.so" not in ROOT.gSystem.GetLibraries():
            ROOT.gROOT.ProcessLine(".L %s/src/EgammaAnalysis/ElectronTools/src/EnergyScaleCorrection_class.cc+" % os.environ['CMSSW_BASE'])
        self._worker = ROOT.EnergyScaleCorrection_class(self.corrFile,self.seed)
        self.rng = ROOT.TRandom3()
        self.rng.SetSeed(self.seed)
    def gauss(self):
        if self.synchronization: return 1.0
        else: return self.rng.Gaus()
    def scaleLep(self, l, event):
        if abs(l.pdgId)!=11: # implemented only for electrons
            calPt.append(-999.) 
            calPt_step1.append(-999.) 
        else:
            if event.isData:
                scale    = self._worker.ScaleCorrection(event.run,abs(l.etaSc)<1.479,l.r9,abs(l.eta),l.pt)
                Unc      = self._worker.ScaleCorrectionUncertainty(event.run,abs(l.etaSc)<1.479,l.r9,abs(l.eta),l.pt)
                l.pt = l.pt * scale
            else:
                smear = self._worker.getSmearingSigma(event.run,abs(l.etaSc)<1.479,l.r9,abs(l.eta),l.pt,0.,0.)
                corr = 1.0 + smear * self.gauss()
                l.pt = l.pt * corr
                Unc  = 0.0
        return l, Unc

