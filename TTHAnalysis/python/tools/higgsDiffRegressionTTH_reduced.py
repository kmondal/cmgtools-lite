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
import tensorflow as tf

import h5py

from keras import optimizers
from keras.models import load_model

class HiggsDiffRegressionTTH_reduced(Module):
    def __init__(self,label="_Recl", variations=[], cut_BDT_rTT_score = 0.0, btagDeepCSVveto = 'M', doSystJEC=True):
        def loss_MSEDeltaVar(y_true, y_pred):
            y_true = tf.cast(y_true,tf.float32)
            y_pred = tf.cast(y_pred,tf.float32)
            y_true_mean = tf.reduce_mean(y_true)
            y_pred_mean = tf.reduce_mean(y_pred)
            base = tf.reduce_mean((y_true-y_pred)**2)
            var_true = tf.reduce_mean((y_true-y_true_mean)**2)
            var_pred = tf.reduce_mean((y_pred-y_pred_mean)**2)
            var_diff = abs(var_true - var_pred)
            val = base*var_diff
            return val
        #self.genpar = Collection(event,"GenPart","nGenPart")
             
        #print self.genpar
        self.label = label
        self.cut_BDT_rTT_score = cut_BDT_rTT_score
        self.btagDeepCSVveto = btagDeepCSVveto
        self.branches = []
        self.systsJEC = {0:"", 1:"_jesTotalCorrUp", -1:"_jesTotalCorrDown", 2:"_jesTotalUnCorrUp", -2:"_jesTotalUnCorrDown"} if doSystJEC else {0:""}
        if(doSystJEC is True):
            if len(variations):
                self.systsJEC = {0:""}
                for i,var in enumerate(variations):
                    self.systsJEC[i+1]   ="_%sUp"%var
                    self.systsJEC[-(i+1)]="_%sDown"%var
        else: self.systsJEC = {0:""}
        self.nlep = 2
        self.njet = 5
        self.ngenjet = 8
        self.model_dnn = load_model(os.path.join(os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/data/regressionMVA/dnn_tagger_new_dr_real.h5"))
        self.model_regression = load_model(os.path.join(os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/data/regressionMVA/dnn_trained_2lss.h5"), custom_objects={'loss_MSEDeltaVar': loss_MSEDeltaVar})#os.p\


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
            self.out.branch('%sdnn_prediction%s'%(self.label, jesLabel)   , 'F')    
            # Gen level, the labels
            self.out.branch('%sHTXS_Higgs_pt'%(self.label) , 'F')
            self.out.branch('%sHTXS_Higgs_y'%(self.label)  , 'F')
            self.out.branch('%sHgen_vis_pt'%(self.label)   , 'F')
            self.out.branch('%sHgen_tru_pt'%(self.label)   , 'F')

    def setDefault(self, event, jesLabel):
        # Counters
        self.out.fillBranch('%snLeps%s'%(self.label,jesLabel), -99)
        self.out.fillBranch('%snJets%s'%(self.label,jesLabel), -99)
        #self.out.fillBranch('%sdnn_prediction%s'%(self.label, jesLabel)   , -1)        

        # Leptons and the precomputed hadronic top
        for suffix in ["_pt", "_eta", "_phi", "_mass"]:
            for iLep in range(self.nlep):
                self.out.fillBranch('%sLep%s%s%s'%(self.label,iLep,jesLabel,suffix)   , -99.)
            self.out.fillBranch('%sHadTop%s%s'%(self.label,jesLabel,suffix), -99.)
        
        # Jets
        for suffix in ["_pt", "_eta", "_phi", "_mass", "_btagdiscr", "_ishadtop"]:
            for iJet in range(self.njet):
                self.out.fillBranch('%sJet%s%s%s'%(self.label,iJet,jesLabel,suffix)   , -99.)
        
        self.out.fillBranch('%sTopScore%s'%(self.label,jesLabel)      , -99.)
        self.out.fillBranch('%smet%s'%(self.label,jesLabel)           , -99.)
        self.out.fillBranch('%smet_phi%s'%(self.label,jesLabel)       , -99.)
    
        self.out.fillBranch('%sJet_Higgs_score%s'%(self.label,jesLabel), -99.)
        self.out.fillBranch('%sreco_score_higgs%s'%(self.label,jesLabel), -99.)
        
        self.out.fillBranch('%sreco_q1_score_higgs_pt%s'%(self.label,jesLabel), -99.)
        self.out.fillBranch('%sreco_q1_score_higgs_eta%s'%(self.label,jesLabel), -99.)
        self.out.fillBranch('%sreco_q1_score_higgs_phi%s'%(self.label,jesLabel), -99.)
        self.out.fillBranch('%sreco_q1_score_higgs_mass%s'%(self.label,jesLabel), -99.)

        self.out.fillBranch('%sreco_q2_score_higgs_pt%s'%(self.label,jesLabel), -99.)
        self.out.fillBranch('%sreco_q2_score_higgs_eta%s'%(self.label,jesLabel), -99.)
        self.out.fillBranch('%sreco_q2_score_higgs_phi%s'%(self.label,jesLabel), -99.)
        self.out.fillBranch('%sreco_q2_score_higgs_mass%s'%(self.label,jesLabel), -99.)
        
        self.out.fillBranch('%sreco_q1_q2_score_higgs_pt%s'%(self.label,jesLabel), -99.)
        self.out.fillBranch('%sreco_q1_q2_score_higgs_eta%s'%(self.label,jesLabel), -99.)
        self.out.fillBranch('%sreco_q1_q2_score_higgs_phi%s'%(self.label,jesLabel), -99.)
        self.out.fillBranch('%sreco_q1_q2_score_higgs_mass%s'%(self.label,jesLabel), -99.)

        self.out.fillBranch('%sMore5_Jets_pt%s'%(self.label,jesLabel), -99.)
        self.out.fillBranch('%sMore5_Jets_eta%s'%(self.label,jesLabel), -99.)
        self.out.fillBranch('%sMore5_Jets_phi%s'%(self.label,jesLabel), -99.)
        self.out.fillBranch('%sMore5_Jets_mass%s'%(self.label,jesLabel), -99.)

        self.out.fillBranch('%sAll5_Jets_pt%s'%(self.label,jesLabel), -99.)
        self.out.fillBranch('%sAll5_Jets_eta%s'%(self.label,jesLabel), -99.)
        self.out.fillBranch('%sAll5_Jets_phi%s'%(self.label,jesLabel), -99.)
        self.out.fillBranch('%sAll5_Jets_mass%s'%(self.label,jesLabel), -99.)

        self.out.fillBranch('%sJets_plus_Lep_pt%s'%(self.label,jesLabel), -99.)
        self.out.fillBranch('%sJets_plus_Lep_eta%s'%(self.label,jesLabel), -99.)
        self.out.fillBranch('%sJets_plus_Lep_phi%s'%(self.label,jesLabel), -99.)
        self.out.fillBranch('%sJets_plus_Lep_mass%s'%(self.label,jesLabel), -99.)

        self.out.fillBranch('%sevt_tag%s'%(self.label,jesLabel)       , -99.)
        self.out.fillBranch('%sdnn_prediction%s'%(self.label, jesLabel)   , -99.)
        # Gen level, the labels
        self.out.fillBranch('%sHTXS_Higgs_pt'%(self.label) , -99.)
        self.out.fillBranch('%sHTXS_Higgs_y'%(self.label)  , -99.)
        self.out.fillBranch('%sHgen_vis_pt'%(self.label)   , -99.)
        self.out.fillBranch('%sHgen_tru_pt'%(self.label)   , -99.)
            
    def buildHadronicTop(self, event, score, alljets, jesLabel):
        HadTop=None
        if score>self.cut_BDT_rTT_score:
            j1top = int(getattr(event,"BDThttTT_eventReco_iJetSel1%s"%jesLabel))
            j2top = int(getattr(event,"BDThttTT_eventReco_iJetSel2%s"%jesLabel))
            j3top = int(getattr(event,"BDThttTT_eventReco_iJetSel3%s"%jesLabel))
            # Build hadronic top
            top1 = ROOT.TLorentzVector(); top1.SetPtEtaPhiM(getattr(alljets[j1top], "pt%s"%jesLabel),alljets[j1top].p4().Eta(), alljets[j1top].p4().Phi(), alljets[j1top].p4().M())
            top2 = ROOT.TLorentzVector(); top2.SetPtEtaPhiM(getattr(alljets[j2top], "pt%s"%jesLabel),alljets[j2top].p4().Eta(), alljets[j2top].p4().Phi(), alljets[j2top].p4().M())
            top3 = ROOT.TLorentzVector(); top3.SetPtEtaPhiM(getattr(alljets[j3top], "pt%s"%jesLabel),alljets[j3top].p4().Eta(), alljets[j3top].p4().Phi(), alljets[j3top].p4().M())
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

        try:
            #genpar = Collection(event,"GenPartFlav","nGenPartFlav")
            gen = leps[0].genPartFlav
            isData = False
        except:
            isData = True
        
        if(isData): self.systsJEC = {0:""}

        #print isData
        #if(isData == True): self.systsJEC = {0:""}

        #print genpart
        # Temporary fix for very strange bug
        #if event._entry == 0 : return False # !!! FIXME !!!
            #print "gen jet pt", GenJet_pt[gj]

        # Enforce selection (non-jet part)
        #if len(leps) < 2                      : return False
        #if leps[0].pt < 25 or leps[1].pt < 15 : return False # pt2515
        #if event.nLepTight_Recl > 2           : return False # exclusive
        #if leps[0].pdgId*leps[1].pdgId < 0    : return False # same-sign
        #if abs(event.mZ1_Recl-91.2)<10        : return False # Z_veto
        
        # Make sure we have prompt leptons
        #if leps[0].genPartFlav != 1 and leps[0].genPartFlav != 15 : return False
        #if leps[1].genPartFlav != 1 and leps[1].genPartFlav != 15 : return False
        
        # No final states with taus, for the moment
        #if event.nTauSel_Recl_Tight > 0                           : return False

        (met, met_phi)  = event.MET_pt, event.MET_phi # what about propagation of JES to MET?

        for jesLabel in self.systsJEC.values():


            # Temporary fix for very strange bug
            if event._entry == 0 : 
                self.setDefault(event, jesLabel)
                continue# !!! FIXME !!!
            #print "gen jet pt", GenJet_pt[gj]

            # Enforce selection (non-jet part)
            if len(leps) < 2                      : 
                self.setDefault(event, jesLabel)
                continue
            if leps[0].pt < 25 or leps[1].pt < 15 : 
                self.setDefault(event, jesLabel)
                continue
            if event.nLepTight_Recl > 2           :
                self.setDefault(event, jesLabel)
                continue
            if leps[0].pdgId*leps[1].pdgId < 0    : 
                self.setDefault(event, jesLabel)
                continue
            if abs(event.mZ1_Recl-91.2)<10        : 
                self.setDefault(event, jesLabel)
                continue

            if event.nTauSel_Recl_Tight > 0                           :
                self.setDefault(event, jesLabel)
                continue

            # Enforce selection (jets part)
            if not ((getattr(event,"nJet25%s_Recl"%jesLabel)>=3 and (getattr(event,"nBJetLoose25%s_Recl"%jesLabel)>= 2 or getattr(event,"nBJetMedium25%s_Recl"%jesLabel)>= 1)) or (getattr(event,"nBJetMedium25%s_Recl"%jesLabel) >= 1 and (getattr(event,"nJet25%s_Recl"%jesLabel)+getattr(event,"nFwdJet%s_Recl"%jesLabel)-getattr(event,"nBJetLoose25%s_Recl"%jesLabel)) > 0)) : 
                self.setDefault(event, jesLabel)
                continue

            # Build the jets
            jets = []
            for j in alljets:
                if alljets.index(j) in [int(getattr(event,"BDThttTT_eventReco_iJetSel1%s"%jesLabel)),int(getattr(event,"BDThttTT_eventReco_iJetSel2%s"%jesLabel)),int(getattr(event,"BDThttTT_eventReco_iJetSel3%s"%jesLabel))]:
                    setattr(j, 'fromHadTop', True)
                else:
                    setattr(j, 'fromHadTop', False)
                #if j.pt < 25: continue
                #print jesLabel
                if(getattr(j, "pt%s"%jesLabel) < 25): continue
                #if j.btagDeepFlavB < btagvetoval: continue
                #jets.append(j)
                #j_temp = TLorentzVector(0,0,0,0)
                #j_temp.SetPtEtaPhiM(getattr(event, "JetSel_Recl_pt%s"%jesLabel), j.eta, j.phi, j.mass )
                jets.append(j)
            # Store all jets
            jet_pts=[]; jet_etas=[]; jet_phis=[]; jet_masses=[]; jet_btagdiscrs=[]; jet_ishadtops=[]
            def my_sort(j):
                #return j.btagDeepFlavB
                return getattr(j, "pt%s"%jesLabel)
            jets.sort(key=my_sort, reverse=True)
            #if(len(jets) > 5): continue
            for j in jets:
                jet_pts.append(getattr(j, "pt%s"%jesLabel))
                jet_etas.append(j.eta)
                jet_phis.append(j.phi)
                jet_masses.append(j.mass)
                jet_btagdiscrs.append( j.btagDeepFlavB > btagvetoval) 
                jet_ishadtops.append(j.fromHadTop)
            #if(len(jets) < 2): 
            #    self.setDefault(event, jesLabel)
            #    continue
            if(len(jets) > 4):
                #for j in jets:
                self.out.fillBranch('%sJet_Higgs_score%s'%(self.label,jesLabel) , getattr(event, "BDThttTT_eventReco_Hj_score"))
            else:
                self.out.fillBranch('%sJet_Higgs_score%s'%(self.label,jesLabel) , -99)


            for i in range(len(jets)):
                ###########MODEL###########
                
                score = float(self.model_dnn.predict(np.transpose(np.array([[ getattr(jets[i], "pt%s"%jesLabel)], [jets[i].p4().Eta()], [jets[i].p4().Phi()], [jets[i].p4().M()], [met], [jets[i].p4().DeltaR(leps[0].p4())], [jets[i].p4().DeltaR(leps[1].p4())]]))))#[jets[i].p4().DeltaR(leps[0].p4())], [jets[i].p4().DeltaR(leps[1].p4())]]))))
                self.out.fillBranch('%sreco_score_higgs%s'%(self.label,jesLabel), score)

            def my_sort_score(j):
                return float(self.model_dnn.predict(np.transpose(np.array([[getattr(j, "pt%s"%jesLabel)], [j.eta], [j.phi], [j.mass], [met], [j.DeltaR(leps[0].p4())], [j.DeltaR(leps[1].p4())]]))))

            jets.sort(key=my_sort_score, reverse=True)

            if(len(jets) >= 2):
                self.out.fillBranch('%sreco_q1_score_higgs_pt%s'%(self.label,jesLabel), getattr(jets[0], "pt%s"%jesLabel))
                self.out.fillBranch('%sreco_q1_score_higgs_eta%s'%(self.label,jesLabel), jets[0].p4().Eta())
                self.out.fillBranch('%sreco_q1_score_higgs_phi%s'%(self.label,jesLabel), jets[0].p4().Phi())
                self.out.fillBranch('%sreco_q1_score_higgs_mass%s'%(self.label,jesLabel), jets[0].p4().M())

                self.out.fillBranch('%sreco_q2_score_higgs_pt%s'%(self.label,jesLabel), getattr(jets[1], "pt%s"%jesLabel))
                self.out.fillBranch('%sreco_q2_score_higgs_eta%s'%(self.label,jesLabel), jets[1].p4().Eta())
                self.out.fillBranch('%sreco_q2_score_higgs_phi%s'%(self.label,jesLabel), jets[1].p4().Phi())
                self.out.fillBranch('%sreco_q2_score_higgs_mass%s'%(self.label,jesLabel), jets[1].p4().M())
                j1_q = TLorentzVector(0,0,0,0)
                j2_q = TLorentzVector(0,0,0,0)
                j1_q.SetPtEtaPhiM(getattr(jets[0], "pt%s"%jesLabel), j.eta, j.phi, j.mass)
                j2_q.SetPtEtaPhiM(getattr(jets[1], "pt%s"%jesLabel), j.eta, j.phi, j.mass)
                self.out.fillBranch('%sreco_q1_q2_score_higgs_pt%s'%(self.label,jesLabel), 
(j1_q+j2_q).Pt())
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

                if(i < len(jets)): 
                    j5_t = TLorentzVector(0,0,0,0)
                    j5_t.SetPtEtaPhiM(getattr(jets[i], "pt%s"%jesLabel), jets[i].eta, jets[i].phi, jets[i].mass)
                    all5_jets = all5_jets + j5_t
 
                self.out.fillBranch('%sJet%s%s_pt'%(self.label,i,jesLabel)       , jet_pts[i] if i < len(jets) and jet_ishadtops[i] is True else -99)
                self.out.fillBranch('%sJet%s%s_eta'%(self.label,i,jesLabel)      , jet_etas[i] if i < len(jets) and jet_ishadtops[i] is True else -99)
                self.out.fillBranch('%sJet%s%s_phi'%(self.label,i,jesLabel)      , jet_phis[i] if i < len(jets) and jet_ishadtops[i] is True else -99)
                self.out.fillBranch('%sJet%s%s_mass'%(self.label,i,jesLabel)     , jet_masses[i] if i < len(jets) and jet_ishadtops[i] is True else -99)
                self.out.fillBranch('%sJet%s%s_btagdiscr'%(self.label,i,jesLabel), jet_btagdiscrs[i] if i < len(jets) and jet_ishadtops[i] is True else -99)
                self.out.fillBranch('%sJet%s%s_ishadtop'%(self.label,i,jesLabel) , jet_ishadtops[i] if i < len(jets) and jet_ishadtops[i] is True else -99)
                
                
            self.out.fillBranch('%sAll5_Jets_pt'%(self.label), all5_jets.Pt() if len(jets) <= 5 else -99)
            self.out.fillBranch('%sAll5_Jets_eta'%(self.label), all5_jets.Eta() if len(jets) <= 5 else -99)
            self.out.fillBranch('%sAll5_Jets_phi'%(self.label), all5_jets.Phi() if len(jets) <= 5 else -99)
            self.out.fillBranch('%sAll5_Jets_mass'%(self.label), all5_jets.M() if len(jets) <= 5 else -99)


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
                jp = TLorentzVector(0,0,0,0)
                jp.SetPtEtaPhiM(getattr(jets[j], "pt%s"%jesLabel), jets[j].eta, jets[j].phi, jets[j].mass)
                all_jets = all_jets + jp
       
            all_jets_sum = all_jets
            for l in range(len(leps)):
                all_jets= all_jets_sum + leps[l].p4()

            self.out.fillBranch('%sJets_plus_Lep_pt'%(self.label), all_jets.Pt()   )
            self.out.fillBranch('%sJets_plus_Lep_eta'%(self.label), all_jets.Eta()   )
            self.out.fillBranch('%sJets_plus_Lep_phi'%(self.label), all_jets.Phi()   )
            self.out.fillBranch('%sJets_plus_Lep_mass'%(self.label), all_jets.M()   )
            

            #Compute met from events
            more5_jets = TLorentzVector()
            more5_jets.SetPtEtaPhiM(0,0,0,0)
            if(len(jets) > self.njet):
                #more5_jets = TLorentzVector()
                #more5_jets.SetPtEtaPhiM(0,0,0,0)
                for j in range(self.njet, len(jets)):
                    m5 = TLorentzVector(0,0,0,0)
                    m5.SetPtEtaPhiM(getattr(jets[j], "pt%s"%jesLabel), jets[j].eta, jets[j].phi, jets[j].mass                    )
                    more5_jets = more5_jets + m5

            self.out.fillBranch('%sMore5_Jets_pt'%(self.label), more5_jets.Pt() if(len(jets)) > self.njet else -99   )
            self.out.fillBranch('%sMore5_Jets_eta'%(self.label), more5_jets.Eta() if(len(jets)) > self.njet else -99  )
            self.out.fillBranch('%sMore5_Jets_phi'%(self.label), more5_jets.Phi() if(len(jets)) > self.njet else -99  )
            self.out.fillBranch('%sMore5_Jets_mass'%(self.label), more5_jets.M() if(len(jets)) > self.njet else -99  )
            

            self.out.fillBranch('%smet%s'     %(self.label,jesLabel), met                                ) 
            self.out.fillBranch('%smet_phi%s' %(self.label,jesLabel), met_phi                            )
            self.out.fillBranch('%sHTXS_Higgs_pt'%(self.label), getattr(event,"HTXS_Higgs_pt") if(isData == False) else -99)
            self.out.fillBranch('%sHTXS_Higgs_y' %(self.label), getattr(event,"HTXS_Higgs_y") if(isData == False) else -99)

            # I must patch these two to fill only for TTH, otherwise the friend does not exist etc. Maybe produce friend also for background
            #self.out.fillBranch('%sHgen_vis_pt%s'  %(self.label,jesLabel), getattr(event,'Hreco_pTTrueGen'))
            #self.out.fillBranch('%sHgen_tru_pt%s'  %(self.label,jesLabel), getattr(event,'Hreco_pTTrueGenPlusNu')) # the same as HTXS_Higgs_pt
            #dnn_pred = self.model_regression.predict(np.transpose(np.array([ [leps[0].p4().Pt()], [leps[0].p4().Eta()], [leps[0].p4().Phi()], [leps[1].p4().Pt()], [leps[1].p4().Eta()], [leps[1].p4().Phi()], [HadTop.Pt()], [HadTop.Eta()], [HadTop.Phi()], [score], [met], [all_jets.Pt()], [all_jets.Eta()], [all_jets.Phi()], [more5_jets.Pt()], [more5_jets.Eta()], [more5_jets.Phi()], [all5_jets.Pt()], [all5_jets.Eta()], [all5_jets.Phi()], [met_phi] ])))
            dnn_pred = self.model_regression.predict(np.transpose(np.array([ [leps[0].p4().Pt()], [leps[0].p4().Eta()], [leps[0].p4().Phi()], [leps[1].p4().Pt()], [leps[1].p4().Eta()], [leps[1].p4().Phi()], [HadTop.Pt() if HadTop is True else -99], [HadTop.Eta() if HadTop is True else -99], [HadTop.Phi() if HadTop is True else -99], [score], [met], [all_jets.Pt()], [all_jets.Eta()], [all_jets.Phi()], [more5_jets.Pt() if(len(jets)) > 5 else -99], [more5_jets.Eta() if(len(jets)) > 5 else -99], [more5_jets.Phi() if(len(jets)) > 5 else -99], [all5_jets.Pt() if(len(jets)) <= 5 else -99], [all5_jets.Eta() if(len(jets)) <= 5 else -99], [all5_jets.Phi() if(len(jets)) <= 5 else -99], [met_phi] ])))

            #print dnn_pred
            self.out.fillBranch('%sdnn_prediction%s'%(self.label,jesLabel), dnn_pred)
            
        return True

higgsDiffRegressionTTH_reduced = lambda : HiggsDiffRegressionTTH_reduced(label='Hreco_',
                                                         btagDeepCSVveto = 'M')
