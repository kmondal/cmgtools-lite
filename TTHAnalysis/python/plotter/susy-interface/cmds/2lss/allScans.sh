#!/bin/bash

## IMPORTANT REMARK: In principle, one could run all models per config/region all together,
## but this will generate a lot of jobs which are all accessing the same background ROOT file.
## This kills memory and performance. Keep in mind to split as good and effective as possible
## to optimize performance.

T="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-11-29_ewkskims80X_M17_MERGED/"  ## tree directory
O="/mnt/t3nfs01/data01/shome/cheidegg/o/2017-01-09_ewk80X_scanTest"          ## output directory
QUEUE="" #"-q 1nh"
FLAGS="" #"-X blinding"
LUMI=36.5


## background only first
#python susy-interface/scanmaker.py 2lss 2lss $T $O -l $LUMI -o SR --models TChiNeuWZ --flags '$FLAGS' --bkgOnly --redoBkg $QUEUE 

## TChiNeuWH
#python susy-interface/scanmaker.py 2lss 2lss $T $O -l $LUMI -o SR --models TChiNeuWH --flags '$FLAGS' --sigOnly $QUEUE --postfix '--postfix-pred fakes_appldata*=fixFakePredictionForZeroEvts --frFile $CMSSW_BASE/src/CMGTools/TTHAnalysis/data/fakerate/fakerate_light_EWKino_Moriond2017_36p5fb.root --frMap FR_susy_wpV_FL_data_comb' --check

## TChiNeuWZ
#python susy-interface/scanmaker.py 2lss 2lss $T $O -l $LUMI -o SR --models TChiNeuWZ --flags '$FLAGS' --sigOnly $QUEUE --postfix '--postfix-pred fakes_appldata*=fixFakePredictionForZeroEvts --frFile $CMSSW_BASE/src/CMGTools/TTHAnalysis/data/fakerate/fakerate_light_EWKino_Moriond2017_36p5fb.root --frMap FR_susy_wpV_FL_data_comb' --check

## TChiNeuSlepSneu_FD
#python susy-interface/scanmaker.py 2lss 2lss $T $O -l $LUMI -o SR --models TChiNeuSlepSneu_FD --flags '$FLAGS' --sigOnly $QUEUE --postfix '--postfix-pred fakes_appldata*=fixFakePredictionForZeroEvts --frFile $CMSSW_BASE/src/CMGTools/TTHAnalysis/data/fakerate/fakerate_light_EWKino_Moriond2017_36p5fb.root --frMap FR_susy_wpV_FL_data_comb' --check

## TChiNeuSlepSneu_05
#python susy-interface/scanmaker.py 2lss 2lss $T $O -l $LUMI -o SR --models TChiNeuSlepSneu_FD --flags '$FLAGS' --sigOnly $QUEUE --postfix '--postfix-pred fakes_appldata*=fixFakePredictionForZeroEvts --frFile $CMSSW_BASE/src/CMGTools/TTHAnalysis/data/fakerate/fakerate_light_EWKino_Moriond2017_36p5fb.root --frMap FR_susy_wpV_FL_data_comb' --check

## TChiNeuSlepSneu_95
#python susy-interface/scanmaker.py 2lss 2lss $T $O -l $LUMI -o SR --models TChiNeuSlepSneu_FD --flags '$FLAGS' --sigOnly $QUEUE --postfix '--postfix-pred fakes_appldata*=fixFakePredictionForZeroEvts --frFile $CMSSW_BASE/src/CMGTools/TTHAnalysis/data/fakerate/fakerate_light_EWKino_Moriond2017_36p5fb.root --frMap FR_susy_wpV_FL_data_comb' --check

