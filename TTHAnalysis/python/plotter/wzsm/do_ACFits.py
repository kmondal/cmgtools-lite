import os, sys, ROOT, array
import numpy as np
from optparse import OptionParser
import CMS_lumi


"""python doACFits.py --file ../../../../data/WZ_MC/AC.root --histo [VAR]_WZ_AC_[BIN] --lX 'Variable' --lY 'Events' """

ROOT.gROOT.SetBatch(True)
pr = OptionParser(usage="%prog [options]")

#Model options
pr.add_option("--file", dest = "file", type="string", default = "plots.root", help = "Root file with the histograms")
pr.add_option("--match", dest = "match", type="string", default = "plots.root", help = "Reweighting card matching index to proper EFT parameters")
pr.add_option("--histo", dest = "histo", type="string", default = "signal", help = "Histogram Name")
pr.add_option("--lX", dest = "labelX", type="string", default = "Variable", help = "X axis label")
pr.add_option("--lY", dest = "labelY", type="string", default = "Events", help = "Y axis label")
pr.add_option("--pdir", dest = "outname", type="string", default = "~/www/ewk_fits/test", help = "Output name")

#Output formats
pr.add_option( "--ext", dest = "exts", type = "string", default = ".pdf,.png,.eps", help = "Output formats of the plot in a comma-separated list")

(options, args) = pr.parse_args()


#Load histogram
rootFile = ROOT.TFile(options.file, "READ")
matcherFile = open(options.match, "r")

def fit3(x1,x2,x3,y1,y2,y3):
  mat = np.array([[x1**2,x1,1],[x2**2,x2,1],[x3**2,x3,1]])
  invmat = np.linalg.inv(mat)
  vec = np.dot(invmat,np.array([y1,y2,y3])) 
  return vec[0], vec[1], vec[2]

#Get 3D parameters
pMatched = []
pMatchedFix0 = []
pMatchedFix1 = []
pMatchedFix2 = []
pVarSM0 = 0
pVarSM1 = 0
pVarSM2 = 0


index = 0
first = True
for line in matcherFile.readlines():
  if "launch" in line:
    if first:
      pAtIndex = []
      first = False
    else:
      pMatched.append(pAtIndex)
      if pAtIndex[0] == pVarSM0:
        pMatchedFix0.append(pAtIndex + [index])
      if pAtIndex[1] == pVarSM1:
        pMatchedFix1.append(pAtIndex + [index])
      if pAtIndex[2] == pVarSM2:
        pMatchedFix2.append(pAtIndex + [index])
      pAtIndex = []
      index += 1
  else:
    pAtIndex.append(float(line.split(" ")[-1]))


print pMatchedFix0, pMatchedFix1, pMatchedFix2
theVar = "pt1"
theHists = []
for b in range(len(pMatched)):
  theHists.append(rootFile.Get(options.histo.replace("[VAR]", theVar).replace("[BIN]", str(b))))

print 
#Now create the histograms for the variable bins (fit input)

xMinVec = [-3.75,-5,-187.5]
xMaxVec = [3.75,5,187.5]

nBins             = theHists[0].GetNbinsX()
theChanneledHists0 = []
theChanneledHists1 = []
theChanneledHists2 = []
hFix0Model = ROOT.TH2D("Fix 0","Fix 0", 5,xMinVec[1],xMaxVec[1],5,xMinVec[2],xMaxVec[2])
hFix1Model = ROOT.TH2D("Fix 1","Fix 1", 5,xMinVec[0],xMaxVec[0],5,xMinVec[2],xMaxVec[2])
hFix2Model = ROOT.TH2D("Fix 2","Fix 2", 5,xMinVec[0],xMaxVec[0],5,xMinVec[1],xMaxVec[1])

