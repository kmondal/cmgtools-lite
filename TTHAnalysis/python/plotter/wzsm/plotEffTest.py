import os, sys, ROOT, array
from optparse import OptionParser
import CMS_lumi

ROOT.gROOT.SetBatch(True)
pr = OptionParser(usage="%prog [options]")

""" An example command to evaluate the efficiency of the BDT cut in the lepton MVA case:
  -lep3_pt_MVA_total is a TH2D in plots_LepEff_BDT.root. For each histogram the code does the quotient of the Y-integrated yields across the --cells argument over the total integral in the Y axis. Thus, if computes the efficiency of a cut in the Y variable limitted to a given --cells range for different bins in the X variable.

python susy-ewkino/3lfor2017Tests/plotEffTest.py --files '/nfs/fanae/user/carlosec/www/BDTtests/ttHBDTwithpT/plots_LepEff_BDT.root,/nfs/fanae/user/carlosec/www/BDTtests/ttH/plots_LepEff_BDT.root'  --lX 'p_{T}(l_{3}) [GeV]' --histos 'lep3_pt_MVA_total,lep3_pt_MVA_total' --lY '#epsilon = #frac{N_{MVA}}{N_{L}}' --pdir ~/www/BDTtests/ttHcompt/lep3_eff --range '5,50,0,1.2' --title '' --cells '0,21;1,21;2,21;3,21;4,21;5,21;6,21;7,21;8,21;9,21;10,21;11,21;12,21;13,21;14,21;15,21;16,21;17,21;18,21;19,21;20,21' --names '0.0,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,0.99' --flabels 'With p_{T},Without p_{T}'
"""

#Model options
pr.add_option( "--logZ"         , dest="doLog"       , action="store_false", default=True, help="Use a logarithmic scale for Z axis")
pr.add_option( "--doCumul"         , dest="doCumulative"       , action="store_false", default=True, help="Do cumulative distributions")
pr.add_option( "--doQuot"         , dest="doQuot"       , action="store_false", default=True, help="Do quotient (needs two distributions")
pr.add_option("--files", dest = "files", type="string", default = "./", help = "Root files")
pr.add_option("--flabels", dest = "flabels", type="string", default = "", help = "Labels in the legend for each case")
pr.add_option("--histos", dest = "histos", type="string", default = "./", help = "Histogram list")
pr.add_option("--title", dest = "title", type="string", default = "S/B cumulative distribution", help = "Title of the plot")
pr.add_option("--lX", dest = "labelX", type="string", default = "P_{T}(l_{1}) [GeV]", help = "X axis label")
pr.add_option("--lY", dest = "labelY", type="string", default = "P_{T}(l_{2}) [GeV]", help = "Y axis label")
pr.add_option("--range", dest = "range", type="string", default = "5,50,0,1.2", help = "Plotting range")
pr.add_option("--pdir", dest = "outname", type="string", default = "./test", help = "Output name")
pr.add_option("--cells", dest = "cellList", type="string", default = "[[0,1],[1,2]]", help = "List of rows [min,max] to integrate for quotient over all")
pr.add_option( "--names", dest = "names", type = "string", default = "[\"first\", \"second\"]", help = "Names for the plots")

#Output formats
pr.add_option( "--ext", dest = "exts", type = "string", default = ".pdf,.png,.eps,.gif", help = "Output formats of the plot in a comma-separated list")


(options, args) = pr.parse_args()

minX, maxX, minY, maxY = eval(options.range)
formats =  options.exts.split(",")
print options.cellList, type(options.cellList)
options.cellList = [eval(k) for k in options.cellList.split(";")]
options.names = options.names.split(",")
options.files = options.files.split(",")
options.histos = options.histos.split(",")
options.flabels = options.flabels.split(",")

def getLimits(histo, uX, uY):
  minVal = 10000000.
  maxVal = 0.
  for i in range(histo.GetNbinsX()+1):
    for j in range(histo.GetNbinsY()+1):
      if (i <= uX) and (j <= uY) and not(histo.GetBinContent(i,j) == 0):
        theVal = histo.GetBinContent(i,j)
        if theVal < minVal: minVal = theVal
        if theVal > maxVal: maxVal = theVal
  return minVal, maxVal

fileIn1 = []
h_2D = []
h_loose = []

for f in options.files:
  fileIn1.append(ROOT.TFile(f, "READ"))
  h_2D.append(fileIn1[-1].Get(options.histo1))
  #For normalization
  h_loose.append(h_2D[-1].ProjectionX("loose"))


def getEff(n1,n2, name):
  h_tight = []
  isSet = False
  for i in range(len(options.files)):
#    print h_tight, len(h_tight)
    h_tight.append(h_2D[i].ProjectionX("tight_" + str(i),n1,n2))
  #  print h_tight.Integral(), h_loose.Integral()
    h_tight[-1].Divide(h_loose[i])
  
    if isSet:
      h_tight[-1].SetLineColor(ROOT.kRed);
      h_tight[-1].SetMarkerColor(ROOT.kRed);
      h_tight[-1].GetXaxis().SetRangeUser(minX,maxX)
      h_tight[-1].GetYaxis().SetRangeUser(minY,maxY)
      h_tight[-1].SetMarkerStyle(ROOT.kCircle)
      h_tight[-1].Draw("p same")
      l.AddEntry(h_tight[-1], options.flabels[i], "p");

    else:
      srHisto = h_tight[-1]
      ROOT.gStyle.SetOptStat(0);
      ROOT.gStyle.SetPaintTextFormat("1.3f");
      canvas = ROOT.TCanvas("c", "c", 1920, 1080)
      canvas.cd()
      if options.doLog:
        pad = canvas.SetLogz(1)  
      srHisto.SetTitle(options.title)
      #print minVal, maxVal, srHisto.GetXaxis().FindBin(maxX-1), srHisto.GetYaxis().FindBin(maxY-1)
      srHisto.GetXaxis().SetRangeUser(minX,maxX)
      srHisto.GetYaxis().SetRangeUser(minY,maxY)
      srHisto.GetXaxis().SetTitle(options.labelX)
      srHisto.GetYaxis().SetTitle(options.labelY)
    
      srHisto.GetXaxis().SetNdivisions(505)
      srHisto.GetXaxis().SetLabelFont(42)
      srHisto.GetXaxis().SetLabelSize(0.045)  
      srHisto.GetXaxis().SetTitleFont(42)
      srHisto.GetXaxis().SetTitleSize(0.050)
      srHisto.GetXaxis().SetTitleOffset(0.9)
    
      srHisto.GetYaxis().SetNdivisions(505)
      srHisto.GetYaxis().SetLabelFont(42)
      srHisto.GetYaxis().SetLabelSize(0.045)
      srHisto.GetYaxis().SetTitleFont(42)
      srHisto.GetYaxis().SetTitleSize(0.045)
      srHisto.GetYaxis().SetTitleOffset(0.8)
      srHisto.SetMarkerStyle(ROOT.kOpenTriangleDown)
      srHisto.Draw("p")
      l = ROOT.TLegend(0.65,0.10,0.85,0.25)
      l.SetFillStyle(1001)
      l.SetFillColor(ROOT.kWhite)
      l.SetLineColor(ROOT.kWhite)
      l.SetLineWidth(2)
      l.AddEntry(srHisto, options.flabels[i], "p");
      isSet = True


  print h_tight, len(h_tight)
  l.Draw()
  for f in formats:
    canvas.SaveAs(options.outname + "_" + name + f)

for k in range(len(options.cellList)):
  getEff(options.cellList[k][0], options.cellList[k][1], str(options.names[k])) 
