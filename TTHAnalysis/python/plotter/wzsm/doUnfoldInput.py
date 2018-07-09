# Created by pietro.vischia@cern.ch
# Build inputs to the unfolding procedure (together with systematics)

pairs={
    'sump4(0, LepZ1_pt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_pt,LepZ2_eta,LepZ2_phi,LepZ2_mass)' : ['[0,5,10,15,20,25,30,40,50,60,70,80,90,100,110,120,130,140,160,180,200,250,300]','Reco p\_\{T\}(Z) [GeV]','Zpt'],
    'LeadJet_pt' : ['[25,30,35,40,50,60,70,80,90,100,110,120,130,140,160,180,200,250,300]','Reco p\_\{T\}(leading jet) [GeV]','LeadJetPt'],
    'm3Lmet' :  ['[100,140,160,180,200,250,300,400,600,1000,3000]','Reco M\_\{WZ\} [GeV]','MWZ'],
    'LepW_pt' : ['[25,30,35,40,50,60,70,80,90,100,110,120,130,140,160,180,200,250,300]','Reco p\_\{T\}(W) [GeV]','Wpt'],
    }


mca='./wzsm/mca_unfoldingInputs.txt'
inputdir='/pool/ciencias/HeppyTrees/RA7/estructura/wzSkimmed/'

# Preliminary cleanup
print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/')
print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eee_fitWZonly/ ')
print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eem_fitWZonly/ ')
print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mme_fitWZonly/ ')
print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mmm_fitWZonly/ ')

doSignSplit=True

if not doSignSplit: 
    for iShape, iPack in pairs.items():
        iRange=iPack[0]
        iXTitle=iPack[1]
        iOut=iPack[2]
        iYTitle='Events'

        print('python makeShapeCardsSusy.py {mca} ./wzsm/cuts_wzsm.txt \'{iShape}\' \'{iRange}\' ./wzsm/systs_wz.txt -P {inputdir} --Fs {{P}}/leptonJetReCleanerWZSM --Fs {{P}}/leptonBuilderWZSM --FMCs {{P}}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W \' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_pt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_pt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_pt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight \' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/ --bin incl -o WZSR -E SR  --neglist promptsub --autoMCStats --XTitle "{iXTitle}" --YTitle "{iYTitle}"'.format(mca=mca, iShape=iShape, iRange=iRange, inputdir=inputdir, iXTitle=iXTitle, iYTitle=iYTitle) )

        print('python makeShapeCardsSusy.py {mca} ./wzsm/cuts_wzsm.txt \'{iShape}\' \'{iRange}\' ./wzsm/systs_wz.txt -P {inputdir} --Fs {{P}}/leptonJetReCleanerWZSM --Fs {{P}}/leptonBuilderWZSM --FMCs {{P}}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W \' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_pt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_pt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_pt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight \' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eee_fitWZonly/ --bin eee -o WZSR -E SR -E eee --neglist promptsub --autoMCStats --XTitle "{iXTitle}" --YTitle "{iYTitle}"'.format(mca=mca, iShape=iShape, iRange=iRange, inputdir=inputdir, iXTitle=iXTitle, iYTitle=iYTitle) )

        print('python makeShapeCardsSusy.py {mca} ./wzsm/cuts_wzsm.txt \'{iShape}\' \'{iRange}\' ./wzsm/systs_wz.txt -P {inputdir} --Fs {{P}}/leptonJetReCleanerWZSM --Fs {{P}}/leptonBuilderWZSM --FMCs {{P}}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W \' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_pt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_pt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_pt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight \' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eem_fitWZonly/ --bin eem -o WZSR -E SR -E eem --neglist promptsub --autoMCStats --XTitle "{iXTitle}" --YTitle "{iYTitle}"'.format(mca=mca, iShape=iShape, iRange=iRange, inputdir=inputdir, iXTitle=iXTitle, iYTitle=iYTitle) )

        print('python makeShapeCardsSusy.py {mca} ./wzsm/cuts_wzsm.txt \'{iShape}\' \'{iRange}\' ./wzsm/systs_wz.txt -P {inputdir} --Fs {{P}}/leptonJetReCleanerWZSM --Fs {{P}}/leptonBuilderWZSM --FMCs {{P}}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W \' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_pt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_pt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_pt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight \' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mme_fitWZonly/ --bin mme -o WZSR -E SR -E mme --neglist promptsub --autoMCStats --XTitle "{iXTitle}" --YTitle "{iYTitle}"'.format(mca=mca, iShape=iShape, iRange=iRange, inputdir=inputdir, iXTitle=iXTitle, iYTitle=iYTitle) )

        print('python makeShapeCardsSusy.py {mca} ./wzsm/cuts_wzsm.txt \'{iShape}\' \'{iRange}\' ./wzsm/systs_wz.txt -P {inputdir} --Fs {{P}}/leptonJetReCleanerWZSM --Fs {{P}}/leptonBuilderWZSM --FMCs {{P}}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W \' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_pt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_pt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_pt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight \' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mmm_fitWZonly/ --bin mmm -o WZSR -E SR -E mmm --neglist promptsub --autoMCStats --XTitle "{iXTitle}" --YTitle "{iYTitle}"'.format(mca=mca, iShape=iShape, iRange=iRange, inputdir=inputdir, iXTitle=iXTitle, iYTitle=iYTitle) )

        print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_%s/' % iOut)
        print('mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_%s/' % iOut)
    
        print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eee_fitWZonly_%s/' % iOut)
        print('mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eee_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eee_fitWZonly_%s/' % iOut)

        print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eem_fitWZonly_%s/' % iOut)
        print('mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eem_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eem_fitWZonly_%s/' % iOut)

        print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mme_fitWZonly_%s/' % iOut)
        print('mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mme_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mme_fitWZonly_%s/' % iOut)

        print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mmm_fitWZonly_%s/' % iOut)
        print('mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mmm_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mmm_fitWZonly_%s/' % iOut)

