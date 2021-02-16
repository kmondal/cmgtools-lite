from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from PhysicsTools.Heppy.physicsobjects.Jet import _btagWPs as HiggsRecoTTHbtagwps

import ROOT, itertools
from ROOT import *
import numpy as np
import math

#ximport dnn_tagger_new_dr
import h5py
#import keras as kr
#from keras.models import Sequential
#from keras.layers import InputLayer, Input
#from keras.layers import Reshape, MaxPooling2D
#from keras.layers import Conv2D, Dense, Flatten, Dropout
#from keras import optimizers
#from keras.layers import Dense, Activation
#from keras.wrappers.scikit_learn import KerasRegressor
#from keras.callbacks import EarlyStopping
#from keras.layers.advanced_activations import PReLU
#from tensorflow.keras.layers import BatchNormalization
from keras import optimizers
from keras.models import load_model
#model_dnn = load_model('dnn_tagger_new_dr.h5')

class HiggsDiffRegressionTTH_new(Module):
    def __init__(self,label="_Recl", variations=[], cut_BDT_rTT_score = 0.0, btagDeepCSVveto = 'M', doSystJEC=True):
        self.label = label
        self.cut_BDT_rTT_score = cut_BDT_rTT_score
        self.btagDeepCSVveto = btagDeepCSVveto
        self.branches = []
        self.systsJEC = {0:"", 1:"_jesTotalCorrUp", -1:"_jesTotalCorrDown", 2:"_jesTotalUnCorrUp", -2:"_jesTotalUnCorrDown"} if doSystJEC else {0:""}
        if len(variations):
            self.systsJEC = {0:""}
            for i,var in enumerate(variations):
                self.systsJEC[i+1]   ="_%sUp"%var
                self.systsJEC[-(i+1)]="_%sDown"%var
        self.nlep = 2
        self.njet = 5
        self.ngenjet = 8
        self.model_dnn = load_model(os.path.join(os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/data/regressionMVA/dnn_tagger_new_dr_real.h5"))

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        #model_dnn = load_model('dnn_tagger_new_dr.h5') 
        self.out = wrappedOutputTree
        self.model_dnn.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        # Independent on JES
        self.out.branch('%snLFromWFromH'%self.label,        'I')
        self.out.branch('%snLFromWFromT'%self.label,        'I')
        self.out.branch('%snQFromWFromH'%self.label,        'I')
        self.out.branch('%snNuFromWFromH'%self.label,       'I')
        self.out.branch('%sLFromWFromH_pt'%self.label,      'F')
        self.out.branch('%sLFromWFromH_eta'%self.label,     'F')
        self.out.branch('%sLFromWFromH_phi'%self.label,     'F')
        self.out.branch('%sLFromWFromH_mass'%self.label,    'F')
        self.out.branch('%sLFromWFromT_pt'%self.label,      'F')
        self.out.branch('%sLFromWFromT_eta'%self.label,     'F')
        self.out.branch('%sLFromWFromT_phi'%self.label,     'F')
        self.out.branch('%sLFromWFromT_mass'%self.label,    'F')
        self.out.branch('%sQ1FromWFromH_pt'%self.label,     'F')
        self.out.branch('%sQ1FromWFromH_eta'%self.label,    'F')
        self.out.branch('%sQ1FromWFromH_phi'%self.label,    'F')
        self.out.branch('%sQ1FromWFromH_mass'%self.label,   'F')
        self.out.branch('%sQ2FromWFromH_pt'%self.label,     'F')
        self.out.branch('%sQ2FromWFromH_eta'%self.label,    'F')
        self.out.branch('%sQ2FromWFromH_phi'%self.label,    'F')
        self.out.branch('%sQ2FromWFromH_mass'%self.label,   'F')
        self.out.branch('%sNuFromWFromH_pt'%self.label,     'F')
        self.out.branch('%sNuFromWFromH_eta'%self.label,    'F')
        self.out.branch('%sNuFromWFromH_phi'%self.label,    'F')
        self.out.branch('%sNuFromWFromH_mass'%self.label,   'F')
        self.out.branch('%snNuFromWFromT'%self.label,       'F')
        self.out.branch('%snNuFromWFromT_lenpt'%self.label, 'F')
        self.out.branch('%sNuFromWFromT_pt'%self.label,     'F')
        self.out.branch('%sNuFromWFromT_eta'%self.label,    'F')
        self.out.branch('%sNuFromWFromT_phi'%self.label,    'F')
        self.out.branch('%sNuFromWFromT_mass'%self.label,   'F')
        self.out.branch('%sJet_FromH_FromW'%self.label,   'I')

        for suffix in ["_pt", "_eta", "_phi", "_mass"]:
            for iGJet in range(self.ngenjet):
                self.out.branch('%sGenJet%s%s'%(self.label,iGJet,suffix)   , 'F')

            for gLep in range(self.nlep):
                self.out.branch('%sGenLep%s%s'%(self.label,gLep,suffix)   , 'F')
            
        # Somehow dependent on JES

        for jesLabel in self.systsJEC.values():
            
            # Counters
            self.out.branch('%snLeps%s'%(self.label,jesLabel), 'I') 
            self.out.branch('%snJets%s'%(self.label,jesLabel), 'I')

            # Leptons and the precomputed hadronic top
            for suffix in ["_pt", "_eta", "_phi", "_mass"]:
                for iLep in range(self.nlep):
                    self.out.branch('%sLep%s%s%s'%(self.label,iLep,jesLabel,suffix)   , 'F') 
                self.out.branch('%sHadTop%s%s'%(self.label,jesLabel,suffix), 'F')

            # Jets
            for suffix in ["_pt", "_eta", "_phi", "_mass", "_btagdiscr", "_ishadtop"]:
                for iJet in range(self.njet):
                    self.out.branch('%sJet%s%s%s'%(self.label,iJet,jesLabel,suffix)   , 'F')

            self.out.branch('%sTopScore%s'%(self.label,jesLabel)      , 'F')      
            self.out.branch('%smet%s'%(self.label,jesLabel)           , 'F')       
            self.out.branch('%smet_phi%s'%(self.label,jesLabel)       , 'F')
            self.out.branch('%sHTXS_Higgs%s_pt'%(self.label,jesLabel) , 'F')
            self.out.branch('%sHTXS_Higgs%s_y'%(self.label,jesLabel)  , 'F')
            self.out.branch('%sHgen_vis_pt%s'%(self.label,jesLabel)   , 'F')
            self.out.branch('%sHgen_tru_pt%s'%(self.label,jesLabel)   , 'F')

            self.out.branch('%sJet_Higgs_score'%(self.label), 'F')
            self.out.branch('%sreco_score_higgs'%(self.label), 'F')

            self.out.branch('%sgen_q1_q2_pt'%(self.label), 'F'   )
            self.out.branch('%sgen_q1_q2_eta'%(self.label), 'F'   )
            self.out.branch('%sgen_q1_q2_phi'%(self.label), 'F'   )
            self.out.branch('%sgen_q1_q2_mass'%(self.label), 'F'   )

            self.out.branch('%sreco_q1_q2_pt'%(self.label) , 'F')
            self.out.branch('%sreco_q1_q2_eta'%(self.label) , 'F')
            self.out.branch('%sreco_q1_q2_phi'%(self.label) , 'F')
            self.out.branch('%sreco_q1_q2_mass'%(self.label) , 'F')
            #self.out.branch('%sreco_q1_q2_label_one'%(self.label) , 'F')

            self.out.branch('%sreco_match_q1_q2_pt'%(self.label) , 'F')
            self.out.branch('%sreco_match_q1_q2_eta'%(self.label) , 'F')
            self.out.branch('%sreco_match_q1_q2_phi'%(self.label) , 'F')
            self.out.branch('%sreco_match_q1_q2_mass'%(self.label) , 'F')
            #self.out.branch('%sreco_match_q1_q2_label'%(self.label) , 'F')
            #self.out.branch('%sreco_match_q1_q2_label_one'%(self.label) , 'F')

            self.out.branch('%sreco_q1_score_higgs_pt'%(self.label), 'F')
            self.out.branch('%sreco_q1_score_higgs_eta'%(self.label), 'F')
            self.out.branch('%sreco_q1_score_higgs_phi'%(self.label), 'F')
            self.out.branch('%sreco_q1_score_higgs_mass'%(self.label), 'F')

            self.out.branch('%sreco_q2_score_higgs_pt'%(self.label), 'F')
            self.out.branch('%sreco_q2_score_higgs_eta'%(self.label), 'F')
            self.out.branch('%sreco_q2_score_higgs_phi'%(self.label), 'F')
            self.out.branch('%sreco_q2_score_higgs_mass'%(self.label), 'F')

            self.out.branch('%sreco_q1_q2_score_higgs_pt'%(self.label), 'F')
            self.out.branch('%sreco_q1_q2_score_higgs_eta'%(self.label), 'F')
            self.out.branch('%sreco_q1_q2_score_higgs_phi'%(self.label), 'F')
            self.out.branch('%sreco_q1_q2_score_higgs_mass'%(self.label), 'F')

            self.out.branch('%sreco_match_real_q1_pt'%(self.label), 'F')
            self.out.branch('%sreco_match_real_q1_eta'%(self.label), 'F')
            self.out.branch('%sreco_match_real_q1_phi'%(self.label), 'F')
            self.out.branch('%sreco_match_real_q1_mass'%(self.label), 'F')

            self.out.branch('%sreco_match_real_q2_pt'%(self.label), 'F')
            self.out.branch('%sreco_match_real_q2_eta'%(self.label), 'F')
            self.out.branch('%sreco_match_real_q2_phi'%(self.label), 'F')
            self.out.branch('%sreco_match_real_q2_mass'%(self.label), 'F')

            self.out.branch('%sreco_match_real_q1_q2_pt'%(self.label), 'F')
            self.out.branch('%sreco_match_real_q1_q2_eta'%(self.label), 'F')
            self.out.branch('%sreco_match_real_q1_q2_phi'%(self.label), 'F')
            self.out.branch('%sreco_match_real_q1_q2_mass'%(self.label), 'F')




            self.out.branch('%sJet_Label'%(self.label) , 'F')
            self.out.branch('%sJet_Label_dr'%(self.label) , 'F')
            self.out.branch('%sJet_Label_dr_real'%(self.label) , 'F')
            self.out.branch('%sJet_Label_pt'%(self.label) , 'F')
            self.out.branch('%sJet_Label_eta'%(self.label) , 'F')
            self.out.branch('%sJet_Label_phi'%(self.label) , 'F')
            self.out.branch('%sJet_Label_mass'%(self.label) , 'F')
            self.out.branch('%sJet_Label_bdisc'%(self.label) , 'F')
            self.out.branch('%sJet_Label_dr_lep0'%(self.label) , 'F')
            self.out.branch('%sJet_Label_dr_lep1'%(self.label) , 'F')

            self.out.branch('%sreco_w_q1_q2_pt'%(self.label) , 'F')
            self.out.branch('%sreco_w_q1_q2_eta'%(self.label) , 'F')
            self.out.branch('%sreco_w_q1_q2_phi'%(self.label) , 'F')
            self.out.branch('%sreco_w_q1_q2_mass'%(self.label) , 'F')

            self.out.branch('%sMore5_Jets_pt'%(self.label), 'F'   )
            self.out.branch('%sMore5_Jets_eta'%(self.label), 'F'   )
            self.out.branch('%sMore5_Jets_phi'%(self.label), 'F'   )
            self.out.branch('%sMore5_Jets_mass'%(self.label), 'F'   )

            self.out.branch('%sAll5_Jets_pt'%(self.label), 'F'   )
            self.out.branch('%sAll5_Jets_eta'%(self.label), 'F'   )
            self.out.branch('%sAll5_Jets_phi'%(self.label), 'F'   )
            self.out.branch('%sAll5_Jets_mass'%(self.label), 'F'   )


            self.out.branch('%sJets_plus_Lep_pt'%(self.label), 'F'   )
            self.out.branch('%sJets_plus_Lep_eta'%(self.label), 'F'   )
            self.out.branch('%sJets_plus_Lep_phi'%(self.label), 'F'   )
            self.out.branch('%sJets_plus_Lep_mass'%(self.label), 'F'   )
            self.out.branch('%sMet_calc_pt'%(self.label), 'F'   )
            self.out.branch('%sMet_calc_eta'%(self.label), 'F'   )
            self.out.branch('%sMet_calc_phi'%(self.label), 'F'   )
            self.out.branch('%sMet_calc_mass'%(self.label), 'F'   )

            self.out.branch('%sevt_tag%s'%(self.label,jesLabel)       , 'F')       
            
            # Tell the network how to connect the lepton and the closest jet
            for iLep in range(self.nlep):
                self.out.branch('%sDeltaRClosestJetToLep%s%s'%(self.label,iLep,jesLabel) , 'F')
                self.out.branch('%sDeltaPtClosestJetToLep%s%s'%(self.label,iLep,jesLabel) , 'F')
                self.out.branch('%sClosestJetToLep_pt%s%s'%(self.label,iLep,jesLabel) , 'F')
                self.out.branch('%sClosestJetToLep_eta%s%s'%(self.label,iLep,jesLabel) , 'F')
                self.out.branch('%sClosestJetToLep_phi%s%s'%(self.label,iLep,jesLabel) , 'F')
                self.out.branch('%sClosestJetToLep_mass%s%s'%(self.label,iLep,jesLabel) , 'F')

            # In principle I need only the DeltaRl0l1 and the previously defined "closest" vars
            for var in ['DeltaRl0l1',
                        #'DeltaRl0j0', 'DeltaRl0j1', 'DeltaRl0j2', 'DeltaRl0j3', 'DeltaRl0j4', 'DeltaRl0j5', 'DeltaRl0j6', 
                        #'DeltaRl1j0', 'DeltaRl1j1', 'DeltaRl1j2', 'DeltaRl1j3', 'DeltaRl1j4', 'DeltaRl1j5', 'DeltaRl1j6', 
                        #'DeltaRj0j0', 'DeltaRj0j1', 'DeltaRj0j2', 'DeltaRj0j3', 'DeltaRj0j4', 'DeltaRj0j5', 'DeltaRj0j6', 
                        #'DeltaRj1j0', 'DeltaRj1j1', 'DeltaRj1j2', 'DeltaRj1j3', 'DeltaRj1j4', 'DeltaRj1j5', 'DeltaRj1j6', 
                        #'DeltaRj2j0', 'DeltaRj2j1', 'DeltaRj2j2', 'DeltaRj2j3', 'DeltaRj2j4', 'DeltaRj2j5', 'DeltaRj2j6', 
                        #'DeltaRj3j0', 'DeltaRj3j1', 'DeltaRj3j2', 'DeltaRj3j3', 'DeltaRj3j4', 'DeltaRj3j5', 'DeltaRj3j6', 
                        #'DeltaRj4j0', 'DeltaRj4j1', 'DeltaRj4j2', 'DeltaRj4j3', 'DeltaRj4j4', 'DeltaRj4j5', 'DeltaRj4j6', 
                        #'DeltaRj5j0', 'DeltaRj5j1', 'DeltaRj5j2', 'DeltaRj5j3', 'DeltaRj5j4', 'DeltaRj5j5', 'DeltaRj5j6', 
                        #'DeltaRj6j0', 'DeltaRj6j1', 'DeltaRj6j2', 'DeltaRj6j3', 'DeltaRj6j4', 'DeltaRj6j5', 'DeltaRj6j6', 
                    ]:
                self.out.branch('%s%s%s'%(self.label,var,jesLabel), 'F')

    def buildHadronicTop(self, event, score, alljets, jesLabel):
        HadTop=None
        if score>self.cut_BDT_rTT_score:
            j1top = int(getattr(event,"BDThttTT_eventReco_iJetSel1%s"%jesLabel))
            j2top = int(getattr(event,"BDThttTT_eventReco_iJetSel2%s"%jesLabel))
            j3top = int(getattr(event,"BDThttTT_eventReco_iJetSel3%s"%jesLabel))
            # Build hadronic top
            top1 = ROOT.TLorentzVector(); top1.SetPtEtaPhiM(alljets[j1top].p4().Pt(),alljets[j1top].p4().Eta(), alljets[j1top].p4().Phi(), alljets[j1top].p4().M())
            top2 = ROOT.TLorentzVector(); top2.SetPtEtaPhiM(alljets[j2top].p4().Pt(),alljets[j2top].p4().Eta(), alljets[j2top].p4().Phi(), alljets[j2top].p4().M())
            top3 = ROOT.TLorentzVector(); top3.SetPtEtaPhiM(alljets[j3top].p4().Pt(),alljets[j3top].p4().Eta(), alljets[j3top].p4().Phi(), alljets[j3top].p4().M())
            HadTop = top1+top2+top3
        return HadTop

    def analyze(self, event):

        # Some useful input parameters
        year=getattr(event,'year')
        btagvetoval=HiggsRecoTTHbtagwps['DeepFlav_%d_%s'%(year,self.btagDeepCSVveto)][1]

        nAllLeps = event.nLepGood
        nRecleanedLeps = event.nLepFO_Recl
        recleanedLepsIdxs = event.iLepFO_Recl
        allLeps = Collection(event,"LepGood","nLepGood")
        leps = [allLeps[recleanedLepsIdxs[i]] for i in xrange(nRecleanedLeps)]
        alljets = [x for x in Collection(event,"JetSel_Recl","nJetSel_Recl")]

        nLFromWFromH = getattr(event,"%snLFromWFromH"%self.label)
        nLFromWFromT = getattr(event,"%snLFromWFromT"%self.label)
        nQFromWFromH = getattr(event,"%snQFromWFromH"%self.label)
        nNuFromWFromH = getattr(event,"%snNuFromWFromH"%self.label)
        LFromWFromH_pt = getattr(event,"%sLFromWFromH_pt"%self.label)
        LFromWFromH_eta = getattr(event,"%sLFromWFromH_eta"%self.label)
        LFromWFromH_phi = getattr(event,"%sLFromWFromH_phi"%self.label)
        LFromWFromH_mass = getattr(event,"%sLFromWFromH_mass"%self.label)
        LFromWFromT_pt = getattr(event,"%sLFromWFromT_pt"%self.label)
        LFromWFromT_eta = getattr(event,"%sLFromWFromT_eta"%self.label)
        LFromWFromT_phi = getattr(event,"%sLFromWFromT_phi"%self.label)
        LFromWFromT_mass = getattr(event,"%sLFromWFromT_mass"%self.label)
        QFromWFromH_pt = getattr(event,"%sQFromWFromH_pt"%self.label)
        QFromWFromH_eta = getattr(event,"%sQFromWFromH_eta"%self.label)
        QFromWFromH_phi = getattr(event,"%sQFromWFromH_phi"%self.label)
        QFromWFromH_mass = getattr(event,"%sQFromWFromH_mass"%self.label)
        NuFromWFromH_pt = getattr(event,"%sNuFromWFromH_pt"%self.label)
        NuFromWFromH_eta = getattr(event,"%sNuFromWFromH_eta"%self.label)
        NuFromWFromH_phi = getattr(event,"%sNuFromWFromH_phi"%self.label)
        NuFromWFromH_mass = getattr(event,"%sNuFromWFromH_mass"%self.label)
        nNuFromWFromT_lenpt = len(getattr(event, 'Hreco_NuFromWFromT_pt'))
        nNuFromWFromT = getattr(event, 'Hreco_nNuFromWFromT')
        NuFromWFromT_pt = getattr(event, 'Hreco_NuFromWFromT_pt')
        NuFromWFromT_eta = getattr(event, 'Hreco_NuFromWFromT_eta')
        NuFromWFromT_phi = getattr(event, 'Hreco_NuFromWFromT_phi')
        NuFromWFromT_mass = getattr(event, 'Hreco_NuFromWFromT_mass')
        GenJet_pt = getattr(event, "%sGenJet_pt"%self.label)
        GenJet_eta = getattr(event, "%sGenJet_eta"%self.label)
        GenJet_phi = getattr(event, "%sGenJet_phi"%self.label)
        GenJet_mass = getattr(event, "%sGenJet_mass"%self.label)
        #GenLep
        nGenLep = getattr(event, "%snGenLep"%self.label)
        GenLep_pt = getattr(event, "%sGenLep_pt"%self.label)
        GenLep_eta = getattr(event, "%sGenLep_eta"%self.label)
        GenLep_phi = getattr(event, "%sGenLep_phi"%self.label)
        GenLep_mass = getattr(event, "%sGenLep_mass"%self.label)
        
        # Temporary fix for very strange bug
        if event._entry == 0 : return False # !!! FIXME !!!
        self.out.fillBranch('%snLFromWFromH'%self.label,      nLFromWFromH)
        self.out.fillBranch('%snLFromWFromT'%self.label,      nLFromWFromT)
        self.out.fillBranch('%snQFromWFromH'%self.label,      nQFromWFromH)
        self.out.fillBranch('%snNuFromWFromH'%self.label,      nNuFromWFromH)
        self.out.fillBranch('%snNuFromWFromT_lenpt'%self.label, nNuFromWFromT_lenpt)
        self.out.fillBranch('%snNuFromWFromT'%self.label, nNuFromWFromT)
        self.out.fillBranch('%sLFromWFromH_pt'%self.label,    LFromWFromH_pt[0] if nLFromWFromH > 0 else -99)
        self.out.fillBranch('%sLFromWFromH_eta'%self.label,   LFromWFromH_eta[0] if nLFromWFromH > 0 else -99)
        self.out.fillBranch('%sLFromWFromH_phi'%self.label,   LFromWFromH_phi[0] if nLFromWFromH > 0 else -99)
        self.out.fillBranch('%sLFromWFromH_mass'%self.label,  LFromWFromH_mass[0] if nLFromWFromH > 0 else -99)
        self.out.fillBranch('%sLFromWFromT_pt'%self.label,    LFromWFromT_pt[0] if nLFromWFromT > 0 else -99)
        self.out.fillBranch('%sLFromWFromT_eta'%self.label,   LFromWFromT_eta[0] if nLFromWFromT > 0 else -99)
        self.out.fillBranch('%sLFromWFromT_phi'%self.label,   LFromWFromT_phi[0] if nLFromWFromT > 0 else -99)
        self.out.fillBranch('%sLFromWFromT_mass'%self.label,  LFromWFromT_mass[0] if nLFromWFromT > 0 else -99)
        self.out.fillBranch('%sQ1FromWFromH_pt'%self.label,   QFromWFromH_pt[0] if nQFromWFromH > 0 else -99)
        self.out.fillBranch('%sQ1FromWFromH_eta'%self.label,  QFromWFromH_eta[0] if nQFromWFromH > 0 else -99)
        self.out.fillBranch('%sQ1FromWFromH_phi'%self.label,  QFromWFromH_phi[0] if nQFromWFromH > 0 else -99)
        self.out.fillBranch('%sQ1FromWFromH_mass'%self.label, QFromWFromH_mass[0] if nQFromWFromH > 0 else -99)
        self.out.fillBranch('%sQ2FromWFromH_pt'%self.label,   QFromWFromH_pt[1] if nQFromWFromH > 1 else -99)
        self.out.fillBranch('%sQ2FromWFromH_eta'%self.label,  QFromWFromH_eta[1] if nQFromWFromH > 1 else -99)
        self.out.fillBranch('%sQ2FromWFromH_phi'%self.label,  QFromWFromH_phi[1] if nQFromWFromH > 1 else -99)
        self.out.fillBranch('%sQ2FromWFromH_mass'%self.label, QFromWFromH_mass[1] if nQFromWFromH > 1 else -99)
        self.out.fillBranch('%sNuFromWFromH_pt'%self.label,   NuFromWFromH_pt[0] if nNuFromWFromH > 0 else -99)
        self.out.fillBranch('%sNuFromWFromH_eta'%self.label,  NuFromWFromH_eta[0] if nNuFromWFromH > 0 else -99)
        self.out.fillBranch('%sNuFromWFromH_phi'%self.label,  NuFromWFromH_phi[0] if nNuFromWFromH > 0 else -99)
        self.out.fillBranch('%sNuFromWFromH_mass'%self.label, NuFromWFromH_mass[0] if nNuFromWFromH > 0 else -99)
        self.out.fillBranch('%sNuFromWFromT_pt'%self.label,   NuFromWFromT_pt[0] if nNuFromWFromT > 0 else -99)
        self.out.fillBranch('%sNuFromWFromT_eta'%self.label,  NuFromWFromT_eta[0] if nNuFromWFromT > 0 else -99)
        self.out.fillBranch('%sNuFromWFromT_phi'%self.label,  NuFromWFromT_phi[0] if nNuFromWFromT > 0 else -99)
        self.out.fillBranch('%sNuFromWFromT_mass'%self.label, NuFromWFromT_mass[0] if nNuFromWFromT > 0 else -99)


        gen_jets = []
        
        for gj in range(self.ngenjet):
            if GenJet_pt[gj] > 25:
                gen_jets.append([GenJet_pt[gj], GenJet_eta[gj], GenJet_phi[gj], GenJet_mass[gj]])
            #print "gen jet ", gj
            #print "gen jet pt", GenJet_pt[gj]

        sorted(gen_jets, reverse=True)
        for i in range(len(gen_jets)):
            #print "jet pt,  ", gen_jets[i][0]
            #print "jet phi, ", gen_jets[i][2]
            self.out.fillBranch('%sGenJet%s_pt'%(self.label,i), gen_jets[i][0] if i < len(gen_jets) else -99)
            self.out.fillBranch('%sGenJet%s_eta'%(self.label,i), gen_jets[i][1] if i < len(gen_jets) else -99)
            self.out.fillBranch('%sGenJet%s_phi'%(self.label,i), gen_jets[i][2] if i < len(gen_jets) else -99)
            self.out.fillBranch('%sGenJet%s_mass'%(self.label,i), gen_jets[i][3] if i < len(gen_jets) else -99)

        #sum gen jets
        q1 = TLorentzVector()
        q2 = TLorentzVector()
        if(len(QFromWFromH_pt) > 1):
            q1.SetPtEtaPhiM(QFromWFromH_pt[0], QFromWFromH_eta[0], QFromWFromH_phi[0], QFromWFromH_mass[0])
            q2.SetPtEtaPhiM(QFromWFromH_pt[1], QFromWFromH_eta[1], QFromWFromH_phi[1], QFromWFromH_mass[1])
            #print((q1+q2).Pt())
            self.out.fillBranch('%sgen_q1_q2_pt'%(self.label), (q1+q2).Pt())
            self.out.fillBranch('%sgen_q1_q2_eta'%(self.label), (q1+q2).Eta())
            self.out.fillBranch('%sgen_q1_q2_phi'%(self.label), (q1+q2).Phi())
            self.out.fillBranch('%sgen_q1_q2_mass'%(self.label), (q1+q2).M())

        else:
            self.out.fillBranch('%sgen_q1_q2_pt'%(self.label), -99)
            self.out.fillBranch('%sgen_q1_q2_eta'%(self.label), -99)
            self.out.fillBranch('%sgen_q1_q2_phi'%(self.label), -99)
            self.out.fillBranch('%sgen_q1_q2_mass'%(self.label), -99)

        if(nGenLep <= 2):
            for i in range(nGenLep):
                if(GenLep_pt[0] < 25 or GenLep_pt[1] < 15): continue
                self.out.fillBranch('%sGenLep%s_pt'%(self.label,i), GenLep_pt[i])
                self.out.fillBranch('%sGenLep%s_eta'%(self.label,i), GenLep_eta[i])
                self.out.fillBranch('%sGenLep%s_phi'%(self.label,i), GenLep_phi[i])
                self.out.fillBranch('%sGenLep%s_mass'%(self.label,i), GenLep_mass[i])


        # Enforce selection (non-jet part)
        if len(leps) < 2                      : return False
        if leps[0].pt < 25 or leps[1].pt < 15 : return False # pt2515
        if event.nLepTight_Recl > 2           : return False # exclusive
        if leps[0].pdgId*leps[1].pdgId < 0    : return False # same-sign
        if abs(event.mZ1_Recl-91.2)<10        : return False # Z_veto
        
        # Make sure we have prompt leptons
        if leps[0].genPartFlav != 1 and leps[0].genPartFlav != 15 : return False
        if leps[1].genPartFlav != 1 and leps[1].genPartFlav != 15 : return False
        
        # No final states with taus, for the moment
        if event.nTauSel_Recl_Tight > 0                           : return False

        (met, met_phi)  = event.MET_pt, event.MET_phi # what about propagation of JES to MET?

        for jesLabel in self.systsJEC.values():

            # Enforce selection (jets part)
            if not ((getattr(event,"nJet25%s_Recl"%jesLabel)>=3 and (getattr(event,"nBJetLoose25%s_Recl"%jesLabel)>= 2 or getattr(event,"nBJetMedium25%s_Recl"%jesLabel)>= 1)) or (getattr(event,"nBJetMedium25%s_Recl"%jesLabel) >= 1 and (getattr(event,"nJet25%s_Recl"%jesLabel)+getattr(event,"nFwdJet%s_Recl"%jesLabel)-getattr(event,"nBJetLoose25%s_Recl"%jesLabel)) > 0)) : continue

            # Build the jets
            jets = []
            for j in alljets:
                if alljets.index(j) in [int(getattr(event,"BDThttTT_eventReco_iJetSel1%s"%jesLabel)),int(getattr(event,"BDThttTT_eventReco_iJetSel2%s"%jesLabel)),int(getattr(event,"BDThttTT_eventReco_iJetSel3%s"%jesLabel))]:
                    setattr(j, 'fromHadTop', True)
                else:
                    setattr(j, 'fromHadTop', False)
                if j.pt < 25: continue
                #if j.btagDeepFlavB < btagvetoval: continue
                jets.append(j)

            # Store all jets
            jet_pts=[]; jet_etas=[]; jet_phis=[]; jet_masses=[]; jet_btagdiscrs=[]; jet_ishadtops=[]
            def my_sort(j):
                #return j.btagDeepFlavB
                return j.pt
            jets.sort(key=my_sort, reverse=True)
            #if(len(jets) > 5): continue
            for j in jets:
                jet_pts.append(j.pt)
                jet_etas.append(j.eta)
                jet_phis.append(j.phi)
                jet_masses.append(j.mass)
                jet_btagdiscrs.append( j.btagDeepFlavB > btagvetoval) 
                jet_ishadtops.append(j.fromHadTop)
            if(len(jets) < 2): return False
            if(len(jets) > 4):
                #for j in jets:
                self.out.fillBranch('%sJet_Higgs_score'%(self.label) , getattr(event, "BDThttTT_eventReco_Hj_score"))
            else:
                self.out.fillBranch('%sJet_Higgs_score'%(self.label) , -99)

            #closest to W
            if(len(jets) > 1):
                jet1_w = TLorentzVector()
                jet2_w = TLorentzVector()
                target_w = 999
                for i in range(len(jets)):
                    jet1_w.SetPtEtaPhiM(jets[i].p4().Pt(), jets[i].p4().Eta(), jets[i].p4().Phi(), jets[i].p4().M())
                    for j in range(i+1, len(jets)):
                        jet2_w.SetPtEtaPhiM(jets[j].p4().Pt(), jets[j].p4().Eta(), jets[j].p4().Phi(), jets[j].p4().M())
                        sum_jets = jet1_w+jet2_w
                        if(abs(sum_jets.M() - 80) < target_w):
                            target_w = sum_jets.M()
                            index1_w = i
                            index2_w = j
                self.out.fillBranch('%sreco_w_q1_q2_pt%s'%(self.label,jesLabel) , (jets[index1_w].p4()+jets[index2_w].p4()).Pt())
                self.out.fillBranch('%sreco_w_q1_q2_eta%s'%(self.label,jesLabel) , (jets[index1_w].p4()+jets[index2_w].p4()).Eta())
                self.out.fillBranch('%sreco_w_q1_q2_phi%s'%(self.label,jesLabel) , (jets[index1_w].p4()+jets[index2_w].p4()).Phi())
                self.out.fillBranch('%sreco_w_q1_q2_mass%s'%(self.label,jesLabel) , (jets[index1_w].p4()+jets[index2_w].p4()).M())
            else:
                self.out.fillBranch('%sreco_w_q1_q2_pt%s'%(self.label,jesLabel) , -99)
                self.out.fillBranch('%sreco_w_q1_q2_eta%s'%(self.label,jesLabel) , -99)
                self.out.fillBranch('%sreco_w_q1_q2_phi%s'%(self.label,jesLabel) , -99)
                self.out.fillBranch('%sreco_w_q1_q2_mass%s'%(self.label,jesLabel) , -99)
            #match dr jet per jet
            QFromWFromH_pt = getattr(event,"%sQFromWFromH_pt"%self.label)
            if(len(QFromWFromH_pt) > 1 and len(jets) > 1):
                jet1_dr = TLorentzVector()
                jet2_dr = TLorentzVector()
                target_dr2_real = 999.
                target_dr1_real = 999.
                index_dr_q1 = -1
                index_dr_q2 = -1
                for i in range(len(jets)):
                    jet1_dr.SetPtEtaPhiM(jets[i].p4().Pt(), jets[i].p4().Eta(), jets[i].p4().Phi(), jets[i].p4().M())
                    if(jet1_dr.DeltaR(q1) < target_dr1_real):
                        target_dr1_real = jet1_dr.DeltaR(q1)
                        index_dr_q1 = i

                for i in range(len(jets)):
                    if(i != index_dr_q1):
                        jet2_dr.SetPtEtaPhiM(jets[i].p4().Pt(), jets[i].p4().Eta(), jets[i].p4().Phi(), jets[i].p4().M())
                        if(jet2_dr.DeltaR(q2) < target_dr2_real):
                            target_dr2_real = jet2_dr.DeltaR(q2)
                            index_dr_q2 = i

                for i in range(len(jets)):
                    if(i == index_dr_q1 or i == index_dr_q2):
                        self.out.fillBranch('%sJet_Label_dr_real%s'%(self.label,jesLabel), 1)
                    else:
                        self.out.fillBranch('%sJet_Label_dr_real%s'%(self.label,jesLabel), 0)

                if(index_dr_q1 == -1): continue
                if(index_dr_q2 == -1): continue
                self.out.fillBranch('%sreco_match_real_q1_pt%s'%(self.label,jesLabel) , jets[index_dr_q1].p4().Pt())
                self.out.fillBranch('%sreco_match_real_q1_eta%s'%(self.label,jesLabel) , jets[index_dr_q1].p4().Eta())
                self.out.fillBranch('%sreco_match_real_q1_phi%s'%(self.label,jesLabel) , jets[index_dr_q1].p4().Phi())
                self.out.fillBranch('%sreco_match_real_q1_mass%s'%(self.label,jesLabel) , jets[index_dr_q1].p4().M())


                self.out.fillBranch('%sreco_match_real_q2_pt%s'%(self.label,jesLabel) , jets[index_dr_q2].p4().Pt())
                self.out.fillBranch('%sreco_match_real_q2_eta%s'%(self.label,jesLabel) , jets[index_dr_q2].p4().Eta())
                self.out.fillBranch('%sreco_match_real_q2_phi%s'%(self.label,jesLabel) , jets[index_dr_q2].p4().Phi())
                self.out.fillBranch('%sreco_match_real_q2_mass%s'%(self.label,jesLabel) , jets[index_dr_q2].p4().M())


                self.out.fillBranch('%sreco_match_real_q1_q2_pt%s'%(self.label,jesLabel) , (jets[index_dr_q1].p4()+jets[index_dr_q2].p4()).Pt())
                self.out.fillBranch('%sreco_match_real_q1_q2_eta%s'%(self.label,jesLabel) , (jets[index_dr_q1].p4()+jets[index_dr_q2].p4()).Eta())
                self.out.fillBranch('%sreco_match_real_q1_q2_phi%s'%(self.label,jesLabel) , (jets[index_dr_q1].p4()+jets[index_dr_q2].p4()).Phi())
                self.out.fillBranch('%sreco_match_real_q1_q2_mass%s'%(self.label,jesLabel) , (jets[index_dr_q1].p4()+jets[index_dr_q2].p4()).M())
            else:
                self.out.fillBranch('%sreco_match_real_q1_pt%s'%(self.label,jesLabel) , -99)
                self.out.fillBranch('%sreco_match_real_q1_eta%s'%(self.label,jesLabel) , -99)
                self.out.fillBranch('%sreco_match_real_q1_phi%s'%(self.label,jesLabel) , -99)
                self.out.fillBranch('%sreco_match_real_q1_mass%s'%(self.label,jesLabel) , -99)

                self.out.fillBranch('%sreco_match_real_q2_pt%s'%(self.label,jesLabel) , -99)
                self.out.fillBranch('%sreco_match_real_q2_eta%s'%(self.label,jesLabel) , -99)
                self.out.fillBranch('%sreco_match_real_q2_phi%s'%(self.label,jesLabel) , -99)
                self.out.fillBranch('%sreco_match_real_q2_mass%s'%(self.label,jesLabel) , -99)

                self.out.fillBranch('%sreco_match_real_q1_q2_pt%s'%(self.label,jesLabel) , -99)
                self.out.fillBranch('%sreco_match_real_q1_q2_eta%s'%(self.label,jesLabel) , -99)
                self.out.fillBranch('%sreco_match_real_q1_q2_phi%s'%(self.label,jesLabel) , -99)
                self.out.fillBranch('%sreco_match_real_q1_q2_mass%s'%(self.label,jesLabel) , -99)
                
                self.out.fillBranch('%sJet_Label_dr_real%s'%(self.label,jesLabel), -99)
            #closest sum to gen
            #QFromWFromH_pt = getattr(event,"%sQFromWFromH_pt"%self.label)
            if(len(QFromWFromH_pt) > 1 and len(jets) > 1):
                jet1 = TLorentzVector()
                jet2 = TLorentzVector()
                target = 999.
                target_dr = 999.
                index_1 = -1
                index_2 = -1
                index_dr_1 = -1
                index_dr_2 = -1
                for i in range(len(jets)):
                    jet1.SetPtEtaPhiM(jets[i].p4().Pt(), jets[i].p4().Eta(), jets[i].p4().Phi(), jets[i].p4().M())
                    for j in range(i+1,len(jets)):
                        jet2.SetPtEtaPhiM(jets[j].p4().Pt(), jets[j].p4().Eta(), jets[j].p4().Phi(), jets[j].p4().M())
                        sum_jets = jet1+jet2
                        if(abs(sum_jets.Pt() - (q1+q2).Pt()) < target):
                            target = abs(sum_jets.Pt() - (q1+q2).Pt())
                            index_1 = i
                            index_2 = j

                        if(sum_jets.DeltaR((q1+q2)) < target_dr):
                           target_dr = sum_jets.DeltaR((q1+q2))
                           index_dr_1 = i
                           index_dr_2 = j


                #fill branch
                if(index_1 == -1): continue
                if(index_2 == -1): continue
                if(index_dr_1 == -1): continue
                if(index_dr_2 == -1): continue
                #fill_pt = (jets[index_1]+jets[index_2]).p4().Pt()
                self.out.fillBranch('%sreco_q1_q2_pt%s'%(self.label,jesLabel) , (jets[index_1].p4()+jets[index_2].p4()).Pt())
                self.out.fillBranch('%sreco_q1_q2_eta%s'%(self.label,jesLabel) , (jets[index_1].p4()+jets[index_2].p4()).Eta())
                self.out.fillBranch('%sreco_q1_q2_phi%s'%(self.label,jesLabel) , (jets[index_1].p4()+jets[index_2].p4()).Phi())
                self.out.fillBranch('%sreco_q1_q2_mass%s'%(self.label,jesLabel) , (jets[index_1].p4()+jets[index_2].p4()).M())
                #self.out.fillBranch('%sreco_q1_q2_label%s'%(self.label,jesLabel) , [1,0])
                #self.out.fillBranch('%sreco_q1_q2_label_one%s'%(self.label,jesLabel) , 1)


                self.out.fillBranch('%sreco_match_q1_q2_pt%s'%(self.label,jesLabel) , (jets[index_dr_1].p4()+jets[index_dr_2].p4()).Pt())
                self.out.fillBranch('%sreco_match_q1_q2_eta%s'%(self.label,jesLabel) , (jets[index_dr_1].p4()+jets[index_dr_2].p4()).Eta())
                self.out.fillBranch('%sreco_match_q1_q2_phi%s'%(self.label,jesLabel) , (jets[index_dr_1].p4()+jets[index_dr_2].p4()).Phi())
                self.out.fillBranch('%sreco_match_q1_q2_mass%s'%(self.label,jesLabel) , (jets[index_dr_1].p4()+jets[index_dr_2].p4()).M())
                #self.out.fillBranch('%sreco_match_q1_q2_label%s'%(self.label,jesLabel) , [1,0])
                #self.out.fillBranch('%sreco_match_q1_q2_label_one%s'%(self.label,jesLabel) , 1)


                
                for i in range(len(jets)):
                    if(i == index_1 or i == index_2):
                        self.out.fillBranch('%sJet_Label%s'%(self.label,jesLabel), 1)
                    else:
                        self.out.fillBranch('%sJet_Label%s'%(self.label,jesLabel), 0)
                    
                    if(i == index_dr_1 or i == index_dr_2):
                        self.out.fillBranch('%sJet_Label_dr%s'%(self.label,jesLabel), 1)
                    else:
                        self.out.fillBranch('%sJet_Label_dr%s'%(self.label,jesLabel), 0)
                        
                    self.out.fillBranch('%sJet_Label_pt%s'%(self.label,jesLabel), jets[i].p4().Pt())
                    self.out.fillBranch('%sJet_Label_eta%s'%(self.label,jesLabel), jets[i].p4().Eta())
                    self.out.fillBranch('%sJet_Label_phi%s'%(self.label,jesLabel), jets[i].p4().Phi())
                    self.out.fillBranch('%sJet_Label_mass%s'%(self.label,jesLabel), jets[i].p4().M())
                    self.out.fillBranch('%sJet_Label_bdisc%s'%(self.label,jesLabel), jet_btagdiscrs[i])
                    self.out.fillBranch('%sJet_Label_dr_lep0%s'%(self.label,jesLabel), jets[i].p4().DeltaR(leps[0].p4()) if len(leps) > 0 else -99)
                    self.out.fillBranch('%sJet_Label_dr_lep1%s'%(self.label,jesLabel), jets[i].p4().DeltaR(leps[1].p4()) if len(leps) > 1 else -99)
                    

            else:
                self.out.fillBranch('%sreco_q1_q2_pt%s'%(self.label,jesLabel) , -99)
                self.out.fillBranch('%sreco_q1_q2_eta%s'%(self.label,jesLabel) , -99)
                self.out.fillBranch('%sreco_q1_q2_phi%s'%(self.label,jesLabel) , -99)
                self.out.fillBranch('%sreco_q1_q2_mass%s'%(self.label,jesLabel) , -99)
                #self.out.fillBranch('%sreco_q1_q2_label%s'%(self.label,jesLabel) , [0,1])
                #self.out.fillBranch('%sreco_q1_q2_label_one%s'%(self.label,jesLabel) , 0)

                self.out.fillBranch('%sreco_match_q1_q2_pt%s'%(self.label,jesLabel) , -99)
                self.out.fillBranch('%sreco_match_q1_q2_eta%s'%(self.label,jesLabel) , -99)
                self.out.fillBranch('%sreco_match_q1_q2_phi%s'%(self.label,jesLabel) , -99)
                self.out.fillBranch('%sreco_match_q1_q2_mass%s'%(self.label,jesLabel) , -99)
                #self.out.fillBranch('%sreco_match_q1_q2_label%s'%(self.label,jesLabel) , [0,1]) 
                #self.out.fillBranch('%sreco_match_q1_q2_label_one%s'%(self.label,jesLabel) , 0)
                self.out.fillBranch('%sJet_Label%s'%(self.label,jesLabel), -99)
                self.out.fillBranch('%sJet_Label_dr%s'%(self.label,jesLabel), -99)

            for i in range(len(jets)):
                ###########MODEL###########
                
                score = float(self.model_dnn.predict(np.transpose(np.array([[jets[i].p4().Pt()], [jets[i].p4().Eta()], [jets[i].p4().Phi()], [jets[i].p4().M()], [met], [jets[i].p4().DeltaR(leps[0].p4())], [jets[i].p4().DeltaR(leps[1].p4())]]))))#[jets[i].p4().DeltaR(leps[0].p4())], [jets[i].p4().DeltaR(leps[1].p4())]]))))
                self.out.fillBranch('%sreco_score_higgs%s'%(self.label,jesLabel), score)

            def my_sort_score(j):
            #return j.btagDeepFlavB
                #print float(self.model_dnn.predict(np.transpose(np.array([j.pt], [j.eta], [j.phi], [j.mass], [met], [100.], [100.]]))))
                return float(self.model_dnn.predict(np.transpose(np.array([[j.pt], [j.eta], [j.phi], [j.mass], [met], [j.DeltaR(leps[0].p4())], [j.DeltaR(leps[1].p4())]]))))

            jets.sort(key=my_sort_score, reverse=True)
            #print len(jets)
            for i in range(len(jets)):
                ###########MODEL###########

                score = float(self.model_dnn.predict(np.transpose(np.array([[jets[i].p4().Pt()], [jets[i].p4().Eta()], [jets[i].p4().Phi()], [jets[i].p4().M()], [met], [jets[i].p4().DeltaR(leps[0].p4())], [jets[i].p4().DeltaR(leps[1].p4())]]))))
                #print score
                self.out.fillBranch('%sreco_score_higgs%s'%(self.label,jesLabel), score)


            if(len(jets) >= 2):
                self.out.fillBranch('%sreco_q1_score_higgs_pt%s'%(self.label,jesLabel), jets[0].p4().Pt())
                self.out.fillBranch('%sreco_q1_score_higgs_eta%s'%(self.label,jesLabel), jets[0].p4().Eta())
                self.out.fillBranch('%sreco_q1_score_higgs_phi%s'%(self.label,jesLabel), jets[0].p4().Phi())
                self.out.fillBranch('%sreco_q1_score_higgs_mass%s'%(self.label,jesLabel), jets[0].p4().M())

                self.out.fillBranch('%sreco_q2_score_higgs_pt%s'%(self.label,jesLabel), jets[1].p4().Pt())
                self.out.fillBranch('%sreco_q2_score_higgs_eta%s'%(self.label,jesLabel), jets[1].p4().Eta())
                self.out.fillBranch('%sreco_q2_score_higgs_phi%s'%(self.label,jesLabel), jets[1].p4().Phi())
                self.out.fillBranch('%sreco_q2_score_higgs_mass%s'%(self.label,jesLabel), jets[1].p4().M())

                self.out.fillBranch('%sreco_q1_q2_score_higgs_pt%s'%(self.label,jesLabel), (jets[0].p4()+jets[1].p4()).Pt())
                self.out.fillBranch('%sreco_q1_q2_score_higgs_eta%s'%(self.label,jesLabel), (jets[0].p4()+jets[1].p4()).Eta())
                self.out.fillBranch('%sreco_q1_q2_score_higgs_phi%s'%(self.label,jesLabel), (jets[0].p4()+jets[1].p4()).Phi())
                self.out.fillBranch('%sreco_q1_q2_score_higgs_mass%s'%(self.label,jesLabel), (jets[0].p4()+jets[1].p4()).M())

            else:
                self.out.fillBranch('%sreco_q1_score_higgs_pt%s'%(self.label,jesLabel), -99)
                self.out.fillBranch('%sreco_q1_score_higgs_eta%s'%(self.label,jesLabel), -99)
                self.out.fillBranch('%sreco_q1_score_higgs_phi%s'%(self.label,jesLabel), -99)
                self.out.fillBranch('%sreco_q1_score_higgs_mass%s'%(self.label,jesLabel), -99)
                
                self.out.fillBranch('%sreco_q2_score_higgs_pt%s'%(self.label,jesLabel),-99)
                self.out.fillBranch('%sreco_q2_score_higgs_eta%s'%(self.label,jesLabel), -99)
                self.out.fillBranch('%sreco_q2_score_higgs_phi%s'%(self.label,jesLabel), -99)
                self.out.fillBranch('%sreco_q2_score_higgs_mass%s'%(self.label,jesLabel), -99)

                self.out.fillBranch('%sreco_q1_q2_score_higgs_pt%s'%(self.label,jesLabel),-99)
                self.out.fillBranch('%sreco_q1_q2_score_higgs_eta%s'%(self.label,jesLabel), -99)
                self.out.fillBranch('%sreco_q1_q2_score_higgs_phi%s'%(self.label,jesLabel), -99)
                self.out.fillBranch('%sreco_q1_q2_score_higgs_mass%s'%(self.label,jesLabel), -99)
                #self.out.fillBranch('%sreco_score_higgs',%(self.label,jesLabel), self.model_dnn.predict(np.transpose(np.array([jets[i].p4().Pt(), jets[i].p4().Eta(), jets[i].p4().Phi(), jets[i].p4().M(), met, jets[i].p4().DeltaR(leps[0].p4()), jets[i].p4().DeltaR(leps[1].p4())]))))

                
                
            all5_jets = TLorentzVector()
            all5_jets.SetPtEtaPhiM(0,0,0,0)

            #all_jet_feature.sort()
            self.out.fillBranch('%snJets%s'%(self.label,jesLabel)        , len(jets))
            for i in range(self.njet):
                #part = jet_btagdiscrs[i]
                #self.out.fillBranch('%snJets%s'%(self.label,i,jesLabel)        , len(jets))  
                #if i<len(jets) else None

                if(i < len(jets)): all5_jets = all5_jets + jets[i].p4()


                self.out.fillBranch('%sJet%s%s_pt'%(self.label,i,jesLabel)       , jet_pts[i] if i < len(jets) and jet_ishadtops[i] is True else -99)
                self.out.fillBranch('%sJet%s%s_eta'%(self.label,i,jesLabel)      , jet_etas[i] if i < len(jets) and jet_ishadtops[i] is True else -99)
                self.out.fillBranch('%sJet%s%s_phi'%(self.label,i,jesLabel)      , jet_phis[i] if i < len(jets) and jet_ishadtops[i] is True else -99) 
                self.out.fillBranch('%sJet%s%s_mass'%(self.label,i,jesLabel)     , jet_masses[i] if i < len(jets) and jet_ishadtops[i] is True else -99)
                self.out.fillBranch('%sJet%s%s_btagdiscr'%(self.label,i,jesLabel), jet_btagdiscrs[i] if i < len(jets) and jet_ishadtops[i] is True else -99)
                self.out.fillBranch('%sJet%s%s_ishadtop'%(self.label,i,jesLabel) , jet_ishadtops[i] if i < len(jets) and jet_ishadtops[i] is True else -99) 

            self.out.fillBranch('%sAll5_Jets_pt'%(self.label), all5_jets.Pt())
            self.out.fillBranch('%sAll5_Jets_eta'%(self.label), all5_jets.Eta())
            self.out.fillBranch('%sAll5_Jets_phi'%(self.label), all5_jets.Phi())
            self.out.fillBranch('%sAll5_Jets_mass'%(self.label), all5_jets.M())


            score = getattr(event,"BDThttTT_eventReco_mvaValue%s"%jesLabel)
            
            HadTop = self.buildHadronicTop(event, score, alljets, jesLabel)

            self.out.fillBranch('%sHadTop%s_pt'  %(self.label,jesLabel), HadTop.Pt()  if HadTop else -99.)
            self.out.fillBranch('%sHadTop%s_eta' %(self.label,jesLabel), HadTop.Eta() if HadTop else -99.)
            self.out.fillBranch('%sHadTop%s_phi' %(self.label,jesLabel), HadTop.Phi() if HadTop else -99.)
            self.out.fillBranch('%sHadTop%s_mass'%(self.label,jesLabel), HadTop.M()   if HadTop else -99.)
            self.out.fillBranch('%sTopScore%s'   %(self.label,jesLabel), score                           ) # by not filling it with -99, a network should be able to learn self.cut_BDT_rTT_score

            # Lepton observables
            self.out.fillBranch('%snLeps%s' %(self.label,jesLabel), len(leps))
            self.out.fillBranch('%sevt_tag%s'%(self.label,jesLabel), leps[0].pdgId*leps[1].pdgId)
            self.out.fillBranch('%sDeltaRl0l1%s' %(self.label,jesLabel), leps[0].p4().DeltaR(leps[1].p4()) if len(leps)>=2 else -99.)

            for iLep in range(self.nlep):
                part = leps[iLep].p4()
                self.out.fillBranch('%sLep%s%s_pt'  %(self.label,iLep,jesLabel), part.Pt()  )
                self.out.fillBranch('%sLep%s%s_eta' %(self.label,iLep,jesLabel), part.Eta() )
                self.out.fillBranch('%sLep%s%s_phi' %(self.label,iLep,jesLabel), part.Phi() )
                self.out.fillBranch('%sLep%s%s_mass'%(self.label,iLep,jesLabel), part.M()   )
            
            #Compute met from events
            all_jets = TLorentzVector()
            all_jets.SetPtEtaPhiM(0,0,0,0)
            for j in range(len(jets)):
                all_jets = all_jets + jets[j].p4()
            
            for l in range(len(leps)):
                all_jets=all_jets + leps[l].p4()

            self.out.fillBranch('%sJets_plus_Lep_pt'%(self.label), all_jets.Pt()   )
            self.out.fillBranch('%sJets_plus_Lep_eta'%(self.label), all_jets.Eta()   )
            self.out.fillBranch('%sJets_plus_Lep_phi'%(self.label), all_jets.Phi()   )
            self.out.fillBranch('%sJets_plus_Lep_mass'%(self.label), all_jets.M()   )
            

            #Compute met from events
            if(len(jets) > self.njet):
                more5_jets = TLorentzVector()
                more5_jets.SetPtEtaPhiM(0,0,0,0)
                for j in range(self.njet, len(jets)):
                    more5_jets = more5_jets + jets[j].p4()

                self.out.fillBranch('%sMore5_Jets_pt'%(self.label), more5_jets.Pt() if(len(jets)) >=self.njet else -10   )
                self.out.fillBranch('%sMore5_Jets_eta'%(self.label), more5_jets.Eta() if(len(jets)) >=self.njet else -10  )
                self.out.fillBranch('%sMore5_Jets_phi'%(self.label), more5_jets.Phi() if(len(jets)) >=self.njet else -10  )
                self.out.fillBranch('%sMore5_Jets_mass'%(self.label), more5_jets.M() if(len(jets)) >=self.njet else -10  )
            

            met_calc = TLorentzVector()
            met_calc.SetPtEtaPhiM(met,-all_jets.Eta(),met_phi,0)

            self.out.fillBranch('%sMet_calc_pt'%(self.label), met_calc.Pt()   )
            self.out.fillBranch('%sMet_calc_eta'%(self.label), met_calc.Eta()   )
            self.out.fillBranch('%sMet_calc_phi'%(self.label), met_calc.Phi()   )
            self.out.fillBranch('%sMet_calc_mass'%(self.label), met_calc.M()   )

            # Compute the deltaR and pt of the closest jet to each lepton
            deltaR_closestJet = [999.,999.]
            deltaPt_closestJet = [999.,999.]
            lep_closestJet = []

            for iLep in range(self.nlep):
                lp4=leps[iLep].p4()
                for j, jp4 in [(ix,x.p4()) for ix,x in enumerate(jets)]:
                    dr_lj = lp4.DeltaR(jp4)
                    dpt_lj = lp4.Pt()-jp4.Pt()

                    if dr_lj < deltaR_closestJet:
                        deltaR_closestJet[iLep] = dr_lj
                        deltaPt_closestJet[iLep] = dpt_lj
                        lep_closestJet.append(lp4+jp4)

            #print(len(lep_closestJet))
            #if(len(lep_closestJet) == 0): print 'cacca ', deltaR_closestJet[0], deltaR_closestJet[1]
            for iLep in range(self.nlep): 
                self.out.fillBranch('%sDeltaRClosestJetToLep%s%s'%(self.label,iLep,jesLabel) ,  deltaR_closestJet[iLep])
                self.out.fillBranch('%sDeltaPtClosestJetToLep%s%s'%(self.label,iLep,jesLabel) , deltaPt_closestJet[iLep])
                self.out.fillBranch('%sClosestJetToLep_pt%s%s'%(self.label,iLep,jesLabel) , lep_closestJet[iLep].Pt() if iLep < len(lep_closestJet) else -99)            # Fill MET and GEN observables        
                self.out.fillBranch('%sClosestJetToLep_eta%s%s'%(self.label,iLep,jesLabel) , lep_closestJet[iLep].Eta() if iLep < len(lep_closestJet) else -99)
                self.out.fillBranch('%sClosestJetToLep_phi%s%s'%(self.label,iLep,jesLabel) , lep_closestJet[iLep].Phi() if iLep < len(lep_closestJet) else -99)
                self.out.fillBranch('%sClosestJetToLep_mass%s%s'%(self.label,iLep,jesLabel) , lep_closestJet[iLep].M() if iLep < len(lep_closestJet) else -99)

            self.out.fillBranch('%smet%s'     %(self.label,jesLabel), met                                ) 
            self.out.fillBranch('%smet_phi%s' %(self.label,jesLabel), met_phi                            )
            self.out.fillBranch('%sHTXS_Higgs_pt%s'%(self.label,jesLabel), getattr(event,"HTXS_Higgs_pt"))
            self.out.fillBranch('%sHTXS_Higgs_y%s' %(self.label,jesLabel), getattr(event,"HTXS_Higgs_y") )

            # I must patch these two to fill only for TTH, otherwise the friend does not exist etc. Maybe produce friend also for background
            self.out.fillBranch('%sHgen_vis_pt%s'  %(self.label,jesLabel), getattr(event,'Hreco_pTTrueGen'))
            self.out.fillBranch('%sHgen_tru_pt%s'  %(self.label,jesLabel), getattr(event,'Hreco_pTTrueGenPlusNu')) # the same as HTXS_Higgs_pt

        return True

higgsDiffRegressionTTH_new = lambda : HiggsDiffRegressionTTH_new(label='Hreco_',
                                                         btagDeepCSVveto = 'M')
