
T="/mnt/t3nfs01/data01/shome/cheidegg/o/2015-11-29_ewkskims80X_M17_MERGED/"
#T="/mnt/t3nfs01/data01/shome/cheidegg/o/2015-11-29_ewkskims80X_M17"
O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-12-07_ewk80X_fullstatus_noLog"
python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots met      -o SR --flags '--perBin' $QUEUE --mca susy-ewkino/3l/mca_ewkino_merged.txt
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots met      -o SR --flags '--perBin' $QUEUE
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots mtW3l    -o SR --flags '--perBin' $QUEUE
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots mll3l    -o SR --flags '--perBin' $QUEUE
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots mT2T3l   -o SR --flags '--perBin' $QUEUE
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots mT2L3l   -o SR --flags '--perBin' $QUEUE
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots flavor3l -o SR --flags '--perBin' $QUEUE
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots charge3l -o SR --flags '--perBin' $QUEUE
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 17.3 --make data --selPlots flavor4l -o SR --flags '--perBin -j 4' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
#python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 17.3 --make data --selPlots charge4l -o SR --flags '--perBin -j 4' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
