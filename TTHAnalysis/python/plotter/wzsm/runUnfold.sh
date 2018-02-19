#!/bin/bash

for fs in incl eee eem mme mmm; do
    # No bias, area constraint
    python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 0 -a -o unfold_nobias/${fs}/data -c common/WZSR.input.root -r
    python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 0 -a -o unfold_nobias/${fs}/mcclosure -c common/WZSR.input.root -r --closure

    # No bias, no area constraint
    python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 0 -o unfold_nobias_noconstraintarea/${fs}/data -c common/WZSR.input.root -r
    python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 0 -o unfold_nobias_noconstraintarea/${fs}/mcclosure -c common/WZSR.input.root -r --closure

    # Bias 1, area constraint
    python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 1 -a -o unfold_1p0bias/${fs}/data -c common/WZSR.input.root -r
    python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 1 -a -o unfold_1p0bias/${fs}/mcclosure -c common/WZSR.input.root -r --closure

    # Bias 1, no area constraint
    python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 1 -o unfold_1p0bias_noconstraintarea/${fs}/data -c common/WZSR.input.root -r
    python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 1 -o unfold_1p0bias_noconstraintarea/${fs}/mcclosure -c common/WZSR.input.root -r --closure

    # Bias 1.11, area constraint
    python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 1.11 -a -o unfold_1p11bias/${fs}/data -c common/WZSR.input.root -r
    python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 1.11 -a -o unfold_1p11bias/${fs}/mcclosure -c common/WZSR.input.root -r --closure

    # Bias 1.11, no area constraint
    python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 1.11 -o unfold_1p11bias_noconstraintarea/${fs}/data -c common/WZSR.input.root -r
    python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 1.11 -o unfold_1p11bias_noconstraintarea/${fs}/mcclosure -c common/WZSR.input.root -r --closure

done


#    parser.add_argument('-i', '--inputDir',   help='Input directory', default=None)
#    parser.add_argument('-o', '--outputDir',  help='Output directory', default='./')
#    parser.add_argument('-d', '--data',       help='File containing data histogram', default=None)
#    parser.add_argument('-m', '--mc',         help='File containing mc reco histogram', default=None)
#    parser.add_argument('-g', '--gen',   help='File containing gen info for matrix', default=None)
#    parser.add_argument('-l', '--lepCat',     help='Lepton multiplicity (1 or 2)', default=1, type=int)
#    #parser.add_argument('-m', '--multiclass', help='Multiclass (ttbar-LF and ttbar-HF are in different classes)', action='store_true')
#    parser.add_argument('-e', '--epochs',     help='Number of epochs', default=100, type=int)
#    parser.add_argument('-s', '--splitMode',  help='Split mode (input or random)', default='input')
#    parser.add_argument('-v', '--verbose',    help='Verbose printing of the L-curve scan', action='store_true')
