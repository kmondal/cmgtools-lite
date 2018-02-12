'''
Script for doing the full unfolding analysis.

Created by Pietro Vischia -- pietro.vischia@cern.ch
'''
import os
import copy

import argparse
import utils
import ROOT
from array import array

#from abc import ABCMeta, abstractmethod
# 
#class AbstractTSpline(object):
#    __metaclass__ = ABCMeta
#     
#    @abstractmethod
#    def run(self):
#        pass

class ResponseComputation:

    def __init__(self, inputFiles):
        print('Initialization')
        print('Input for matrix creation: %s' % inputFiles)
        self.inputFiles=inputFiles
        
        
        
        
class AcceptanceComputer:

    def __init__(self, inputFiles):
        print('Initialization')
        print('Input files are: %s' % inputFiles)

### End class AcceptanceCounter

class Unfolder(object):

    def __init__(self, args, var):
        print('Initialization')
        self.var=var
        self.unfold=None
        self.response_nom=None
        self.response_alt=None
        self.response_inc=None
        self.data=None
        self.mc=None
        self.bkg=None
        self.verbose=args.verbose
        self.combineInput=args.combineInput
        self.nScan=30
        # Automatic L-curve scan: start with taumin=taumax=0.0
        self.tauMin=0.0
        self.tauMax=0.0
        self.iBest=None # Best value
        self.logTauX=ROOT.TSpline3() # TSpline*
        self.logTauY=ROOT.TSpline3() # TSpline*
        self.lCurve=ROOT.TGraph(0) # TGraph*
        self.gHistInvEMatrix=ROOT.TH2D() # store the inverse of error matrix
        self.gHistInvJEMatrix=None
        self.inputDir=args.inputDir
        self.outputDir=args.outputDir
        self.responseAsPdf=args.responseAsPdf
        self.histmap=ROOT.TUnfold.kHistMapOutputVert
        self.regmode=ROOT.TUnfold.kRegModeNone
        self.constraint=ROOT.TUnfold.kEConstraintArea
        self.densitymode=ROOT.TUnfoldDensity.kDensityModeeNone
        self.load_data(args.data, args.mc, args.gen)

        # Make sure histogram errors are ON
        ROOT.TH1.SetDefaultSumw2()


    def load_data(self, dataFName, mcFName, genFName, treeName=['tree']):
        folder=self.inputDir
        dataFile=None
        mcFile=None
        #genFile=None # Taken from a separate file  
        print('Opening file %s.' % utils.get_file_from_glob(os.path.join(folder, 'incl_fitWZonly_%s/%s' % (self.var, self.combineInput) ) if folder else self.combineInput) )
        file_handle = ROOT.TFile.Open(utils.get_file_from_glob(os.path.join(folder,  'incl_fitWZonly_%s/%s' % (self.var, self.combineInput)) if folder else self.combineInput))
        # gdata=file_handle.Get('x_data')
        # gdata.Draw('AP')
        # hdata=self.get_graph_as_hist(gdata, ('recodata','recodata',4,0,4))
        # data   = copy.deepcopy(ROOT.TH1F(hdata))
        data   = copy.deepcopy(file_handle.Get('x_data'))
        signal = copy.deepcopy(file_handle.Get('x_prompt_WZ'))
        bkg    = copy.deepcopy(self.get_total_bkg_as_hist(file_handle, 'list'))   
        # bkg    = copy.deepcopy(self.get_total_bkg_as_hist(file_handle, 'sum'))
        # Subtraction is done by the TUnfoldDensityClass
        # Scheme 1: subtraction
        # print('Before subtraction. Data: %f, Bkg: %f, Signal: %f' % (data.Integral(), bkg.Integral(), signal.Integral()))  
        #data.Add(bkg, -1)
        self.data=data
        self.mc=signal
        self.bkg=bkg

        print('bins of input data: %d' % self.data.GetNbinsX() ) 
        print('bins of input signal: %d' % self.mc.GetNbinsX() ) 
        #print('bins of input bkg: %d' % self.bkg.GetNbinsX()   ) 
        print('bins of input bkg: %d' % self.bkg[0].GetNbinsX()   ) 

        
        # print('Subtraction completed. Data-bkg: %f, Signal: %f' % (self.data.Integral(), self.mc.Integral() ))
        # print('Expected mu=(data-bkg)/NLO: %f' % (self.data.Integral()/self.mc.Integral()) )
            
        #genFile  = utils.get_file_from_glob(os.path.join(folder, genFName)  if folder else genFName)

        # Add reading gen file to build response matrix
        self.get_responses()

        # Pass through numpy arrays?
        print('Data correctly loaded.')
        #return data, mc, response
        
    def get_responses(self):
        print('Acquiring response matrices.')
        folder=os.path.join(self.inputDir, 'response/%s_response_WZ_' % self.var)
        file_handle_nom = ROOT.TFile.Open('%s%s.root' % (folder, 'Pow'))
        file_handle_alt = ROOT.TFile.Open('%s%s.root' % (folder, 'aMC'))
        file_handle_inc = ROOT.TFile.Open('%s%s.root' % (folder, 'Inc'))

        self.response_nom = copy.deepcopy(ROOT.TH2D(file_handle_nom.Get('%s_response_canvas' % self.var).GetPrimitive('%s_response_WZ_%s' %(self.var, 'Pow'))))
        self.response_alt = copy.deepcopy(ROOT.TH2D(file_handle_alt.Get('%s_response_canvas' % self.var).GetPrimitive('%s_response_WZ_%s' %(self.var, 'aMC'))))
        self.response_inc = copy.deepcopy(ROOT.TH2D(file_handle_inc.Get('%s_response_canvas' % self.var).GetPrimitive('%s_response_WZ_%s' %(self.var, 'Inc'))))

    def print_responses(self):
        c = ROOT.TCanvas('matrix', 'Response Matrix', 2000, 2000)
        c.cd()
        # Margin not being applied somehow. Must do it via gStyle?
        ROOT.gStyle.SetPadTopMargin(0.1)
        ROOT.gStyle.SetPadBottomMargin(0.1)
        ROOT.gStyle.SetPadLeftMargin(0.1)
        ROOT.gStyle.SetPadRightMargin(0.1)
        ROOT.gStyle.SetOptStat('uo')
        if self.responseAsPdf:
            resp_nom=copy.deepcopy(ROOT.TH2D(self.response_nom))
            resp_alt=copy.deepcopy(ROOT.TH2D(self.response_alt))
            resp_inc=copy.deepcopy(ROOT.TH2D(self.response_inc))
            
            resp_nom.Scale(1./resp_nom.Integral())
            resp_alt.Scale(1./resp_alt.Integral())
            resp_inc.Scale(1./resp_inc.Integral())
            # Compute stability
            diagonalSum_nom=0
            diagonalSum_alt=0
            diagonalSum_inc=0
            odbN_nom=0
            odbN_alt=0
            odbN_inc=0
            for ibin in range(0, resp_nom.GetNbinsX()):
                # Am I taking the overflow diagonal one as well? Must check
                diagonalSum_nom+= resp_nom.GetBinContent(ibin, ibin)
                diagonalSum_alt+= resp_alt.GetBinContent(ibin, ibin)
                diagonalSum_inc+= resp_inc.GetBinContent(ibin, ibin)
                for jbin in range(0, resp_nom.GetNbinsY()):
                    if ibin != jbin:
                        if resp_nom.GetBinContent(ibin, jbin) != 0: odbN_nom+=1
                        if resp_alt.GetBinContent(ibin, jbin) != 0: odbN_alt+=1
                        if resp_inc.GetBinContent(ibin, jbin) != 0: odbN_inc+=1

            oodFraction_nom=(1-diagonalSum_nom) 
            oodFraction_alt=(1-diagonalSum_alt)
            oodFraction_inc=(1-diagonalSum_inc)
            odbFraction_nom = odbN_nom/(resp_nom.GetNbinsX()*resp_nom.GetNbinsY())
            odbFraction_alt = odbN_alt/(resp_alt.GetNbinsX()*resp_alt.GetNbinsY())
            odbFraction_inc = odbN_inc/(resp_inc.GetNbinsX()*resp_inc.GetNbinsY())
            print('Overall fraction of out-of-diagonal events | Fraction of out-of-diagonal filled bins:')
            print('\t nom: %0.3f | %0.3f = %d/%d' % (oodFraction_nom, odbFraction_nom, odbN_nom, (resp_nom.GetNbinsX()*resp_nom.GetNbinsY())))
            print('\t alt: %0.3f | %0.3f = %d/%d' % (oodFraction_alt, odbFraction_alt, odbN_alt, (resp_alt.GetNbinsX()*resp_alt.GetNbinsY())))
            print('\t inc: %0.3f | %0.3f = %d/%d' % (oodFraction_inc, odbFraction_inc, odbN_inc, (resp_inc.GetNbinsX()*resp_inc.GetNbinsY())))
            resp_nom.Draw('COLZ')
            utils.saveCanva(c, os.path.join(self.outputDir, '1_responseMatrixAsPdf_%s_Nom' % self.var))
            c.Clear()
            resp_alt.Draw('COLZ')
            utils.saveCanva(c, os.path.join(self.outputDir, '1_responseMatrixAsPdf_%s_Alt' % self.var))
            c.Clear()
            resp_inc.Draw('COLZ')
            utils.saveCanva(c, os.path.join(self.outputDir, '1_responseMatrixAsPdf_%s_Inc' % self.var))

        self.response_nom.Draw('COLZ')
        utils.saveCanva(c, os.path.join(self.outputDir, '1_responseMatrix_%s_Nom' % self.var))
        c.Clear()
        self.response_alt.Draw('COLZ')
        utils.saveCanva(c, os.path.join(self.outputDir, '1_responseMatrix_%s_Alt' % self.var))
        c.Clear()
        self.response_inc.Draw('COLZ')
        utils.saveCanva(c, os.path.join(self.outputDir, '1_responseMatrix_%s_Inc' % self.var))
    
    def get_total_bkg_as_hist(self, file_handle, action):
        totbkg = []
        totbkg.append(copy.deepcopy(file_handle.Get('x_prompt_ZZH')))
        totbkg.append(copy.deepcopy(file_handle.Get('x_fakes_appldata')))
        totbkg.append(copy.deepcopy(file_handle.Get('x_convs')))
        totbkg.append(copy.deepcopy(file_handle.Get('x_rares_ttX')))
        totbkg.append(copy.deepcopy(file_handle.Get('x_rares_VVV')))
        totbkg.append(copy.deepcopy(file_handle.Get('x_rares_tZq')))
        if 'sum' in action:
            for i in range(1,len(totbkg)):
                totbkg[0].Add(totbkg[i])
            return totbkg[0]
        return totbkg

    def get_graph_as_hist(self, g, args):
        h = ROOT.TH1F(args[0], args[1], args[2], args[3], args[4])

        for ibin in range(0,args[2]):
            x=0
            y=0
            g.GetPoint(ibin, ROOT.Double(x), ROOT.Double(y))
            h.Fill(x,y)
        print('h bins: %d; g bin: %d' %(h.GetNbinsX(), g.GetN()))
        #g.Draw('PAE')
        #print('h bins: %d; g bin: %d' %(h.GetNbinsX(), g.GetN()))
        #h=copy.deepcopy(ROOT.TH1F(g.GetHistogram()))
        print('h bins: %d; g bin: %d' %(h.GetNbinsX(), g.GetN()))
        return h

    def print_histo(self,h,key,label,opt=''):
        c = ROOT.TCanvas(h.GetName(), h.GetTitle(), 2000, 2000)
        c.cd()
        h.Draw(opt)
        utils.saveCanva(c, os.path.join(args.outputDir, '2_unfoldResults_%s_%s_%s_%s' % (label, key, self.var, h.GetName()) ))

    def do_unfolding(self, key):

        self.histmap=ROOT.TUnfold.kHistMapOutputVert
        # kHistMapOutputHoriz (truth is in X axis), kHistMapOutputVert (truth is in Y axis)
        self.regmode=ROOT.TUnfold.kRegModeNone
        # kRegModeNone (no reg), kRegModeSize (reg amplitude of output), kRegModeDerivative (reg 1st derivative of output), kRegModeCurvature (reg 2nd derivative of output),  kRegModeMixed (mixed reg patterns)
        self.constraint=ROOT.TUnfold.kEConstraintArea
        # kEConstraintNone (no extra constraint), kEConstraintArea (enforce preservation of area)
        self.densitymode= ROOT.TUnfoldDensity.kDensityModeBinWidth
        # kDensityModeNone (no scale factors, matrix L is similar to unity matrix), kDensityModeBinWidth (scale factors from multidimensional bin width), kDensityModeUser (scale factors from user function in TUnfoldBinning), kDensityModeBinWidthAndUser (scale factors from multidimensional bin width and user function)

        label='noreg'
        # First do it with no regularization
        self.set_unfolding(key)
        self.do_scan()
        self.print_unfolding_results(key, label)
     
        # Now add simple regularization on the amplitude
        self.regmode=ROOT.TUnfold.kRegModeSize
        label='regamp'
        self.set_unfolding(key)
        self.do_scan()
        self.print_unfolding_results(key, label)


    def set_unfolding(self, key):

        if   key == 'nom':
            self.unfold = ROOT.TUnfoldDensity(self.response_nom, self.histmap, self.regmode, self.constraint, self.densitymode)
        elif key == 'alt':
            self.unfold = ROOT.TUnfoldDensity(self.response_alt, self.histmap, self.regmode, self.constraint, self.densitymode)
        elif key == 'inc':
            self.unfold = ROOT.TUnfoldDensity(self.response_inc, self.histmap, self.regmode, self.constraint, self.densitymode)
        else:
            print('ERROR: the response matrix you asked for (%s) does not exist' % key)
        # Check if the input data points are enough to constrain the unfolding process
        check = self.unfold.SetInput(self.data)
        if check>=10000:
            print('TUnfoldDensity error %d! Unfolding result may be wrong (not enough data to constrain the unfolding process)' % check)
        # Now I should do subtraction using the class. I assign a 10% error on each background. This will have to be set automatically
        scale_bgr=1.0
        dscale_bgr=0.1
        for iBkg in self.bkg:
            self.unfold.SubtractBackground(iBkg,iBkg.GetName(),scale_bgr,dscale_bgr);
        # Add systematic error
        # unfold.AddSysError(histUnfoldMatrixSys,"signalshape_SYS", TUnfold::kHistMapOutputHoriz, TUnfoldSys::kSysErrModeMatrix)

            

    def do_scan(self):
        # Scan the L-curve and find the best point
        
        # Set verbosity
        oldinfo=ROOT.gErrorIgnoreLevel
        if self.verbose:
            ROOT.gErrorIgnoreLevel=kInfo

        # Scan the parameter tau, finding the kink in the L-curve. Finally, do the unfolding for the best choice of tau
        if self.regmode == ROOT.TUnfold.kRegModeNone:
            self.unfold.DoUnfold(0.0)
            self.iBest=0.0
        else:
            self.iBest=self.unfold.ScanLcurve(self.nScan, self.tauMin, self.tauMax, self.lCurve, self.logTauX, self.logTauY)

        # Reset verbosity
        if self.verbose:
            ROOT.gErrorIgnoreLevel=oldInfo

        # Here do something for the error
        ### 

    def print_unfolding_results(self, key, label):
        # Print results
        print('Tau: %d' % self.unfold.GetTau())
        print('chi^2: %d+%d/%d' %(self.unfold.GetChi2A(), self.unfold.GetChi2L(), self.unfold.GetNdf() ) )
        print('chi^2(syst): %d' % self.unfold.GetChi2Sys())
        
        print('ibest: %d, type %s' % ( self.iBest, type(self.iBest)))
        # Visualize best choice of tau

        bestLcurve = None
        bestLogTauLogChi2 = None
        if self.regmode is not ROOT.TUnfold.kRegModeNone:
            t=0.0
            x=0.0
            y=0.0
            self.logTauX.GetKnot(self.iBest, ROOT.Double(t), ROOT.Double(x))
            self.logTauY.GetKnot(self.iBest, ROOT.Double(t), ROOT.Double(y))
            vt =array('d')
            vx =array('d')
            vy =array('d')
            vt.append(t)
            vx.append(x)
            vy.append(y)
            bestLcurve = ROOT.TGraph(1, vx, vy)
            bestLogTauLogChi2 = ROOT.TGraph(1, vt, vx);
        
        # Retrieve results as histograms
        histMunfold=self.unfold.GetOutput('Unfolded') # Unfolded result
        histMdetFold=self.unfold.GetFoldedOutput('FoldedBack') # Unfolding result, folded back
        histEmatData=self.unfold.GetEmatrixInput('EmatData') # Error matrix (stat errors only)
        histEmatTotal=self.unfold.GetEmatrixTotal('EmatTotal') # Total error matrix. Migration matrix uncorrelated and correlated syst errors added in quadrature to the data statistical errors
        
        
        #TH1 *histDetNormBgr1=unfold.GetBackground("bgr1 normalized",
        #                                          "background1");
        histDetNormBgrTotal=self.unfold.GetBackground("Total background (normalized)")



        nDet=self.response_nom.GetNbinsX()
        nGen=self.response_nom.GetNbinsY()
        xminDet=self.response_nom.GetXaxis().GetBinLowEdge(1)
        xmaxDet=self.response_nom.GetXaxis().GetBinUpEdge(self.response_nom.GetNbinsX())
        xminGen=self.response_nom.GetYaxis().GetBinLowEdge(1)
        xmaxGen=self.response_nom.GetYaxis().GetBinUpEdge(self.response_nom.GetNbinsY())
        histTotalError = ROOT.TH1D('TotalError',';%s(gen)' % self.var, nGen, xminGen, xmaxGen)# Data histogram with total errors
        for bin in range(1,nGen):
            histTotalError.SetBinContent(bin, histMunfold.GetBinContent(bin))
            histTotalError.SetBinError(bin, ROOT.TMath.Sqrt(histEmatTotal.GetBinContent(bin,bin)))


        print('Now get global correlation coefficients')
        # get global correlation coefficients
        # for this calculation one has to specify whether the
        # underflow/overflow bins are included or not
        # default: include all bins
        # here: exclude underflow and overflow bins

        #self.gHistInvEMatrix=copy.deepcopy(self.response_nom)
        #self.gHistInvEMatrix.SetName('gHistInvEMatrix')
        #self.gHistInvEMatrix.Print()
        #histRhoi=self.unfold.GetRhoItotal('rho_I',
        #                                  '', # use default title
        #                                  '', # all distributions
        #                                  "*[UO]", # discard underflow and overflow bins on all axes
        #                                  ROOT.kTRUE, # use original binning
        #                                  self.gHistInvEMatrix # store inverse of error matrix
        #                                  )

        # other try self.gHistInvJEMatrix=self.unfold.GetRhoIJtotal('rho_I',
        # other try                                     '', # use default title
        # other try                                     '', # all distributions
        # other try                                     "*[UO]", # discard underflow and overflow bins on all axes
        # other try                                     ROOT.kTRUE, # use original binning
        # other try                                     )
        #  
        #  #======================================================================
        #  # fit Breit-Wigner shape to unfolded data, using the full error matrix
        #  # here we use a "user" chi**2 function to take into account
        #  # the full covariance matrix
        #  
        #  #gFitter=TVirtualFitter::Fitter(histMunfold)
        #  #gFitter.SetFCN(chisquare_corr)
        #  
        #  bw=TF1("bw",bw_func,xminGen,xmaxGen,3)
        #  bw.SetParameter(0,1000.)
        #  bw.SetParameter(1,3.8)
        #  bw.SetParameter(2,0.2)
        #  
        #  # for (wrong!) fitting without correlations, drop the option "U"
        #  # here.
        #  histMunfold.Fit(bw,"UE")

        # =====================================================================
        #  plot some histograms
        output=ROOT.TCanvas('out', 'out', 2000, 2000)
        output.Divide(3,2)

        # Show the matrix which connects input and output
        # There are overflow bins at the bottom, not shown in the plot
        # These contain the background shape.
        # The overflow bins to the left and right contain
        # events which are not reconstructed. These are necessary for proper MC
        # normalisation
        #output.cd(1)
        ##histMdetGenMC.Draw("BOX")

        output.cd(1)
        # Data, MC prediction, background
        self.data.SetMinimum(0.0)
        self.data.Draw("E")
        self.mc.SetMinimum(0.0)
        self.mc.SetLineColor(ROOT.kBlue)
        self.mc.SetLineWidth(3)
        histDetNormBgrTotal.SetLineColor(ROOT.kRed)
        histDetNormBgrTotal.SetLineWidth(3)
        #histDetNormBgr1->SetLineColor(kCyan);
        self.mc.Draw("SAME HIST")
        #histDetNormBgr1->Draw("SAME HIST");
        histDetNormBgrTotal.Draw("SAME HIST")

        print(self.data.GetNbinsX())
        print(self.mc.GetNbinsX())
        print(histDetNormBgrTotal.GetNbinsX())
        
        # draw generator-level distribution:
        #   data (red) [for real data this is not available]
        #   MC input (black) [with completely wrong peak position and shape]
        #   unfolded data (blue)
        output.cd(2)
        # Data with total error
        histTotalError.SetLineColor(ROOT.kBlue)
        histTotalError.Draw("E")
        # Unfolded data
        histMunfold.SetLineColor(ROOT.kGreen)
        histMunfold.Draw("SAME E1")
        # MC truth (folded) Must substitute with input truth from response matrix probably
        self.mc.Draw("SAME HIST")
        ###histDensityGenData.SetLineColor(kRed)
        ##histDensityGenData.Draw("SAME")
        ##histDensityGenMC.Draw("SAME HIST")
        
        # show detector level distributions
        #    data (red)
        #    MC (black) [with completely wrong peak position and shape]
        #    unfolded data (blue)
        output.cd(3)
        # Folded back
        histMdetFold.SetLineColor(ROOT.kBlue)
        histMdetFold.Draw()
        # Original folded MC
        self.mc.Draw("SAME HIST")

        histInput=self.unfold.GetInput("Minput",";mass(det)")

        histInput.SetLineColor(ROOT.kRed)
        histInput.SetLineWidth(3)
        histInput.Draw("SAME")

        # show correlation coefficients
        output.cd(4)
        ##histRhoi.Draw()


        if self.regmode is not ROOT.TUnfold.kRegModeNone:
            # show tau as a function of chi**2
            output.cd(5)
            self.logTauX.Draw()
            bestLogTauLogChi2.SetMarkerColor(ROOT.kRed)
            bestLogTauLogChi2.SetLineWidth(3)
            bestLogTauLogChi2.Draw("*")            
            # show the L curve
            output.cd(6)
            self.lCurve.Draw("AL")
            bestLcurve.SetMarkerColor(ROOT.kRed)
            bestLcurve.SetMarkerStyle(21)
            bestLcurve.Draw("*")
            
        output.SaveAs(os.path.join(self.outputDir, '2_unfold_%s_%s_%s.png' % (label, key, self.var)))

        # Individual saving.
        self.print_histo(histMunfold, key, label)
        self.print_histo(histMdetFold, key, label)
        self.print_histo(histEmatData, key, label, 'colz')
        self.print_histo(histEmatTotal, key, label, 'colz')
        self.print_histo(histTotalError, key, label)


