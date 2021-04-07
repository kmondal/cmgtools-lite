# Do Analysis of Unfolding
# Restructured everything in a single steering script
# Code by pietro.vischia@cern.ch

# First restructure the doUnfoldInput.py script 

# Created by pietro.vischia@cern.ch
# Build inputs to the unfolding procedure (together with systematics)
# and run the unfolding (either using TUnfold or combine)

import os
import sys
from multiprocessing import Pool


sys.path.append('{cmsswpath}/src/CMGTools/TTHAnalysis/python/plotter/RunII_SM_WZ/utils/'.format(cmsswpath=os.environ['CMSSW_BASE']))
from yearlyStuff import *


# This is needed for multiprocessing.Pool, and cannot be into the class (<type 'instancemethod'> is not pickable)
def runner(cmd):
    print(cmd)
    #os.system(cmd)
    


class Steer:

    def __init__(self, args):
        self.year= args.year if args.year == 'runII' else int(args.year)
        self.queue=args.queue
        self.outputDir=args.outputDir+str(self.year)
        self.channels=['incl', 'eee', 'eem', 'mme', 'mmm']
        self.mca='./mca_unfoldingInputs.txt' # File to be updated
        self.nthreads=args.nthreads
        self.singlevar=args.singlevar
        self.onlyMC=args.onlyMonteCarlo
        self.base=args.base
        self.dryrun=args.dryrun
        self.matrix=args.matrix

        if not os.path.isdir(self.outputDir):
            #os.mkdir(self.outputDir)
            print('mkdir -p {outputDir}'.format(outputDir=self.outputDir))

        for ch in self.channels:
            if not os.path.isdir('%s_%s'.format(self.outputDir,ch)):
                #os.mkdir('%s_%s'.format(self.outputDir,ch))
                print('mkdir -p {outputDir}_{ch}'.format(outputDir=self.outputDir,ch=ch))
            
        print('echo "Folders with base {outdir} have been created"'.format(outdir=self.outputDir))

        self.chanCuts ={ 'incl':'',
                         'eee':'-E eee',
                         'eem':'-E eem',
                         'mme':'-E mme',
                         'mmm':'-E mmm'
                     }

        self.inputPairs={
            'sump4(0, LepZ1_pt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_pt,LepZ2_eta,LepZ2_phi,LepZ2_mass)' : ['[0,5,10,15,20,25,30,40,50,60,70,80,90,100,110,120,130,140,160,180,200,250,300]','Reco p\_\{T\}(Z) [GeV]','Zpt'],
            #'JetClean25_pt[0]' : ['[25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,180,185,190,200,210,220,230,240,250,260,270,280,290,300]','Reco p\_\{T\}(leading jet) [GeV]','LeadJetPt'],
            #'JetClean25_pt[0]' : ['[25,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,180,185,190,200,210,220,230,240,250,260,270,280,290,300,400]','Reco p\_\{T\}(leading jet) [GeV]','LeadJetPt'],
            #'JetClean25_pt[0]' : ['[25,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,210,230,250,270,290,400]','Reco p\_\{T\}(leading jet) [GeV]','LeadJetPt'],
            'JetClean25_pt[0]' : ['[25,50,70,90,110,130,150,170,190,230,270,400]','Reco p\_\{T\}(leading jet) [GeV]','LeadJetPt'],
            'm3Lmet' :  ['[100,140,160,180,200,250,300,400,600,1000,3000]','Reco M\_\{WZ\} [GeV]','MWZ'],
            'LepW_pt' : ['[25,30,35,40,50,60,70,80,90,100,110,120,130,140,160,180,200,250,300]','Reco p\_\{T\}(W) [GeV]','Wpt'],
            'nJetClean25'   : ['[0,1,2,3,4,5]', 'Reco N\_\{jets\}', 'Njets'], 
            'cos_ThetaWDn_HE'   : ['[-1,-0.75,-0.5,-0.25,0.0,0.25,0.5,0.75,1.0]', 'cos(#theta_{W}^{Dn})', 'Wpol'],
            'cos_ThetaZDn_HE'   : ['[-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]', 'cos(#theta_{Z}^{Dn})', 'Zpol'],
        }


        self.responsePairs={
            'sump4(0, genLepZ1_pt,genLepZ1_eta,genLepZ1_phi,genLepZ1_mass,genLepZ2_pt,genLepZ2_eta,genLepZ2_phi,genLepZ2_mass):sump4(0,LepZ1_pt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_pt,LepZ2_eta,LepZ2_phi,LepZ2_mass)' : ['[0,5,10,15,20,25,30,40,50,60,70,80,90,100,110,120,130,140,160,180,200,250,300]*[0,10,20,30,50,70,90,110,130,160,200,300]','Reco p\_\{T\}(Z) [GeV]','Gen p\_\{T\}(Z) [GeV]','Zpt'],

            # HIG 'sump4(0, genLepZ1_pt,genLepZ1_eta,genLepZ1_phi,genLepZ1_mass,genLepZ2_pt,genLepZ2_eta,genLepZ2_phi,genLepZ2_mass):sump4(0,LepZ1_pt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_pt,LepZ2_eta,LepZ2_phi,LepZ2_mass)' : ['[0,5,10,15,20,25,30,40,50,60,70,80,90,100,110,120,130,140,160,180,200,250,400,1000]*[0,75,150,250,400,1000]','Reco p\_\{T\}(Z) [GeV]','Gen p\_\{T\}(Z) [GeV]','Zpt'],
            #'GenJet_pt[JetClean25_genJetIdx[0]]:JetClean25_pt[0]' : ['[25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,180,185,190,200,210,220,230,240,250,260,270,280,290,300]*[25,35,45,55,65,75,85,95,105,115,125,135,145,155,165,175,185,200,220,240,260,280,300]','Reco p\_\{T\}(leading jet) [GeV]','Gen p\_\{T\}(leading jet) [GeV]','LeadJetPt'],
            #'GenJet_pt[JetClean25_genJetIdx[0]]:JetClean25_pt[0]' : ['[25,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,220,240,260,280,300,350,400]*[25,50,70,90,110,130,150,170,190,220,260,300,400]','Reco p\_\{T\}(leading jet) [GeV]','Gen p\_\{T\}(leading jet) [GeV]','LeadJetPt'],
            'MaxIf\\$(GenJet_pt,GenJet_pt>25&&abs(GenJet_eta)<2.5&&deltaR(GenJet_eta,GenJet_phi,genLepZ1_eta,genLepZ1_phi)>0.5&&deltaR(GenJet_eta,GenJet_phi,genLepZ2_eta,genLepZ2_phi)>0.5&&deltaR(GenJet_eta,GenJet_phi,genLepW_eta,genLepW_phi)>0.5):JetClean25_pt[0]' : ['[25,50,70,90,110,130,150,170,190,230,270,400]*[25,70,110,150,190,400]','Reco p\_\{T\}(leading jet) [GeV]','Gen p\_\{T\}(leading jet) [GeV]','LeadJetPt'],
            'm3Lmet_gen:m3Lmet' : ['[100,140,160,180,200,250,300,400,600,1000,3000]*[100,160,200,300,600,3000]','Reco M\_\{WZ\} [GeV]','Gen M\_\{WZ\} [GeV]','MWZ'],
            'genLepW_pt:LepW_pt' : ['[25,30,35,40,50,60,70,80,90,100,110,120,130,140,160,180,200,250,300]*[25,35,50,70,90,110,130,160,200,300]','Reco p\_\{T\}(W) [GeV]','Gen p\_\{T\}(W) [GeV]','Wpt'],

            # HIG 'genLepW_pt:LepW_pt' : ['[25,30,35,40,50,60,70,80,90,100,110,120,130,140,160,180,200,250,400,1000]*[0,75,150,250,400,1000]','Reco p\_\{T\}(W) [GeV]','Gen p\_\{T\}(W) [GeV]','Wpt'],


            'Sum\\$(GenJet_pt>25&&abs(GenJet_eta)<2.5&&deltaR(GenJet_eta,GenJet_phi,genLepZ1_eta,genLepZ1_phi)>0.5&&deltaR(GenJet_eta,GenJet_phi,genLepZ2_eta,genLepZ2_phi)>0.5&&deltaR(GenJet_eta,GenJet_phi,genLepW_eta,genLepW_phi)>0.5):nJetClean25'   : ['[0,1,2,3,4,5]*[0,1,2,3,4]', 'Reco N\_\{jets\}', 'Gen N\_\{jets\}', 'Njets'], # Not sure that genLepW is what we want
            'cos_genThetaWDn_HE:cos_ThetaWDn_HE' : ['[-1,-0.75,-0.5,-0.25,0.0,0.25,0.5,0.75,1.0]*[-1,-0.5,0.0,0.5,1.0]','Reco cos(#theta_{W}^{Dn})','Gen cos(#theta_{W}^{Dn})', 'Wpol' ],
            'cos_genThetaZDn_HE:cos_ThetaZDn_HE' : ['[-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]*[-1,-0.8,-0.6,-0.4,-0.2,0.0,0.2,0.4,0.6,0.8,1.0]','Reco cos(#theta_{Z}^{Dn})','Gen cos(#theta_{Z}^{Dn})', 'Zpol' ],
            # HE helicity frame, CS collins-soper
             # Dn / Up --> CS lo mismo (se cancelan cosas y se resuelve analiticamente, para HE no (a nivel reco recosntruyes 4mom W, y te falta pz neutrino (dos soluciones)
        }

    def prepareInputs(self):
        
        for ch in self.channels:
            if not os.path.isdir('%s_%s/inputs'.format(self.outputDir,ch)):
                #os.mkdir('%s_%s/inputs'.format(self.outputDir,ch))
                print('mkdir -p {outputDir}_{ch}/inputs'.format(outputDir=self.outputDir,ch=ch))
                
        # Preliminary cleanup
        for ch in self.channels:
            pass #print('rm -r {outputDir}_{ch}/inputs/*'.format(outputDir=self.outputDir, ch=ch))
            
        # Always do sign split
        doSignSplit=True

        for iShape, iPack in self.inputPairs.items():
            iRange=iPack[0]
            iXTitle=iPack[1]
            iOut=iPack[2]
            iYTitle='Events'
            
            if self.singlevar:
                if not self.singlevar in iOut:
                    continue

            for iChan, iChanCut in self.chanCuts.items():
                print('mkdir -p {outdir}/{year}_{chan}_fitWZonly_{thevar}/'.format(outdir=self.outputDir, year=self.year,chan=iChan, cut=iChanCut, thevar=iOut))
                if self.year=='runII':
                    print('mkdir -p {outdir}/{year}_{chan}_fitWZonly_{thevar}/common/'.format(outdir=self.outputDir, year=self.year,chan=iChan, cut=iChanCut, thevar=iOut))
                    print('hadd -f {outdir}/{year}_{chan}_fitWZonly_{thevar}/common/WZSR_{year}.input.root temp2016/2016_{chan}_fitWZonly_{thevar}/common/WZSR_2016.input.root temp2017/2017_{chan}_fitWZonly_{thevar}/common/WZSR_2017.input.root temp2018/2018_{chan}_fitWZonly_{thevar}/common/WZSR_2018.input.root '.format(outdir=self.outputDir,year=self.year,chan=iChan, thevar=iOut))
                else:
                    requestJet='-E onejet' if 'JetPt' in iOut else ''
                    perchan = ' --od {outdir}/{year}_{chan}_fitWZonly_{thevar}/ --bin {chan} -E SRWZ {requestJet} {cut} '.format(outdir=self.outputDir, year=self.year,chan=iChan, requestJet=requestJet, cut=iChanCut, thevar=iOut)
                    
                    print('sbatch -p {queue} -c {nthreads} --wrap "python makeShapeCardsSusy.py RunII_SM_WZ/{year}/mca_wz_v5.txt RunII_SM_WZ/{year}/cuts_wzsm.txt \'{iShape}\' \'{iRange}\' RunII_SM_WZ/{year}/systs_wz.txt  --tree treeProducerSusyMultilepton -P /pool/ciencias/HeppyTrees/RA7/nanoAODv5_{year}_skimWZ/   --Fs {{P}}/leptonPtCorrections/ {prefiringTrees} {pileupTrees} --FMCs {{P}}/leptonMatcher/ --Fs {{P}}/leptonJetReCleanerWZSM/ --Fs {{P}}/leptonBuilderWZSM/ --Fs {{P}}/jet25Cleaned/  {triggerTrees}  --FMCs {{P}}/bTagEventWeights/ --FMCs {{P}}/lepgenVarsWZSM/ --Fs {{P}}/bosonPolarization/ -L RunII_SM_WZ/functionsSF.cc -L RunII_SM_WZ/functionsMCMatch.cc -L RunII_SM_WZ/functionsWZ.cc -W \'getLeptonSF_v4(0,0,{year},LepSel_pt[0],LepSel_eta[0],LepSel_pdgId[0])*getLeptonSF_v4(0,0,{year},LepSel_pt[1],LepSel_eta[1],LepSel_pdgId[1])*getLeptonSF_v4(0,0,{year},LepSel_pt[2],LepSel_eta[2],LepSel_pdgId[2])*{pileupWeights}*bTagWeightDeepCSVT_nom{prefiringWeights}\' --neg --plotgroup data_fakes+=promptsub --plotgroup data_fakes_frup+=promptsub_frup --plotgroup data_fakes_frdn+=promptsub_frdn --obj Events -j {nthreads} -l {lumi} -f  -E SRWZ {perchan} --neglist promptsub --autoMCStats  --XTitle \\"{iXTitle}\\" --YTitle \\"{iYTitle}\\" -o WZSR_{year}" '.format(queue=self.queue,year=self.year,prefiringTrees=prefiringTrees[self.year],prefiringWeights=prefiringWeights[self.year],triggerTrees=triggerTrees[self.year],lumi=lumi[self.year],pileupTrees=pileupTrees[self.year],pileupWeights=pileupWeights[self.year], perchan=perchan, nthreads=self.nthreads, iShape=iShape, iRange=iRange, iXTitle=iXTitle, iYTitle=iYTitle) )


                    # Must configure for cleanup or stuff like that
                    #print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_%s/' % iOut)
                    #print('mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_%s/' % iOut)
    
        enabler={
            'plus' : ' -E pmp ',
            'minus' : ' -E pmm',
        }

        for iWhat, iCut in enabler.items():
        
            ## Preliminary cleanup
            #print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/')
            #print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eee_fitWZonly/ ')
            #print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eem_fitWZonly/ ')
            #print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mme_fitWZonly/ ')
            #print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mmm_fitWZonly/ ')
                
            # WZ exclusive
            for iShape, iPack in self.inputPairs.items():
                iRange=iPack[0]
                iXTitle=iPack[1]
                iOut=iPack[2]
                iYTitle='Events'
                if self.singlevar:
                    if not self.singlevar in iOut:
                        continue

                for iChan, iChanCut in self.chanCuts.items():
                    print('mkdir -p {outdir}/{year}_{chan}_fitWZonly_{thevar}_{iWhat}/'.format(outdir=self.outputDir, year=self.year,chan=iChan, cut=iChanCut,thevar=iOut, iWhat=iWhat) )
                    if self.year=='runII':
                          print('mkdir -p {outdir}/{year}_{chan}_fitWZonly_{thevar}_{iWhat}/common/'.format(outdir=self.outputDir, year=self.year,chan=iChan, cut=iChanCut, thevar=iOut, iWhat=iWhat))
                          print('hadd -f {outdir}/{year}_{chan}_fitWZonly_{thevar}_{iWhat}/common/WZSR_{year}.input.root temp2016/2016_{chan}_fitWZonly_{thevar}_{iWhat}/common/WZSR_2016.input.root temp2017/2017_{chan}_fitWZonly_{thevar}_{iWhat}/common/WZSR_2017.input.root temp2018/2018_{chan}_fitWZonly_{thevar}_{iWhat}/common/WZSR_2018.input.root '.format(outdir=self.outputDir,year=self.year,chan=iChan, thevar=iOut, iWhat=iWhat))
                    else:
                        requestJet='-E onejet' if 'JetPt' in iOut else ''
                        perchan = ' --od {outdir}/{year}_{chan}_fitWZonly_{thevar}_{iWhat}/ --bin {chan} -E SRWZ {requestJet} {cut} '.format(outdir=self.outputDir, year=self.year,chan=iChan, requestJet=requestJet, cut=iChanCut, thevar=iOut, iWhat=iWhat)
                    
                        print('sbatch -p {queue} -c {nthreads} --wrap "python makeShapeCardsSusy.py RunII_SM_WZ/{year}/mca_wz_v5.txt RunII_SM_WZ/{year}/cuts_wzsm.txt \'{iShape}\' \'{iRange}\' RunII_SM_WZ/{year}/systs_wz.txt  --tree treeProducerSusyMultilepton -P /pool/ciencias/HeppyTrees/RA7/nanoAODv5_{year}_skimWZ/   --Fs {{P}}/leptonPtCorrections/ {prefiringTrees} {pileupTrees} --Fs {{P}}/leptonJetReCleanerWZSM/ --Fs {{P}}/leptonBuilderWZSM/  --Fs {{P}}/jet25Cleaned/ {triggerTrees} --FMCs {{P}}/leptonMatcher/ --FMCs {{P}}/bTagEventWeights/ --FMCs {{P}}/lepgenVarsWZSM/ --Fs {{P}}/bosonPolarization/ -L RunII_SM_WZ/functionsSF.cc -L RunII_SM_WZ/functionsMCMatch.cc -L RunII_SM_WZ/functionsWZ.cc -W \'getLeptonSF_v4(0,0,{year},LepSel_pt[0],LepSel_eta[0],LepSel_pdgId[0])*getLeptonSF_v4(0,0,{year},LepSel_pt[1],LepSel_eta[1],LepSel_pdgId[1])*getLeptonSF_v4(0,0,{year},LepSel_pt[2],LepSel_eta[2],LepSel_pdgId[2])*{pileupWeights}*bTagWeightDeepCSVT_nom{prefiringWeights}\' --neg --plotgroup data_fakes+=promptsub --plotgroup data_fakes_frup+=promptsub_frup --plotgroup data_fakes_frdn+=promptsub_frdn --obj Events -j {nthreads} -l {lumi} -f  -E SRWZ {perchan} {chargecut} --neglist promptsub --autoMCStats  --XTitle \\"{iXTitle}\\" --YTitle \\"{iYTitle}\\" -o WZSR_{year}" '.format(queue=self.queue,year=self.year,prefiringTrees=prefiringTrees[self.year],prefiringWeights=prefiringWeights[self.year],triggerTrees=triggerTrees[self.year],lumi=lumi[self.year],pileupTrees=pileupTrees[self.year],pileupWeights=pileupWeights[self.year], perchan=perchan, nthreads=self.nthreads, iShape=iShape, iRange=iRange, iXTitle=iXTitle, iYTitle=iYTitle, chargecut=iCut) )
                    
                        # Must configure for cleanup or stuff like that
                        #print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_%s_%s/' % (iOut, iWhat))
                        #print('mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_%s_%s/' % (iOut, iWhat))
                print('echo Done inputs preparation!')

    # End of prepareInputs()


    def prepareResponses(self, genshapes=False):

        print('Blah')
        addon="" if genshapes else "+(1-((Trigger_3l_{year}) && abs(LepZ1_pdgId)<14 && abs(LepZ2_pdgId)<14 && abs(LepW_pdgId)<14 && nLepSel == 3 && LepZ1_isTight && LepZ2_isTight && LepW_isTight && LepZ1_pt>25 && LepZ2_pt>10 && LepW_pt>25 && nOSSF_3l > 0 && minMllAFAS_Mini > 4 && MET_pt > 30 && abs(91.1876-mll_3l)<15 && m3L > 100 && nBJetTight25_Mini == 0 && ((LepGood_mcUCSX_v2[iF_Mini[0]]==0 || LepGood_mcUCSX_v2[iF_Mini[0]]==1) && (LepGood_mcUCSX_v2[iF_Mini[1]]==0 || LepGood_mcUCSX_v2[iF_Mini[1]]==1) && (LepGood_mcUCSX_v2[iF_Mini[2]]==0 || LepGood_mcUCSX_v2[iF_Mini[2]]==1))))*400000000000000".format(year=self.year)
        # Then restructure the doVariedResponses.py script


        mca='./wzsm/mca_unfolding.txt'
        #inputdir='/pool/ciencias/HeppyTrees/RA7/estructura/wzSkimmed/'
        #inputdir='/pool/cienciasrw/HeppyTrees/RA7/wz/wzUnskimmed/'
        inputdir = "/pool/ciencias/HeppyTrees/RA7/nanoAODv5_%s_unSkimmed_estructure/"%(str(self.year))
        baseoutputdir='/nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/responses/'
        #baseoutputdir="tempo/"
        fts=' --Fs {P}/lepgenVarsWZSM --Fs {P}/leptonJetReCleanerWZSM --Fs {P}/leptonBuilderWZSM --FMCs {P}/bTagEventWeightFullSimWZ30 '
        #processes="-p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub "
        processes=' -p prompt_altWZ.* '
        
        # Preliminary cleanup
        #echo "rm -r ${baseoutputdir}incl_fitWZonly/"
        #echo "rm -r ${baseoutputdir}eee_fitWZonly/ "
        #echo "rm -r ${baseoutputdir}eem_fitWZonly/ "
        #echo "rm -r ${baseoutputdir}mme_fitWZonly/ "
        #echo "rm -r ${baseoutputdir}mmm_fitWZonly/ "
        for iShape, iPack in self.responsePairs.items():
            iRange=iPack[0]
            iXTitle=iPack[1]
            iYTitle=iPack[2]
            iOut=iPack[3]
            print('echo \"{iShape}, range {iRange}\"'.format(iShape=iShape,iRange=iRange))
            if self.singlevar:
                if not self.singlevar in iOut:
                    continue
                        
            for iChan, iChanCut in self.chanCuts.items():
                print('mkdir -p {outdir}/responses/{year}_{chan}_fitWZonly_{iOut}/'.format(outdir=self.outputDir, year=self.year,chan=iChan, cut=iChanCut, iOut=iOut))
                if self.year=='runII':
                    print('mkdir -p {outdir}/responses/{year}_{chan}_fitWZonly_{iOut}/common/'.format(outdir=self.outputDir, year=self.year,chan=iChan, cut=iChanCut, iOut=iOut))
                    print('mkdir -p {outdir}/responses/{year}_{chan}_fitWZonly_{iOut}/prompt_altWZ_Pow/'.format(outdir=self.outputDir, year=self.year,chan=iChan, cut=iChanCut, iOut=iOut))
                    #print('hadd -f {outdir}/responses/{year}_{chan}_fitWZonly_{iOut}/common/WZSR_{year}.input.root temp2016/responses/2016_{chan}_fitWZonly_{iOut}/common/WZSR_2016.input.root temp2017/responses/2017_{chan}_fitWZonly_{iOut}/common/WZSR_2017.input.root temp2018/responses/2018_{chan}_fitWZonly_{iOut}/common/WZSR_2018.input.root '.format(outdir=self.outputDir,year=self.year,chan=iChan, iOut=iOut))
                    print('hadd -f {outdir}/responses{dogenshapesname}/{year}_{chan}_fitWZonly_{iOut}/common/WZSR_{year}.input.root temp2016/responses{dogenshapesname}/2016_{chan}_fitWZonly_{iOut}/common/WZSR_2016.input.root temp2017/responses{dogenshapesname}/2017_{chan}_fitWZonly_{iOut}/common/WZSR_2017.input.root temp2018/responses{dogenshapesname}/2018_{chan}_fitWZonly_{iOut}/common/WZSR_2018.input.root '.format(outdir=self.outputDir,year=self.year,chan=iChan, iOut=iOut,dogenshapesname='_genshapes' if genshapes else ''))
                    print('cp temp2016/responses/2016_{chan}_fitWZonly_{iOut}/prompt_altWZ_Pow/WZSR_2016.card.txt {outdir}/responses/{year}_{chan}_fitWZonly_{iOut}/prompt_altWZ_Pow/WZSR_{year}.card.txt'.format(outdir=self.outputDir,year=self.year,chan=iChan, iOut=iOut))

                else:
                    requestJet='-E onejet' if 'JetPt' in iOut else ''
                    perchan = ' --od {outdir}/responses{dogenshapesname}/{year}_{chan}_fitWZonly_{iOut}/ --bin {chan} {dogenshapes} {requestJet} {cut} '.format(outdir=self.outputDir, year=self.year,chan=iChan, requestJet=requestJet, dogenshapes='-X SR' if genshapes else '', cut=iChanCut, iOut=iOut, dogenshapesname='_genshapes' if genshapes else '')
                    print('sbatch -p {queue} -c {nthreads} --wrap "python makeShapeCardsSusy.py RunII_SM_WZ/unfolding/mca_unfolding_{year}.txt RunII_SM_WZ/{year}/cuts_fiducial.txt \'{iShape}{addon}\' \'{iRange}\' RunII_SM_WZ/{year}/systs_wz.txt  --tree treeProducerSusyMultilepton -P /pool/ciencias/HeppyTrees/RA7/nanoAODv5_{year}_unSkimmed_estructure/ --FMCs {{P}}/leptonMatcher   --Fs {{P}}/leptonPtCorrections/ {prefiringTrees} {pileupTrees} --Fs {{P}}/leptonJetReCleanerWZSM/ --Fs {{P}}/leptonBuilderWZSM/  --Fs {{P}}/jet25Cleaned/ {triggerTrees} --FMCs {{P}}/bTagEventWeights/ --FMCs {{P}}/lepgenVarsWZSM/ --Fs {{P}}/bosonPolarization/ -L RunII_SM_WZ/functionsSF.cc -L RunII_SM_WZ/functionsMCMatch.cc -L RunII_SM_WZ/functionsWZ.cc -W \'getLeptonSF_v4(0,0,{year},LepSel_pt[0],LepSel_eta[0],LepSel_pdgId[0])*getLeptonSF_v4(0,0,{year},LepSel_pt[1],LepSel_eta[1],LepSel_pdgId[1])*getLeptonSF_v4(0,0,{year},LepSel_pt[2],LepSel_eta[2],LepSel_pdgId[2])*{pileupWeights}*bTagWeightDeepCSVT_nom{prefiringWeights}\' --obj Events -j {nthreads} -l {lumi} -f  -E SRWZ {perchan} {chargecut} --neglist promptsub --asimov --autoMCStats  --XTitle \\"{iXTitle}\\" --YTitle \\"{iYTitle}\\" -o WZSR_{year}" '.format(queue=self.queue,year=self.year,prefiringTrees=prefiringTrees[self.year],prefiringWeights=prefiringWeights[self.year],addon=addon,triggerTrees=triggerTrees[self.year],lumi=lumi[self.year],pileupTrees=pileupTrees[self.year],pileupWeights=pileupWeights[self.year], perchan=perchan, nthreads=self.nthreads,iShape=iShape, iRange=iRange, iXTitle=iXTitle, iYTitle=iYTitle, chargecut=iChanCut) )

                    #print('rm -r {baseoutputdir}incl_fitWZonly_{iout}/'.format(baseoutputdir=baseoutputdir,iout=iOut))
                    #print('mv {baseoutputdir}incl_fitWZonly/ {baseoutputdir}incl_fitWZonly_{iout}/'.format(baseoutputdir=baseoutputdir,iout=iOut))
        enabler={
            'plus' : ' -E pmp ',
            'minus' : ' -E pmm',
        }

        for iWhat, iCut in enabler.items():

            for iShape, iPack in self.responsePairs.items():
                iRange=iPack[0]
                iXTitle=iPack[1]
                iYTitle=iPack[2]
                iOut=iPack[3]
                
                print('echo \"{iShape}, range {iRange}\"'.format(iShape=iShape,iRange=iRange))
                if self.singlevar:
                    if not self.singlevar in iOut:
                        continue

                for iChan, iChanCut in self.chanCuts.items():
                    print('mkdir -p {outdir}/responses/{year}_{chan}_fitWZonly_{iout}_{chargeinfo}/'.format(outdir=self.outputDir, year=self.year,chan=iChan, cut=iChanCut, iout=iOut,chargeinfo=iWhat))
                    if self.year=='runII':
                        print('mkdir -p {outdir}/responses/{year}_{chan}_fitWZonly_{iOut}_{chargeinfo}/common/'.format(outdir=self.outputDir, year=self.year,chan=iChan, cut=iChanCut, iOut=iOut, chargeinfo=iWhat))
                        print('mkdir -p {outdir}/responses/{year}_{chan}_fitWZonly_{iOut}_{chargeinfo}/prompt_altWZ_Pow/'.format(outdir=self.outputDir, year=self.year,chan=iChan, cut=iChanCut, iOut=iOut, chargeinfo=iWhat))
                        #print('hadd -f {outdir}/responses/{year}_{chan}_fitWZonly_{iOut}_{chargeinfo}/common/WZSR_{year}.input.root temp2016/responses/2016_{chan}_fitWZonly_{iOut}_{chargeinfo}/common/WZSR_2016.input.root temp2017/responses/2017_{chan}_fitWZonly_{iOut}_{chargeinfo}/common/WZSR_2017.input.root temp2018/responses/2018_{chan}_fitWZonly_{iOut}_{chargeinfo}/common/WZSR_2018.input.root '.format(outdir=self.outputDir,year=self.year,chan=iChan, iOut=iOut, chargeinfo=iWhat))
                        print('hadd -f {outdir}/responses{dogenshapesname}/{year}_{chan}_fitWZonly_{iOut}_{chargeinfo}/common/WZSR_{year}.input.root temp2016/responses{dogenshapesname}/2016_{chan}_fitWZonly_{iOut}_{chargeinfo}/common/WZSR_2016.input.root temp2017/responses{dogenshapesname}/2017_{chan}_fitWZonly_{iOut}_{chargeinfo}/common/WZSR_2017.input.root temp2018/responses{dogenshapesname}/2018_{chan}_fitWZonly_{iOut}_{chargeinfo}/common/WZSR_2018.input.root '.format(outdir=self.outputDir,year=self.year,chan=iChan, iOut=iOut, chargeinfo=iWhat, dogenshapesname='_genshapes' if genshapes else ''))
                        print('cp temp2016/responses/2016_{chan}_fitWZonly_{iOut}_{chargeinfo}/prompt_altWZ_Pow/WZSR_2016.card.txt {outdir}/responses/{year}_{chan}_fitWZonly_{iOut}_{chargeinfo}/prompt_altWZ_Pow/WZSR_{year}.card.txt'.format(outdir=self.outputDir,year=self.year,chan=iChan, iOut=iOut, chargeinfo=iWhat))
                    else:
                        requestJet='-E onejet' if 'JetPt' in iOut else ''
                        perchan = ' --od {outdir}/responses{dogenshapesname}/{year}_{chan}_fitWZonly_{iout}_{chargeinfo}/ --bin {chan} {dogenshapes} {requestJet} {cut} '.format(outdir=self.outputDir, year=self.year,chan=iChan, requestJet=requestJet, dogenshapes='-X SR' if genshapes else '', cut=iChanCut, iout=iOut,chargeinfo=iWhat, dogenshapesname='_genshapes' if genshapes else '')
                    
                        print('sbatch -p {queue} -c {nthreads} --wrap "python makeShapeCardsSusy.py RunII_SM_WZ/unfolding/mca_unfolding_{year}.txt RunII_SM_WZ/{year}/cuts_fiducial.txt \'{iShape}{addon}\' \'{iRange}\' RunII_SM_WZ/{year}/systs_wz.txt  --tree treeProducerSusyMultilepton -P /pool/ciencias/HeppyTrees/RA7/nanoAODv5_{year}_unSkimmed_estructure/ --FMCs {{P}}/leptonMatcher/ --Fs {{P}}/leptonPtCorrections/ {prefiringTrees} {pileupTrees} --Fs {{P}}/leptonJetReCleanerWZSM/ --Fs {{P}}/leptonBuilderWZSM/  --Fs {{P}}/jet25Cleaned/ {triggerTrees} --FMCs {{P}}/bTagEventWeights/ --FMCs {{P}}/lepgenVarsWZSM/ --Fs {{P}}/bosonPolarization/ -L RunII_SM_WZ/functionsSF.cc -L RunII_SM_WZ/functionsMCMatch.cc -L RunII_SM_WZ/functionsWZ.cc -W \'getLeptonSF_v4(0,0,{year},LepSel_pt[0],LepSel_eta[0],LepSel_pdgId[0])*getLeptonSF_v4(0,0,{year},LepSel_pt[1],LepSel_eta[1],LepSel_pdgId[1])*getLeptonSF_v4(0,0,{year},LepSel_pt[2],LepSel_eta[2],LepSel_pdgId[2])*{pileupWeights}*bTagWeightDeepCSVT_nom{prefiringWeights}\' --obj Events -j {nthreads} -l {lumi} -f  -E SRWZ {perchan} {chargecut} --neglist promptsub --autoMCStats --asimov  --XTitle \\"{iXTitle}\\" --YTitle \\"{iYTitle}\\" -o WZSR_{year}" '.format(queue=self.queue,year=self.year,prefiringTrees=prefiringTrees[self.year],prefiringWeights=prefiringWeights[self.year],addon=addon,triggerTrees=triggerTrees[self.year],lumi=lumi[self.year],pileupTrees=pileupTrees[self.year],pileupWeights=pileupWeights[self.year], perchan=perchan, nthreads=self.nthreads, iShape=iShape, iRange=iRange, iXTitle=iXTitle, iYTitle=iYTitle, chargecut=iCut) )

                        #print('rm -r {baseoutputdir}incl_fitWZonly_{iout}_{chargeinfo}/'.format(baseoutputdir=baseoutputdir,iout=iOut,chargeinfo=iWhat))
                        #print('mv {baseoutputdir}incl_fitWZonly/ {baseoutputdir}incl_fitWZonly_{iout}_{chargeinfo}/'.format(baseoutputdir=baseoutputdir,iout=iOut,chargeinfo=iWhat))
            


    def get_list_of_jobs(self, base):
    
        ret=[]
        executable='RunII_SM_WZ/unfolding/unfold.py'
        thematrix = '--matrix ./MATRIX/' if self.matrix else ''
        singlevar = '--singlevar %s'%self.singlevar if self.singlevar else ''
        if self.onlyMC:
            singlevar = '%s --onlyMonteCarlo '%singlevar

        #for charge in [ '', '_plus', '_minus' ]:
        #for charge in [ '_plus', '_minus' ]:
        for charge in [ '_none', '_plus', '_minus' ]:
            for fs in [ 'incl', 'eee', 'eem', 'mme', 'mmm']:
                if not base:
            
                    # Bias 1, area constraint
                    ret.append('sbatch -p {queue} -c {nthreads} --wrap "python {executable} -i {outputdir} -y {year} {singlevar} -f {fs} --charge {charge}  -b 1.0 -a -o {year}/unfold_1p0bias/{fs}{charge}/data -c common/WZSR_{year}.input.root -r {thematrix} >& logs/{year}_1p0bias_{charge}_data_{fs}.log"'.format(queue=self.queue,outputdir=self.outputDir,year=self.year,singlevar=singlevar,executable=executable,fs=fs,nthreads=self.nthreads,charge=charge,thematrix=thematrix))
                    ret.append('sbatch -p {queue} -c {nthreads} --wrap "python {executable} -i {outputdir} -y {year} {singlevar} -f {fs} --charge {charge}  -b 1.0 -a -o {year}/unfold_1p0bias/{fs}{charge}/mcclosure -c common/WZSR_{year}.input.root -r --closure {thematrix} >& logs/{year}_1p0bias_{charge}_mcclosure_{fs}.log"'.format(queue=self.queue,outputdir=self.outputDir,year=self.year,singlevar=singlevar,executable=executable,fs=fs,nthreads=self.nthreads,charge=charge,thematrix=thematrix))
                
                    # Bias 1, no area constraint
                    ret.append('sbatch -p {queue} -c {nthreads} --wrap "python {executable} -i {outputdir} -y {year} {singlevar} -f {fs} --charge {charge}  -b 1.0 -o {year}/unfold_1p0bias_noconstraintarea/{fs}{charge}/data -c common/WZSR_{year}.input.root -r {thematrix} >& logs/{year}_1p0bias_{charge}_noconstraintarea_data_{fs}.log"'.format(queue=self.queue,outputdir=self.outputDir,year=self.year,singlevar=singlevar,executable=executable,fs=fs,nthreads=self.nthreads,charge=charge,thematrix=thematrix))
                    ret.append('sbatch -p {queue} -c {nthreads} --wrap "python {executable} -i {outputdir} -y {year} {singlevar} -f {fs} --charge {charge}  -b 1.0 -o {year}/unfold_1p0bias_noconstraintarea/{fs}{charge}/mcclosure -c common/WZSR_{year}.input.root -r --closure {thematrix} >& logs/{year}_1p0bias_{charge}_noconstraintarea_mcclosure_{fs}.log"'.format(queue=self.queue,outputdir=self.outputDir,year=self.year,singlevar=singlevar,executable=executable,fs=fs,nthreads=self.nthreads,charge=charge,thematrix=thematrix))
        
                    # Bias 1.13, no area constraint
                    ret.append('sbatch -p {queue} -c {nthreads} --wrap "python {executable} -i {outputdir} -y {year} {singlevar} -f {fs} --charge {charge}  -b 1.13 -o {year}/unfold_nnlobias_noconstraintarea/{fs}{charge}/data -c common/WZSR_{year}.input.root {thematrix} -r >& logs/{year}_nnlobias_{charge}_noconstraintarea_data_{fs}.log"'.format(queue=self.queue,outputdir=self.outputDir,year=self.year,singlevar=singlevar,executable=executable,fs=fs,nthreads=self.nthreads,charge=charge,thematrix=thematrix))
                    ret.append('sbatch -p {queue} -c {nthreads} --wrap "python {executable} -i {outputdir} -y {year} {singlevar} -f {fs} --charge {charge}  -b 1.13 -o {year}/unfold_nnlobias_noconstraintarea/{fs}{charge}/mcclosure -c common/WZSR_{year}.input.root {thematrix} -r --closure >& logs/{year}_nnlobias_{charge}_noconstraintarea_mcclosure_{fs}.log"'.format(queue=self.queue,outputdir=self.outputDir,year=self.year,singlevar=singlevar,executable=executable,fs=fs,nthreads=self.nthreads,charge=charge,thematrix=thematrix))

                else:
                    # No bias, area constraint     
                    ret.append('sbatch -p {queue} -c {nthreads} --wrap "python {executable} -i {outputdir} -y {year} {singlevar} -f {fs} --charge {charge}  -b 0 -a -o {year}/unfold_nobias/{fs}{charge}/data -c common/WZSR_{year}.input.root -r {thematrix} >& logs/{year}_nobias_{charge}_data_{fs}.log"'.format(queue=self.queue,outputdir=self.outputDir,year=self.year,singlevar=singlevar,executable=executable,fs=fs,nthreads=self.nthreads,charge=charge,thematrix=thematrix))
                    ret.append('sbatch -p {queue} -c {nthreads} --wrap "python {executable} -i {outputdir} -y {year} {singlevar} -f {fs} --charge {charge}  -b 0 -a -o {year}/unfold_nobias/{fs}{charge}/mcclosure -c common/WZSR_{year}.input.root -r --closure {thematrix} >& logs/{year}_nobias_{charge}_mcclosure_{fs}.log"'.format(queue=self.queue,outputdir=self.outputDir,year=self.year,singlevar=singlevar,executable=executable,fs=fs,nthreads=self.nthreads,charge=charge,thematrix=thematrix))

                    # No bias, no area constraint
                    ret.append('sbatch -p {queue} -c {nthreads} --wrap "python {executable} -i {outputdir} -y {year} {singlevar} -f {fs} --charge {charge}  -b 0 -o {year}/unfold_nobias_noconstraintarea/{fs}{charge}/data -c common/WZSR_{year}.input.root -r {thematrix} >& logs/{year}_nobias_{charge}_noconstraintarea_data_{fs}.log"'.format(queue=self.queue,outputdir=self.outputDir,year=self.year,singlevar=singlevar,executable=executable,fs=fs,nthreads=self.nthreads,charge=charge,thematrix=thematrix))
                    ret.append('sbatch -p {queue} -c {nthreads} --wrap "python {executable} -i {outputdir} -y {year} {singlevar} -f {fs} --charge {charge}  -b 0 -o {year}/unfold_nobias_noconstraintarea/{fs}{charge}/mcclosure -c common/WZSR_{year}.input.root -r --closure {thematrix} >& logs/{year}_nobias_{charge}_noconstraintarea_mcclosure_{fs}.log"'.format(queue=self.queue,outputdir=self.outputDir,year=self.year,singlevar=singlevar,executable=executable,fs=fs,nthreads=self.nthreads,charge=charge,thematrix=thematrix))

                    # Bias 1, area constraint
                    ret.append('sbatch -p {queue} -c {nthreads} --wrap "python {executable} -i {outputdir} -y {year} {singlevar} -f {fs} --charge {charge}  -b 1.0 -a -o {year}/unfold_1p0bias/{fs}{charge}/data -c common/WZSR_{year}.input.root -r {thematrix} >& logs/{year}_1p0bias_{charge}_data_{fs}.log"'.format(queue=self.queue,outputdir=self.outputDir,year=self.year,singlevar=singlevar,executable=executable,fs=fs,nthreads=self.nthreads,charge=charge,thematrix=thematrix))
                    ret.append('sbatch -p {queue} -c {nthreads} --wrap "python {executable} -i {outputdir} -y {year} {singlevar} -f {fs} --charge {charge}  -b 1.0 -a -o {year}/unfold_1p0bias/{fs}{charge}/mcclosure -c common/WZSR_{year}.input.root -r --closure {thematrix} >& logs/{year}_1p0bias_{charge}_mcclosure_{fs}.log"'.format(queue=self.queue,outputdir=self.outputDir,year=self.year,singlevar=singlevar,executable=executable,fs=fs,nthreads=self.nthreads,charge=charge,thematrix=thematrix))
                    
                    # Bias 1, no area constraint
                    ret.append('sbatch -p {queue} -c {nthreads} --wrap "python {executable} -i {outputdir} -y {year} {singlevar} -f {fs} --charge {charge}  -b 1.0 -o {year}/unfold_1p0bias_noconstraintarea/{fs}{charge}/data -c common/WZSR_{year}.input.root -r {thematrix} >& logs/{year}_1p0bias_{charge}_noconstraintarea_data_{fs}.log"'.format(queue=self.queue,outputdir=self.outputDir,year=self.year,singlevar=singlevar,executable=executable,fs=fs,nthreads=self.nthreads,charge=charge,thematrix=thematrix))
                    ret.append('sbatch -p {queue} -c {nthreads} --wrap "python {executable} -i {outputdir} -y {year} {singlevar} -f {fs} --charge {charge}  -b 1.0 -o {year}/unfold_1p0bias_noconstraintarea/{fs}{charge}/mcclosure -c common/WZSR_{year}.input.root -r --closure {thematrix} >& logs/{year}_1p0bias_{charge}_noconstraintarea_mcclosure_{fs}.log"'.format(queue=self.queue,outputdir=self.outputDir,year=self.year,singlevar=singlevar,executable=executable,fs=fs,nthreads=self.nthreads,charge=charge,thematrix=thematrix))
        
                    # Bias 1.13, area constraint
                    #ret.append('sbatch -p {queue} -c {nthreads} --wrap "python {executable} -i {outputdir} -y {year} {singlevar} -f {fs} --charge {charge}  -b 1.13 -a -o {year}/unfold_nnlobias/{fs}{charge}/data -c common/WZSR_{year}.input.root -r {thematrix} >& logs/{year}_nnlobias_{charge}_data_{fs}.log"'.format(queue=self.queue,outputdir=self.outputDir,year=self.year,singlevar=singlevar,executable=executable,fs=fs,nthreads=self.nthreads,charge=charge,thematrix=thematrix))
                    #ret.append('sbatch -p {queue} -c {nthreads} --wrap "python {executable} -i {outputdir} -y {year} {singlevar} -f {fs} --charge {charge}  -b 1.13 -a -o {year}/unfold_nnlobias/{fs}{charge}/mcclosure -c common/WZSR_{year}.input.root -r --closure {thematrix} >& logs/{year}_nnlobias_{charge}_mcclosure_{fs}.log"'.format(queue=self.queue,outputdir=self.outputDir,year=self.year,singlevar=singlevar,executable=executable,fs=fs,nthreads=self.nthreads,charge=charge,thematrix=thematrix))
            
                    
        return ret

    def doTheUnfolding(self):
        # Finally call runUnfold and unfold.py 
        print("I am calling runUnfold using the batch system")
        
        jobs = self.get_list_of_jobs(args.base)
        
        if self.dryrun: # When I was submitting directly in-job. Now I just print the command anyway (to be redirected using the shell's pipe)
            print jobs
            quit()
        pool=Pool(self.nthreads)
        pool.map(runner, jobs)
        pool.close()
        pool.join()
        

