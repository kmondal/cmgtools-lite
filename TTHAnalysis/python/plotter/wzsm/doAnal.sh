#!/bin/bash

 
#INPUTDIR="/pool/ciencias/HeppyTrees/RA7/estructura/treesM17" #Use skimmed (3LepGood, minMllAFAS > 4) instead
INPUTDIR="/pool/ciencias/userstorage/carlosec/wzSkimmed/"
TREESDIR=${INPUTDIR}                                                                                     
OUTPUTDIR="/OBSOLETE"                                                                                    
WEBDIR="/nfs/fanae/user/carlosec/www/wz/"                                            

#    mcPlots.py WZSM/mca_includes.txt WZSM/cuts_wzsm.txt WZSM/plots_wzsm.txt -P  --Fs {P}/leptonJetReCleanerWZSM --Fs {P}/leptonBuilderWZSM --FMCs {P}/bTagEventWeightFullSimWZ30 --pdir /nfs/fanae/user/nachos/www/WZ2016/mWZ_varbin -j 24 -l 35.867 --s2v --tree treeProducerSusyMultilepton --mcc WZSM/mcc_varsub_wzsm.txt --mcc WZSM/mcc_triggerdefs.txt --legendWidth 0.18 --legendFontSize 0.026 -f --sP m3l_l,m3lmet_l --perBin -p data -p prompt.* -p rares.* -p fakes_appldata --plotgroup fakes_appldata+=promptsub --neglist promptsub -W puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1)*bTagWeight --showMCError --load-macro WZSM/functionsPUW.cc --load-macro WZSM/functionsSF.cc --load-macro WZSM/functionsWZ.cc --print C,pdf,png,txt --showRatio --ratioOffset 0.03 --maxRatioRange 0.5 2.0 --fixRatioRange --env oviedo



if [ "$1" == "all" ]; then
    sh wzsm/doAnal.sh plot srwz VT ${2}
    sh wzsm/doAnal.sh plot ttcr VT ${2}
    sh wzsm/doAnal.sh plot dycr VT ${2}
    sh wzsm/doAnal.sh plot srwz M  ${2}
    sh wzsm/doAnal.sh plot ttcr M  ${2}
    sh wzsm/doAnal.sh plot dycr M  ${2}

    sh wzsm/doAnal.sh plot srwz VT ${2}  mc
    sh wzsm/doAnal.sh plot ttcr VT ${2}  mc
    sh wzsm/doAnal.sh plot dycr VT ${2}  mc
    sh wzsm/doAnal.sh plot srwz M  ${2} mc
    sh wzsm/doAnal.sh plot ttcr M  ${2} mc
    sh wzsm/doAnal.sh plot dycr M  ${2} mc

    sh wzsm/doAnal.sh plot srwz T ${2}  pog
    sh wzsm/doAnal.sh plot ttcr T ${2}  pog
    sh wzsm/doAnal.sh plot dycr T ${2}  pog
    sh wzsm/doAnal.sh plot srwz M  ${2} pog
    sh wzsm/doAnal.sh plot ttcr M  ${2} pog
    sh wzsm/doAnal.sh plot dycr M  ${2} pog

    sh wzsm/doAnal.sh plot srwz T ${2}  pogmc
    sh wzsm/doAnal.sh plot ttcr T ${2}  pogmc
    sh wzsm/doAnal.sh plot dycr T ${2}  pogmc
    sh wzsm/doAnal.sh plot srwz M  ${2} pogmc
    sh wzsm/doAnal.sh plot ttcr M  ${2} pogmc
    sh wzsm/doAnal.sh plot dycr M  ${2} pogmc
    
elif [ "$1" == "SR" ]; then
    sh wzsm/doAnal.sh plot dycr VT ${2}
    sh wzsm/doAnal.sh plot dycr M  ${2}

elif [ "$1" == "TT" ]; then
    sh wzsm/doAnal.sh plot dycr VT ${2}
    sh wzsm/doAnal.sh plot dycr M  ${2}

elif [ "$1" == "DY" ]; then
    sh wzsm/doAnal.sh plot dycr VT ${2}
    sh wzsm/doAnal.sh plot dycr M  ${2}

elif [ "$1" == "VT" ]; then
    sh wzsm/doAnal.sh plot srwz VT
    sh wzsm/doAnal.sh plot ttcr VT
    sh wzsm/doAnal.sh plot dycr VT
    sh wzsm/doAnal.sh plot llnot VT 

elif [ "$1" == "M" ]; then
    sh wzsm/doAnal.sh plot srwz M
    sh wzsm/doAnal.sh plot ttcr M
    sh wzsm/doAnal.sh plot dycr M

elif [ "$1" == "mc" ]; then
    sh wzsm/doAnal.sh plot mcsrwz VT ${2} mc
    sh wzsm/doAnal.sh plot mcttcr VT ${2} mc
    sh wzsm/doAnal.sh plot mcdycr VT ${2} mc
    sh wzsm/doAnal.sh plot mcsrwz M  ${2} mc
    sh wzsm/doAnal.sh plot mcttcr M  ${2} mc
    sh wzsm/doAnal.sh plot mcdycr M  ${2} mc
    
    sh wzsm/doAnal.sh plot srwz T ${2}  pogmc
    sh wzsm/doAnal.sh plot ttcr T ${2}  pogmc
    sh wzsm/doAnal.sh plot dycr T ${2}  pogmc
    sh wzsm/doAnal.sh plot srwz M  ${2} pogmc
    sh wzsm/doAnal.sh plot ttcr M  ${2} pogmc
    sh wzsm/doAnal.sh plot dycr M  ${2} pogmc


elif [ "$1" == "plot" ]; then
    
    ACTION=""
    WP=""
    SUBACTION=""
    STUFF=""
    # ACTION can be general
    
    if [ "$2" == "" ]; then
        echo "ACTION is empty. It can be 'srwz' or 'crwz' or 'www'"
        exit -1
    else
        ACTION=" -a ${2}"
        if [ "$3" != "" ]; then
            WP=" -w ${3} "
            if [ "$4" != "" ]; then
                SUBACTION=" -s ${4} "
                if [ "$5" == "pog" ]; then
                    STUFF=" --pog "
                elif [ "$5" == "mc" ]; then
                    STUFF=" --mconly "
                elif [ "$5" != "" ]; then
                    STUFF=" --pog --mconly "
                fi
            fi
        fi
    fi
    
    PRETEND=" --pretend  "
#    PRETEND=""
    python wzsm/doAnal.py -i ${INPUTDIR} -o ${WEBDIR} $STUFF ${WP} ${ACTION} ${SUBACTION} ${PRETEND}

elif [ "$1" == "fr" ]; then
    
    frstring="sMiX4mrE2"

    sh ttH-multilepton/make_fake_rates_MC.sh susy $frstring


#sh ../python/plotter/susy-interface/cmds/tau-ewkino/chunkDealer.sh  /nfs/fanae/user/vischia/workarea/cmssw/wz/fts/leptonJetReCleanerSusyEWK2L/ merge evVarFriend


fi
exit 0
