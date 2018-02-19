import os, sys, ROOT, array
import numpy as np
from optparse import OptionParser


"""python doACFits3D.py --file ../../../../data/WZ_MC/AC.root --histo [VAR]_WZ_AC_[BIN] --lX 'Variable' --lY 'Events' """

ROOT.gROOT.SetBatch(True)
pr = OptionParser(usage="%prog [options]")

#Model options
pr.add_option("--file", dest = "file", type="string", default = "plots.root", help = "Root file with the histograms")
pr.add_option("--match", dest = "match", type="string", default = "plots.root", help = "Reweighting card matching index to proper EFT parameters")
pr.add_option("--histo", dest = "histo", type="string", default = "signal", help = "Histogram Name")
pr.add_option("--var", dest = "var", type="string", default = "met", help = "Variable Name")
pr.add_option("--lX", dest = "labelX", type="string", default = "Variable", help = "X axis label")
pr.add_option("--lY", dest = "labelY", type="string", default = "Events", help = "Y axis label")
pr.add_option("--pdir", dest = "outname", type="string", default = "~/www/ewk_fits/test", help = "Output name")

#Output formats
pr.add_option( "--ext", dest = "exts", type = "string", default = ".pdf,.png,.eps", help = "Output formats of the plot in a comma-separated list")

(options, args) = pr.parse_args()
doTestPlots = True

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

index = 0
first = True
for line in matcherFile.readlines():
  if "launch" in line:
    if first:
      pAtIndex = []
      first = False
    else:
      pMatched.append(pAtIndex + [index])
      index += 1
      pAtIndex = []
  else:
    pAtIndex.append(float(line.split(" ")[-1]))

print index


theHists = []
for b in range(len(pMatched)):
  theHists.append(rootFile.Get(options.histo.replace("[VAR]",options.var).replace("[BIN]", str(b))))
 
#Now create the histograms for the variable bins (fit input)

xMinVec = [-3.75,-5,-187.5]
xMaxVec = [3.75,5,187.5]

nBins             = theHists[0].GetNbinsX()
theChanneledHists = []
hFixModel = ROOT.TH3D("All","All",5,xMinVec[0],xMaxVec[0],5,xMinVec[1],xMaxVec[1],5,xMinVec[2],xMaxVec[2])


for n in range(1,nBins+1):
  theChanneledHists.append(hFixModel.Clone())
  theChanneledHists[-1].SetName("Bin%iFits"%n)
  for values in pMatched:
    theChanneledHists[-1].SetBinContent( max(1, min(5, theChanneledHists[-1].GetXaxis().FindBin(values[0]))) , max(1, min(5, theChanneledHists[-1].GetYaxis().FindBin(values[1]))) ,  max(1, min(5, theChanneledHists[-1].GetZaxis().FindBin(values[2]))) , theHists[values[-1]].GetBinContent(n))
    if n == 14: print values, theHists[values[-1]].GetBinContent(n)
  theChanneledHists[-1].Scale(1./theChanneledHists[-1].GetBinContent(3,3,3))


#Once the histograms are made, perform the fits

chi2 = []
theFits = []
theFitsSwap = []
funcTemplate = ROOT.TF3("ex","[0]+[1]*x+[2]*y+[3]*x*x+[4]*y*y+[5]*x*y+[6]*z+[7]*z*z+[8]*x*z+[9]*y*z")

#Change of variables from EFT to ATGC
def rebaseParameters(c0,c1,c2,c3,c4,c5,c6,c7,c8,c9):
  o0 = c0
  o1 = 1./0.0038394*c1
  o2 = 1./0.004155072*c2+1/0.3008299294950178*1./0.0038394*c6
  o3 = 1./0.0038394*1./0.0038394*c3
  o4 = 1./0.004155072*1./0.004155072*c4 + 1/0.3008299294950178*1./0.0038394*1/0.3008299294950178*1./0.0038394*c7 + 1./0.004155072*1/0.3008299294950178*1./0.0038394*c9
  o5 = 1./0.0038394*1./0.004155072*c5+1./0.0038394*1/0.3008299294950178*1./0.0038394*c8
  o6 = -1./0.00097194*c6
  o7 = 1./0.00097194*1./0.00097194*c7
  o8 = -1./0.00097194*1./0.0038394*c8
  o9 = -2*1/0.3008299294950178*1./0.0038394*1./0.00097194*c7-1./0.004155072*1./0.00097194*c9
  return o0,o1,o2,o3,o4,o5,o6,o7,o8,o9

