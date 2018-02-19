python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f incl -o unfold/incl/data -c common/WZSR.input.root -r
python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f incl -o unfold/incl/mcclosure -c common/WZSR.input.root -r --closure

python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f eee -o unfold/eee/data -c common/WZSR.input.root -r
python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f eee -o unfold/eee/mcclosure -c common/WZSR.input.root -r --closure

python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f eem -o unfold/eem/data -c common/WZSR.input.root -r
python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f eem -o unfold/eem/mcclosure -c common/WZSR.input.root -r --closure

python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f mme -o unfold/mme/data -c common/WZSR.input.root -r
python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f mme -o unfold/mme/mcclosure -c common/WZSR.input.root -r --closure

python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f mmm -o unfold/mmm/data -c common/WZSR.input.root -r
python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f mmm -o unfold/mmm/mcclosure -c common/WZSR.input.root -r --closure

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
