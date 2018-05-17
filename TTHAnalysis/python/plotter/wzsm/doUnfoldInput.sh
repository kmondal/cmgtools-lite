#!/bin/bash
# Created by pietro.vischia@cern.ch
# Build inputs to the unfolding procedure (together with systematics)

#declare -A pairs=( ['nJet30']='[-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5]' ['sump4(0, LepZ1_pt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_pt,LepZ2_eta,LepZ2_phi,LepZ2_mass)']='[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140]' ['sump4(0, LepZ1_pt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_pt,LepZ2_eta,LepZ2_phi,LepZ2_mass)']='[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140]' )

#declare -A pairs=( ['nJet30']='[-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5]' ['sump4(0, LepZ1_pt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_pt,LepZ2_eta,LepZ2_phi,LepZ2_mass)']='[0,20,40,60,80,100,130,160,200,300]' ['sump4(0, LepZ1_pt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_pt,LepZ2_eta,LepZ2_phi,LepZ2_mass)']='[0,20,40,60,80,100,130,160,200,300]' )

#declare -A pairs=( ['nJet30']='[-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5]' ['sump4(0, LepZ1_pt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_pt,LepZ2_eta,LepZ2_phi,LepZ2_mass)']='[0,10,20,30,40,50,60,80,100,130,160,200,300]' ['sump4(0, LepZ1_pt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_pt,LepZ2_eta,LepZ2_phi,LepZ2_mass)']='[0,20,40,60,80,100,130,160,200,300]' )

#declare -A pairs=(  ['sump4(0, LepZ1_pt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_pt,LepZ2_eta,LepZ2_phi,LepZ2_mass)']='[0,10,20,30,40,50,60,80,100,130,160,200,300]'  )

declare -A pairs=(  ['sump4(0, LepZ1_pt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_pt,LepZ2_eta,LepZ2_phi,LepZ2_mass)']='[0,5,10,15,20,25,30,40,50,60,70,80,90,100,110,120,130,140,160,180,200,250,300]' ["LeadJet_pt"]='[25,30,35,40,50,60,70,80,90,100,110,120,130,140,160,180,200,250,300]' ["m3Lmet"]='[50,60,70,80,90,100,120,140,160,180,200,240,280,320,360,400,450,500,550,600,650,700,800,1000,1500,2000,3000]' )

#mca=".wzsm/mca_includes.txt"
mca="./wzsm/mca_unfoldingInputs.txt"
inputdir="/pool/ciencias/HeppyTrees/RA7/estructura/wzSkimmed/"


# Preliminary cleanup
echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/"
echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eee_fitWZonly/ "
echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eem_fitWZonly/ "
echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mme_fitWZonly/ "
echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mmm_fitWZonly/ "

