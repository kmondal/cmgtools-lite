import os
import subprocess

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