### End class Unfolder
def main(args): 
    print('start')
    #for var in ['Zpt', 'ZconePt', 'nJet30']: # Must build correct gen matrix for nJet30 (need friend trees). Also, don't study conePt for now
    for var in ['Zpt']:
        u = Unfolder(args,var)
        u.print_responses()
        u.do_unfolding('nom')
        u.do_unfolding('alt')
        u.do_unfolding('inc')

### End main

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputDir',     help='Input directory', default=None)
    parser.add_argument('-o', '--outputDir',    help='Output directory', default='./')
    parser.add_argument('-c', '--combineInput', help='Data and postfit from combine output', default=None)
    parser.add_argument('-d', '--data',         help='File containing data histogram', default=None)
    parser.add_argument('-m', '--mc',           help='File containing mc reco histogram', default=None)
    parser.add_argument('-g', '--gen',          help='File containing gen info for matrix', default=None)
    parser.add_argument('-l', '--lepCat',       help='Lepton multiplicity (1 or 2)', default=1, type=int)
    parser.add_argument('-e', '--epochs',       help='Number of epochs', default=100, type=int)
    parser.add_argument('-s', '--splitMode',    help='Split mode (input or random)', default='input')
    parser.add_argument('-v', '--verbose',      help='Verbose printing of the L-curve scan', action='store_true')
    parser.add_argument('-r', '--responseAsPdf', help='Print response matrix as pdf', action='store_true') 
    args = parser.parse_args()
    # execute only if run as a script
    ROOT.gROOT.SetBatch()
    main(args)
