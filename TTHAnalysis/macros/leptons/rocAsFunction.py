import drawROCs
import argparse
import array
import ROOT
import copy
from ROOT import TH1F


drawROCs.parser.add_argument('-q', '--quant'  , dest='quant'  , help='quantity to be studied', default='LepGood_pt')
drawROCs.parser.add_argument('--binning', dest='binning', help='quantity to be studied', default='10,20,40,60,100')
drawROCs.parser.add_argument('--hasOverFlow', dest='hasOverFlow', action='store_true', help='Make an overflow bin?')


(opt, args) = drawROCs.parser.parse_known_args()

bins = [ float(x) for x in opt.binning.split(',')]
if opt.hasOverFlow:
    bins.append( 2*bins[-1] - bins[-2])
print bins

bins = array.array('d', bins )



isFirst=True
hROCs = {}


for binDown, binUp in zip( opt.binning.split(','), opt.binning.split(',')[1:]):
    cut = '%s > %s && %s < %s'%(opt.quant, binDown, opt.quant, binUp)
    rocS = drawROCs.drawROCs(drawROCs.parser, values=['--specSelSig',cut,'--specSelBkg',cut])
    if isFirst:
        isFirst=False
        for key in rocS:
            hROCs[key] = TH1F('rocAd%s'%opt.quant + key, '', len(bins)-1, bins)
    for key in rocS:
        hROCs[key].SetBinContent(hROCs[key].FindBin((float(binUp)+float(binDown))/2), rocS[key])


if opt.hasOverFlow:
    cut = '%s > %s'%(opt.quant, opt.binning.split(',')[-1])
    print cut, (1.5*float(opt.binning.split(',')[-1])-0.5*float(opt.binning.split(',')[-2]))
    rocS = drawROCs.drawROCs(drawROCs.parser, values=['--specSelSig',cut,'--specSelBkg',cut])
    for key in rocS:
        print float(opt.binning.split(',')[-1]), float(opt.binning.split(',')[-2]), rocS[key]
        hROCs[key].SetBinContent(hROCs[key].FindBin((1.5*float(opt.binning.split(',')[-1])-0.5*float(opt.binning.split(',')[-2]))), rocS[key])

print hROCs

isFirst=True
idx = 0

leg = ROOT.TLegend(0.3,0.3,0.58,0.58)
leg.SetBorderSize(0)
leg.SetTextSize(0.025)

c = ROOT.TCanvas()
for key in hROCs:
    print key
    if 'mu' in key: continue
    hROCs[key].SetLineWidth(2)
    hROCs[key].SetLineColor(idx+1)
    hROCs[key].Draw('same,hist' if idx else 'hist')
    leg.AddEntry(hROCs[key], key, 'l')
    idx = idx+1
leg.Draw('same')
c.SaveAs('electron.pdf')

c = ROOT.TCanvas()
idx =0 
leg = ROOT.TLegend(0.3,0.3,0.58,0.58)
leg.SetBorderSize(0)
leg.SetTextSize(0.025)
for key in hROCs:
    print key
    if not 'mu' in key: continue
    hROCs[key].SetLineWidth(2)
    hROCs[key].SetLineColor(idx+1)
    hROCs[key].Draw('same,hist' if idx else 'hist')
    leg.AddEntry(hROCs[key], key, 'l')
    idx = idx+1
leg.Draw('same')
c.SaveAs('muon.pdf')
