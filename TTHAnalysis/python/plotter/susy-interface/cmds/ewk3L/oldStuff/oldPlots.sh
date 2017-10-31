#!/bin/bash

T="/mnt/t3nfs01/data01/shome/cheidegg/o/2015-11-29_ewkskims80X_M17_MERGED"
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-12-09_ewk80X_mccTest" # Do NOT give a trailing /
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-12-09_ewk80X_test" # Do NOT give a trailing /
O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-12-09_ewk80X_fullstatusAll" # Do NOT give a trailing /
L=17.3
FL=36.5
QUEUE="" #"-q all.q"

## WITH LOGARITHMIC SCALE
## =================================================================

## signal regions and baseline regions plots
## -----------------------------------------------------------------

## data fakes
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l $L  --make data --plots perCateg -o SR   --flags '--perBin' $QUEUE
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK"     $T $O -l $L  --make data --plots perCateg -o SR   --flags '--perBin' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l $L  --make data --plots evt      -o SR   --flags '--perBin' $QUEUE
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK"     $T $O -l $L  --make data --plots evt      -o SR   --flags '--perBin' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l $L  --make data --plots lep      -o SR   --flags '--perBin' $QUEUE
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK"     $T $O -l $L  --make data --plots lep      -o SR   --flags '--perBin' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt

