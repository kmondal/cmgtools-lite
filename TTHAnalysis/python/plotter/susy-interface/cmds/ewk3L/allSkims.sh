
##IN="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X"
##OUT="/mnt/t3nfs01/data01/shome/cheidegg/o/2016-07-13_ewkskims80X_fancyPancySkimsy"
##SAMPLES="--allSamples" ## or add them with --samples, or put --procs data
##python susy-interface/skimmaker.py 3l 3lA $T $O $SAMPLES -X blinding -X filters -X trigger -X SRevent -X veto -X convveto -X met 

## 3l and 4l
#T="/mnt/t3nfs01/data01/shome/cheidegg/o/newData/"
#O="/mnt/t3nfs01/data01/shome/cheidegg/o/newDataSkimmed"
#S="--allIn"
#python susy-interface/skimmaker.py 3l 3lA $T $O $S --cuts dummy.txt --accept SingleMuon_Run2016B_03Feb2017_ver2_v2_runs_273150_275376 

### 3l and 4l
#T="/mnt/t3nfs01/data01/shome/cheidegg/o/2017-02-25_ewktrees80X_M17_bkg"
#O="/mnt/t3nfs01/data01/shome/cheidegg/o/2017-02-25_ewkskims80X_M17_3l_bkg"
#S=" --allIn --accept WZZ"
#python susy-interface/skimmaker.py 3l 3lA $T $O $S --cuts susy-ewkino/3l/cuts_skim.txt

## forJuan
#T="/mnt/t3nfs01/data01/shome/cheidegg/o/2017-02-25_ewktrees80X_M17_bkg"
#O="/mnt/t3nfs01/data01/shome/cheidegg/o/2017-02-25_ewkskims80X_M17_2lss_bkg"
#S="-q all.q --allIn"
#python susy-interface/skimmaker.py 2lss 2lss $T $O $S --cuts susy-ewkino/2lss/cuts-forSkim_susy-int.txt
#
### forNacho
#T="/mnt/t3nfs01/data01/shome/cheidegg/o/2017-02-25_ewktrees80X_M17_bkg"
#O="/mnt/t3nfs01/data01/shome/cheidegg/o/2017-02-25_ewkskims80X_M17_crwz_bkg"
#S="-q all.q --allIn"
#python susy-interface/skimmaker.py crwz crwz $T $O $S --cuts susy-ewkino/crwz/cuts-skim_crwz.txt

## forPietro
T="$SCRATCH/2017-02-18_ewktrees80X_M17_data"
O="/mnt/t3nfs01/data01/shome/cheidegg/o/2017-02-25_ewkskims80X_M17_conv_data"
S="--allIn"
python susy-interface/skimmaker.py 2lss 2lss $T $O $S --cuts susy-ewkino/crconv/cuts-skim.txt

## WZ CR
#T="/mnt/t3nfs01/data01/shome/cheidegg/o/2015-11-29_ewktrees80X_M17"
#O="/mnt/t3nfs01/data01/shome/cheidegg/o/skimsForWZCR"
#S="-q all.q --allIn --exclude WZTo"
#python susy-interface/skimmaker.py crwz crwz $T $O $S --cuts susy-ewkino/crwz/cuts_skim.txt

## eTau CR
#T="/mnt/t3nfs01/data01/shome/cheidegg/o/2015-11-29_ewktrees80X_M17"
#O="/mnt/t3nfs01/data01/shome/cheidegg/o/skimsForETauCR"
#S="--allIn --accept DoubleMuon_Run2016C_23Sep2016_v1_runs_271036_284044_part2"
#python susy-interface/skimmaker.py cretau cretau $T $O $S --cuts susy-ewkino/cretau/cuts_skim.txt

