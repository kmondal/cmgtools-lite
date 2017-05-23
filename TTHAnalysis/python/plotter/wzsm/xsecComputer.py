import os
from utils import getErrorFraction,getErrorFractionWithErr,readYieldsFromTable
from math import sqrt
# Author: Pietro Vischia, pietro.vischia@cern.ch


print("Welcome to the cross section computer")
print("\t Let's start from elementary level")

import optparse
# Command line options
usage = 'usage: %prog [--newData]'
parser = optparse.OptionParser(usage)
parser.add_option('-i', '--input',          dest='inputDir',       help='input directory',        default='/pool/ciencias/HeppyTrees/RA7/estructura/trees_8011_July5_allscans/',           type='string')
parser.add_option('-o', '--output',         dest='outputDir',      help='output directory',       default='~/www/susyRA7/',           type='string')
parser.add_option('-a', '--action',         dest='action',         help='which action to perform', default='crtau', type='string')
parser.add_option('-s', '--subaction',      dest='subaction',      help='which subAction to perform', default='', type='string')
parser.add_option('-p', '--pretend',        dest='pretend',        help='only print commands out', action='store_true')

(opt, args) = parser.parse_args()


print("WARNING, prototype. Using ttbar values from 2012 for tests")

# ttbar_init(20416081); //SIMPLE evt processed
# ttbar_init(8228517); // evt processed from debug.txt
signal_init=8228517
signal_yield=2322
signal_yield_stat=15
signal_yield_syst=162
lum=19696
#38.867
th_xsec=245.8
#scale=lum*11.9413*(1-0.04129783)/ signal_init;   
scale=lum*th_xsec/signal_init


# Formula: sigma = (N-B)/(Lumi*A)
# where N = data
# B = background
# Lumi lumi
# A total acceptance which contains all branching ratios of the s and taus and trigger efficiency. The product of all s, geometric and kinematic acceptance, efficiencies for trigger, lepton identification and cuts on the event kinematic variables yields a total acceptance that is evaluated with respect to the inclusive tt sample. After the OS cut:

acc_et=0.000483
acc_et_stat=0.000003
acc_et_syst=0.000037

acc_mt=0.000586
acc_mt_stat=0.000003
acc_mt_syst=0.000046

meas_et=232
meas_et_stat=4
meas_et_syst=22
meas_et_lumi=6
meas_mt=237
meas_mt_stat=4
meas_mt_syst=23
meas_mt_lumi=6


#et: 232 \pm  4(stat)  22(syst)  6(lumi)
#mt: 237 \pm  4(stat)  23(syst)  6(lumi)


acceptance        = signal_yield/(signal_init*scale)
acceptance_stat   = getErrorFraction((signal_yield/scale),signal_init)
true_error = getErrorFractionWithErr( signal_yield, signal_init*scale, signal_yield_stat , sqrt(signal_init)*scale );
acceptance_syst = signal_yield_syst/(signal_init*scale);

#acceptance=acc_et
#acceptance_stat=acc_et_stat
#acceptance_syst=acc_et_syst

print("Acceptance          : {acc} +/- {acc_stat} +/- {acc_syst}".format(acc=acceptance,acc_stat=acceptance_stat,acc_syst=acceptance_syst))
print("Acceptance (trueerr): {acc} +/- {tru_erro} +/- {acc_syst}".format(acc=acceptance,tru_erro=true_error,acc_syst=acceptance_syst))

print("Signal yield: {signal_yield}".format(signal_yield=signal_yield))
print("Numerator for acceptance : {signal_yield}".format(signal_yield=signal_yield))
print("Initial is               : {signal_init}".format(signal_init=signal_init))
print("Scale                    : {scale}".format(scale=scale))

print("Setting acceptance_stat from {acceptance_stat} to true error {true_error}".format(acceptance_stat=acceptance_stat,true_error=true_error))
acceptance_stat=true_error

# Compute the cross section    

