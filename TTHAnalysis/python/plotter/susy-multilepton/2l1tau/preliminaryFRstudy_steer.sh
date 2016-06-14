#!/bin/bash

ANALYZER=../../mcAnalysis.py
PLOTTER=../../mcPlots.py

TREESPATH=/afs/cern.ch/user/i/igsuarez/work/public/trees76Xv2/
TREE=treeProducerSusyMultilepton

MCA=preliminaryFRstudy_mca.txt
CUTS=preliminaryFRstudy_cuts.txt
MCC=mcc_susy_2lssinc_triggerdefs.txt

PLOTS=preliminaryFRstudy_plots.txt

PLOTSDIR=~/www/susyRA7/

NPROC=8

LUMI=10.0

if [ "${1}" = "anal" ]; then

    python ${ANALYZER} ${MCA} ${CUTS} --path ${TREESPATH} --tree ${TREE}  --lumi ${LUMI} --s2v -j ${NPROC} --Fs ${TREESPATH}leptonJetReCleanerSusyRA7mva --Fs ${TREESPATH}leptonChoiceEWK --mcc ${MCC} -f -G

elif [ "${1}" = "plot" ]; then

    # TT
    python ${PLOTTER} --exclude-process data --exclude-process DY ${MCA} ${CUTS} ${PLOTS} --path ${TREESPATH} --tree ${TREE} --lumi ${LUMI} --s2v -j ${NPROC} --Fs ${TREESPATH}leptonJetReCleanerSusyRA7mva --Fs ${TREESPATH}leptonChoiceEWK -mcc ${MCC} -f --rspam "%(lumi) (13 TeV)" --lspam "#bf{CMS} #it{Preliminary}" --legendBorder=0 --legendFontSize 0.055 --legendWidth=0.30 --showMCError --pdir ${PLOTSDIR}

    # DY
    python ${PLOTTER} --exclude-process data --exclude-process TT ${MCA} ${CUTS} ${PLOTS} --path ${TREESPATH} --tree ${TREE} --lumi ${LUMI} --s2v -j ${NPROC} --Fs ${TREESPATH}leptonJetReCleanerSusyRA7mva --Fs ${TREESPATH}leptonChoiceEWK -mcc ${MCC} -f --rspam "%(lumi) (13 TeV)" --lspam "#bf{CMS} #it{Preliminary}" --legendBorder=0 --legendFontSize 0.055 --legendWidth=0.30 --showMCError --pdir ${PLOTSDIR}

    # Data
    python ${PLOTTER} --exclude-process TT --exclude-process DY ${MCA} ${CUTS} ${PLOTS} --path ${TREESPATH} --tree ${TREE} --lumi ${LUMI} --s2v -j ${NPROC} --Fs ${TREESPATH}leptonJetReCleanerSusyRA7mva --Fs ${TREESPATH}leptonChoiceEWK -mcc ${MCC} -f --rspam "%(lumi) (13 TeV)" --lspam "#bf{CMS} #it{Preliminary}" --legendBorder=0 --legendFontSize 0.055 --legendWidth=0.30 --showMCError --pdir ${PLOTSDIR}
fi


exit 0