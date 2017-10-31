#!/bin/bash

T="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-11-29_ewkskims80X_M17_MERGED/"
O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-12-19_limitTest"
python susy-interface/limitmaker.py 3l 3lA $T $O -l 17.3 -o SR --sigs "sig_TChiNeuWZ_350_25" --flags '--postfix-pred fakes_appldata*=fixFakePredictionForZeroEvts --frFile /mnt/t3nfs01/data01/shome/cheidegg/d/CMSSW_8_0_20/src/CMGTools/TTHAnalysis/data/fakerate/fakerate_light_EWKino_Moriond2017_36p5fb.root --frMap FR_susy_wpM_FL_data_comb' --finalize --sys susy-ewkino/systs_dummy.txt

