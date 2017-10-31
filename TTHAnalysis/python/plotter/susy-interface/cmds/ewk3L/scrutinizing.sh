#!/bin/bash

T="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-11-29_ewkskims80X_M17_MERGED"
O="/afs/cern.ch/user/c/cheidegg/www/heppy/2017-01-09_ewk80X_scrutinizing" # Do NOT give a trailing /
L=35.9
FL=35.9
QUEUE="" #"-q all.q"
BLIND="-X blinding" #""

#python susy-interface/plotmaker.py 3l "3lC" $T $O -l $L  --make data --plots perCateg -o SR   --flags "--perBin -X filters $BLIND" $QUEUE

#python susy-interface/plotmaker.py 3l "4lJ;4lK" $T $O -l $L  --make data --plots perCateg -o SRmc --flags "--perBin $BLIND" $QUEUE -p "fakes_matched;prompt_.*;rares_.*;convs;data" 

python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l $L  --make data --selPlots "minDR3l;minDR3lmm" -o SR   --flags "--perBin $BLIND" $QUEUE
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK"     $T $O -l $L  --make data --selPlots "minDR4l;minDR4lmm" -o SR   --flags "--perBin $BLIND" $QUEUE
