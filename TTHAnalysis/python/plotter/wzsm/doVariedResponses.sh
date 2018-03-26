#!/bin/bash
# Created by pietro.vischia@cern.ch
# Build inputs to the unfolding procedure (together with systematics)

#declare -A pairs=( ['nJet30']='[-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5]' ['sump4(0, LepZ1_pt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_pt,LepZ2_eta,LepZ2_phi,LepZ2_mass)']='[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140]' ['sump4(0, LepZ1_conePt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_conePt,LepZ2_eta,LepZ2_phi,LepZ2_mass)']='[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140]' )

#declare -A pairs=( ['nJet30']='[-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5]' ['sump4(0, LepZ1_pt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_pt,LepZ2_eta,LepZ2_phi,LepZ2_mass)']='[0,20,40,60,80,100,130,160,200,300]' ['sump4(0, LepZ1_conePt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_conePt,LepZ2_eta,LepZ2_phi,LepZ2_mass)']='[0,20,40,60,80,100,130,160,200,300]' )

#declare -A pairs=( ['nJet30']='[-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5]' ['sump4(0, LepZ1_pt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_pt,LepZ2_eta,LepZ2_phi,LepZ2_mass)']='[0,10,20,30,40,50,60,80,100,130,160,200,300]' ['sump4(0, LepZ1_conePt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_conePt,LepZ2_eta,LepZ2_phi,LepZ2_mass)']='[0,20,40,60,80,100,130,160,200,300]' )

#declare -A pairs=(  ['sump4(0, LepZ1_pt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_pt,LepZ2_eta,LepZ2_phi,LepZ2_mass)']='[0,10,20,30,40,50,60,80,100,130,160,200,300]'  )


# DA GUT ONE declare -A pairs=(  ['sump4(0, LepZ1_pt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_pt,LepZ2_eta,LepZ2_phi,LepZ2_mass)']='[0,5,10,15,20,25,30,40,50,60,70,80,90,100,110,120,130,140,160,180,200,250,300]' ["LeadJet_pt"]='[25,30,35,40,50,60,70,80,90,100,110,120,130,140,160,180,200,250,300]'  )

#declare -A pairs=(  ['sump4(0,LepZ1_pt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_pt,LepZ2_eta,LepZ2_phi,LepZ2_mass)']='[0,5,10,15,20,25,30,40,50,60,70,80,90,100,110,120,130,140,160,180,200,250,300]' ["LeadJet_pt"]='[25,30,35,40,50,60,70,80,90,100,110,120,130,140,160,180,200,250,300]'  )

# The space after "0," is needed for the looper to run on the Zpt first, otherwise it will run on LeadJetPt, because of weird behaviour of bash. LoL
declare -A pairs=(  ['sump4(0, genLepZ1_pt,genLepZ1_eta,genLepZ1_phi,genLepZ1_mass,genLepZ2_pt,genLepZ2_eta,genLepZ2_phi,genLepZ2_mass):sump4(0,LepZ1_pt,LepZ1_eta,LepZ1_phi,LepZ1_mass,LepZ2_pt,LepZ2_eta,LepZ2_phi,LepZ2_mass)']='[0,5,10,15,20,25,30,40,50,60,70,80,90,100,110,120,130,140,160,180,200,250,300]*[0,10,20,30,50,70,90,110,130,160,200,300]' ["LeadJet_mcPt:LeadJet_pt"]='[25,30,35,40,50,60,70,80,90,100,110,120,130,140,160,180,200,250,300]*[25,35,50,70,90,110,130,160,200,300]'  )



### m3Lmet,sump4(3, sump4(0, genLepZ1_pt,genLepZ1_eta,genLepZ1_phi,genLepZ1_mass,genLepZ2_pt,genLepZ2_eta,genLepZ2_phi,genLepZ2_mass),sump4(1, genLepZ1_pt,genLepZ1_eta,genLepZ1_phi,genLepZ1_mass,genLepZ2_pt,genLepZ2_eta,genLepZ2_phi,genLepZ2_mass),sump4(2, genLepZ1_pt,genLepZ1_eta,genLepZ1_phi,genLepZ1_mass,genLepZ2_pt,genLepZ2_eta,genLepZ2_phi,genLepZ2_mass),sump4(3, genLepZ1_pt,genLepZ1_eta,genLepZ1_phi,genLepZ1_mass,genLepZ2_pt,genLepZ2_eta,genLepZ2_phi,genLepZ2_mass),sump4(0, genLepW_pt,genLepW_eta,genLepW_phi,genLepW_mass,met_genPt,met_genEta,met_genPhi,0),sump4(1, genLepW_pt,genLepW_eta,genLepW_phi,genLepW_mass,met_genPt,met_genEta,met_genPhi,0),sump4(2, genLepW_pt,genLepW_eta,genLepW_phi,genLepW_mass,met_genPt,met_genEta,met_genPhi,0),sump4(3, genLepW_pt,genLepW_eta,genLepW_phi,genLepW_mass,met_genPt,met_genEta,met_genPhi,0))



count=0

#mca=".wzsm/mca_includes.txt"
mca="./wzsm/mca_unfoldingInputs.txt"
mca="./wzsm/mca_unfolding.txt"
inputdir="/pool/ciencias/HeppyTrees/RA7/estructura/wzSkimmed/"
inputdir="/pool/ciencias/HeppyTrees/RA7/wz/wzUnskimmed/"
baseoutputdir="/nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding/responses_CHOCHO/"
#baseoutputdir="tempo/"
fts="--Fs {P}/lepgenVarsWZSM --Fs {P}/leptonJetReCleanerWZSM --Fs {P}/leptonBuilderWZSM --FMCs {P}/bTagEventWeightFullSimWZ30 "
#processes="-p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata.* --plotgroup fakes_appldata+=promptsub "
processes=" -p prompt_altWZ.* "

