#!/bin/bash

 
INPUTDIR="/pool/ciencias/HeppyTrees/RA7/estructura/treesM17"
TREESDIR=${INPUTDIR}                                                                                     
OUTPUTDIR="/OBSOLETE"                                                                                    
WEBDIR="/nfs/fanae/user/vischia/www/wz/"                                            

#    mcPlots.py WZSM/mca_includes.txt WZSM/cuts_wzsm.txt WZSM/plots_wzsm.txt -P  --Fs {P}/leptonJetReCleanerWZSM --Fs {P}/leptonBuilderWZSM --FMCs {P}/bTagEventWeightFullSimWZ30 --pdir /nfs/fanae/user/nachos/www/WZ2016/mWZ_varbin -j 24 -l 35.867 --s2v --tree treeProducerSusyMultilepton --mcc WZSM/mcc_varsub_wzsm.txt --mcc WZSM/mcc_triggerdefs.txt --legendWidth 0.18 --legendFontSize 0.026 -f --sP m3l_l,m3lmet_l --perBin -p data -p prompt.* -p rares.* -p fakes_appldata --plotgroup fakes_appldata+=promptsub --neglist promptsub -W puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1)*bTagWeight --showMCError --load-macro WZSM/functionsPUW.cc --load-macro WZSM/functionsSF.cc --load-macro WZSM/functionsWZ.cc --print C,pdf,png,txt --showRatio --ratioOffset 0.03 --maxRatioRange 0.5 2.0 --fixRatioRange --env oviedo

    
if [ "$1" == "plot" ]; then
    
    ACTION=""
    SUBACTION=""
    # ACTION can be general
    
    if [ "$2" == "" ]; then
        echo "ACTION is empty. It can be 'srwz' or 'crwz' or 'www'"
        exit -1
    else
        ACTION=" -a ${2}"
        if [ "$3" != "" ]; then
            SUBACTION=" -s ${3} "
        fi
    fi
    
    PRETEND=" --pretend  "
    PRETEND=""
    python wzsm/doAnal.py -i ${INPUTDIR} -o ${WEBDIR} ${ACTION} ${SUBACTION} ${PRETEND}

elif [ "$1" == "fr" ]; then
    
    frstring="sMiX4mrE2"

    sh ttH-multilepton/make_fake_rates_MC.sh susy $frstring
fi
exit 0