import os
from ROOT import TCanvas, TROOT, TH1F, TH2F, TFile, TTree, gROOT, kRed, kGreen, TLegend

gROOT.SetBatch(True)
odir="./test_compare_skim"
subdir='v6'
if not os.path.isdir(odir):
    os.mkdir(odir)
    print('Output directory %s did not exist. I now created it.'%odir)
if not os.path.isdir('%s/%s'%(odir,subdir)):
    os.mkdir('%s/%s'%(odir,subdir))
    print('Output directory %s/%s did not exist. I now created it.'%(odir,subdir))

gROOT.SetBatch(True)
    ## open files 
f1  = TFile("./skimmedTrees_16/testing/TTHnobb_fxfx_Friend.root")    #v6 under full event selection
if not f1:
    raise ValueError('File 1 not opened')
tr1 = f1.Get("Friends")
if not tr1:
    raise ValueError('Tree 1 not loaded')
f2  = TFile("/nfs/user/elfaham/104X/v6/2016/2lss_diff_Top-tagged/TTHnobb_fxfx_Friend.root")    #v6 under loose skimi
if not f2:
    raise ValueError('File 2 not opened')
tr2 = f2.Get("Friends")
if not tr2:
    raise ValueError('Tree 2 not loaded')

# This seems to be unused...
plotlist = {
    "Hreco_delR_H_q1l"                  : ["Hreco_delR_H_q1l>=0"                   ,"delR_q1l"      , 100, 0., 10. ],
    "Hreco_delR_H_q2l"                  : ["Hreco_delR_H_q2l>=0"                   ,"delR_q2l"      , 100, 0., 10. ],
    "Hreco_delR_H_partons"              : ["Hreco_delR_H_partons>=0"               ,"delR_partons"  , 100, 0., 10. ],
    "Hreco_delR_H_j1l"                  : ["Hreco_delR_H_j1l>=0"                   ,"delR_j1l"      , 100, 0., 10. ],
    "Hreco_delR_H_j2l"                  : ["Hreco_delR_H_j2l>=0"                   ,"delR_j2l"      , 100, 0., 10. ],
    "Hreco_BDThttTT_eventReco_mvaValue" : ["Hreco_BDThttTT_eventReco_mvaValue>=0"  ,"all_score_test", 100, 0., 10. ],
    "Hreco_nmatchedpartons"             : ["Hreco_nmatchedpartons==1"              ,"hnum_top_1"    , 100, 0., 10. ],
    "Hreco_nmatchedpartons"             : ["Hreco_nmatchedpartons==2"              ,"hnum_top_2"    , 100, 0., 10. ],
    "Hreco_nmatchedpartons"             : ["Hreco_nmatchedpartons>=0"              ,"hden_no_top"   , 100, 0., 10. ],
    "Hreco_pTHgen"                      : ["Hreco_pTHgen>=0"                       ,"pTHgen"        , 100, 0., 400.],
    "Hreco_pTHvis"                      : ["Hreco_pTHvis>=0"                       ,"pTHvis"        , 100, 0., 400.],
}
 
    ## compare skimming from the same ntuples version in different variables
currentPlotsDict = {
    "Hreco_pTHgen"     : [ "Hreco_pTHgen>=0"     ,"pTHgen"   ,100, 0., 400.],
    "Hreco_pTHvis"     : [ "Hreco_pTHvis>=0"     ,"pTHvis"   ,100, 0., 400.],
    "Hreco_delR_H_j1l" : [ "Hreco_delR_H_j1l>=0" ,"delR_j1l" , 100, 0., 10.],
    "Hreco_delR_H_j2l" : [ "Hreco_delR_H_j2l>=0" ,"delR_j2l" , 100, 0., 10.],
    "Hreco_delR_H_q1l" : [ "Hreco_delR_H_q1l>=0" ,"delR_q1l" , 100, 0., 10.],
    "Hreco_delR_H_q2l" : [ "Hreco_delR_H_q2l>=0" ,"delR_q2l" , 100, 0., 10.],
}


def draw_comparison(args):
    for var, vals in args.items():
        cut, fname, nbins, lowbin, highbin = vals
        c   = TCanvas()
        leg = TLegend(0.5,0.6,0.9,0.9)
        c.cd()
        theplot_1 = TH1F(var,var, nbins, lowbin, highbin)
        tr1.Draw("%s>>%s"%(var,var),cut)
        theplot_2 = TH1F("%s_2"%var,var, nbins, lowbin, highbin) # Avoid issues with same names
        tr2.Draw("%s>>%s_2"%(var,var),cut)
        theplot_1.Scale(1/theplot_1.Integral())
        theplot_2.Scale(1/theplot_2.Integral())
        theplot_2.SetLineColor(kRed)
        theplot_1.Draw("HIST")
        theplot_2.Draw("HIST SAME")
        leg.AddEntry(theplot_1,"full_event_selection")
        leg.AddEntry(theplot_2,"loose_skim_only")
        leg.Draw()
        c.Print("%s/%s/%s_comp_skim.png"%(odir,subdir,fname)) # Avoid overwriting single var plots



draw_comparison(currentPlotsDict)