for n in range(1,nBins+1):
  theChanneledHists0.append(hFix0Model.Clone())
  theChanneledHists1.append(hFix1Model.Clone())
  theChanneledHists2.append(hFix2Model.Clone())
  theChanneledHists0[-1].SetName("Bin%iFits0"%n)
  theChanneledHists1[-1].SetName("Bin%iFits1"%n)
  theChanneledHists2[-1].SetName("Bin%iFits2"%n)

  for values in pMatchedFix0:
    theChanneledHists0[-1].SetBinContent( max(1, min(5, theChanneledHists0[-1].GetXaxis().FindBin(values[1]))) ,  max(1, min(5, theChanneledHists0[-1].GetYaxis().FindBin(values[2]))) , theHists[values[-1]].GetBinContent(n))

  for values in pMatchedFix1:
    theChanneledHists1[-1].SetBinContent( max(1, min(5, theChanneledHists1[-1].GetXaxis().FindBin(values[0]))) ,  max(1, min(5, theChanneledHists1[-1].GetYaxis().FindBin(values[2]))) , theHists[values[-1]].GetBinContent(n))

  for values in pMatchedFix2:
    theChanneledHists2[-1].SetBinContent( max(1, min(5, theChanneledHists2[-1].GetXaxis().FindBin(values[0]))) ,  max(1, min(5, theChanneledHists2[-1].GetYaxis().FindBin(values[1]))) , theHists[values[-1]].GetBinContent(n))


#Once the histograms are made, perform the fits

theFits0 = []
theFits1 = []
theFits2 = []
funcTemplate = ROOT.TF2("ex","[0]+[1]*x+[2]*y+[3]*x*y+[4]*y*y+[5]*x*x")
test = ROOT.TH2F()
outFile = ROOT.TFile("./signal_proc_flavor.root", "RECREATE")

