import os
import subprocess
from math import sqrt,fabs

"""
"""
def command(cmd, pretend):

        if pretend:
                print 'Command is: ', cmd
        else:
                os.system(cmd)

        return
        # Old stuff below. 
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
    
        
        newCmd = 'python {cmd}'.format(cmd=p.split('python')[1])
        if pretend:
                print newCmd
        else:
                os.system(newCmd)
                
        print "Done."
"""
"""

def clean(outDir):
        os.system('mkdir -p {outDir}'.format(outDir=outDir))
        os.system('rm {outDir}/*png'.format(outDir=outDir))
        os.system('rm {outDir}/*pdf'.format(outDir=outDir))
        os.system('rm {outDir}/*txt'.format(outDir=outDir))
        print 'Old plots in {outDir} cleaned.'.format(outDir=outDir)


  
def getErrorFraction(a, b):
        ret=0
        if (b!=0):  
                temp = fabs(a)/(b*b)+ fabs( (a*a)/(b*b*b))
                ret = sqrt(temp);
        return ret

def getErrorFractionWithErr(a, b, err_a, err_b):
        ret=0
        if (b!=0):
                temp = (err_a*err_a)/(b*b)+( (a*a)/(b*b*b*b) )*( err_b*err_b )
                ret = sqrt(temp);
        return ret


import re

def readYieldsFromTable(fname):
        yields={}
        for line in open(fname):
                # Strip whitespaces
                line=re.sub( '\s+', ' ', line ).strip()
                fields = line.split(' ')
                if len(fields) < 2: continue
                #if fields[3].strip() != 'FUNC': continue
                if len(fields) < 3:
                        yields[fields[0]] = [float(fields[1])]
                elif len(fields) <6:
                        yields[fields[0]] = [float(fields[1]), float(fields[3])]
                else:
                        yields[fields[0]] = [float(fields[1]), float(fields[3]), float(fields[6])]
        return yields