for iShape in "${!pairs[@]}"; do
    iRange=${pairs[$iShape]}

    echo "echo \"${iShape}, range ${iRange}, count ${count}\""
    echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir}  ${fts}  -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' ${processes} --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od ${baseoutputdir}incl_fitWZonly/ -o WZSR -E SR  --neglist promptsub --autoMCStats --asimov"

    echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir}  ${fts}  -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' ${processes} --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od ${baseoutputdir}eee_fitWZonly/ -o WZSR -E SR -E eee --neglist promptsub --autoMCStats --asimov"

    echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir}  ${fts}  -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' ${processes} --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od ${baseoutputdir}eem_fitWZonly/ -o WZSR -E SR -E eem --neglist promptsub --autoMCStats --asimov"

    echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir}  ${fts}  -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' ${processes} --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od ${baseoutputdir}mme_fitWZonly/ -o WZSR -E SR -E mme --neglist promptsub --autoMCStats --asimov"

    echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir}  ${fts}  -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' ${processes} --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od ${baseoutputdir}mmm_fitWZonly/ -o WZSR -E SR -E mmm --neglist promptsub --autoMCStats --asimov"


    
    #echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir}  ${fts}  -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' ${processes} --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od ${baseoutputdir}incl_fitWZonly/ -o ZZCR -E ZZCR  --neglist promptsub --autoMCStats --asimov"

    #echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir}  ${fts}  -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' ${processes} --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od ${baseoutputdir}incl_fitWZonly/ -o TTCR -E TTCR  --neglist promptsub --autoMCStats --asimov"

    #echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir}  ${fts}  -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' ${processes} --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od ${baseoutputdir}incl_fitWZonly/  -o CONVCR -E convCR --neglist promptsub --autoMCStats --asimov"

    #echo "python makeShapeCardsSusy.py ${mca} ./wzsm/cuts_wzsm.txt '${iShape}' '${iRange}' ./wzsm/systs_wz.txt -P ${inputdir}  ${fts}  -j 64 -l 35.9 --s2v --s2v --tree treeProducerSusyMultilepton --mcc wzsm/mcc_varsub_wzsm.txt --mcc wzsm/mcc_triggerdefs.txt -f -W ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,1)*bTagWeight ' ${processes} --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc  --load-macro wzsm/functionsWZ.cc --od ${baseoutputdir}incl_closureFakes_fitWZonly/  -o DYCR -E DYCR --neglist promptsub --autoMCStats --asimov"

    ###if    [ "$count" == "0" ]; then
    ###    echo "rm -r ${baseoutputdir}incl_fitWZonly_nJet30/"
    ###    echo "mv ${baseoutputdir}incl_fitWZonly/ ${baseoutputdir}incl_fitWZonly_nJet30/"
    if    [ "$count" == "0" ]; then
        echo "rm -r ${baseoutputdir}incl_fitWZonly_Zpt/"
        echo "mv ${baseoutputdir}incl_fitWZonly/ ${baseoutputdir}incl_fitWZonly_Zpt/"

        echo "rm -r ${baseoutputdir}eee_fitWZonly_Zpt/"
        echo "mv ${baseoutputdir}eee_fitWZonly/ ${baseoutputdir}eee_fitWZonly_Zpt/"

        echo "rm -r ${baseoutputdir}eem_fitWZonly_Zpt/"
        echo "mv ${baseoutputdir}eem_fitWZonly/ ${baseoutputdir}eem_fitWZonly_Zpt/"

        echo "rm -r ${baseoutputdir}mme_fitWZonly_Zpt/"
        echo "mv ${baseoutputdir}mme_fitWZonly/ ${baseoutputdir}mme_fitWZonly_Zpt/"

        echo "rm -r ${baseoutputdir}mmm_fitWZonly_Zpt/"
        echo "mv ${baseoutputdir}mmm_fitWZonly/ ${baseoutputdir}mmm_fitWZonly_Zpt/"

    elif [ "$count" == "1" ]; then
        echo "rm -r ${baseoutputdir}incl_fitWZonly_LeadJetPt/"
        echo "mv ${baseoutputdir}incl_fitWZonly/ ${baseoutputdir}incl_fitWZonly_LeadJetPt/"

        echo "rm -r ${baseoutputdir}eee_fitWZonly_LeadJetPt/"
        echo "mv ${baseoutputdir}eee_fitWZonly/ ${baseoutputdir}eee_fitWZonly_LeadJetPt/"

        echo "rm -r ${baseoutputdir}eem_fitWZonly_LeadJetPt/"
        echo "mv ${baseoutputdir}eem_fitWZonly/ ${baseoutputdir}eem_fitWZonly_LeadJetPt/"

        echo "rm -r ${baseoutputdir}mme_fitWZonly_LeadJetPt/"
        echo "mv ${baseoutputdir}mme_fitWZonly/ ${baseoutputdir}mme_fitWZonly_LeadJetPt/"

        echo "rm -r ${baseoutputdir}mmm_fitWZonly_LeadJetPt/"
        echo "mv ${baseoutputdir}mmm_fitWZonly/ ${baseoutputdir}mmm_fitWZonly_LeadJetPt/"

    fi
    ###elif [ "$count" == "2" ]; then
    ###    echo "rm -r ${baseoutputdir}incl_fitWZonly_ZconePt/"
    ###    echo "mv ${baseoutputdir}incl_fitWZonly/ ${baseoutputdir}incl_fitWZonly_ZconePt/"
    ###fi
    let "count=count+1"
done
