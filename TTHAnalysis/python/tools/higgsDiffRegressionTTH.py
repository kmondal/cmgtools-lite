from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from PhysicsTools.Heppy.physicsobjects.Jet import _btagWPs as HiggsRecoTTHbtagwps

import ROOT, itertools
import numpy as np

class HiggsDiffRegressionTTH(Module):
    def __init__(self,label="_Recl", cut_BDT_rTT_score = 0.0, btagDeepCSVveto = 'M', doSystJEC=False):
        self.label = label
        self.cut_BDT_rTT_score = cut_BDT_rTT_score
        self.btagDeepCSVveto = btagDeepCSVveto
        self.branches = []
        self.systsJEC = {0:"", 1:"_jesTotalUp", -1:"_jesTotalDown"} if doSystJEC else {0:""}
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

        # Independent on JES

        # Somehow dependent on JES

        for jesLabel in self.systsJEC.values():
            
            # Counters
            self.out.branch('%snLeps%s'%(self.label,jesLabel), 'I') 
            self.out.branch('%snJets%s'%(self.label,jesLabel), 'I')

            for suffix in ["_pt", "_eta", "_phi", "_mass"]:
                for iLep in range(2):
                    self.out.branch('%sLep%s%s%s'%(self.label,iLep,jesLabel,suffix)   , 'F') 
                for iJet in range(7):
                    self.out.branch('%sJet%s%s%s'%(self.label,iJet,jesLabel,suffix)   , 'F')
                self.out.branch('%sHadTop%s%s'%(self.label,jesLabel,suffix), 'F')
                
            
            for iJet in range(7):
                self.out.branch('%sJet%s%s_btagdiscr'%(self.label,iJet,jesLabel), 'F')

            self.out.branch('%sTopScore%s'%(self.label,jesLabel)      , 'F')      
            self.out.branch('%smet%s'%(self.label,jesLabel)           , 'F')       
            self.out.branch('%smet_phi%s'%(self.label,jesLabel)       , 'F')
            self.out.branch('%sHTXS_Higgs%s_pt'%(self.label,jesLabel) , 'F')
            self.out.branch('%sHTXS_Higgs%s_y'%(self.label,jesLabel)  , 'F')
            self.out.branch('%sHgen_vis_pt%s'%(self.label,jesLabel)        , 'F')
            self.out.branch('%sHgen_tru_pt%s'%(self.label,jesLabel)        , 'F')
            self.out.branch('%sevt_tag%s'%(self.label,jesLabel)       , 'F')       
            
            # Tell the network how to connect the lepton and the closest jet
            for iLep in range(2):
                self.out.branch('%sDeltaRClosestJetToLep%s%s'%(self.label,iLep,jesLabel) , 'F')
                self.out.branch('%sDeltaPtClosestJetToLep%s%s'%(self.label,iLep,jesLabel) , 'F')

            for var in ['DeltaRl0l1',
                        
                        'DeltaRl0j0', 'DeltaRl0j1', 'DeltaRl0j2', 'DeltaRl0j3', 'DeltaRl0j4', 'DeltaRl0j5', 'DeltaRl0j6', 
                        'DeltaRl1j0', 'DeltaRl1j1', 'DeltaRl1j2', 'DeltaRl1j3', 'DeltaRl1j4', 'DeltaRl1j5', 'DeltaRl1j6', 
                        
                        'DeltaRj0j0', 'DeltaRj0j1', 'DeltaRj0j2', 'DeltaRj0j3', 'DeltaRj0j4', 'DeltaRj0j5', 'DeltaRj0j6', 
                        'DeltaRj1j0', 'DeltaRj1j1', 'DeltaRj1j2', 'DeltaRj1j3', 'DeltaRj1j4', 'DeltaRj1j5', 'DeltaRj1j6', 
                        'DeltaRj2j0', 'DeltaRj2j1', 'DeltaRj2j2', 'DeltaRj2j3', 'DeltaRj2j4', 'DeltaRj2j5', 'DeltaRj2j6', 
                        'DeltaRj3j0', 'DeltaRj3j1', 'DeltaRj3j2', 'DeltaRj3j3', 'DeltaRj3j4', 'DeltaRj3j5', 'DeltaRj3j6', 
                        'DeltaRj4j0', 'DeltaRj4j1', 'DeltaRj4j2', 'DeltaRj4j3', 'DeltaRj4j4', 'DeltaRj4j5', 'DeltaRj4j6', 
                        'DeltaRj5j0', 'DeltaRj5j1', 'DeltaRj5j2', 'DeltaRj5j3', 'DeltaRj5j4', 'DeltaRj5j5', 'DeltaRj5j6', 
                        'DeltaRj6j0', 'DeltaRj6j1', 'DeltaRj6j2', 'DeltaRj6j3', 'DeltaRj6j4', 'DeltaRj6j5', 'DeltaRj6j6', 
                    ]:
                self.out.branch('%s%s%s'%(self.label,var,jesLabel), 'F')


    def analyze(self, event):

        # Some useful input parameters
        year=getattr(event,'year')
        btagvetoval=HiggsRecoTTHbtagwps['DeepFlav_%d_%s'%(year,self.btagDeepCSVveto)][1]

        nleps = getattr(event,"nLepGood")
        nFO = getattr(event,"nLepFO_Recl")
        ileps = getattr(event,"iLepFO_Recl")
        leps = Collection(event,"LepGood","nLepGood")
        lepsFO = [leps[ileps[i]] for i in xrange(nFO)]
        alljets = [x for x in Collection(event,"JetSel_Recl","nJetSel_Recl")]
        jets = [j for j in alljets if j.p4().Pt()>25.] # Pick only jets with our regular pt cut --- not used
        
        (met, met_phi)  = event.MET_pt, event.MET_phi

        for jesLabel in self.systsJEC.values():
            score = getattr(event,"BDThttTT_eventReco_mvaValue%s"%jesLabel)
            
            candidates=[]
            top1 = None
            top2 = None
            top3 = None
            HadTop = None

            if score>self.cut_BDT_rTT_score:

                j1top = int(getattr(event,"BDThttTT_eventReco_iJetSel1%s"%jesLabel))
                j2top = int(getattr(event,"BDThttTT_eventReco_iJetSel2%s"%jesLabel))
                j3top = int(getattr(event,"BDThttTT_eventReco_iJetSel3%s"%jesLabel))
                # make had top and fill
                #top1 = ROOT.TLorentzVector(); top1.SetPtEtaPhiM(getattr(jets[jets.index(j1top)],'pt%s'%self.systsJEC[var]),jets[jets.index(j1top)].Eta(), jets[jets.index(j1top)].Phi(), jets[jets.index(j1top)].M())
                #top2 = ROOT.TLorentzVector(); top2.SetPtEtaPhiM(getattr(jets[jets.index(j2top)],'pt%s'%self.systsJEC[var]),jets[jets.index(j2top)].Eta(), jets[jets.index(j2top)].Phi(), jets[jets.index(j2top)].M())
                #top3 = ROOT.TLorentzVector(); top3.SetPtEtaPhiM(getattr(jets[jets.index(j3top)],'pt%s'%self.systsJEC[var]),jets[jets.index(j3top)].Eta(), jets[jets.index(j3top)].Phi(), jets[jets.index(j3top)].M())
                
                top1 = ROOT.TLorentzVector(); top1.SetPtEtaPhiM(alljets[j1top].p4().Pt(),alljets[j1top].p4().Eta(), alljets[j1top].p4().Phi(), alljets[j1top].p4().M())
                top2 = ROOT.TLorentzVector(); top2.SetPtEtaPhiM(alljets[j2top].p4().Pt(),alljets[j2top].p4().Eta(), alljets[j2top].p4().Phi(), alljets[j2top].p4().M())
                top3 = ROOT.TLorentzVector(); top3.SetPtEtaPhiM(alljets[j3top].p4().Pt(),alljets[j3top].p4().Eta(), alljets[j3top].p4().Phi(), alljets[j3top].p4().M())
                HadTop = top1+top2+top3
                
                # Unused
                #jetsNoTopNoB = [j for i,j in enumerate(jets) if i not in [j1top,j2top,j3top] and j.btagDeepB<btagvetoval]
                #jetsNoTopNoB = [j for j in jetsNoTopNoB if j.p4().Pt()>25.] # exclude low-pt jets---must do it here otherwise I mess up the jNtop indices a

                # Later fill only j1 j2 j3, but for now let's use all jets
                #for _lep,lep in [(ix,x.p4()) for ix,x in enumerate(lepsFO)]:
                #    for _j1,_j2,j1,j2 in [(jets.index(x1),jets.index(x2),x1.p4(),x2.p4()) for x1,x2 in itertools.combinations(jetsNoTopNoB,2)]:
                #        j1.SetPtEtaPhiM(getattr(jets[jets.index(x1)],'pt%s'%self.systsJEC[var]),j1.Eta(), j1.Phi(), j1.M())
                #        j2.SetPtEtaPhiM(getattr(jets[jets.index(x2)],'pt%s'%self.systsJEC[var]),j2.Eta(), j2.Phi(), j2.M())
                #        W = j1+j2
                #        mW = W.M()
                #        if mW<self.cuts_mW_had[0] or mW>self.cuts_mW_had[1]: continue
                #        Wconstr = ROOT.TLorentzVector()
                #        Wconstr.SetPtEtaPhiM(W.Pt(),W.Eta(),W.Phi(),80.4)
                #        Hvisconstr = lep+Wconstr
                #        mHvisconstr = Hvisconstr.M()
                #        if mHvisconstr<self.cuts_mH_vis[0] or mHvisconstr>self.cuts_mH_vis[1]: continue
                #        mindR = min(lep.DeltaR(j1),lep.DeltaR(j2))
                #        candidates.append((mindR,mHvisconstr,mW,_lep,_j1,_j2))
                        
            self.out.fillBranch('%sHadTop%s_pt'  %(self.label,jesLabel), HadTop.Pt()  if HadTop else -99.)
            self.out.fillBranch('%sHadTop%s_eta' %(self.label,jesLabel), HadTop.Eta() if HadTop else -99.)
            self.out.fillBranch('%sHadTop%s_phi' %(self.label,jesLabel), HadTop.Phi() if HadTop else -99.)
            self.out.fillBranch('%sHadTop%s_mass'%(self.label,jesLabel), HadTop.M()   if HadTop else -99.)
            self.out.fillBranch('%sTopScore%s'   %(self.label,jesLabel), score                          ) # else -99? Or not?

            evt_tag = 1
            self.out.fillBranch('%sDeltaRl0l1%s' %(self.label,jesLabel), lepsFO[0].p4().DeltaR(lepsFO[1].p4()) if len(lepsFO)>=2 else -99.)
            

            selleps=[]
            drs = []
            dpts = []
            for l,lp4 in [(ix,x.p4()) for ix,x in enumerate(lepsFO)]:
                if len(lepsFO)<3:  # This should be always OK because we are running this on 2lss events. If we start running on other events, it won't be fine anymore.
                    selleps.append(lp4)
                    evt_tag *= lepsFO[l].pdgId
                
                    tdrs=[]
                    tdpts=[]
                    for j, jp4 in [(ix,x.p4()) for ix,x in enumerate(jets)]:
                        tdrs.append(lp4.DeltaR(jp4))
                        tdpts.append(lp4.Pt()-jp4.Pt())
                    drs.append(tdrs)
                    dpts.append(tdpts)

            self.out.fillBranch('%snLeps%s' %(self.label,jesLabel), len(selleps))
            for iLep in range(2):
                part = selleps[iLep] if iLep<len(selleps) else None
                self.out.fillBranch('%sLep%s%s_pt'  %(self.label,iLep,jesLabel), part.Pt()  if iLep < len(selleps) else -99.)
                self.out.fillBranch('%sLep%s%s_eta' %(self.label,iLep,jesLabel), part.Eta() if iLep < len(selleps) else -99.)
                self.out.fillBranch('%sLep%s%s_phi' %(self.label,iLep,jesLabel), part.Phi() if iLep < len(selleps) else -99.)
                self.out.fillBranch('%sLep%s%s_mass'%(self.label,iLep,jesLabel), part.M()   if iLep < len(selleps) else -99.)

            for l in range(len(drs)):
                for j in range(len(drs[l])):
                    if j<6:
                        self.out.fillBranch('%sDeltaRl%sj%s%s' %(self.label,l,j,jesLabel), drs[l][j])
            
            self.out.fillBranch('%sevt_tag%s'%(self.label,jesLabel), evt_tag)

            seljets=[]
            seljetsbtag=[]
            jdrs = []
            if len(jets) <4:
                print("We have", len(jets), "jets.")
            for j, jp4 in [(ix,x.p4()) for ix,x in enumerate(jets)]:
                #jp4.SetPtEtaPhiM(getattr(jets[jets.index(j)],'pt%s'%self.systsJEC[var]),jp4.Eta(), jp4.Phi(), jp4.M())
                if j <7: # fix this
                    seljets.append(jp4)
                    seljetsbtag.append(jets[j].btagDeepB)

                    tjdrs=[]
                    for jo, jpo4 in [(ixo,xo.p4()) for ixo,xo in enumerate(jets)]:
                        if jo <7: # fix this
                          tjdrs.append(jp4.DeltaR(jpo4))
                    jdrs.append(tjdrs)
            
            for j1 in range(len(jdrs)):
                for j2 in range(len(jdrs)):
                    self.out.fillBranch('%sDeltaRj%sj%s%s'%(self.label,j1,j2,jesLabel), jdrs[j1][j2] if (j1<len(seljets) and j2<len(seljets)) else -99. )

            self.out.fillBranch('%snJets%s' %(self.label,jesLabel), len(seljets))

            for iJet in range(7):
                    part = seljets[iJet] if iJet<len(seljets) else None
                    self.out.fillBranch('%sJet%s%s_pt'  %(self.label,iJet,jesLabel), part.Pt() if iJet<len(seljets) else -99.)
                    self.out.fillBranch('%sJet%s%s_eta' %(self.label,iJet,jesLabel), part.Eta()if iJet<len(seljets) else -99.)
                    self.out.fillBranch('%sJet%s%s_phi' %(self.label,iJet,jesLabel), part.Phi()if iJet<len(seljets) else -99.)
                    self.out.fillBranch('%sJet%s%s_mass'%(self.label,iJet,jesLabel), part.M()  if iJet<len(seljets) else -99.)
                    self.out.fillBranch('%sJet%s%s_btagdiscr'%(self.label,iJet,jesLabel), seljetsbtag[iJet] if iJet<len(seljets) else -99.)
                
            if len(drs)==2:
                for iLep in range(2):
                    deltars=drs[iLep]
                    deltapts=dpts[iLep]
                    idx   = list(range(len(deltars)))
                    idx.sort(key=deltars.__getitem__)
                    deltars[:]  = [deltars[i] for i in idx]
                    deltapts[:] = [deltapts[i] for i in idx]
                    self.out.fillBranch('%sDeltaRClosestJetToLep%s%s'%(self.label,iLep,jesLabel) ,  deltars[-1] if len(deltars)>0 else -98.)
                    self.out.fillBranch('%sDeltaPtClosestJetToLep%s%s'%(self.label,iLep,jesLabel) , deltapts[-1]if len(deltars)>0 else -98.)
            else:
                for iLep in range(2):
                    self.out.fillBranch('%sDeltaRClosestJetToLep%s%s'%(self.label,iLep,jesLabel) ,  -99.)
                    self.out.fillBranch('%sDeltaPtClosestJetToLep%s%s'%(self.label,iLep,jesLabel) , -99.)
                    
            # some debugging # print("CHIPPI")
            # some debugging # for iJet in range(7):
            # some debugging #         part = seljets[iJet] if iJet<len(seljets) else None
            # some debugging #         print("pt ", part.Pt() if iJet<len(seljets) else -99.)
            # some debugging #         print("eta ", part.Eta()if iJet<len(seljets) else -99.)
            # some debugging #         print("phi ", part.Phi()if iJet<len(seljets) else -99.)
            # some debugging #         print("m ", part.M()  if iJet<len(seljets) else -99.)


            self.out.fillBranch('%smet%s'     %(self.label,jesLabel), met                                ) 
            self.out.fillBranch('%smet_phi%s' %(self.label,jesLabel), met_phi                            )
            self.out.fillBranch('%sHTXS_Higgs_pt%s'%(self.label,jesLabel), getattr(event,"HTXS_Higgs_pt"))
            self.out.fillBranch('%sHTXS_Higgs_y%s' %(self.label,jesLabel), getattr(event,"HTXS_Higgs_y") )
            # I must patch these two to fill only for TTH, otherwise the friend does not exist etc. Maybe produce friend also for background
            self.out.fillBranch('%sHgen_vis_pt%s'  %(self.label,jesLabel), getattr(event,'Hreco_pTTrueGen'))
            self.out.fillBranch('%sHgen_tru_pt%s'  %(self.label,jesLabel), getattr(event,'Hreco_pTTrueGenPlusNu')) # the same as HTXS_Higgs_pt

        return True

higgsDiffRegressionTTH = lambda : HiggsDiffRegressionTTH(label='Hreco_',
                                                         btagDeepCSVveto = 'M')
