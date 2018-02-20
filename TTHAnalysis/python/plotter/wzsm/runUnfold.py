import os
import argparse
from multiprocessing import Pool

'''
Helper script for doing the full unfolding analysis.

Created by Pietro Vischia -- pietro.vischia@cern.ch
'''

# Run me with 
#  python wzsm/runUnfold.py [-p nthreads=8]
#

# Create the list of jobs to be run
def get_list_of_jobs():
    
    ret=[]

    for fs in [ 'incl', 'eee', 'eem', 'mme', 'mmm']:
        # No bias, area constraint     
        ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} -b 0 -a -o unfold_nobias/{fs}/data -c common/WZSR.input.root -r >& logs/nobias_data_{fs}.log'.format(fs=fs))
        ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} -b 0 -a -o unfold_nobias/{fs}/mcclosure -c common/WZSR.input.root -r --closure >& logs/nobias_mcclosure_{fs}.log'.format(fs=fs))

        # No bias, no area constraint
        ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} -b 0 -o unfold_nobias_noconstraintarea/{fs}/data -c common/WZSR.input.root -r >& logs/nobias_noconstraintarea_data_{fs}.log'.format(fs=fs))
        ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} -b 0 -o unfold_nobias_noconstraintarea/{fs}/mcclosure -c common/WZSR.input.root -r --closure >& logs/nobias_noconstraintarea_mcclosure_{fs}.log'.format(fs=fs))
        
        # Bias 1, area constraint
        ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} -b 1.0 -a -o unfold_1p0bias/{fs}/data -c common/WZSR.input.root -r >& logs/1p0bias_data_{fs}.log'.format(fs=fs))
        ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} -b 1.0 -a -o unfold_1p0bias/{fs}/mcclosure -c common/WZSR.input.root -r --closure >& logs/1p0bias_mcclosure_{fs}.log'.format(fs=fs))

        # Bias 1, no area constraint
        ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} -b 1.0 -o unfold_1p0bias_noconstraintarea/{fs}/data -c common/WZSR.input.root -r >& logs/1p0bias_noconstraintarea_data_{fs}.log'.format(fs=fs))
        ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} -b 1.0 -o unfold_1p0bias_noconstraintarea/{fs}/mcclosure -c common/WZSR.input.root -r --closure >& logs/1p0bias_noconstraintarea_mcclosure_{fs}.log'.format(fs=fs))

        # Bias 1.13, area constraint
        ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} -b 1.13 -a -o unfold_1p11bias/{fs}/data -c common/WZSR.input.root -r >& logs/1p11bias_data_{fs}.log'.format(fs=fs))
        ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} -b 1.13 -a -o unfold_1p11bias/{fs}/mcclosure -c common/WZSR.input.root -r --closure >& logs/1p11bias_mcclosure_{fs}.log'.format(fs=fs))

        # Bias 1.11, no area constraint
        ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} -b 1.13 -o unfold_1p11bias_noconstraintarea/{fs}/data -c common/WZSR.input.root -r >& logs/1p11bias_noconstraintarea_data_{fs}.log'.format(fs=fs))
        ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} -b 1.13 -o unfold_1p11bias_noconstraintarea/{fs}/mcclosure -c common/WZSR.input.root -r --closure >& logs/1p11bias_noconstraintarea_mcclosure_{fs}.log'.format(fs=fs))

    return ret

def runner(cmd):
    os.system(cmd)
    
if __name__ == '__main__':
    # execute only if run as a script
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--nthreads',       help='Number of parallel threads', default=8, type=int)
    args = parser.parse_args()
    print('You have requested to run with a %d-threads pool. Good luck!' % args.nthreads)

    # Get jobs
    jobs = get_list_of_jobs()
    
    pool=Pool(args.nthreads)
    pool.map(runner, jobs)
    pool.close()
    pool.join()
