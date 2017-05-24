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
parser.add_option('-p', '--pretend',        dest='pretend',        help='only print commands out', action='store_true')
parser.add_option('-s', '--signal',         dest='sigLabel',       help='label of signal in tables', default='WZ', type='string')

(opt, args) = parser.parse_args()

sigLabel=opt.sigLabel

print("WARNING, prototype. Initial number of events and signal cross section are the proper one for WZ signal, and 0 otherwise")

table_yields=readYieldsFromTable("/nfs/fanae/user/vischia/www/wz/test/m3l.txt")

signal_init=(1993200+87860471) if sigLabel=='WZ' else 0
th_xsec=4.42965 if sigLabel=='WZ' else 0

signal_yield=table_yields[sigLabel][0]
signal_yield_stat=table_yields[sigLabel][1]
signal_yield_syst=table_yields[sigLabel][2]

lum=38.867
#scale=lum*11.9413*(1-0.04129783)/ signal_init;   
scale=lum*th_xsec/signal_init

acceptance        = signal_yield/(signal_init*scale)
acceptance_stat   = getErrorFraction((signal_yield/scale),signal_init)
true_error = getErrorFractionWithErr( signal_yield, signal_init*scale, signal_yield_stat , sqrt(signal_init)*scale );
acceptance_syst = signal_yield_syst/(signal_init*scale);

print("Acceptance          : {acc} +/- {acc_stat} +/- {acc_syst}".format(acc=acceptance,acc_stat=acceptance_stat,acc_syst=acceptance_syst))
print("Acceptance (trueerr): {acc} +/- {tru_erro} +/- {acc_syst}".format(acc=acceptance,tru_erro=true_error,acc_syst=acceptance_syst))

print("Signal yield: {signal_yield}".format(signal_yield=signal_yield))
print("Numerator for acceptance : {signal_yield}".format(signal_yield=signal_yield))
print("Initial is               : {signal_init}".format(signal_init=signal_init))
print("Scale                    : {scale}".format(scale=scale))

print("Setting acceptance_stat from {acceptance_stat} to true error {true_error}".format(acceptance_stat=acceptance_stat,true_error=true_error))
acceptance_stat=true_error

# Now compute the cross section    

data_yields=table_yields['DATA'][0]
fakes=table_yields['Nonprompt'][0]
fakes_stat2=pow(table_yields['Nonprompt'][1],2)
fakes_syst2=pow(table_yields['Nonprompt'][2],2)

other_bkg=0
other_bkg_stat2=0
other_bkg_syst2=0

for sample, sample_y in table_yields.iteritems():
    if(sample==sigLabel or sample=='DATA' or sample=='Nonprompt' or sample=='BACKGROUND'): continue
    other_bkg       += sample_y[0]
    other_bkg_stat2 += pow(sample_y[1],2)
    other_bkg_syst2 += pow(sample_y[2],2)
    
lumFactor=1
bkg       = fakes       + other_bkg*lumFactor;
bkg_stat2 = fakes_stat2 + other_bkg_stat2*pow(lumFactor,2);
bkg_syst2 = fakes_syst2 + other_bkg_syst2*pow(lumFactor,2);
   
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
print(" fakes: {fakes}  stat2 :{fakes_stat2} syst2 : {fakes_syst2}".format(fakes=fakes,fakes_stat2=fakes_stat2,fakes_syst2=fakes_syst2))
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


print(" xsec: {xsec} +/- {xsec_stat} +/- {xsec_syst}".format(xsec=xsec,xsec_stat=(100*xsec_stat/xsec),xsec_syst=(100*xsec_syst/xsec)))
brs=3*0.033658*3*0.1067
print(" NLO: {nlo}".format(nlo=(50*brs)))
print(" th: {th_xsec}".format(th_xsec=(th_xsec/brs)))
print(" scale factor: {sf}".format(sf=(xsec/th_xsec)))
print( "br: {br}".format(br=brs))
xsec_inclusive=xsec/brs
xsec_inclusive_stat=xsec_stat/brs
xsec_inclusive_syst=xsec_syst/brs
print(" xsec: {xsec_inc} +/- {xsec_inc_stat} +/- {xsec_inc_syst}".format(xsec_inc=xsec_inclusive,xsec_inc_stat=xsec_inclusive_stat,xsec_inc_syst=xsec_inclusive_syst))
