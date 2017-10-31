#!/bin/bash

T="/mnt/t3nfs01/data01/shome/cheidegg/o/2017-02-23_ewkskims80X_M17_3l_bkg;/mnt/t3nfs01/data01/shome/cheidegg/o/2017-02-23_ewkskims80X_M17_3l_data"
#T="/mnt/t3nfs01/data01/shome/cheidegg/o/2017-01-27_ewkskims80X_M17_MERGED/"
O="/afs/cern.ch/user/c/cheidegg/www/heppy/2017-02-24_ewk80X_frTau_reminiAOD" # Do NOT give a trailing /
L=35.9
FL=35.9
QUEUE="" #"-q all.q"
BLIND="-X blinding" #""

python susy-interface/plotmaker.py frtau frtau $T "${O}_data_denom" -l $L --make bkgs --selPlots map -o MR --flags "--perBin $BLIND --plotgroup dataFakes+=promptsub" $QUEUE
python susy-interface/plotmaker.py frtau frtau $T "${O}_data_num"   -l $L --make bkgs --selPlots map -o MR --flags "--perBin $BLIND --plotgroup dataFakes+=promptsub -A flavor numerator 'allTightTau(3, LepSel1_pdgId, LepSel1_isTight, LepSel2_pdgId, LepSel2_isTight, LepSel3_pdgId, LepSel3_isTight)'" $QUEUE 

python susy-interface/plotmaker.py frtau frtau $T "${O}_dy_denom" -l $L --make bkgs --selPlots map -o MR --flags "--perBin $BLIND -X met" $QUEUE -p "dyFakes" --noWeight --noFlags
python susy-interface/plotmaker.py frtau frtau $T "${O}_dy_num"   -l $L --make bkgs --selPlots map -o MR --flags "--perBin $BLIND -X met -A flavor numerator 'allTightTau(3, LepSel1_pdgId, LepSel1_isTight, LepSel2_pdgId, LepSel2_isTight, LepSel3_pdgId, LepSel3_isTight)'" $QUEUE -p "dyFakes" --noWeight --noFlags 


## postproduction:
#python makeFR.py $O
#python plot2d.py tauFR.root data_ratio --zrange 0.1 0.3
#python plot2d.py tauFR.root dy_ratio --zrange 0.1 0.3 --lspam Simulation
#mv data_ratio.* /afs/cern.ch/user/c/cheidegg/www/dropbox/tauFR/data
#mv dy_ratio.* /afs/cern.ch/user/c/cheidegg/www/dropbox/tauFR/data