### MC fakes
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l $L  --make data --plots perCateg -o SRmc --flags '--perBin --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" 
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK"     $T $O -l $L  --make data --plots perCateg -o SRmc --flags '--perBin --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" --mccs susy-ewkino/4l/mcc_ewkino.txt
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l $L  --make data --plots evt      -o SRmc --flags '--perBin --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" 
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK"     $T $O -l $L  --make data --plots evt      -o SRmc --flags '--perBin --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" --mccs susy-ewkino/4l/mcc_ewkino.txt
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l $L  --make data --plots lep      -o SRmc --flags '--perBin --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" 
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK"     $T $O -l $L  --make data --plots lep      -o SRmc --flags '--perBin --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" --mccs susy-ewkino/4l/mcc_ewkino.txt
#
### sideband
### -----------------------------------------------------------------
#
## MC fakes
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l $FL --make data --plots perCateg -o SBfakes --flags '-X blinding -I SRevent --perBin --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" 
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK"     $T $O -l $FL --make data --plots perCateg -o SBfakes --flags '-X blinding -I SRevent --perBin --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" --mccs susy-ewkino/4l/mcc_ewkino.txt
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l $FL --make data --plots evt      -o SBfakes --flags '-X blinding -I SRevent --perBin --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" 
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK"     $T $O -l $FL --make data --plots evt      -o SBfakes --flags '-X blinding -I SRevent --perBin --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" --mccs susy-ewkino/4l/mcc_ewkino.txt
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l $FL --make data --plots lep      -o SBfakes --flags '-X blinding -I SRevent --perBin --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" 
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK"     $T $O -l $FL --make data --plots lep      -o SBfakes --flags '-X blinding -I SRevent --perBin --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" --mccs susy-ewkino/4l/mcc_ewkino.txt
#
#
#
### NO LOGARITHMIC SCALE
### =================================================================
O="${O}_noLog"
#
### signal regions and baseline regions plots
### -----------------------------------------------------------------
#
## data fakes
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l $L --make data --plots perCateg -o SR   --flags '--perBin' $QUEUE --plot susy-ewkino/3l/plots_ewkino_nolog.txt
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK"     $T $O -l $L --make data --plots perCateg -o SR   --flags '--perBin' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt --plot susy-ewkino/3l/plots_ewkino_nolog.txt
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l $L --make data --plots evt      -o SR   --flags '--perBin' $QUEUE --plot susy-ewkino/3l/plots_ewkino_nolog.txt
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK"     $T $O -l $L --make data --plots evt      -o SR   --flags '--perBin' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt --plot susy-ewkino/3l/plots_ewkino_nolog.txt
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l $L --make data --plots lep      -o SR   --flags '--perBin' $QUEUE --plot susy-ewkino/3l/plots_ewkino_nolog.txt
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK"     $T $O -l $L --make data --plots lep      -o SR   --flags '--perBin' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt --plot susy-ewkino/3l/plots_ewkino_nolog.txt
#
## MC fakes
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l $L --make data --plots perCateg -o SRmc --flags '--perBin --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" --plot susy-ewkino/3l/plots_ewkino_nolog.txt
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK"     $T $O -l $L --make data --plots perCateg -o SRmc --flags '--perBin --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" --mccs susy-ewkino/4l/mcc_ewkino.txt --plot susy-ewkino/3l/plots_ewkino_nolog.txt
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l $L --make data --plots evt      -o SRmc --flags '--perBin --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" --plot susy-ewkino/3l/plots_ewkino_nolog.txt
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK"     $T $O -l $L --make data --plots evt      -o SRmc --flags '--perBin --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" --mccs susy-ewkino/4l/mcc_ewkino.txt --plot susy-ewkino/3l/plots_ewkino_nolog.txt
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l $L --make data --plots lep      -o SRmc --flags '--perBin --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" --plot susy-ewkino/3l/plots_ewkino_nolog.txt
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK"     $T $O -l $L --make data --plots lep      -o SRmc --flags '--perBin --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" --mccs susy-ewkino/4l/mcc_ewkino.txt --plot susy-ewkino/3l/plots_ewkino_nolog.txt
#
### sideband
### -----------------------------------------------------------------
#
## MC fakes
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l $FL --make data --plots perCateg -o SBfakes --flags '-X blinding -I SRevent --perBin --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST --plotgroup prompt_WZ+=nonprompt_WZ --plotgroup prompt_ZZH+=nonprompt_ZZH --plotgroup rares_ttX+=nonprompt_ttX --plotgroup rares_VVV+=nonprompt_VVV' $QUEUE -p "fakes_matched_.*;nonprompt_.*;prompt_.*;rares_.*;convs;data" --plot susy-ewkino/3l/plots_ewkino_nolog.txt 
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK"     $T $O -l $FL --make data --plots perCateg -o SBfakes --flags '-X blinding -I SRevent --perBin --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST --plotgroup prompt_WZ+=nonprompt_WZ --plotgroup prompt_ZZH+=nonprompt_ZZH --plotgroup rares_ttX+=nonprompt_ttX --plotgroup rares_VVV+=nonprompt_VVV' $QUEUE -p "fakes_matched_.*;nonprompt_.*;prompt_.*;rares_.*;convs;data" --mccs susy-ewkino/4l/mcc_ewkino.txt --plot susy-ewkino/3l/plots_ewkino_nolog.txt
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l $FL --make data --plots evt      -o SBfakes --flags '-X blinding -I SRevent --perBin --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" --plot susy-ewkino/3l/plots_ewkino_nolog.txt
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK"     $T $O -l $FL --make data --plots evt      -o SBfakes --flags '-X blinding -I SRevent --perBin --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" --mccs susy-ewkino/4l/mcc_ewkino.txt --plot susy-ewkino/3l/plots_ewkino_nolog.txt
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l $FL --make data --plots lep      -o SBfakes --flags '-X blinding -I SRevent --perBin --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" --plot susy-ewkino/3l/plots_ewkino_nolog.txt
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK"     $T $O -l $FL --make data --plots lep      -o SBfakes --flags '-X blinding -I SRevent --perBin --plotgroup fakes_matched_DY+=fakes_matched_WW --plotgroup fakes_matched_DY+=fakes_matched_WJ --plotgroup fakes_matched_DY+=fakes_matched_TT --plotgroup fakes_matched_DY+=fakes_matched_ST' $QUEUE -p "fakes_matched_.*;prompt_.*;rares_.*;convs;data" --mccs susy-ewkino/4l/mcc_ewkino.txt --plot susy-ewkino/3l/plots_ewkino_nolog.txt

