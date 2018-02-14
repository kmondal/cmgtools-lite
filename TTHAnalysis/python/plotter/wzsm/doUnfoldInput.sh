#!/bin/bash
# Created by pietro.vischia@cern.ch
# Build inputs to the unfolding procedure (together with systematics)

#declare -A pairs=( ['nJet30']='[-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5]' ['sump4(0, LepZ1_pt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_pt,LepZ2_eta,LepZ2_phi,LepZ2_mass)']='[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140]' ['sump4(0, LepZ1_conePt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_conePt,LepZ2_eta,LepZ2_phi,LepZ2_mass)']='[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140]' )

declare -A pairs=( ['nJet30']='[-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5]' ['sump4(0, LepZ1_pt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_pt,LepZ2_eta,LepZ2_phi,LepZ2_mass)']='[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,150,160,170,190,220,250,300]' ['sump4(0, LepZ1_conePt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_conePt,LepZ2_eta,LepZ2_phi,LepZ2_mass)']='[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,150,160,170,190,220,250,300]' )

count=0

#mca=".wzsm/mca_includes.txt"
mca="./wzsm/mca_unfoldingInputs.txt"
inputdir="/pool/ciencias/HeppyTrees/RA7/estructura/wzSkimmed/"

for iShape in "${!pairs[@]}"; do
    iRange=${pairs[$iShape]}

    echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir} --Fs {P}/leptonJetReCleanerWZSM --Fs {P}/leptonBuilderWZSM --FMCs {P}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/ -o WZSR -E SR  --neglist promptsub --autoMCStats"
    
    #echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir} --Fs {P}/leptonJetReCleanerWZSM --Fs {P}/leptonBuilderWZSM --FMCs {P}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/ -o ZZCR -E ZZCR  --neglist promptsub --autoMCStats"

    #echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir} --Fs {P}/leptonJetReCleanerWZSM --Fs {P}/leptonBuilderWZSM --FMCs {P}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/ -o TTCR -E TTCR  --neglist promptsub --autoMCStats"

    #echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir} --Fs {P}/leptonJetReCleanerWZSM --Fs {P}/leptonBuilderWZSM --FMCs {P}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/  -o CONVCR -E convCR --neglist promptsub --autoMCStats"

    #echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir} --Fs {P}/leptonJetReCleanerWZSM --Fs {P}/leptonBuilderWZSM --FMCs {P}/bTagEventWeightFullSimWZ30 -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub  --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_closureFakes_fitWZonly/  -o DYCR -E DYCR --neglist promptsub --autoMCStats"

    if    [ "$count" == "0" ]; then
        echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_nJet30/"
        echo "mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_nJet30/"
    elif [ "$count" == "1" ]; then
        echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_Zpt/"
        echo "mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_Zpt/"
    elif [ "$count" == "2" ]; then
        echo "rm -r /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_ZconePt/"
        echo "mv /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly/ /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/incl_fitWZonly_ZconePt/"
    fi
    let "count=count+1"
done
