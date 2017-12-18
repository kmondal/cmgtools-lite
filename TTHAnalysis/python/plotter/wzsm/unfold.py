import os
import copy

import argparse

import utils
import ROOT
from ROOT import * # Lazy bastard

class AcceptanceComputer:

    def __init__(self, inputFiles):
        print('Initialization')
        print('Input files are: %s' % inputFiles)

### End class AcceptanceCounter

class Unfolder(object):

    def __init__(self, args):
        print('Initialization')
        self.unfold=None
        self.response=None
        self.data=None
        self.mc=None
        self.response=None
        self.proofOfConcept=True
        self.verbose=args.verbose
        self.nScan=30
        # Automatic L-curve scan: start with taumin=taumax=0.0
        self.tauMin=0.0
        self.tauMax=0.0
        self.iBest=None # Best value
        self.logTauX=None # TSpline*
        self.logTauY=None # TSpline*
        self.lCurve=TGraph(0) # TGraph*

        self.load_data(args.inputDir, args.data, args.mc, args.gen)

    def load_data(self, folder, dataFName, mcFName, genFName, treeName=['tree']):
        # To be extended with the damn friend trees
        # Alternatively, take some minitrees as input (with only the few variables we are interested in. This is a better option, actually.
        # TH1D MgenMC;1
        # TH1D MdetMC;1
        # TH2D MdetgenMC;1
        # TH2D MdetgenSysMC;1
        # TH1D MgenData;1
        # TH1D MdetData;1
        # TH1D DensityGenData;1
        # TH1D DensityGenMC;1
        if self.proofOfConcept:
            file_handle = TFile.Open('wzsm/testUnfold.root')
            self.data     = copy.deepcopy(TH1D(file_handle.Get('MdetData') ))
            self.mc       = copy.deepcopy(TH1D(file_handle.Get('MdetMC')   ))
            self.response = copy.deepcopy(TH2D(file_handle.Get('MdetgenMC')))

        else:
            dataFile = get_file_from_glob(os.path.join(folder, dataFName) if folder else dataFName)
            mcFile   = get_file_from_glob(os.path.join(folder, mcFName)   if folder else mcFName)
            genFile  = get_file_from_glob(os.path.join(folder, genFName)  if folder else genFName)
            #data_handle = TFile.Open(dataFile)
            #mc_handle   = TFile.Open(mcFile)
            # Pass histograms, not trees?
            self.data = TChain("data")
            self.data.Add(dataFile+'/'+treeName)
            self.mc = TChain("mc")
            self.mc.Add(mcFile+'/'+treeName)
            # Add reading gen file to build response matrix

        # Pass through numpy arrays?
        #return data, mc, response
        
    def build_response(self):
        print('Dummy function at the moment. Here we build the matrix, if it does not arrive pre-computed.')

    def print_response(self):
        c = TCanvas('matrix', 'Response Matrix', 2000, 2000)
        c.cd()
        self.response.Draw('COLZ')
        utils.saveCanva(c, os.path.join(args.outputDir, 'responseMatrix'))

    def set_unfolding(self):
        self.unfold = TUnfoldDensity(self.response,TUnfold.kHistMapOutputVert)
        # Check if the input data points are enough to constrain the unfolding process
        check = self.unfold.SetInput(self.data)
        if check>=10000:
            print('TUnfoldDensity error %d! Unfolding result may be wrong (not enough data to constrain the unfolding process)' % check)

    def do_scan(self):
        # Scan the L-curve and find the best point
        
        # Set verbosity
        oldinfo=ROOT.gErrorIgnoreLevel
        if self.verbose:
            ROOT.gErrorIgnoreLevel=kInfo

        # Scan the parameter tau, finding the kink in the L-curve. Finally, do the unfolding for the best choice of tau
        iBest=self.unfold.ScanLcurve(self.nScan, self.tauMin, self.tauMax, self.lCurve, self.logTauX, self.logTauY)

        # Reset verbosity
        if self.verbose:
            ROOT.gErrorIgnoreLevel=oldInfo

        # Here do something for the error
        ### 

    def print_unfolding_results(self):
        # Print results
        print('Tau: %d' % self.unfold.GetTau())
        print('chi^2: %d+%d/%d' %(self.unfold.GetChi2A(), self.unfold.GetChi2L(), self.unfold.GetNdf() ) )
        print('chi^2(syst): %d' % self.unfold.GetChi2Sys())
            
        # Visualize best choice of tau
        t=[]
        x=[]
        y=[]
        self.logTauX.GetKnot(self.iBest, t, x)
        self.logTauY.GetKnot(self.iBest, t, y)
        bestLcurve = TGraph(1, x, y)
        bestLogTauLogChi2 = TGraph(1, t, x);
        
        # Retrieve results as histograms

        histMunfold=TH1(self.unfold.GetOutput('Unfolded')) # Unfolded result
        histMdetFuld=TH1(self.unfold.GetFoldedOutput('FoldedBack')) # Unfolding result, folded back
        # histEmatData=TH1(self.unfold.GetEmatrix('EmatData0')) # Error matrix (stat errors only)
        histEmatTotal=TH2(self.unfold.GetEmatrixTotal('EmatTotal')) # Total error matrix. Migration matrix uncorrelated and correlated syst errors added in quadrature to the data statistical errors

        histTotalError = TH1D('TotalError',';mass(gen)', nGen, xminGen, xmaxGen)# Data histogram with total errors


### End class Unfolder
def main(args): 
    u = Unfolder(args)
    u.build_response() # Not really needed at the moment (assuming it's already built outside)
    u.print_response()
    u.set_unfolding()
    u.do_scan()
    u.print_unfolding_results()

### End main
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputDir',   help='Input directory', default=None)
    parser.add_argument('-o', '--outputDir',  help='Output directory', default='./')
    parser.add_argument('-d', '--data',       help='File containing data histogram', default=None)
    parser.add_argument('-m', '--mc',         help='File containing mc reco histogram', default=None)
    parser.add_argument('-g', '--gen',   help='File containing gen info for matrix', default=None)
    parser.add_argument('-l', '--lepCat',     help='Lepton multiplicity (1 or 2)', default=1, type=int)
    #parser.add_argument('-m', '--multiclass', help='Multiclass (ttbar-LF and ttbar-HF are in different classes)', action='store_true')
    parser.add_argument('-e', '--epochs',     help='Number of epochs', default=100, type=int)
    parser.add_argument('-s', '--splitMode',  help='Split mode (input or random)', default='input')
    parser.add_argument('-v', '--verbose',    help='Verbose printing of the L-curve scan', action='store_true')

#parser.add_argument('-n', '--nevts',      help='Number of events to be loaded from tree', default=-1, type=int)
    args = parser.parse_args()
    # execute only if run as a script
    gROOT.SetBatch()
    main(args)
