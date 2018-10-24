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
def get_list_of_jobs(base):
    
    ret=[]

    #for charge in [ '', '_plus', '_minus' ]:
    #for charge in [ '_plus', '_minus' ]:
    for charge in [ '_none', '_plus', '_minus' ]:
        for fs in [ 'incl', 'eee', 'eem', 'mme', 'mmm']:
            if not base:
                # No bias, area constraint     
                ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} --charge {charge}  -b 0 -a -o unfold_nobias/{fs}{charge}/data -c common/WZSR.input.root -r >& logs/nobias_data_{fs}.log'.format(fs=fs,charge=charge))
                ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} --charge {charge}  -b 0 -a -o unfold_nobias/{fs}{charge}/mcclosure -c common/WZSR.input.root -r --closure >& logs/nobias_mcclosure_{fs}.log'.format(fs=fs,charge=charge))

                # No bias, no area constraint
                ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} --charge {charge}  -b 0 -o unfold_nobias_noconstraintarea/{fs}{charge}/data -c common/WZSR.input.root -r >& logs/nobias_noconstraintarea_data_{fs}.log'.format(fs=fs,charge=charge))
                ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} --charge {charge}  -b 0 -o unfold_nobias_noconstraintarea/{fs}{charge}/mcclosure -c common/WZSR.input.root -r --closure >& logs/nobias_noconstraintarea_mcclosure_{fs}.log'.format(fs=fs,charge=charge))
            
                # Bias 1, area constraint
                ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} --charge {charge}  -b 1.0 -a -o unfold_1p0bias/{fs}{charge}/data -c common/WZSR.input.root -r >& logs/1p0bias_data_{fs}.log'.format(fs=fs,charge=charge))
                ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} --charge {charge}  -b 1.0 -a -o unfold_1p0bias/{fs}{charge}/mcclosure -c common/WZSR.input.root -r --closure >& logs/1p0bias_mcclosure_{fs}.log'.format(fs=fs,charge=charge))
                
                # Bias 1, no area constraint
                ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} --charge {charge}  -b 1.0 -o unfold_1p0bias_noconstraintarea/{fs}{charge}/data -c common/WZSR.input.root -r >& logs/1p0bias_noconstraintarea_data_{fs}.log'.format(fs=fs,charge=charge))
                ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} --charge {charge}  -b 1.0 -o unfold_1p0bias_noconstraintarea/{fs}{charge}/mcclosure -c common/WZSR.input.root -r --closure >& logs/1p0bias_noconstraintarea_mcclosure_{fs}.log'.format(fs=fs,charge=charge))
        
                # Bias 1.13, no area constraint
                ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} --charge {charge}  -b 1.13 -o unfold_nnlobias_noconstraintarea/{fs}{charge}/data -c common/WZSR.input.root -r >& logs/nnlobias_noconstraintarea_data_{fs}.log'.format(fs=fs,charge=charge))
                ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} --charge {charge}  -b 1.13 -o unfold_nnlobias_noconstraintarea/{fs}{charge}/mcclosure -c common/WZSR.input.root -r --closure >& logs/nnlobias_noconstraintarea_mcclosure_{fs}.log'.format(fs=fs,charge=charge))

            else:
                # Bias 1.13, area constraint
                ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} --charge {charge}  -b 1.13 -a -o unfold_nnlobias/{fs}{charge}/data -c common/WZSR.input.root -r >& logs/nnlobias_data_{fs}.log'.format(fs=fs,charge=charge))
                ret.append('python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f {fs} --charge {charge}  -b 1.13 -a -o unfold_nnlobias/{fs}{charge}/mcclosure -c common/WZSR.input.root -r --closure >& logs/nnlobias_mcclosure_{fs}.log'.format(fs=fs,charge=charge))
            

    return ret

def runner(cmd):
    print(cmd)
    os.system(cmd)
    
if __name__ == '__main__':
    # execute only if run as a script
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--nthreads',       help='Number of parallel threads', default=8, type=int)
    parser.add_argument('-b', '--base',           help='Run only on base parameter set', action='store_true')
    parser.add_argument('-d', '--dryrun',         help='Only print commands and exit', action='store_true')
    args = parser.parse_args()
    print('You have requested to run with a %d-threads pool. Good luck!' % args.nthreads)
    # Get jobs
    jobs = get_list_of_jobs(args.base)
    
    if args.dryrun:
        print jobs
        quit()
    pool=Pool(args.nthreads)
    pool.map(runner, jobs)
    pool.close()
    pool.join()
