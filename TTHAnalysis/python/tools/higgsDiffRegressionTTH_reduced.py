from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from PhysicsTools.Heppy.physicsobjects.Jet import _btagWPs as HiggsRecoTTHbtagwps

import ROOT, itertools
from ROOT import *
import numpy as np
import math
import os

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

class HiggsDiffRegressionTTH_reduced(Module):
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

            self.out.branch('%sJet_Higgs_score%s'%(self.label,jesLabel), 'F')
            self.out.branch('%sreco_score_higgs%s'%(self.label,jesLabel), 'F')

            self.out.branch('%sreco_q1_score_higgs_pt%s'%(self.label,jesLabel), 'F')
            self.out.branch('%sreco_q1_score_higgs_eta%s'%(self.label,jesLabel), 'F')
            self.out.branch('%sreco_q1_score_higgs_phi%s'%(self.label,jesLabel), 'F')
            self.out.branch('%sreco_q1_score_higgs_mass%s'%(self.label,jesLabel), 'F')

            self.out.branch('%sreco_q2_score_higgs_pt%s'%(self.label,jesLabel), 'F')
            self.out.branch('%sreco_q2_score_higgs_eta%s'%(self.label,jesLabel), 'F')
            self.out.branch('%sreco_q2_score_higgs_phi%s'%(self.label,jesLabel), 'F')
            self.out.branch('%sreco_q2_score_higgs_mass%s'%(self.label,jesLabel), 'F')

            self.out.branch('%sreco_q1_q2_score_higgs_pt%s'%(self.label,jesLabel), 'F')
            self.out.branch('%sreco_q1_q2_score_higgs_eta%s'%(self.label,jesLabel), 'F')
            self.out.branch('%sreco_q1_q2_score_higgs_phi%s'%(self.label,jesLabel), 'F')
            self.out.branch('%sreco_q1_q2_score_higgs_mass%s'%(self.label,jesLabel), 'F')

            self.out.branch('%sMore5_Jets_pt%s'%(self.label,jesLabel), 'F'   )
            self.out.branch('%sMore5_Jets_eta%s'%(self.label,jesLabel), 'F'   )
            self.out.branch('%sMore5_Jets_phi%s'%(self.label,jesLabel), 'F'   )
            self.out.branch('%sMore5_Jets_mass%s'%(self.label,jesLabel), 'F'   )

            self.out.branch('%sAll5_Jets_pt%s'%(self.label,jesLabel), 'F'   )
            self.out.branch('%sAll5_Jets_eta%s'%(self.label,jesLabel), 'F'   )
            self.out.branch('%sAll5_Jets_phi%s'%(self.label,jesLabel), 'F'   )
            self.out.branch('%sAll5_Jets_mass%s'%(self.label,jesLabel), 'F'   )


            self.out.branch('%sJets_plus_Lep_pt%s'%(self.label,jesLabel), 'F'   )
            self.out.branch('%sJets_plus_Lep_eta%s'%(self.label,jesLabel), 'F'   )
            self.out.branch('%sJets_plus_Lep_phi%s'%(self.label,jesLabel), 'F'   )
            self.out.branch('%sJets_plus_Lep_mass%s'%(self.label,jesLabel), 'F'   )

            self.out.branch('%sevt_tag%s'%(self.label,jesLabel)       , 'F')       
            
            # Gen level, the labels
            self.out.branch('%sHTXS_Higgs_pt'%(self.label) , 'F')
            self.out.branch('%sHTXS_Higgs_y'%(self.label)  , 'F')
            self.out.branch('%sHgen_vis_pt'%(self.label)   , 'F')
            self.out.branch('%sHgen_tru_pt'%(self.label)   , 'F')

            
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
        
        # Temporary fix for very strange bug
        if event._entry == 0 : return False # !!! FIXME !!!
            #print "gen jet pt", GenJet_pt[gj]

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
                self.out.fillBranch('%sJet_Higgs_score%s'%(self.label,jesLabel) , getattr(event, "BDThttTT_eventReco_Hj_score"))
            else:
                self.out.fillBranch('%sJet_Higgs_score%s'%(self.label,jesLabel) , -99)


            for i in range(len(jets)):
                ###########MODEL###########
                
                score = float(self.model_dnn.predict(np.transpose(np.array([[jets[i].p4().Pt()], [jets[i].p4().Eta()], [jets[i].p4().Phi()], [jets[i].p4().M()], [met], [jets[i].p4().DeltaR(leps[0].p4())], [jets[i].p4().DeltaR(leps[1].p4())]]))))#[jets[i].p4().DeltaR(leps[0].p4())], [jets[i].p4().DeltaR(leps[1].p4())]]))))
                self.out.fillBranch('%sreco_score_higgs%s'%(self.label,jesLabel), score)

            def my_sort_score(j):
                return float(self.model_dnn.predict(np.transpose(np.array([[j.pt], [j.eta], [j.phi], [j.mass], [met], [j.DeltaR(leps[0].p4())], [j.DeltaR(leps[1].p4())]]))))

            jets.sort(key=my_sort_score, reverse=True)

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
                
            all5_jets = TLorentzVector()
            all5_jets.SetPtEtaPhiM(0,0,0,0)

            #all_jet_feature.sort()
            self.out.fillBranch('%snJets%s'%(self.label,jesLabel)        , len(jets))
            for i in range(self.njet):

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
            

            self.out.fillBranch('%smet%s'     %(self.label,jesLabel), met                                ) 
            self.out.fillBranch('%smet_phi%s' %(self.label,jesLabel), met_phi                            )
            self.out.fillBranch('%sHTXS_Higgs_pt'%(self.label), getattr(event,"HTXS_Higgs_pt"))
            self.out.fillBranch('%sHTXS_Higgs_y' %(self.label), getattr(event,"HTXS_Higgs_y") )

            # I must patch these two to fill only for TTH, otherwise the friend does not exist etc. Maybe produce friend also for background
            #self.out.fillBranch('%sHgen_vis_pt%s'  %(self.label,jesLabel), getattr(event,'Hreco_pTTrueGen'))
            #self.out.fillBranch('%sHgen_tru_pt%s'  %(self.label,jesLabel), getattr(event,'Hreco_pTTrueGenPlusNu')) # the same as HTXS_Higgs_pt

        return True

higgsDiffRegressionTTH_reduced = lambda : HiggsDiffRegressionTTH_reduced(label='Hreco_',
                                                         btagDeepCSVveto = 'M')