count=0
for iShape in "${!pairs[@]}"; do
    iRange=${pairs[$iShape]}

    iXTitle=""
    iYTitle="Events"
    if [[ $iShape = *"m3Lmet"* ]]; then
        iXTitle="Reco M\_\{WZ\} [GeV]"
    elif [[ $iShape = *"LeadJet_pt"* ]]; then
        iXTitle="Reco p\_\{T\}(leading jet) [GeV]"
    elif [[ $iShape = *"sump4"* ]]; then
        iXTitle="Reco p\_\{T\}(Z) [GeV]"
    fi

    echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir} --Fs {P}/leptonJetReCleanerWZSM --Fs {P}/leptonBuilderWZSM --FMCs {P}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_pt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_pt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_pt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/ --bin incl -o WZSR -E SR  --neglist promptsub --autoMCStats --XTitle \"$iXTitle\" --YTitle \"$iYTitle\""

    echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir} --Fs {P}/leptonJetReCleanerWZSM --Fs {P}/leptonBuilderWZSM --FMCs {P}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_pt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_pt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_pt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eee_fitWZonly/ --bin eee -o WZSR -E SR -E eee --neglist promptsub --autoMCStats --XTitle \"$iXTitle\" --YTitle \"$iYTitle\""

    echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir} --Fs {P}/leptonJetReCleanerWZSM --Fs {P}/leptonBuilderWZSM --FMCs {P}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_pt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_pt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_pt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eem_fitWZonly/ --bin eem -o WZSR -E SR -E eem --neglist promptsub --autoMCStats --XTitle \"$iXTitle\" --YTitle \"$iYTitle\""

    echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir} --Fs {P}/leptonJetReCleanerWZSM --Fs {P}/leptonBuilderWZSM --FMCs {P}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_pt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_pt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_pt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mme_fitWZonly/ --bin mme -o WZSR -E SR -E mme --neglist promptsub --autoMCStats --XTitle \"$iXTitle\" --YTitle \"$iYTitle\""

    echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir} --Fs {P}/leptonJetReCleanerWZSM --Fs {P}/leptonBuilderWZSM --FMCs {P}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_pt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_pt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_pt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mmm_fitWZonly/ --bin mmm -o WZSR -E SR -E mmm --neglist promptsub --autoMCStats --XTitle \"$iXTitle\" --YTitle \"$iYTitle\""


    
    #echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir} --Fs {P}/leptonJetReCleanerWZSM --Fs {P}/leptonBuilderWZSM --FMCs {P}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_pt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_pt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_pt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/ -o ZZCR -E ZZCR  --neglist promptsub --autoMCStats"

    #echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir} --Fs {P}/leptonJetReCleanerWZSM --Fs {P}/leptonBuilderWZSM --FMCs {P}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_pt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_pt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_pt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/ -o TTCR -E TTCR  --neglist promptsub --autoMCStats"

    #echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir} --Fs {P}/leptonJetReCleanerWZSM --Fs {P}/leptonBuilderWZSM --FMCs {P}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_pt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_pt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_pt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/  -o CONVCR -E convCR --neglist promptsub --autoMCStats"

    #echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir} --Fs {P}/leptonJetReCleanerWZSM --Fs {P}/leptonBuilderWZSM --FMCs {P}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_pt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_pt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_pt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_closureFakes_fitWZonly/  -o DYCR -E DYCR --neglist promptsub --autoMCStats"

    ###if    [ "$count" == "0" ]; then
    ###    echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_nJet30/"
    ###    echo "mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_nJet30/"
    if    [ "$count" == "0" ]; then
        echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_Zpt/"
        echo "mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_Zpt/"

        echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eee_fitWZonly_Zpt/"
        echo "mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eee_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eee_fitWZonly_Zpt/"

        echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eem_fitWZonly_Zpt/"
        echo "mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eem_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eem_fitWZonly_Zpt/"

        echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mme_fitWZonly_Zpt/"
        echo "mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mme_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mme_fitWZonly_Zpt/"

        echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mmm_fitWZonly_Zpt/"
        echo "mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mmm_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mmm_fitWZonly_Zpt/"

    elif [ "$count" == "1" ]; then
        echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_LeadJetPt/"
        echo "mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_LeadJetPt/"

        echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eee_fitWZonly_LeadJetPt/"
        echo "mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eee_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eee_fitWZonly_LeadJetPt/"

        echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eem_fitWZonly_LeadJetPt/"
        echo "mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eem_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eem_fitWZonly_LeadJetPt/"

        echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mme_fitWZonly_LeadJetPt/"
        echo "mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mme_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mme_fitWZonly_LeadJetPt/"

        echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mmm_fitWZonly_LeadJetPt/"
        echo "mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mmm_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mmm_fitWZonly_LeadJetPt/"

    elif [ "$count" == "2" ]; then
        echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_MWZ/"
        echo "mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_MWZ/"

        echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eee_fitWZonly_MWZ/"
        echo "mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eee_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eee_fitWZonly_MWZ/"

        echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eem_fitWZonly_MWZ/"
        echo "mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eem_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/eem_fitWZonly_MWZ/"

        echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mme_fitWZonly_MWZ/"
        echo "mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mme_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mme_fitWZonly_MWZ/"

        echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mmm_fitWZonly_MWZ/"
        echo "mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mmm_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/mmm_fitWZonly_MWZ/"

    fi
    ###elif [ "$count" == "2" ]; then
    ###    echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_Zpt/"
    ###    echo "mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_Zpt/"
    ###fi
    let "count=count+1"
done