dtAll = []
dtEvery = []
alpha = 0
for h in theChanneledHists:
  print h.GetXaxis().GetBinCenter(2),h.GetXaxis().GetBinCenter(3),h.GetXaxis().GetBinCenter(4), h.GetBinContent(2,3,3), h.GetBinContent(3,3,3), h.GetBinContent(4,3,3)
  ax,bx,dx = fit3(h.GetXaxis().GetBinCenter(2),h.GetXaxis().GetBinCenter(3),h.GetXaxis().GetBinCenter(4), h.GetBinContent(2,3,3), h.GetBinContent(3,3,3), h.GetBinContent(4,3,3))
  ay,by,dy = fit3(h.GetYaxis().GetBinCenter(2),h.GetYaxis().GetBinCenter(3),h.GetYaxis().GetBinCenter(4), h.GetBinContent(3,2,3), h.GetBinContent(3,3,3), h.GetBinContent(3,4,3))
  az,bz,dz = fit3(h.GetZaxis().GetBinCenter(2),h.GetZaxis().GetBinCenter(3),h.GetZaxis().GetBinCenter(4), h.GetBinContent(3,3,2), h.GetBinContent(3,3,3), h.GetBinContent(3,3,4))
  theFits.append(funcTemplate.Clone())
  theFits[-1].SetName("bin_content_par1_par2_par3_" + str(len(theFits)))
  theFits[-1].SetParameters((dx+dy+dz)/3., bx, by, ax,ay,0,bz,az,0,0)
  r = ROOT.TFitResultPtr(h.Fit(theFits[-1],"S"))
  h.Fit(theFits[-1])
  chi2.append([h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetProb(), h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetChisquare()])
  print "Chi2:  ", h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetProb(), h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetChisquare()
  print "Input: ", (dx+dy+dz)/3., bx, by, ax,ay,0,bz,az,0,0
  print "Output: ", h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(0), h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(1), h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(2),h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(3), h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(4), h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(5),h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(6),h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(7),h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(8),h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(9), "\n \n"
  outFile = ROOT.TFile("./signal_proc_[VAR].root".replace("[VAR]",options.var), "UPDATE")
  outFile.WriteTObject(h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))))
  outFile.Close()

  theFitsSwap.append(funcTemplate.Clone())
  theFitsSwap[-1].SetParameters(array.array('d',rebaseParameters(h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(0), h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(1), h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(2),h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(3), h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(4), h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(5),h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(6),h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(7),h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(8),h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(9))))
  theFitsSwap[-1].SetName("bin_content_par1_par2_par3_" + str(len(theFitsSwap)))
  outFileSwap = ROOT.TFile("./signal_proc_[VAR]_swap.root".replace("[VAR]",options.var), "UPDATE")
  outFileSwap.WriteTObject(theFitsSwap[-1])
  outFileSwap.Close()

  dt = 0.
  dtEverytemp = [-1,-1,-1]
  for i in range(1,h.GetNbinsX()+1):
    for j in range(1,h.GetNbinsY()+1):
      for k in range(1,h.GetNbinsZ()+1):
        if (i== 5 and j==5 and k==5): h.SetBinContent(i,j,k, h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).Eval(h.GetXaxis().GetBinCenter(i),h.GetYaxis().GetBinCenter(j),h.GetZaxis().GetBinCenter(k)))
        tempdt = abs(h.GetBinContent(i,j,k) - h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).Eval(h.GetXaxis().GetBinCenter(i),h.GetYaxis().GetBinCenter(j),h.GetZaxis().GetBinCenter(k)))
        if tempdt > dt:
          dt = tempdt
          dtEverytemp = [i,j,k] 
  dtAll.append(dt)
  dtEvery.append(dtEverytemp)
  if doTestPlots == True:
    for j in range(1,h.GetNbinsX()+1):
      for k in range(1,h.GetNbinsY()+1):
        theProj = h.ProjectionZ("bin_%i_%i"%(j,k), j,j,k,k)
        funcProj = ROOT.TF1("ex","[0]+[1]*[11]+[2]*[10]+[3]*[11]*[11]+[4]*[10]*[10]+[5]*[11]*[10]+[6]*x+[7]*x*x+[8]*[11]*x+[9]*[10]*x", -170,170)
        funcProj.SetParameters(array.array('d',[h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(0), h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(1), h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(2),h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(3), h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(4), h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(5),h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(6),h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(7),h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(8),h.GetFunction("bin_content_par1_par2_par3_" + str(len(theFits))).GetParameter(9), h.GetYaxis().GetBinCenter(k),h.GetXaxis().GetBinCenter(j)]))
        ROOT.gStyle.SetOptStat(0)
        c = ROOT.TCanvas("c","c")
        theProj.GetXaxis().SetTitle("c_{b}/#Lambda^{2} [TeV^{-2}]")
	theProj.GetYaxis().SetTitle("AC yields/SM Yields")
        theProj.Draw("hist")
        funcProj.Draw("same")
        c.SaveAs("./test/bin_Var%i_X%i_Y%i.pdf"%(alpha,j,k))
        c.SaveAs("./test/bin_Var%i_X%i_Y%i.png"%(alpha,j,k))
    alpha += 1
        
print "Chi-square values of the fit: ", chi2
print "Maximum differences on the fit by bin: ", dtAll
print "Max at: " , dtEvery
