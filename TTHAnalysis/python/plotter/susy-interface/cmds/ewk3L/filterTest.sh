#!/bin/bash

T="/mnt/t3nfs01/data01/shome/cheidegg/o/2017-01-27_ewkskims80X_M17_MERGED"
O="/afs/cern.ch/user/c/cheidegg/www/heppy/2017-02-01_ewk80X_preapproval_oldFilters" # Do NOT give a trailing /
L=35.9
FL=35.9
QUEUE="" #"-q all.q"
BLIND="-X blinding -R filters filters '\$DATA{METfiltersOld} \$MC{1} \$FASTSIM{1}'" #""

## signal regions and baseline regions plots
## -----------------------------------------------------------------

## data fakes
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l $L  --make data --plots perCateg -o SR   --flags "--perBin $BLIND" $QUEUE
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l $L  --make data --plots evt      -o SR   --flags "--perBin $BLIND" $QUEUE
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l $L  --make data --plots lep      -o SR   --flags "--perBin $BLIND" $QUEUE
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lF;4lG;4lH;4lI;4lJ;4lK" $T $O -l $L  --make data --plots perCateg -o SR   --flags "--perBin $BLIND" $QUEUE
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lF;4lG;4lH;4lI;4lJ;4lK" $T $O -l $L  --make data --plots evt      -o SR   --flags "--perBin $BLIND" $QUEUE
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lF;4lG;4lH;4lI;4lJ;4lK" $T $O -l $L  --make data --plots lep      -o SR   --flags "--perBin $BLIND" $QUEUE
#python susy-interface/plotmaker.py 3l "3lE"                                     $T $O -l $L  --make data --plots perCateg -o SR   --flags "--perBin $BLIND" $QUEUE -p "fakes_appldata;flips_appldata;prompt_.*;rares_.*;convs;data"
#python susy-interface/plotmaker.py 3l "3lE"                                     $T $O -l $L  --make data --plots evt      -o SR   --flags "--perBin $BLIND" $QUEUE -p "fakes_appldata;flips_appldata;prompt_.*;rares_.*;convs;data"
#python susy-interface/plotmaker.py 3l "3lE"                                     $T $O -l $L  --make data --plots lep      -o SR   --flags "--perBin $BLIND" $QUEUE -p "fakes_appldata;flips_appldata;prompt_.*;rares_.*;convs;data"


## bad Muon Pt
## -----------------------------------------------------------------

python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lF;4lG;4lH;4lI;4lJ;4lK" $T $O -l $L --make data --selPlots "mu_pt_badClone;mu_pt_badNotClone" -o SR --flags "--perBin $BLIND --emptyStack" $QUEUE -p "dataBkg"

O="/afs/cern.ch/user/c/cheidegg/www/heppy/2017-02-01_ewk80X_preapproval" # Do NOT give a trailing /
BLIND="-X blinding"
python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lF;4lG;4lH;4lI;4lJ;4lK" $T $O -l $L --make data --selPlots "mu_pt_badClone;mu_pt_badNotClone" -o SR --flags "--perBin $BLIND --emptyStack" $QUEUE -p "dataBkg"
