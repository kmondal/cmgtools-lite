import os
import subprocess
from math import sqrt,fabs

# Author: Pietro Vischia, pietro.vischia@cern.ch

"""
"""
def get_file_from_glob(f):                                                    
        files = glob.glob(f)                                                      
        if len(files) != 1:                                                       
                raise Exception('Only one input file is supported per glob pattern: %\
s -> %s' % (f, files))                                                        
        
        return files[0]                                                           

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

def writeYieldsToLatex(yields,sigLabel):
        """
        Input is expected to be in the output format of readYieldsFromTable above
        """
        
        table=[]
        yieldLine='{sample} & {val} \\pm {stat} \\pm {syst} \\\\\n'
        yieldLineRed='{sample} & {val} \\\\\n'
        table.append('\\begin{tabular}{c|c}\n')
        table.append('Process & Yield \\pm stat. \\pm syst.\\\\\n')

        for sample, sample_y in yields.iteritems():
                if sigLabel not in sample:
                        continue
                table.append(yieldLine.format(sample=sample, val=sample_y[0], stat=sample_y[1], syst=sample_y[2]))

        table.append('\\hline\n')
        for sample, sample_y in yields.iteritems():
                if((sigLabel in sample) or ('DATA') in sample or ('BACKGROUND' in sample)):
                        continue
                table.append(yieldLine.format(sample=sample, val=sample_y[0], stat=sample_y[1], syst=sample_y[2]))

        table.append('\\hline\n')
        for sample, sample_y in yields.iteritems():
                if 'BACKGROUND' not in sample:
                        continue
                systBkg=0.
                for s, s_y in yields.iteritems():
                        if ('BACKGROUND' in s) or ('DATA' in s):
                                continue
                        systBkg+=pow(s_y[2],2)
                systBkg=sqrt(systBkg)
                table.append(yieldLine.format(sample='Total SM', val=sample_y[0], stat=sample_y[1], syst=round(systBkg,2)))
        table.append('\\hline\n')
        table.append('\\hline\n')
        for sample, sample_y in yields.iteritems():
                if 'DATA' not in sample:
                        continue
                table.append(yieldLineRed.format(sample='Data', val=sample_y[0]))
        
        table.append('\\hline\n')
        table.append('\\end{tabular}\n')
        ret = ''.join(table)
                     
        return ret


