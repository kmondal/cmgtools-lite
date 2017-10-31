#!/bin/bash

T="/mnt/t3nfs01/data01/shome/cheidegg/o/2015-11-29_ewkskims80X_M17_MERGED"
L=17.3
FL=36.5
QUEUE="" #"-q all.q"


## just Testing
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-12-09_ewk80X_testUCSX"
#python susy-interface/plotmaker.py 3l "3lC" $T $O -l $FL --make data --plots perCateg -o SBfakes --flags '-X blinding -I SRevent --perBin --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" --plot susy-ewkino/3l/plots_ewkino_nolog.txt 
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-12-09_ewk80X_testNoSLTriggers"
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l $FL --make data --plots perCateg -o SBfakes --flags '-X blinding -I SRevent --perBin --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST -R trigger triggerDL "!isData || Triggers_DL"' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" --plot susy-ewkino/3l/plots_ewkino_nolog.txt 
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-12-09_ewk80X_testHeppy"
#python susy-interface/plotmaker.py 3l "3lC" $T $O -l $FL --make data --plots perCateg -o SBfakes --flags '-X blinding -I SRevent --perBin --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST --plotgroup prompt_WZ+=nonprompt_WZ --plotgroup prompt_ZZH+=nonprompt_ZZH --plotgroup rares_ttX+=nonprompt_ttX --plotgroup rares_VVV+=nonprompt_VVV' $QUEUE -p "fakes_matched_.*;nonprompt_.*;prompt_.*;rares_.*;convs;data" --plot susy-ewkino/3l/plots_ewkino_nolog.txt 
