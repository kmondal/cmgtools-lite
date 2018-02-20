#!/bin/bash

# Run me with 
# sh wzsm/runUnfold | sh

for fs in incl eee eem mme mmm; do
    # No bias, area constraint     
    echo "python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 0 -a -o unfold_nobias/${fs}/data -c common/WZSR.input.root -r > nobias_data_${fs}.log"
    echo "python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 0 -a -o unfold_nobias/${fs}/mcclosure -c common/WZSR.input.root -r --closure > nobias_mcclosure_${fs}.log"

    # No bias, no area constraint
    echo "python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 0 -o unfold_nobias_noconstraintarea/${fs}/data -c common/WZSR.input.root -r > nobias_noconstraintarea_data_${fs}.log"
    echo "python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 0 -o unfold_nobias_noconstraintarea/${fs}/mcclosure -c common/WZSR.input.root -r --closure > nobias_noconstraintarea_mcclosure_${fs}.log"

    # Bias 1, area constraint
    echo "python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 1.0 -a -o unfold_1p0bias/${fs}/data -c common/WZSR.input.root -r > 1p0bias_data_${fs}.log"
    echo "python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 1.0 -a -o unfold_1p0bias/${fs}/mcclosure -c common/WZSR.input.root -r --closure > 1p0bias_mcclosure_${fs}.log"

    # Bias 1, no area constraint
    echo "python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 1.0 -o unfold_1p0bias_noconstraintarea/${fs}/data -c common/WZSR.input.root -r > 1p0bias_noconstraintarea_data_${fs}.log"
    echo "python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 1.0 -o unfold_1p0bias_noconstraintarea/${fs}/mcclosure -c common/WZSR.input.root -r --closure > 1p0bias_noconstraintarea_mcclosure_${fs}.log"

    # Bias 1.11, area constraint
    echo "python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 1.11 -a -o unfold_1p11bias/${fs}/data -c common/WZSR.input.root -r > 1p11bias_data_${fs}.log"
    echo "python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 1.11 -a -o unfold_1p11bias/${fs}/mcclosure -c common/WZSR.input.root -r --closure > 1p11bias_mcclosure_${fs}.log"

    # Bias 1.11, no area constraint
    echo "python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 1.11 -o unfold_1p11bias_noconstraintarea/${fs}/data -c common/WZSR.input.root -r > 1p11bias_noconstraintarea_data_${fs}.log"
    echo "python wzsm/unfold.py -i /nfs/fanae/user/vischia/workarea/cmssw/combine/CMSSW_8_1_0/src/wz_unfolding -f ${fs} -b 1.11 -o unfold_1p11bias_noconstraintarea/${fs}/mcclosure -c common/WZSR.input.root -r --closure > 1p11bias_noconstraintarea_mcclosure_${fs}.log"

done