"""
for h in theChanneledHists0:
  print h.GetXaxis().GetBinCenter(2),h.GetXaxis().GetBinCenter(3),h.GetXaxis().GetBinCenter(4), h.GetBinContent(2,3), h.GetBinContent(3,3), h.GetBinContent(4,3)
  print h.GetYaxis().GetBinCenter(2),h.GetYaxis().GetBinCenter(3),h.GetYaxis().GetBinCenter(4), h.GetBinContent(3,2), h.GetBinContent(3,3), h.GetBinContent(3,4)
  ax,bx,cx = fit3(h.GetXaxis().GetBinCenter(2),h.GetXaxis().GetBinCenter(3),h.GetXaxis().GetBinCenter(4), h.GetBinContent(2,3), h.GetBinContent(3,3), h.GetBinContent(4,3))
  ay,by,cy = fit3(h.GetYaxis().GetBinCenter(2),h.GetYaxis().GetBinCenter(3),h.GetYaxis().GetBinCenter(4), h.GetBinContent(3,2), h.GetBinContent(3,3), h.GetBinContent(3,4))

  print  "\n\n\n\n\n\n", ax, bx, cx, ay,by,cy, "\n\n\n\n\n\n"
  x = ROOT.RooRealVar("x","x",xMinVec[1], xMaxVec[1])
  y = ROOT.RooRealVar("y","y",xMinVec[2], xMaxVec[2])
  c0 = ROOT.RooRealVar("c0", "c0", (cx+cy)/2., (cx+cy)/2.*0.8, (cx+cy)/2.*1.2)
  cx = ROOT.RooRealVar("cx", "cx", bx, -20., 20.)
  cy = ROOT.RooRealVar("cy", "cy", by, -20., 20.)
  cxy = ROOT.RooRealVar("cxy", "cxy", 0., -10., 10.)
  cxx = ROOT.RooRealVar("cxx", "cxx", ax, -10., 10.)
  cyy = ROOT.RooRealVar("cyy", "cyy", ay, -1., 1.)
  thePolyForm = ROOT.RooGenericPdf("polynomialFit2ndorder", "c0 + cx*x + cy*y +cxy*x*y + cxx*x*x + cyy*y*y",ROOT.RooArgList(x,y,c0,cx,cy,cxy,cxx,cyy))
  theData     = ROOT.RooDataHist("x,y", "dataset x,y", ROOT.RooArgList(x,y), h)
  #thePoly = ROOT.RooPolynomial("model2","c0 + cx*x + cy*y +cxy*x*y + cxx*x*x + cyy*y*y", ROOT.RooArgList(x,y) ,ROOT.RooArgList(c0,cx,cy,cxy,cxx,cyy));
  thePolyForm.fitTo(theData)
  #And the TF2
  theFits0.append(funcTemplate.Clone())
  theFits0[-1].SetParameters(c0.getValV(),cx.getValV(),cy.getValV(),cxy.getValV(),cyy.getValV(),cxx.getValV())
  theFits0[-1].SetName("bin_content_{X}_" + len(theChanneledHists{Y}))
  theFits0[-1].SetRange(-5,-187.5,5,185.5)
  print h.GetBinContent(0,3),h.GetBinContent(1,3),h.GetBinContent(2,3),h.GetBinContent(3,3), h.GetBinContent(4,3),h.GetBinContent(5,3),h.GetBinContent(6,3)
  outFile.WriteTObject(theFits0[-1])
"""
for h in theChanneledHists0:
  print h.GetXaxis().GetBinCenter(2),h.GetXaxis().GetBinCenter(3),h.GetXaxis().GetBinCenter(4), h.GetBinContent(2,3), h.GetBinContent(3,3), h.GetBinContent(4,3)
  print h.GetYaxis().GetBinCenter(2),h.GetYaxis().GetBinCenter(3),h.GetYaxis().GetBinCenter(4), h.GetBinContent(3,2), h.GetBinContent(3,3), h.GetBinContent(3,4)
  ax,bx,dx = fit3(h.GetXaxis().GetBinCenter(2),h.GetXaxis().GetBinCenter(3),h.GetXaxis().GetBinCenter(4), h.GetBinContent(2,3), h.GetBinContent(3,3), h.GetBinContent(4,3))
  ay,by,dy = fit3(h.GetYaxis().GetBinCenter(2),h.GetYaxis().GetBinCenter(3),h.GetYaxis().GetBinCenter(4), h.GetBinContent(3,2), h.GetBinContent(3,3), h.GetBinContent(3,4))
  theFits0.append(funcTemplate.Clone())
  theFits0[-1].SetName("bin_content_par2_par3_" + str(len(theFits0)))
  theFits0[-1].SetParameters((dx+dy)/2., bx, by, 0, ay,ax)
  r = ROOT.TFitResultPtr(h.Fit(theFits0[-1],"S"))
  h.Fit(theFits0[-1])
  print "Chi2:  ", h.GetFunction("bin_content_par2_par3_" + str(len(theFits0))).GetProb(), h.GetFunction("bin_content_par2_par3_" + str(len(theFits0))).GetChisquare()
  print "Input: ", (dx+dy)/2., bx, by, 0, ay,ax
  print "Output: ", h.GetFunction("bin_content_par2_par3_" + str(len(theFits0))).GetParameter(0), h.GetFunction("bin_content_par2_par3_" + str(len(theFits0))).GetParameter(1), h.GetFunction("bin_content_par2_par3_" + str(len(theFits0))).GetParameter(2),h.GetFunction("bin_content_par2_par3_" + str(len(theFits0))).GetParameter(3), h.GetFunction("bin_content_par2_par3_" + str(len(theFits0))).GetParameter(4), h.GetFunction("bin_content_par2_par3_" + str(len(theFits0))).GetParameter(5), "\n \n"
  outFile.WriteTObject(h.GetFunction("bin_content_par2_par3_" + str(len(theFits0))))