#Yields:
#                             &         $e\tau_h$  &            $\mu\tau_h$      
#ttbar signal   & 2322   $\pm$ 15   $\pm$ 162   &  2837   $\pm$ 17   $\pm$ 198   \\
#fakes          & 1312   $\pm$  2   $\pm$ 92    &  1625   $\pm$  3   $\pm$ 114   \\
#ttbar bkg      &   57.0 $\pm$  2.2 $\pm$ 1.6   &    69.4 $\pm$  2.4 $\pm$   2.3 \\
#DY ll          &   11   $\pm$  5   $\pm$ 5     &    12   $\pm$  5   $\pm$   5   \\
#DY tautau      &   85   $\pm$ 14   $\pm$ 7     &   166   $\pm$ 20   $\pm$  16   \\
#single top     &  104   $\pm$  7   $\pm$ 9     &   133   $\pm$  8   $\pm$  10   \\
#dibosons       &   14.5 $\pm$  1.0 $\pm$ 0.8   &    19.1 $\pm$  1.2 $\pm$   0.9 \\
#Total expected & 3906   $\pm$ 22   $\pm$ 187   &  4862   $\pm$ 28   $\pm$ 229   \\
#Data           & 3779                          &   4767         \\                                                                                                                         


data_yields=3779
tau_fakes=1312
tau_fakes_stat2=2*2
tau_fakes_syst2=92*92
other_bkg=57.0+11+85+104+14.5
other_bkg_stat2=(2.2*2.2 + 5*5 + 14*14 + 7*7 + 1.0*1.0)
other_bkg_syst2=(1.6*1.6 + 5*5 + 7*7   + 9*9 + 0.8*0.8)
lumFactor=1
bkg       = tau_fakes       + other_bkg*lumFactor;
bkg_stat2 = tau_fakes_stat2 + other_bkg_stat2*pow(lumFactor,2);
bkg_syst2 = tau_fakes_syst2 + other_bkg_syst2*pow(lumFactor,2);
   
num=data_yields-bkg; 
num_stat=sqrt(bkg_stat2+data_yields);
num_syst=sqrt(bkg_syst2);

den     =acceptance*lum*lumFactor;  
den_stat=acceptance_stat*lum*lumFactor;  
den_syst=acceptance_syst*lum*lumFactor;

xsec = num/den ; 
xsec_stat = getErrorFractionWithErr( num,den,num_stat,den_stat);
xsec_syst = getErrorFractionWithErr( num,den,num_syst,den_syst);




print("---------------------------------------------------------------------------------------------")
print(" tau fakes: {tau_fakes}  stat2 :{tau_fakes_stat2} syst2 : {tau_fakes_syst2}".format(tau_fakes=tau_fakes,tau_fakes_stat2=tau_fakes_stat2,tau_fakes_syst2=tau_fakes_syst2))
print(" other bkg: {other_bkg}  stat2 :{other_bkg_stat2} syst2 : {other_bkg_syst2}".format(other_bkg=other_bkg,other_bkg_stat2=other_bkg_stat2,other_bkg_syst2=other_bkg_syst2))
print("---------------------------------------------------------------------------------------------")
print(" total bkg: {bkg}    stat2: {bkg_stat2}    syst2: {bkg_syst2}".format(bkg=bkg,bkg_stat2=bkg_stat2,bkg_syst2=bkg_syst2))
print("---------------------------------------------------------------------------------------------")
print(" data yields: {data_yields}".format(data_yields=data_yields))
print("---------------------------------------------------------------------------------------------")
print(" XSEC ")
print(" num  {num}  +/- {num_stat} +/- {num_syst}".format(num=num,num_stat=num_stat,num_syst=num_syst))
print(" den  {den}  +/- {den_stat} +/- {den_syst}".format(den=den,den_stat=den_stat,den_syst=den_syst))
print(" acceptance: {acc}  +/- {acc_stat} +/- {acc_syst}".format(acc=acceptance,acc_stat=acceptance_stat,acc_syst=acceptance_syst))
print(" xsec: {xsec} +/- {xsec_stat} +/- {xsec_syst}".format(xsec=xsec,xsec_stat=xsec_stat,xsec_syst=xsec_syst))
print("=============================================================================")
print("To be compared with")
print("Acc: {acc_et} +/- {acc_et_stat} +/- {acc_et_syst}".format(acc_et=acc_et,acc_et_stat=acc_et_stat,acc_et_syst=acc_et_syst))
print("Xsec: {meas_et} +/- {meas_et_stat} +/- {meas_et_syst} +/- {meas_et_lumi}".format(meas_et=meas_et,meas_et_stat=meas_et_stat,meas_et_syst=meas_et_syst,meas_et_lumi=meas_et_lumi))


table_yields=readYieldsFromTable("/nfs/fanae/user/vischia/www/wz/test/m3l.txt")

