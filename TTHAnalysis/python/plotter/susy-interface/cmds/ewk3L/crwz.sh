
T="/mnt/t3nfs01/data01/shome/cheidegg/o/2015-11-29_ewktrees80X_M17/"
LUMI=35.9

python mcPlots.py susy-ewkino/crwz/mca_crwz_FSR.txt susy-ewkino/crwz/cuts_crwz.txt susy-ewkino/crwz/plots_crwz.txt -P /afs/cern.ch/work/c/cheidegg/scratch/newDataFriends/ --Fs {P}/leptonJetReCleanerSusyEWK2L --Fs {P}/leptonBuilderEWK --pdir ~/WZCR_EWK_test -j 6 -l $LUMI --s2v --tree treeProducerSusyMultilepton --mcc susy-ewkino/crwz/lepchoice-crwz-FO.txt --mcc susy-ewkino/mcc_triggerdefs.txt --legendWidth 0.18 --legendFontSize 0.030  -f --sP 'mT_3l,mll_3l,MET_WZ,nJet40,htJet40_WZ' --perBin -p data -p prompt.* -p convs -p fakes_appldata --plotgroup fakes_appldata+=promptsub  -W 'puw_nInt_Moriond(nTrueInt)*getLepSF(LepGood1_conePt,LepGood1_eta,LepGood1_pdgId,1)*getLepSF(LepGood2_conePt,LepGood2_eta,LepGood2_pdgId,1)*getLepSF(LepGood3_conePt,LepGood3_eta,LepGood3_pdgId,1)' --showMCError --load-macro susy-ewkino/functionsSF.cc --load-macro susy-ewkino/functionsPUW.cc --print 'C,pdf,png,txt'