for h in theChanneledHists1:
  print h.GetXaxis().GetBinCenter(2),h.GetXaxis().GetBinCenter(3),h.GetXaxis().GetBinCenter(4), h.GetBinContent(2,3), h.GetBinContent(3,3), h.GetBinContent(4,3)
  print h.GetYaxis().GetBinCenter(2),h.GetYaxis().GetBinCenter(3),h.GetYaxis().GetBinCenter(4), h.GetBinContent(3,2), h.GetBinContent(3,3), h.GetBinContent(3,4)
  ax,bx,dx = fit3(h.GetXaxis().GetBinCenter(2),h.GetXaxis().GetBinCenter(3),h.GetXaxis().GetBinCenter(4), h.GetBinContent(2,3), h.GetBinContent(3,3), h.GetBinContent(4,3))
  ay,by,dy = fit3(h.GetYaxis().GetBinCenter(2),h.GetYaxis().GetBinCenter(3),h.GetYaxis().GetBinCenter(4), h.GetBinContent(3,2), h.GetBinContent(3,3), h.GetBinContent(3,4))
  theFits1.append(funcTemplate.Clone())
  theFits1[-1].SetName("bin_content_par1_par3_" + str(len(theFits1)))
  theFits1[-1].SetParameters((dx+dy)/2., bx, by, 0, ay,ax)
  r = ROOT.TFitResultPtr(h.Fit(theFits1[-1],"S"))
  h.Fit(theFits1[-1])
  print "Chi2:  ", h.GetFunction("bin_content_par1_par3_" + str(len(theFits1))).GetProb(), h.GetFunction("bin_content_par1_par3_" + str(len(theFits1))).GetChisquare()
  print "Input: ", (dx+dy)/2., bx, by, 0, ay,ax
  print "Output: ", h.GetFunction("bin_content_par1_par3_" + str(len(theFits1))).GetParameter(0), h.GetFunction("bin_content_par1_par3_" + str(len(theFits1))).GetParameter(1), h.GetFunction("bin_content_par1_par3_" + str(len(theFits1))).GetParameter(2),h.GetFunction("bin_content_par1_par3_" + str(len(theFits1))).GetParameter(3), h.GetFunction("bin_content_par1_par3_" + str(len(theFits1))).GetParameter(4), h.GetFunction("bin_content_par1_par3_" + str(len(theFits1))).GetParameter(5), "\n \n"
  outFile.WriteTObject(h.GetFunction("bin_content_par1_par3_" + str(len(theFits1))))



for h in theChanneledHists2:
  print h.GetXaxis().GetBinCenter(2),h.GetXaxis().GetBinCenter(3),h.GetXaxis().GetBinCenter(4), h.GetBinContent(2,3), h.GetBinContent(3,3), h.GetBinContent(4,3)
  print h.GetYaxis().GetBinCenter(2),h.GetYaxis().GetBinCenter(3),h.GetYaxis().GetBinCenter(4), h.GetBinContent(3,2), h.GetBinContent(3,3), h.GetBinContent(3,4)
  ax,bx,dx = fit3(h.GetXaxis().GetBinCenter(2),h.GetXaxis().GetBinCenter(3),h.GetXaxis().GetBinCenter(4), h.GetBinContent(2,3), h.GetBinContent(3,3), h.GetBinContent(4,3))
  ay,by,dy = fit3(h.GetYaxis().GetBinCenter(2),h.GetYaxis().GetBinCenter(3),h.GetYaxis().GetBinCenter(4), h.GetBinContent(3,2), h.GetBinContent(3,3), h.GetBinContent(3,4))
  theFits2.append(funcTemplate.Clone())
  theFits2[-1].SetName("bin_content_par1_par2_" + str(len(theFits2)))
  theFits2[-1].SetParameters((dx+dy)/2., bx, by, 0, ay,ax)
  h.Fit(theFits2[-1])
  print "Chi2:  ", h.GetFunction("bin_content_par1_par2_" + str(len(theFits2))).GetProb(), h.GetFunction("bin_content_par1_par2_" + str(len(theFits2))).GetChisquare()
  print "Input: ", (dx+dy)/2., bx, by, 0, ay,ax
  print "Output: ", h.GetFunction("bin_content_par1_par2_" + str(len(theFits2))).GetParameter(0), h.GetFunction("bin_content_par1_par2_" + str(len(theFits2))).GetParameter(1), h.GetFunction("bin_content_par1_par2_" + str(len(theFits2))).GetParameter(2),h.GetFunction("bin_content_par1_par2_" + str(len(theFits2))).GetParameter(3), h.GetFunction("bin_content_par1_par2_" + str(len(theFits2))).GetParameter(4), h.GetFunction("bin_content_par1_par2_" + str(len(theFits2))).GetParameter(5), "\n \n"
  outFile.WriteTObject(h.GetFunction("bin_content_par1_par2_" + str(len(theFits2))))

"""
for h in theChanneledHists0:
  outFile.WriteTObject(h)

for h in theChanneledHists1:
  outFile.WriteTObject(h)

for h in theChanneledHists2:
  outFile.WriteTObject(h)
"""

outFile.Close()

