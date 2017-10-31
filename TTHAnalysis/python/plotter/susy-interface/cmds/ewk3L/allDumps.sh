#!/bin/bash

T="/mnt/t3nfs01/data01/shome/cheidegg/o/2015-11-29_ewkskims80X_M17"
O="/afs/cern.ch/user/c/cheidegg/www/heppy/2016-12-07_ewk80X_fullstatus_dumps"

python susy-interface/dumpmaker.py 3l 3lF $T $O -p data

