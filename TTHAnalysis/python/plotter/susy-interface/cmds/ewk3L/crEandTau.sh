#!/bin/bash

#T="/mnt/t3nfs01/data01/shome/cheidegg/o/skimsForETauCR/"
T="/mnt/t3nfs01/data01/shome/cheidegg/o/2015-11-29_ewktrees80X_M17"
O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-12-13_ewk80X_eAndTau"
#O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-12-07_ewk80X_eAndTau"
PLOTS="all"
QUEUE="" #"-q all.q"
LUMI=35.9

O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-12-13_ewk80X_eAndTauUCSX"
python susy-interface/plotmaker.py cretau cretau $T $O -l $LUMI --make data --plots $PLOTS -o SR --flags '-X blinding --perBin' -p "fakes_matched_DY;data" --noWeight $QUEUE
#python susy-interface/plotmaker.py cretau cretau $T $O -l $LUMI --make data --plots $PLOTS -o SR --flags '-X blinding --perBin' $QUEUE