else:

    enabler={
        'plus' : ' -E pmp ',
        'minus' : ' -E pmm',
        }

    for iWhat, iCut in enabler.items():
        
        # Preliminary cleanup
        print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/')
        print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eee_fitWZonly/ ')
        print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eem_fitWZonly/ ')
        print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mme_fitWZonly/ ')
        print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mmm_fitWZonly/ ')

        # WZ exclusive
        for iShape, iPack in pairs.items():
            iRange=iPack[0]
            iXTitle=iPack[1]
            iOut=iPack[2]
            iYTitle='Events'
        
            print('python makeShapeCardsSusy.py {mca} ./wzsm/cuts_wzsm.txt \'{iShape}\' \'{iRange}\' ./wzsm/systs_wz.txt -P {inputdir} --Fs {{P}}/leptonJetReCleanerWZSM --Fs {{P}}/leptonBuilderWZSM --FMCs {{P}}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W \' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_pt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_pt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_pt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight \' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/ --bin incl -o WZSR -E SR {chargecut}   --neglist promptsub --autoMCStats --XTitle "{iXTitle}" --YTitle "{iYTitle}"'.format(mca=mca, iShape=iShape, iRange=iRange, inputdir=inputdir, chargecut=iCut, iXTitle=iXTitle, iYTitle=iYTitle) )
            
            print('python makeShapeCardsSusy.py {mca} ./wzsm/cuts_wzsm.txt \'{iShape}\' \'{iRange}\' ./wzsm/systs_wz.txt -P {inputdir} --Fs {{P}}/leptonJetReCleanerWZSM --Fs {{P}}/leptonBuilderWZSM --FMCs {{P}}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W \' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_pt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_pt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_pt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight \' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eee_fitWZonly/ --bin eee -o WZSR -E SR {chargecut}  -E eee --neglist promptsub --autoMCStats --XTitle "{iXTitle}" --YTitle "{iYTitle}"'.format(mca=mca, iShape=iShape, iRange=iRange, inputdir=inputdir, chargecut=iCut, iXTitle=iXTitle, iYTitle=iYTitle) )

            print('python makeShapeCardsSusy.py {mca} ./wzsm/cuts_wzsm.txt \'{iShape}\' \'{iRange}\' ./wzsm/systs_wz.txt -P {inputdir} --Fs {{P}}/leptonJetReCleanerWZSM --Fs {{P}}/leptonBuilderWZSM --FMCs {{P}}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W \' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_pt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_pt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_pt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight \' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eem_fitWZonly/ --bin eem -o WZSR -E SR {chargecut}  -E eem --neglist promptsub --autoMCStats --XTitle "{iXTitle}" --YTitle "{iYTitle}"'.format(mca=mca, iShape=iShape, iRange=iRange, inputdir=inputdir, chargecut=iCut, iXTitle=iXTitle, iYTitle=iYTitle) )

            print('python makeShapeCardsSusy.py {mca} ./wzsm/cuts_wzsm.txt \'{iShape}\' \'{iRange}\' ./wzsm/systs_wz.txt -P {inputdir} --Fs {{P}}/leptonJetReCleanerWZSM --Fs {{P}}/leptonBuilderWZSM --FMCs {{P}}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W \' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_pt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_pt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_pt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight \' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mme_fitWZonly/ --bin mme -o WZSR -E SR {chargecut}  -E mme --neglist promptsub --autoMCStats --XTitle "{iXTitle}" --YTitle "{iYTitle}"'.format(mca=mca, iShape=iShape, iRange=iRange, inputdir=inputdir, chargecut=iCut, iXTitle=iXTitle, iYTitle=iYTitle) )

            print('python makeShapeCardsSusy.py {mca} ./wzsm/cuts_wzsm.txt \'{iShape}\' \'{iRange}\' ./wzsm/systs_wz.txt -P {inputdir} --Fs {{P}}/leptonJetReCleanerWZSM --Fs {{P}}/leptonBuilderWZSM --FMCs {{P}}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W \' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_pt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_pt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_pt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight \' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mmm_fitWZonly/ --bin mmm -o WZSR -E SR {chargecut}  -E mmm --neglist promptsub --autoMCStats --XTitle "{iXTitle}" --YTitle "{iYTitle}"'.format(mca=mca, iShape=iShape, iRange=iRange, inputdir=inputdir, chargecut=iCut, iXTitle=iXTitle, iYTitle=iYTitle) )

            print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_%s_%s/' % (iOut, iWhat))
            print('mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_%s_%s/' % (iOut, iWhat))
    
            print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eee_fitWZonly_%s_%s/' % (iOut, iWhat))
            print('mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eee_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eee_fitWZonly_%s_%s/' % (iOut, iWhat))
    
            print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eem_fitWZonly_%s_%s/' % (iOut, iWhat))
            print('mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eem_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eem_fitWZonly_%s_%s/' % (iOut, iWhat))

            print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mme_fitWZonly_%s_%s/' % (iOut, iWhat))
            print('mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mme_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mme_fitWZonly_%s_%s/' % (iOut, iWhat))
    
            print('rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mmm_fitWZonly_%s_%s/' % (iOut, iWhat))
            print('mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mmm_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mmm_fitWZonly_%s_%s/' % (iOut, iWhat))

print('echo Done!')
