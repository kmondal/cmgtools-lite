
T="/mnt/t3nfs01/data01/shome/cheidegg/o/2015-11-29_ewkskims80X_M17"
O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-12-07_ewk80X_fullstatus"

## 3l event observables
echo "starting with 3evt observables"
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots mll3l    -o SR --flags '--perBin -j 4' $QUEUE
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots met      -o SR --flags '--perBin -j 4' $QUEUE
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots mtW3l    -o SR --flags '--perBin -j 4' $QUEUE
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots htJet30j -o SR --flags '--perBin -j 4' $QUEUE
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots nJet30   -o SR --flags '--perBin -j 4' $QUEUE
#python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots nBJet25 -o SR --flags '--perBin -j 4' $QUEUE
python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots m3l     -o SR --flags '--perBin -j 4' $QUEUE
python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots mT2L3l  -o SR --flags '--perBin -j 4' $QUEUE
python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots mT2T3l  -o SR --flags '--perBin -j 4' $QUEUE

## 3l lepton observables
echo "starting with 3lep observables"
python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots el_pt   -o SR --flags '--perBin -j 4' $QUEUE
python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots mu_pt   -o SR --flags '--perBin -j 4' $QUEUE
python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots tau_pt  -o SR --flags '--perBin -j 4' $QUEUE
python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots el_eta  -o SR --flags '--perBin -j 4' $QUEUE
python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots mu_eta  -o SR --flags '--perBin -j 4' $QUEUE
python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots tau_eta -o SR --flags '--perBin -j 4' $QUEUE
python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots lep1_pt -o SR --flags '--perBin -j 4' $QUEUE
python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots lep2_pt -o SR --flags '--perBin -j 4' $QUEUE
python susy-interface/plotmaker.py 3l "3lA;3lB;3lC;3lD;3lE;3lF" $T $O -l 17.3 --make data --selPlots lep3_pt -o SR --flags '--perBin -j 4' $QUEUE

## 4l event observables
echo "starting with 4evt observables"
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 17.3 --make data --selPlots mll4l    -o SR --flags '--perBin -j 4' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 17.3 --make data --selPlots met      -o SR --flags '--perBin -j 4' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 17.3 --make data --selPlots mtW4l    -o SR --flags '--perBin -j 4' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 17.3 --make data --selPlots htJet30j -o SR --flags '--perBin -j 4' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 17.3 --make data --selPlots nJet30   -o SR --flags '--perBin -j 4' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 17.3 --make data --selPlots nBJet25  -o SR --flags '--perBin -j 4' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 17.3 --make data --selPlots m4l      -o SR --flags '--perBin -j 4' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 17.3 --make data --selPlots mT2L4l   -o SR --flags '--perBin -j 4' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 17.3 --make data --selPlots mT2T4l   -o SR --flags '--perBin -j 4' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt

## 4l lepton observables
echo "starting with 4evt observables"
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 17.3 --make data --selPlots el_pt    -o SR --flags '--perBin -j 4' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 17.3 --make data --selPlots mu_pt    -o SR --flags '--perBin -j 4' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 17.3 --make data --selPlots tau_pt   -o SR --flags '--perBin -j 4' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 17.3 --make data --selPlots el_eta   -o SR --flags '--perBin -j 4' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 17.3 --make data --selPlots mu_eta   -o SR --flags '--perBin -j 4' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 17.3 --make data --selPlots tau_eta  -o SR --flags '--perBin -j 4' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 17.3 --make data --selPlots lep1_pt  -o SR --flags '--perBin -j 4' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 17.3 --make data --selPlots lep2_pt  -o SR --flags '--perBin -j 4' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 17.3 --make data --selPlots lep3_pt  -o SR --flags '--perBin -j 4' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt
python susy-interface/plotmaker.py 3l "4lG;4lH;4lI;4lJ;4lK" $T $O -l 17.3 --make data --selPlots lep4_pt  -o SR --flags '--perBin -j 4' $QUEUE --mccs susy-ewkino/4l/mcc_ewkino.txt



