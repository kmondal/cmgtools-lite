import os
from utils import readYieldsFromTable,readYieldsFromTable,writeYieldsToLatex


import optparse
# Command line options
usage = 'usage: %prog [--newData]'
parser = optparse.OptionParser(usage)
parser.add_option('-i', '--input',          dest='inputDir',       help='input directory',        default='/pool/ciencias/HeppyTrees/RA7/estructura/trees_8011_July5_allscans/',           type='string')
parser.add_option('-o', '--output',         dest='outputDir',      help='output directory',       default='~/www/susyRA7/',           type='string')
parser.add_option('-a', '--action',         dest='action',         help='which action to perform', default='crtau', type='string')
parser.add_option('-p', '--pretend',        dest='pretend',        help='only print commands out', action='store_true')
parser.add_option('-s', '--signal',         dest='sigLabel',       help='label of signal in tables', default='WZ', type='string')
parser.add_option('-w', '--workingPoint',   dest='wp', default='VT', help='working point for lepton ID (default is: VT)')

(opt, args) = parser.parse_args()
sigLabel=opt.sigLabel
wp=opt.wp

rawYields=readYieldsFromTable("/nfs/fanae/user/vischia/www/wz/wz/lepmva{wp}/srwz/m3lmet.txt".format(wp=wp))

table = writeYieldsToLatex(rawYields,sigLabel)

print table