def bad(what):
    ret=True
    if 'all' in what:
        ret=False
    if 'inputs' in what:
        ret=False
    if 'responses' in what:
        ret=False
    if 'genshapes' in what:
        ret=False
    if 'unfolding' in what:
        ret=False
    return ret

def main(args):

    print('echo "Args what: %s"'% args.what)
    if bad(args.what):
        print("I don't recognize this action. Why don't you do it yourself with pen and paper?")
        return 1
        
    anal=Steer(args) # Perhaps (depending on combination strategy) I will put the scan on the year inside the unfolding script

    if 'all' in args.what:
        args.what='inputs responses unfolding'
        
    if 'inputs' in args.what:
        anal.prepareInputs()
    if 'responses' in args.what:
        anal.prepareResponses()
    if 'genshapes' in args.what:
        anal.prepareResponses(genshapes=True)
    if 'unfolding' in args.what:
        anal.doTheUnfolding()


import argparse
import ROOT

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--what',             help='Action to be taken [inputs, responses, unfolding, all]', default='all')
    parser.add_argument('-o', '--outputDir',        help='Output directory', default='./temp')
    parser.add_argument('-om', '--onlyMonteCarlo', help='Produce the final plot only comparing predictions with each other', action='store_true')
    parser.add_argument('-y', '--year',             help='Year', default=2016)
    parser.add_argument('-n', '--nthreads',         help='Number of multiprocessing threads (only for -w unfolding)', default=4, type=int)
    parser.add_argument('-b', '--base',             help='Run only on base (the one to put in the paper) parameter set (only for -w unfolding)', action='store_true')
    parser.add_argument('-d', '--dryrun',           help='Only print commands and exit (only for -w unfolding, because of legacy structure)', action='store_true')
    parser.add_argument('-q', '--queue',            help='Batch queue [default is short]', default='short')
    parser.add_argument('--singlevar',              help='Run only on a given variable')
    parser.add_argument('--matrix',                 help='Compare to MATRIX NNLO', action='store_true')
    args = parser.parse_args()
    # execute only if run as a script
    ROOT.gROOT.SetBatch()
    main(args)

