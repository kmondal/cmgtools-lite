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

import tdrstyle as tdr
import CMS_lumi

CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
# PAS: CMS_lumi.extraText = "Preliminary"
CMS_lumi.extraText = ""
CMS_lumi.lumi_sqrtS = "13 TeV"
CMS_lumi.lumiTextSize     = 0.80
CMS_lumi.lumiTextOffset   = 0.2
#CMS_lumi.cmsTextSize      = 0.55
CMS_lumi.cmsTextSize      = 0.80
CMS_lumi.cmsTextOffset    = 0.1

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
        
        
        
class DatacardReader:

    def __init__(self, inputCard, signalString=None):
        print('Initialization for card %s' % inputCard)
        self.inputCard=inputCard
        self.signalString=signalString
        self.systs = [] #Systematics, ordered by appearance
        self.normSysts = [] # Normalization-only uncertainties
        self.unsymNormSystsUp = [] # Normalization-only uncertainties, non symmetrized
        self.unsymNormSystsDn = [] # Normalization-only uncertainties, non symmetrized
        self.shapeSysts = [] # Shape(+eventually norm) uncertainties
        self.systsLines = [] #The - - - number1 - - systematic lines
        self.shapeFiles = [] #The input shape rootfiles
        self.shapeBins  = [] #The input bins (in datacard line bins)
        self.proctoFile = {} #To pass from process to the file with the shapes
        self.processes = [] # List of processes
        self.readDataCard()
        if self.signalString:
            self.filterSystsByProcess()

    def getSysts(self):
        return self.systs

    def getNormAndShapeSysts(self):
        return self.normSysts, self.shapeSysts

    def getUnsymNormSysts(self):
        return self.unsymNormSystsUp, self.unsymNormSystsDn

    def getSystsAndLines(self):
        return self.systs, self.systsLines, self.altSysts

    def filterSystsByProcess(self):
        sig_idx=self.processes.index(self.signalString)
        tempSysts = []
        for line in self.systsLines:
            tempLine=line.split()
            if '1' in tempLine[sig_idx+2]:
                tempSysts.append(self.systs[self.systsLines.index(line)])
                if 'lnN' in tempLine[1]:
                    tempForSym=tempLine[sig_idx+2].split('/')
                    danum=0.0
                    for iTempForSym in tempForSym:
                        if abs(1-float(iTempForSym)) > danum:
                            danum=abs(1-float(iTempForSym))
                    self.normSysts.append([ self.systs[self.systsLines.index(line)] , '%f' % (1+abs(danum)) ])
                    if len(tempForSym) > 1:
                        self.unsymNormSystsUp.append([ self.systs[self.systsLines.index(line)] , '%f' % (float(tempForSym[0])) ])
                        self.unsymNormSystsDn.append([ self.systs[self.systsLines.index(line)] , '%f' % (float(tempForSym[1])) ])

                if 'shape' in tempLine[1]:
                    print('Line is %s' % tempLine)
                    print('\t\t Accessing syst %s for process %s ' % (self.systs[self.systsLines.index(line)], self.signalString) )
                    print(os.path.join(os.path.dirname(self.inputCard), self.shapeFiles[0]))
                    print('x_%s_%sUp' %( self.signalString, self.systs[self.systsLines.index(line)]))
                    print('x_%s_%sDown' %( self.signalString, self.systs[self.systsLines.index(line)] )) 
                    handle_No=ROOT.TFile.Open(os.path.join(os.path.dirname(self.inputCard), self.shapeFiles[0]))
                    handle_Up=ROOT.TFile.Open(os.path.join(os.path.dirname(self.inputCard), self.shapeFiles[0]))
                    handle_Dn=ROOT.TFile.Open(os.path.join(os.path.dirname(self.inputCard), self.shapeFiles[0]))
                    myshapeNo=copy.deepcopy(handle_No.Get('x_%s' %( self.signalString ) ))
                    myshapeUp=copy.deepcopy(handle_Up.Get('x_%s_%sUp' %( self.signalString, self.systs[self.systsLines.index(line)] ) ))
                    myshapeDn=copy.deepcopy(handle_Dn.Get('x_%s_%sDown' %( self.signalString, self.systs[self.systsLines.index(line)] ) ))
                    unc= myshapeUp if (abs(myshapeUp.Integral()) > abs(myshapeDn.Integral())) else myshapeDn
                    self.shapeSysts.append([ self.systs[self.systsLines.index(line)] , unc ] )
                    
        self.systs = tempSysts

    def readDataCard(self):
        """ Get Text info from the original datacard """
        processGet = False
        tempFile = open(self.inputCard,"r")
        for line in tempFile.readlines():
          if line[0] == "#": continue
          tempLine = line.split()
          if tempLine[0] in ["jmax","kmax","observation","rate"]: continue
          if tempLine[0] == "bin":
            if len(tempLine) == (len(self.shapeBins) + 1):
              continue
            else:
              self.shapebinsforProcesses = tempLine[1:]
              continue
          if tempLine[0] == "imax":
            self.imax = line
            continue
          if tempLine[0] == "shapes":
            self.shapeBins.append(tempLine[2])
            for word in tempLine:
              if ".root" in word:
                self.shapeFiles.append(word)
            self.proctoFile[tempLine[2]] = self.shapeFiles[-1]
            continue
        
          if tempLine[0]=="process":
            if not processGet: 
              self.processes = tempLine[1:]
              processGet = True
            else:
              self.processesNums = tempLine[1:]
              processGet = False
            continue      
          if 'stat' in tempLine[0]: continue
          if 'autoMCStats' in tempLine[1]: continue
          self.systs.append(tempLine[0])
          self.systsLines.append(line)

        #if self.nBins == -1: #This breaks if more than one shapes file is being used
        #  temp = ROOT.TFile("/".join(self.inputCard.split("/")[:-1]) + "/" + self.shapeFiles[0], "READ")
        #  self.nBins = temp.Get("data_obs").GetNbinsX()
        #  temp.Close()


### End class DatacardReader
        
class AcceptanceComputer:

    def __init__(self, inputFiles):
        print('Initialization')
        print('Input files are: %s' % inputFiles)

### End class AcceptanceCounter

class Unfolder(object):

    def __init__(self, args, var, fancyvar, diffvar):
        print('Initialization')
        self.var=var
        self.fancyvar=fancyvar
        self.diffvar=diffvar
        self.logx = False if self.var is not 'MWZ' else True
        self.unfold=None
        self.response_nom=None
        self.response_alt=None
        self.response_inc=None
        self.varied_responses=None
        self.data=None
        self.dataTruth_nom=None
        self.dataTruth_nom_up=None
        self.dataTruth_nom_dn=None
        self.dataTruth_alt=None
        self.dataTruth_inc=None
        self.mc=None
        self.bkg=None
        self.normSystsList=None
        self.unsymSystsList=None
        self.shapeSystsList=None
        self.finalState=args.finalState
        self.charge=args.charge
        if 'none' in self.charge:
            self.charge = ''
        self.bias=args.bias
        self.areaConstraint=args.areaConstraint
        self.verbose=args.verbose
        self.combineInput=args.combineInput
        self.nScan=20
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
        self.constraint=ROOT.TUnfold.kEConstraintNone
        self.densitymode=ROOT.TUnfoldDensity.kDensityModeeNone
        self.closure=args.closure
        self.load_data(args.data, args.mc, args.gen)

        ROOT.gStyle.SetOptStat(0)
        # Make sure histogram errors are ON
        ROOT.TH1.SetDefaultSumw2()


    def load_data(self, dataFName, mcFName, genFName, treeName=['tree']):
        folder=self.inputDir
        dataFile=None
        mcFile=None
        #genFile=None # Taken from a separate file  
        print('diocane is', self.charge)
        print('Opening file %s.' % utils.get_file_from_glob(os.path.join(folder, '%s_fitWZonly_%s%s/%s' % (self.finalState, self.var, self.charge, self.combineInput) ) if folder else self.combineInput) )
        file_handle = ROOT.TFile.Open(utils.get_file_from_glob(os.path.join(folder,  '%s_fitWZonly_%s%s/%s' % (self.finalState, self.var, self.charge, self.combineInput)) if folder else self.combineInput))
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
        if self.closure:
            data=self.getDataFromClosure(signal, bkg)
            
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
        #self.rebin_all(4)
        # Pass through numpy arrays?
        print('Data correctly loaded.')
        #return data, mc, response

    def getDataFromClosure(self, hin, bkg):
        hout=copy.deepcopy(hin)
        for ibkg in bkg:
            hout.Add(ibkg)

        for ibin in range(0, hout.GetNbinsX()+2):
            g=ROOT.TRandom3(0) # Random seed
            c=g.Gaus(hout.GetBinContent(ibin), hout.GetBinError(ibin))
            e=hout.GetBinError(ibin)*c/hout.GetBinContent(ibin) if hout.GetBinContent(ibin)!=0 else 0
            hout.SetBinContent(ibin, c)
            hout.SetBinError(ibin, e)
        print('Closure data bins: %d' % hout.GetNbinsX())
        return hout
    
        
    def rebin_all(self,n):
        self.data.Rebin(n/2)
        self.mc.Rebin(n/2)
        for i in range(1,len(self.bkg)):
            self.bkg[i].Rebin(n/2)
        self.response_nom.RebinX(n/2)
        self.response_alt.RebinX(n/2)
        self.response_inc.RebinX(n/2)
        self.response_nom.RebinY(n/2)
        self.response_alt.RebinY(n/2)
        self.response_inc.RebinY(n/2)
        self.dataTruth_nom.RebinY(n/2)
        self.dataTruth_alt.RebinY(n/2)
        self.dataTruth_inc.RebinY(n/2)

    def study_responses(self):
        self.compute_stability_and_purity()
        for matrix in [self.response_nom, self.response_alt, self.response_inc]:
            # Errors are the standard deviation of the Y values
            profX=matrix.ProfileX('%s_profX'%matrix.GetName(), 0, matrix.GetNbinsY(),'s')
            profY=matrix.ProfileY('%s_profY'%matrix.GetName(), 0, matrix.GetNbinsX(),'s')
            print(profX)
            print(profY)
            c = ROOT.TCanvas('matrix', 'Response Matrix', 2000, 1000)
            tdr.setTDRStyle()
            # Margin not being applied somehow. Must do it via gStyle? Current suspicion: now that I have the TStyle, they are screwing the tdr style up
            #ROOT.gStyle.SetPadTopMargin(0.1)
            #ROOT.gStyle.SetPadBottomMargin(0.1)
            #ROOT.gStyle.SetPadLeftMargin(0.1)
            #ROOT.gStyle.SetPadRightMargin(0.1)
            #ROOT.gStyle.SetOptStat('uo')
            c.Divide(2,1)
            c.cd(1)
            ROOT.gPad.SetGrid()
            profX.SetMarkerStyle(ROOT.kFullSquare)
            profX.SetTitle('Response (gen profiled)')
            profX.GetXaxis().SetTitle('Reco %s' % self.fancyvar)
            profX.GetYaxis().SetTitle('Mean Gen %s' % self.fancyvar)
            profX.Draw("PE")
            c.cd(2)
            ROOT.gPad.SetGrid()
            profY.SetMarkerStyle(ROOT.kFullSquare)
            profY.SetTitle('Response (reco profiled)')
            profY.GetXaxis().SetTitle('Gen %s' % self.fancyvar)
            profY.GetXaxis().SetTitle('Mean Reco %s' % self.fancyvar)
            profY.Draw("PE")
            CMS_lumi.CMS_lumi(c, 4, 0, aLittleExtra=0.08)
            utils.saveCanva(c, os.path.join(self.outputDir, '1_responseProfiled_%s_%s' % (matrix.GetName(), self.var)))            
            c.IsA().Destructor(c)


    def get_truth_theory_variations(self, datacardReader):

        # For the moment, add only the overall normalization uncertainty, without bothering with the shape component 
        #self.dataTruth_nom_up, self.dataTruth_nom_dn = ... datacardReader.getTheoUncsOnNom()
        
        self.unsymNormSystsDn, self.unsymNormSystsUp = datacardReader.getUnsymNormSysts()
        
        self.dataTruth_nom_up = copy.deepcopy(ROOT.TH1D(self.dataTruth_nom))
        self.dataTruth_nom_dn = copy.deepcopy(ROOT.TH1D(self.dataTruth_nom))
        factorUp=0.0
        factorDn=0.0
        for [sysName, sysValue] in self.unsymNormSystsUp:
            sysValue=float(sysValue)
            if ('scaleNorm' in sysName) or ('pdfNorm' in sysName):
                factorUp += sysValue*sysValue
        for [sysName, sysValue] in self.unsymNormSystsDn:
            sysValue=float(sysValue)
            if ('scaleNorm' in sysName) or ('pdfNorm' in sysName):
                factorDn += sysValue*sysValue

        factorUp=ROOT.TMath.Sqrt(factorUp)
        factorDn=ROOT.TMath.Sqrt(factorDn)
        print("PORCHODIO")
        print(factorUp, factorDn)
        print(self.dataTruth_nom_up.Integral(), self.dataTruth_nom_dn.Integral())
        self.dataTruth_nom_up.Scale(factorUp)
        self.dataTruth_nom_dn.Scale(factorDn)
        print(self.dataTruth_nom_up.Integral(), self.dataTruth_nom_dn.Integral())

    def get_responses(self):
        print('Acquiring response matrices.')
        folder=os.path.join(self.inputDir, 'responses/%s_fitWZonly_%s%s/common/' % (self.finalState, self.var, self.charge) )        

        file_handle = ROOT.TFile.Open('%sWZSR.input.root' % (folder))
        print('Opening file: %s' % file_handle.GetName())
        #file_handle_alt = ROOT.TFile.Open('%sWZSR.input.root' % (folder))
        #file_handle_inc = ROOT.TFile.Open('%sWZSR.input.root' % (folder))
        
        self.response_nom = copy.deepcopy(ROOT.TH2D(file_handle.Get('x_prompt_altWZ_%s' % 'Pow')))
        self.response_alt = copy.deepcopy(ROOT.TH2D(file_handle.Get('x_prompt_altWZ_%s' % 'aMC')))
        self.response_inc = copy.deepcopy(ROOT.TH2D(file_handle.Get('x_prompt_altWZ_%s' % 'Inc')))

        self.dataTruth_nom = copy.deepcopy(ROOT.TH1D(self.response_nom.ProjectionY('dataTruth_nom', 0, self.response_nom.GetNbinsX())))
        self.dataTruth_alt = copy.deepcopy(ROOT.TH1D(self.response_alt.ProjectionY('dataTruth_alt', 0, self.response_alt.GetNbinsX())))
        self.dataTruth_inc = copy.deepcopy(ROOT.TH1D(self.response_inc.ProjectionY('dataTruth_inc', 0, self.response_inc.GetNbinsX())))

        print('Response binsX %d, binsY %d' % (self.response_nom.GetNbinsX(), self.response_nom.GetNbinsY()))
        
        for ibin in range(0, self.response_nom.GetNbinsX()+2):
            for jbin in range(0, self.response_nom.GetNbinsY()+2):
                if ibin==0 or jbin==0 or ibin>self.response_nom.GetNbinsX() or jbin>self.response_nom.GetNbinsY():
                    self.response_nom.SetBinContent(ibin, jbin, 0)
                    self.response_alt.SetBinContent(ibin, jbin, 0)
                    self.response_inc.SetBinContent(ibin, jbin, 0)
                    self.response_nom.SetBinError(ibin, jbin, 0)
                    self.response_alt.SetBinError(ibin, jbin, 0)
                    self.response_inc.SetBinError(ibin, jbin, 0)
                    
        datacardReader = DatacardReader(os.path.join(self.inputDir, 'responses/%s_fitWZonly_%s%s/prompt_altWZ_Pow/WZSR.card.txt' % (self.finalState, self.var,self.charge)), 'prompt_altWZ_Pow')
        self.normSystsList, self.shapeSystsList = datacardReader.getNormAndShapeSysts()
        # Get theory variations
        self.get_truth_theory_variations(datacardReader)
        



    def print_responses(self):
        c = ROOT.TCanvas('matrix', 'Response Matrix', 2000, 2000)
        c.cd()
        # Margin not being applied somehow. Must do it via gStyle?
        #ROOT.gStyle.SetPadTopMargin(0.1)
        #ROOT.gStyle.SetPadBottomMargin(0.1)
        #ROOT.gStyle.SetPadLeftMargin(0.1)
        #ROOT.gStyle.SetPadRightMargin(0.1)
        #ROOT.gStyle.SetOptStat('uo')
        self.response_nom.GetXaxis().SetTitle('Reco %s' % self.fancyvar)
        self.response_alt.GetXaxis().SetTitle('Reco %s' % self.fancyvar)
        self.response_inc.GetXaxis().SetTitle('Reco %s' % self.fancyvar)
        self.response_nom.GetYaxis().SetTitle('Gen %s' % self.fancyvar)
        self.response_alt.GetYaxis().SetTitle('Gen %s' % self.fancyvar)
        self.response_inc.GetYaxis().SetTitle('Gen %s' % self.fancyvar)
        self.response_nom.GetYaxis().SetTitleOffset(1.7)
        self.response_alt.GetYaxis().SetTitleOffset(1.7)
        self.response_inc.GetYaxis().SetTitleOffset(1.7)

        tdr.setTDRStyle()
        self.response_nom.Draw('COLZ')
        CMS_lumi.CMS_lumi(c, 4, 0, aLittleExtra=0.08)
        ROOT.gPad.SetRightMargin(0.2)
        utils.saveCanva(c, os.path.join(self.outputDir, '1_responseMatrix_%s_Nom' % self.var))
        c.Clear()
        tdr.setTDRStyle()
        self.response_alt.Draw('COLZ')
        CMS_lumi.CMS_lumi(c, 4, 0, aLittleExtra=0.08)
        utils.saveCanva(c, os.path.join(self.outputDir, '1_responseMatrix_%s_Alt' % self.var))
        c.Clear()
        tdr.setTDRStyle()
        self.response_inc.Draw('COLZ')
        CMS_lumi.CMS_lumi(c, 4, 0, aLittleExtra=0.08)
        utils.saveCanva(c, os.path.join(self.outputDir, '1_responseMatrix_%s_Inc' % self.var))

        if self.responseAsPdf:
            resp_nom=copy.deepcopy(ROOT.TH2D(self.response_nom))
            resp_alt=copy.deepcopy(ROOT.TH2D(self.response_alt))
            resp_inc=copy.deepcopy(ROOT.TH2D(self.response_inc))

            resp_nom.Scale(1./resp_nom.Integral())
            resp_alt.Scale(1./resp_alt.Integral())
            resp_inc.Scale(1./resp_inc.Integral())
            resp_nom.GetXaxis().SetTitle('Reco %s' % self.fancyvar)
            resp_alt.GetXaxis().SetTitle('Reco %s' % self.fancyvar)
            resp_inc.GetXaxis().SetTitle('Reco %s' % self.fancyvar)
            resp_nom.GetYaxis().SetTitle('Gen %s' % self.fancyvar)
            resp_alt.GetYaxis().SetTitle('Gen %s' % self.fancyvar)
            resp_inc.GetYaxis().SetTitle('Gen %s' % self.fancyvar)

            # Compute stability
            diagonalSum_nom=0
            diagonalSum_alt=0
            diagonalSum_inc=0
            odbN_nom=0
            odbN_alt=0
            odbN_inc=0
            for ibin in range(0, resp_nom.GetNbinsX()+2):
                # Am I taking the overflow diagonal one as well? Must check
                # must use FindBin, but I need the maximum first
                diagonalSum_nom+= resp_nom.GetBinContent(ibin, ibin)
                diagonalSum_alt+= resp_alt.GetBinContent(ibin, ibin)
                diagonalSum_inc+= resp_inc.GetBinContent(ibin, ibin)
                
                for jbin in range(0, resp_nom.GetNbinsY()+2):
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


        c.IsA().Destructor(c)

    def compute_stability_and_purity(self):

        purity_nom=self.response_nom.ProjectionX('%s_purity'%self.response_nom.GetName(), 0, self.response_nom.GetNbinsY())
        purity_alt=self.response_alt.ProjectionX('%s_purity'%self.response_alt.GetName(), 0, self.response_alt.GetNbinsY())
        purity_inc=self.response_inc.ProjectionX('%s_purity'%self.response_inc.GetName(), 0, self.response_inc.GetNbinsY())
        stability_nom=self.response_nom.ProjectionY('%s_stability'%self.response_nom.GetName(), 0, self.response_nom.GetNbinsX())
        stability_alt=self.response_alt.ProjectionY('%s_stability'%self.response_alt.GetName(), 0, self.response_alt.GetNbinsX())
        stability_inc=self.response_inc.ProjectionY('%s_stability'%self.response_inc.GetName(), 0, self.response_inc.GetNbinsX())
        
        purity_nom.Reset("ICE")
        purity_alt.Reset("ICE")
        purity_inc.Reset("ICE")
        stability_nom.Reset("ICE")
        stability_alt.Reset("ICE")
        stability_inc.Reset("ICE")

        puritydenom_nom=copy.deepcopy(ROOT.TH1D(purity_nom))
        puritydenom_alt=copy.deepcopy(ROOT.TH1D(purity_alt))
        puritydenom_inc=copy.deepcopy(ROOT.TH1D(purity_inc))
        stabilitydenom_nom=copy.deepcopy(ROOT.TH1D(stability_nom))
        stabilitydenom_alt=copy.deepcopy(ROOT.TH1D(stability_alt))
        stabilitydenom_inc=copy.deepcopy(ROOT.TH1D(stability_inc))

        # Fill purity
        for xbin in range(0, self.response_nom.GetNbinsX()+2):
            recobinevts_nom=0
            recobinevts_alt=0
            recobinevts_inc=0
            for ybin in range(0, self.response_nom.GetNbinsY()+2):
                recobinevts_nom += self.response_nom.GetBinContent(xbin, ybin)
                recobinevts_alt += self.response_alt.GetBinContent(xbin, ybin)
                recobinevts_inc += self.response_inc.GetBinContent(xbin, ybin)


            purity_nom.SetBinContent(xbin, self.response_nom.GetBinContent(xbin,xbin))
            purity_alt.SetBinContent(xbin, self.response_alt.GetBinContent(xbin,xbin))
            purity_inc.SetBinContent(xbin, self.response_inc.GetBinContent(xbin,xbin))
            puritydenom_nom.SetBinContent(xbin, recobinevts_nom)
            puritydenom_alt.SetBinContent(xbin, recobinevts_alt)
            puritydenom_inc.SetBinContent(xbin, recobinevts_inc)

        # Fill stability
        for ybin in range(0, self.response_nom.GetNbinsY()+2):
            recobinevts_nom=0
            recobinevts_alt=0
            recobinevts_inc=0
            for xbin in range(0, self.response_nom.GetNbinsX()+2):
                recobinevts_nom += self.response_nom.GetBinContent(xbin, ybin)
                recobinevts_alt += self.response_alt.GetBinContent(xbin, ybin)
                recobinevts_inc += self.response_inc.GetBinContent(xbin, ybin)

                    
            stability_nom.SetBinContent(ybin, self.response_nom.GetBinContent(ybin,ybin))
            stability_alt.SetBinContent(ybin, self.response_alt.GetBinContent(ybin,ybin))
            stability_inc.SetBinContent(ybin, self.response_inc.GetBinContent(ybin,ybin))
            stabilitydenom_nom.SetBinContent(ybin, recobinevts_nom)
            stabilitydenom_alt.SetBinContent(ybin, recobinevts_alt)
            stabilitydenom_inc.SetBinContent(ybin, recobinevts_inc)


        purity_nom.Divide(puritydenom_nom)
        purity_alt.Divide(puritydenom_alt)
        purity_inc.Divide(puritydenom_inc)
        stability_nom.Divide(stabilitydenom_nom)
        stability_alt.Divide(stabilitydenom_alt)
        stability_inc.Divide(stabilitydenom_inc)

        # Paint them
        print(purity_nom)
        print(stability_nom)
        c = ROOT.TCanvas('matrix', 'Response Matrix', 3000, 1000)
        # Margin not being applied somehow. Must do it via gStyle?
        #ROOT.gStyle.SetPadTopMargin(0.1)
        #ROOT.gStyle.SetPadBottomMargin(0.1)
        #ROOT.gStyle.SetPadLeftMargin(0.1)
        #ROOT.gStyle.SetPadRightMargin(0.1)
        #ROOT.gStyle.SetOptStat('uo')
        c.Divide(3,1)
        c.cd(1)
        print(purity_nom)
        print(stability_nom)
        purity_nom.SetMarkerColor(ROOT.kRed)
        purity_nom.SetMarkerStyle(ROOT.kFullSquare)
        stability_nom.SetMarkerColor(ROOT.kBlue)
        stability_nom.SetMarkerStyle(ROOT.kFullCircle)
        purity_nom.Draw("PE")
        stability_nom.Draw("PESAME")
        leg_1 = ROOT.TLegend(0.4,0.5,0.9,0.9)
        leg_1.SetTextSize(0.04)
        leg_1.SetBorderSize(0)
        leg_1.AddEntry(purity_nom, 'Purity', 'p')
        leg_1.AddEntry(stability_nom, 'Stability', 'p')
        leg_1.Draw()
        c.cd(2)
        purity_alt.SetMarkerColor(ROOT.kRed)
        purity_alt.SetMarkerStyle(ROOT.kFullSquare)
        stability_alt.SetMarkerColor(ROOT.kBlue)
        stability_alt.SetMarkerStyle(ROOT.kFullCircle)
        purity_alt.Draw("PE")
        stability_alt.Draw("PESAME")
        leg_1.Draw()
        c.cd(3)
        purity_inc.SetMarkerColor(ROOT.kRed)
        purity_inc.SetMarkerStyle(ROOT.kFullSquare)
        stability_inc.SetMarkerColor(ROOT.kBlue)
        stability_inc.SetMarkerStyle(ROOT.kFullCircle)
        purity_inc.Draw("PE")
        stability_inc.Draw("PESAME")
        leg_1.Draw()
        CMS_lumi.CMS_lumi(c, 4, 0, aLittleExtra=0.08)
        utils.saveCanva(c, os.path.join(self.outputDir, '1_checkBinning_%s' % self.var))
        c.IsA().Destructor(c)

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
        CMS_lumi.CMS_lumi(c, 4, 0, aLittleExtra=0.08)
        utils.saveCanva(c, os.path.join(args.outputDir, '2_unfoldResults_%s_%s_%s_%s' % (label, key, self.var, h.GetName()) ))

    def do_unfolding(self, key):

        self.histmap=ROOT.TUnfold.kHistMapOutputVert
        # kHistMapOutputHoriz (truth is in X axis), kHistMapOutputVert (truth is in Y axis)
        self.regmode=ROOT.TUnfold.kRegModeNone
        # kRegModeNone (no reg), kRegModeSize (reg amplitude of output), kRegModeDerivative (reg 1st derivative of output), kRegModeCurvature (reg 2nd derivative of output),  kRegModeMixed (mixed reg patterns)
        if self.areaConstraint:
            self.constraint=ROOT.TUnfold.kEConstraintArea
        else:
            self.constraint=ROOT.TUnfold.kEConstraintNone
        # kEConstraintNone (no extra constraint), kEConstraintArea (enforce preservation of area)
        self.densitymode= ROOT.TUnfoldDensity.kDensityModeeNone
        # kDensityModeNone (no scale factors, matrix L is similar to unity matrix), kDensityModeBinWidth (scale factors from multidimensional bin width), kDensityModeUser (scale factors from user function in TUnfoldBinning), kDensityModeBinWidthAndUser (scale factors from multidimensional bin width and user function)


        # First do it with no regularization
        print('NOW I AM DOING UNFOLDING WITHOUT REGULARIZATION')
        label='noreg'
        self.set_unfolding(key)
        self.do_scan()
        self.print_unfolding_results(key, label)
     
        print('NOW I AM DOING UNFOLDING WITH REGULARIZATION')
        # Now add simple regularization on the amplitude
        self.logTauX=ROOT.TSpline3() # TSpline*
        self.logTauY=ROOT.TSpline3() # TSpline*
        self.lCurve=ROOT.TGraph(0) # TGraph*
        self.logTauCurvature=ROOT.TSpline3() # TSpline*
        self.regmode=ROOT.TUnfold.kRegModeCurvature
        label='regamp'
        self.set_unfolding(key)
        self.do_scan()
        self.print_unfolding_results(key, label)

     
    def set_unfolding(self, key):
        #destruir = lambda x : x.IsA().Destructor(x)
        #if self.unfold: destruir(self.unfold)
        if self.unfold:
            self.unfold.IsA().Destructor(self.unfold)

        print('DATA BINNING: %d' % self.data.GetNbinsX() )
        print('SIGNAL BINNING: %d' % self.mc.GetNbinsX() )
        print('BKG[0] BINNING: %d' % self.bkg[0].GetNbinsX() )
        print('Matrix binning: reco = %d, gen = %d' %( self.response_nom.GetNbinsX(), self.response_nom.GetNbinsY()) )
        if   key == 'nom':
            self.unfold = ROOT.TUnfoldDensity(self.response_nom, self.histmap, self.regmode, self.constraint, self.densitymode)
        elif key == 'alt':
            self.unfold = ROOT.TUnfoldDensity(self.response_alt, self.histmap, self.regmode, self.constraint, self.densitymode)
        elif key == 'inc':
            self.unfold = ROOT.TUnfoldDensity(self.response_inc, self.histmap, self.regmode, self.constraint, self.densitymode)
        else:
            print('ERROR: the response matrix you asked for (%s) does not exist' % key)
        # Check if the input data points are enough to constrain the unfolding process
        # Set scale bias
        if self.bias != 0.0:
            check = self.unfold.SetInput(self.data, self.bias)
        else:
            check = self.unfold.SetInput(self.data)
        if check>=10000:
            print('TUnfoldDensity error %d! Unfolding result may be wrong (not enough data to constrain the unfolding process)' % check)
        # Now I should do subtraction using the class. I assign a 10% error on each background. This will have to be set automatically
        scale_bgr=1.0
        dscale_bgr=0.05
        for iBkg in self.bkg:
            print('Background %s has bins %d' % (iBkg.GetName(), iBkg.GetNbinsX()) )
            if 'convs' in iBkg.GetName():
                dscale_bgr=0.20
            elif 'rares_ttX' in iBkg.GetName():
                dscale_bgr=0.15
            elif 'rares_VVV' in iBkg.GetName():
                dscale_bgr=0.5
            elif 'rares_tZq' in iBkg.GetName():
                dscale_bgr=0.35
            elif 'fakes_appldata' in iBkg.GetName():
                dscale_bgr=0.3
            elif 'prompt_ZZH' in iBkg.GetName():
                dscale_bgr=0.07
            self.unfold.SubtractBackground(iBkg,iBkg.GetName(),scale_bgr,dscale_bgr);

        # Add systematic uncertainties
        self.add_systematic_uncertainties()
        # unfold.AddSysError(histUnfoldMatrixSys,"signalshape_SYS", TUnfold::kHistMapOutputHoriz, TUnfoldSys::kSysErrModeMatrix)

        # Bias term! It corresponds to the distribution I expect to see after unfolding (e.g. the true Zpt distribution)
        if self.bias != 0:
            self.unfold.SetBias(self.dataTruth_nom)

        # Alternative matrix:
        if   key == 'nom':
            self.unfold.AddSysError(self.response_alt, 'aMC response', self.histmap, ROOT.TUnfoldDensity.kSysErrModeMatrix)
        elif key == 'alt':
            self.unfold.AddSysError(self.response_nom, 'pow response', self.histmap, ROOT.TUnfoldDensity.kSysErrModeMatrix)
        elif key == 'inc':
            self.unfold.AddSysError(self.response_nom, 'pow response', self.histmap, ROOT.TUnfoldDensity.kSysErrModeMatrix)
        else:
            print('ERROR: the response matrix you asked for (%s) does not exist' % key)
        

    def add_systematic_uncertainties(self):
        for [sysName, sysValue] in self.normSystsList:
            shifted_response=copy.deepcopy(self.response_nom)
            shifted_response.Scale(float(sysValue))
            print(sysName, sysValue, shifted_response.Integral()/self.response_nom.Integral())
            self.unfold.AddSysError(shifted_response, sysName, self.histmap, ROOT.TUnfoldDensity.kSysErrModeMatrix)
        for [sysName, sysValue] in self.shapeSystsList:
            self.unfold.AddSysError(sysValue, sysName, self.histmap, ROOT.TUnfoldDensity.kSysErrModeMatrix)
            print(sysName, sysValue.Integral()/self.response_nom.Integral())

    def do_scan(self):
        # Scan the L-curve and find the best point
        
        # Set verbosity
        oldinfo=ROOT.gErrorIgnoreLevel
        if self.verbose:
            ROOT.gErrorIgnoreLevel=kInfo

        # Scan the parameter tau, finding the kink in the L-curve. Finally, do the unfolding for the best choice of tau
        if self.regmode == ROOT.TUnfold.kRegModeNone:
            unfoldingReturn=self.unfold.DoUnfold(0.0)
            print('UNREGOLARIZED UNFOLDING RETURNS: %f' % unfoldingReturn)
            if unfoldingReturn >=1:
                print('================================================ ERROR ERROR ERROR, unregularized unfolding failed (max global correlation coefficient %f >=1) ==========================="' % unfoldingReturn)
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
        print('Best tau: %d' % self.unfold.GetTau())
        print('chi^2: %d+%d/%d' %(self.unfold.GetChi2A(), self.unfold.GetChi2L(), self.unfold.GetNdf() ) )
        print('chi^2(syst): %d' % self.unfold.GetChi2Sys())
        
        print('ibest: %d, type %s' % ( self.iBest, type(self.iBest)))
        # Visualize best choice of tau

        bestLcurve = None
        bestLogTauLogChi2 = None
        if self.regmode is not ROOT.TUnfold.kRegModeNone:
            t=ROOT.Double(0)
            x=ROOT.Double(0)
            y=ROOT.Double(0)
            self.logTauX.GetKnot(self.iBest, t, x)
            self.logTauY.GetKnot(self.iBest, t, y)
            vt =array('d')
            vx =array('d')
            vy =array('d')
            vt.append(t)
            vx.append(x)
            vy.append(y)
            bestLcurve = ROOT.TGraph(1, vx, vy)
            bestLogTauLogChi2 = ROOT.TGraph(1, vt, vx);
        
        # Retrieve results as histograms
        histMunfold=self.unfold.GetOutput('%s(unfold,stat+bgrerr)' %self.var) # Unfolded result
        histMdetFold=self.unfold.GetFoldedOutput('FoldedBack') # Unfolding result, folded back
        histEmatStat=self.unfold.GetEmatrixInput('Error matrix (stat errors only)') # Error matrix (stat errors only)
        histEmatTotal=self.unfold.GetEmatrixTotal('Error matrix (total errors)') # Total error matrix. Migration matrix uncorrelated and correlated syst errors added in quadrature to the data statistical errors
        
        
        #TH1 *histDetNormBgr1=unfold.GetBackground("bgr1 normalized",
        #                                          "background1");
        histDetNormBgrTotal=self.unfold.GetBackground("Total background (normalized)")

        print('Bins of unfolded distribution: %d' % histMunfold.GetNbinsX() )
        print('Bins of folded back distribution: %d' % histMdetFold.GetNbinsX() )
        print('Bins of first stacked histo: %d' % histDetNormBgrTotal.GetNbinsX() )
        print('Bins of second stacked histo: %d' % self.mc.GetNbinsX() )
        print('ndet %d' % self.response_nom.GetNbinsX())
        print('ngen %d' % self.response_nom.GetNbinsY())
              

        nDet=self.response_nom.GetNbinsX()
        nGen=self.response_nom.GetNbinsY()
        xminDet=self.response_nom.GetXaxis().GetBinLowEdge(1)
        xmaxDet=self.response_nom.GetXaxis().GetBinUpEdge(self.response_nom.GetNbinsX())
        xminGen=self.response_nom.GetYaxis().GetBinLowEdge(1)
        xmaxGen=self.response_nom.GetYaxis().GetBinUpEdge(self.response_nom.GetNbinsY())
        #histUnfoldTotal = ROOT.TH1D('%s(unfold,toterr)' % self.var,';%s(gen)' % self.var, nGen, xminGen, xmaxGen) # Unfolded data histogram with total errors
        histUnfoldTotal = copy.deepcopy(ROOT.TH1D(self.dataTruth_nom)) # Unfolded data histogram with total errors
        histUnfoldTotal.Reset('ICE')
        histUnfoldTotal.SetName('%s(unfold,toterr)' % self.var)
        histUnfoldStat = copy.deepcopy(ROOT.TH1D(self.dataTruth_nom)) # Unfolded data histogram with statistical errors only
        histUnfoldStat.Reset('ICE')
        histUnfoldStat.SetName('%s(unfold,staterr)' % self.var)
        for ibin in range(0,nGen+2):
            c=histMunfold.GetBinContent(ibin)
            histUnfoldStat.SetBinContent(ibin, c)
            histUnfoldStat.SetBinError(ibin, ROOT.TMath.Sqrt(histEmatStat.GetBinContent(ibin,ibin)))
            histUnfoldTotal.SetBinContent(ibin, histMunfold.GetBinContent(ibin))
            histUnfoldTotal.SetBinError(ibin, ROOT.TMath.Sqrt(histEmatTotal.GetBinContent(ibin,ibin)))

        histCorr=ROOT.TH2D("Corr(total)",";%s bin (gen);%s bin(gen)" % (self.var, self.var), nGen,0,nGen,nGen,0,nGen)
        for ibin in range(0, nGen+2):
            ei=0
            ej=0
            ei=ROOT.TMath.Sqrt(histEmatTotal.GetBinContent(ibin,ibin))
            if ei<=0.0:
                continue
            for jbin in range(0, nGen+2):
                ej=ROOT.TMath.Sqrt(histEmatTotal.GetBinContent(jbin,jbin))
                if ej<=0.0:
                    continue
                histCorr.SetBinContent(ibin,jbin,histEmatTotal.GetBinContent(ibin,jbin)/ei/ej)

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
        #output.Divide(4,2)
        output.cd()
        # Show the matrix which connects input and output
        # There are overflow bins at the bottom, not shown in the plot
        # These contain the background shape.
        # The overflow bins to the left and right contain
        # events which are not reconstructed. These are necessary for proper MC
        # normalisation
        #output.cd(1)
        ##histMdetGenMC.Draw("BOX")
        
        #output.cd(1)
        # Data, MC prediction, background
        self.data.SetMinimum(0.0)
        self.data.SetTitle('Inputs (folded space)')
        self.data.GetXaxis().SetTitle('Reco %s' % self.fancyvar)
        self.data.GetYaxis().SetTitle('Events')
        self.data.GetYaxis().SetTitleOffset(1.6)
        self.data.DrawCopy("E")
        self.mc.SetMinimum(0.0)
        self.mc.SetLineColor(ROOT.kBlue)
        self.mc.SetLineWidth(3)
        bkgStacked=copy.deepcopy(histDetNormBgrTotal)
        bkgStacked.Add(self.mc)
        bkgStacked.SetLineColor(ROOT.kRed)
        bkgStacked.SetLineWidth(3)
        #histDetNormBgr1.SetLineColor(kCyan);
        self.mc.Draw("SAME HIST")
        #histDetNormBgr1.Draw("SAME HIST");
        bkgStacked.Draw("SAME HIST")

        leg_1 = ROOT.TLegend(0.4,0.7,0.9,0.9)
        leg_1.SetTextSize(0.04)
        leg_1.SetBorderSize(0)
        leg_1.AddEntry(self.data, 'Data', 'p')
        leg_1.AddEntry(self.mc, 'Exp. signal', 'lf')
        leg_1.AddEntry(bkgStacked, 'Exp. signal+background', 'l')
        leg_1.Draw()

        print(self.data.GetNbinsX())
        print(self.mc.GetNbinsX())
        print(histDetNormBgrTotal.GetNbinsX())
        CMS_lumi.CMS_lumi(output, 4, 0, aLittleExtra=0.08)
        output.SaveAs(os.path.join(self.outputDir, '2_p1_unfold_%s_%s_%s.pdf' % (label, key, self.var)))
        #output.SaveAs(os.path.join(self.outputDir, '2_p1_unfold_%s_%s_%s.png' % (label, key, self.var)))
        output.SaveAs(os.path.join(self.outputDir, '2_p1_unfold_%s_%s_%s.C' % (label, key, self.var)))
        output.Clear()
        # draw generator-level distribution:
        #   data (red) [for real data this is not available]
        #   MC input (black) [with completely wrong peak position and shape]
        #   unfolded data (blue)
        #output.cd(2)
        # Data truth
        self.dataTruth_nom.SetLineColor(ROOT.kRed+1)
        self.dataTruth_nom.SetLineWidth(2)
        self.dataTruth_nom.SetMaximum(1.2*self.dataTruth_nom.GetMaximum())
        self.dataTruth_nom.SetTitle("")
        self.dataTruth_nom.GetXaxis().SetTitle('Reco %s' % self.fancyvar)
        self.dataTruth_nom.GetYaxis().SetTitle('Events')
        self.dataTruth_nom.GetYaxis().SetTitleSize(0.035)
        self.dataTruth_nom.GetYaxis().SetLabelSize(0.035)
        self.dataTruth_nom.DrawNormalized("E HIST")
        # Unfolded data with total error
        histUnfoldTotal.SetMarkerColor(ROOT.kBlue)
        histUnfoldTotal.SetLineColor(ROOT.kBlue)
        histUnfoldTotal.SetLineWidth(1)
        histUnfoldTotal.SetMarkerStyle(ROOT.kFullCircle)
        # Outer error: total error
        histUnfoldTotal.SetTitle('Unfolded space')
        histUnfoldTotal.DrawNormalized('PESAME')
        # Middle error: stat+bgr
        histMunfold.SetLineColor(ROOT.kBlue+2)
        histMunfold.SetLineWidth(2)
        histMunfold.DrawNormalized('SAME E1')
        # Inner error: stat only
        histUnfoldStat.SetLineColor(ROOT.kBlue+4)
        histUnfoldStat.SetLineWidth(3)
        histUnfoldStat.DrawNormalized('SAME E1')
        ###histDensityGenData.SetLineColor(kRed)
        ##histDensityGenData.Draw("SAME")
        ##histDensityGenMC.Draw("SAME HIST")
        leg_2 = ROOT.TLegend(0.4,0.7,0.9,0.9)
        leg_2.SetTextSize(0.04)
        leg_2.SetBorderSize(0)
        leg_2.AddEntry(histUnfoldTotal, 'Unfolded data', 'pel')
        leg_2.AddEntry(self.dataTruth_nom, 'POWHEG prediction', 'la')
        leg_2.AddEntry(histUnfoldStat, '#frac{#chi^{2}}{NDOF}=%0.3f' % histUnfoldTotal.Chi2Test(self.dataTruth_nom, 'CHI2/NDF WW'), '')
        leg_2.Draw()
        CMS_lumi.CMS_lumi(output, 4, 0, aLittleExtra=0.08)
        output.SaveAs(os.path.join(self.outputDir, '2_p2_unfold_%s_%s_%s.pdf' % (label, key, self.var)))
        #output.SaveAs(os.path.join(self.outputDir, '2_p2_unfold_%s_%s_%s.png' % (label, key, self.var)))
        output.SaveAs(os.path.join(self.outputDir, '2_p2_unfold_%s_%s_%s.C' % (label, key, self.var)))
        output.Clear()
        # show detector level distributions
        #    data (red)
        #    MC (black) [with completely wrong peak position and shape]
        #    unfolded data (blue)
        #output.cd(3)
        # Data
        subdata=self.sub_bkg_by_hand()
        subdata.SetLineColor(ROOT.kBlack-3)
        subdata.SetLineWidth(3)
        subdata.SetTitle('Folded space')
        #self.data.SetTitle('Folded space')
        #self.data.Draw('PE')
        subdata.GetXaxis().SetTitle('Reco %s' % self.fancyvar)
        subdata.GetYaxis().SetTitle('Events')
        subdata.Draw('PE')
        # MC folded back
        histMdetFold.SetLineColor(ROOT.kRed+1)
        histMdetFold.SetLineWidth(3)
        histMdetFold.Draw('SAME')
        # Original folded MC
        self.mc.Draw("SAME HIST")
        #bkgStacked.Draw("SAME HIST")
        #histInput=self.unfold.GetInput("Minput",";mass(det)")
        #histInput.SetLineColor(ROOT.kRed)
        #histInput.SetLineWidth(3)
        #histInput.Draw("SAME")
        leg_3 = ROOT.TLegend(0.4,0.7,0.9,0.9)
        leg_3.SetTextSize(0.04)
        leg_3.SetBorderSize(0)
        #leg_3.AddEntry(self.data, 'Data', 'pe')
        leg_3.AddEntry(subdata, 'Data-bkg', 'pe')
        leg_3.AddEntry(histMdetFold, 'MC folded back', 'l')
        #leg_3.AddEntry(bkgStacked, 'Exp. signal+background', 'l')
        leg_3.AddEntry(self.mc, 'Exp. signal', 'l')
        leg_3.AddEntry(histUnfoldStat, '#frac{#chi^{2}}{NDOF}(D-b, MCf.b.)=%0.3f' % subdata.Chi2Test(histMdetFold, 'CHI2/NDF WW'), '')
        #leg_3.AddEntry(histInput, 'Input', 'la')
        leg_3.Draw()
        CMS_lumi.CMS_lumi(output, 4, 0, aLittleExtra=0.08)
        output.SaveAs(os.path.join(self.outputDir, '2_p3_unfold_%s_%s_%s.pdf' % (label, key, self.var)))
        #output.SaveAs(os.path.join(self.outputDir, '2_p3_unfold_%s_%s_%s.png' % (label, key, self.var)))
        output.SaveAs(os.path.join(self.outputDir, '2_p3_unfold_%s_%s_%s.C' % (label, key, self.var)))
        output.Clear()
        #output.cd(4) 
        # show correlation coefficients
        # #histRhoi.Draw()
        # Data-bkg by hand
        subdata.Draw('pe')
        self.mc.Draw('SAME HIST')
        histInput=self.unfold.GetInput("Minput",";mass(det)")
        histInput.SetLineColor(ROOT.kRed)
        histInput.SetLineWidth(3)
        #histInput.Draw("SAME")
        leg_4 = ROOT.TLegend(0.4,0.7,0.9,0.9)
        leg_4.SetTextSize(0.04)
        leg_4.SetBorderSize(0)
        leg_4.AddEntry(self.mc, 'Exp. signal', 'lf')
        leg_4.AddEntry(subdata, 'Data-bkg by hand', 'pe')
        #leg_4.AddEntry(histInput, 'Data-bkg by tool', 'la')
        leg_4.Draw()
        CMS_lumi.CMS_lumi(output, 4, 0, aLittleExtra=0.08)
        output.SaveAs(os.path.join(self.outputDir, '2_p4_unfold_%s_%s_%s.pdf' % (label, key, self.var)))
        #output.SaveAs(os.path.join(self.outputDir, '2_p4_unfold_%s_%s_%s.png' % (label, key, self.var)))
        output.SaveAs(os.path.join(self.outputDir, '2_p4_unfold_%s_%s_%s.C' % (label, key, self.var)))
        output.Clear()
        if self.regmode is not ROOT.TUnfold.kRegModeNone:

            # from v610# # Show logTauCurvature (should be peaked similarly to a Gaussian)
            # from v610# output.cd(4)
            # from v610# self.logTauCurvature.SetLineWidth(3)
            # from v610# self.logTauCurvature.Draw()
            # show tau as a function of chi**2
            #output.cd(5)
            tdr.setTDRStyle()
            self.logTauX.Draw('L')
            bestLogTauLogChi2.SetMarkerColor(ROOT.kRed)
            bestLogTauLogChi2.SetMarkerStyle(ROOT.kFullSquare)
            bestLogTauLogChi2.SetMarkerSize(2)
            bestLogTauLogChi2.Draw('P')
            # show the L curve
            CMS_lumi.CMS_lumi(output, 4, 0, aLittleExtra=0.08)
            output.SaveAs(os.path.join(self.outputDir, '2_p5_unfold_%s_%s_%s.pdf' % (label, key, self.var)))
            #output.SaveAs(os.path.join(self.outputDir, '2_p5_unfold_%s_%s_%s.png' % (label, key, self.var)))
            output.SaveAs(os.path.join(self.outputDir, '2_p5_unfold_%s_%s_%s.C' % (label, key, self.var)))
            output.Clear()
            #output.cd(6)
            tdr.setTDRStyle()
            self.lCurve.GetXaxis().SetTitle('log#chi_{A}^{2}')
            self.lCurve.GetYaxis().SetTitle('log#chi_{L}^{2}')
            self.lCurve.Draw("AL")
            bestLcurve.SetMarkerColor(ROOT.kRed)
            bestLcurve.SetMarkerStyle(ROOT.kFullSquare)
            bestLcurve.SetMarkerSize(2)
            bestLcurve.Draw("P")
            CMS_lumi.CMS_lumi(output, 4, 0, aLittleExtra=0.08)
            output.SaveAs(os.path.join(self.outputDir, '2_p6_unfold_%s_%s_%s.pdf' % (label, key, self.var)))
            #output.SaveAs(os.path.join(self.outputDir, '2_p6_unfold_%s_%s_%s.png' % (label, key, self.var)))
            output.SaveAs(os.path.join(self.outputDir, '2_p6_unfold_%s_%s_%s.C' % (label, key, self.var)))
            output.Clear()
       
        #output.cd(7)
        #ROOT.gStyle.SetPadRightMargin(0.10)
        output.Clear()
        #outputti=ROOT.TCanvas('outt', 'outt', 2000, 2000)
        #outputti.cd()
        #ROOT.gStyle.SetPadBorderMode(0)
        #ROOT.gPad.SetRightMargin(0.1)
        if 'nom' in key:
            self.response_nom.Scale(1./self.response_nom.Integral())
            self.response_nom.SetTitle('Response Matrix (powheg)')
            self.response_nom.Draw("colz")
        elif 'alt' in key:
            self.response_alt.Scale(1./self.response_alt.Integral())
            self.response_alt.SetTitle('Response Matrix (amcatnlo)')
            self.response_alt.Draw('colz')
        elif 'inc' in key:
            self.response_inc.Scale(1./self.response_inc.Integral())
            self.response_inc.SetTitle('Response Matrix (pythia)')
            self.response_inc.Draw('colz')
        CMS_lumi.CMS_lumi(output, 4, 0, aLittleExtra=0.08)
        ROOT.gPad.Update()
        output.SaveAs(os.path.join(self.outputDir, '2_p7_unfold_%s_%s_%s.pdf' % (label, key, self.var)))
        #output.SaveAs(os.path.join(self.outputDir, '2_p7_unfold_%s_%s_%s.png' % (label, key, self.var)))
        #outputti.SaveAs(os.path.join(self.outputDir, '2_p7_unfold_%s_%s_%s.C' % (label, key, self.var)))
        output.Clear()
        #output.cd(8)
        histCorr.SetTitle('Correlation matrix')
        histCorr.Draw('COLZ')
        CMS_lumi.CMS_lumi(output, 4, 0, aLittleExtra=0.08)
        output.SaveAs(os.path.join(self.outputDir, '2_p8_unfold_%s_%s_%s.pdf' % (label, key, self.var)))
        #output.SaveAs(os.path.join(self.outputDir, '2_p8_unfold_%s_%s_%s.png' % (label, key, self.var)))
        output.SaveAs(os.path.join(self.outputDir, '2_p8_unfold_%s_%s_%s.C' % (label, key, self.var)))
        #output.SaveAs(os.path.join(self.outputDir, '2_unfold_%s_%s_%s.png' % (label, key, self.var)))
 
        # =====================================================================
        #  money plot
        ROOT.TH1.SetDefaultSumw2()
        
        moneyplot=ROOT.TCanvas('out', 'out', 2000, 2000)
        moneyplot.cd()
        # Normalize properly for differential xsec
        # Data truth
        dt=copy.deepcopy(self.dataTruth_nom)
        dt_alt=copy.deepcopy(self.dataTruth_alt)
        dt_inc=copy.deepcopy(self.dataTruth_inc)
        # # Rewrite the nom_up and dn
        # self.dataTruth_nom_up=copy.deepcopy(dt)
        # self.dataTruth_nom_dn=copy.deepcopy(dt)
        # self.dataTruth_nom_up.Scale(1.06)
        # self.dataTruth_nom_dn.Scale(0.94)
        dt_nom_up=copy.deepcopy(self.dataTruth_nom_up)
        dt_nom_dn=copy.deepcopy(self.dataTruth_nom_dn)
        print('YADDA ', dt.Integral(), dt_nom_dn.Integral(), dt_nom_up.Integral()) 
        factorUp=dt_nom_up.Integral()/dt.Integral()
        factorDn=dt_nom_dn.Integral()/dt.Integral()
        for ibin in range(0, dt.GetNbinsX()+2):
            dt.SetBinContent(ibin,dt.GetBinContent(ibin)/dt.GetBinWidth(ibin))
            dt.SetBinError(ibin,dt.GetBinError(ibin)/dt.GetBinWidth(ibin))
            dt_nom_up.SetBinContent(ibin,dt_nom_up.GetBinContent(ibin)/dt.GetBinWidth(ibin))
            dt_nom_up.SetBinError(ibin,dt_nom_up.GetBinError(ibin)/dt.GetBinWidth(ibin))
            dt_nom_dn.SetBinContent(ibin,dt_nom_dn.GetBinContent(ibin)/dt.GetBinWidth(ibin))
            dt_nom_dn.SetBinError(ibin,dt_nom_dn.GetBinError(ibin)/dt.GetBinWidth(ibin))
            #self.dataTruth_nom_up.SetBinContent(ibin,dt.GetBinContent(ibin)/dt.GetBinWidth(ibin))
            #self.dataTruth_nom_dn.SetBinContent(ibin,dt.GetBinContent(ibin)/dt.GetBinWidth(ibin))
            dt_alt.SetBinContent(ibin,dt_alt.GetBinContent(ibin)/dt_alt.GetBinWidth(ibin))
            dt_alt.SetBinError(  ibin,dt_alt.GetBinError(ibin)  /dt_alt.GetBinWidth(ibin))
            dt_inc.SetBinContent(ibin,dt_inc.GetBinContent(ibin)/dt_inc.GetBinWidth(ibin))
            dt_inc.SetBinError(  ibin,dt_inc.GetBinError(ibin)  /dt_inc.GetBinWidth(ibin))



        dt.Scale(1./dt.Integral())
        dt_nom_up.Scale(factorUp/dt_nom_up.Integral())
        dt_nom_dn.Scale(factorDn/dt_nom_dn.Integral())

        print('YADDA2 ', dt.Integral(), dt_nom_dn.Integral(), dt_nom_up.Integral()) 
        dt_alt.Scale(1./dt_alt.Integral())
        dt_inc.Scale(1./dt_inc.Integral())
        dt.GetXaxis().SetTitle('%s' % self.fancyvar)
        dt.GetYaxis().SetTitle('(d#sigma/d%s)/#sigma' % self.diffvar)
        dt.SetMaximum(1.2*dt.GetMaximum())
        if self.logx:
            ROOT.gPad.SetLogx()
        if 'MWZ' in self.var:
            ROOT.gPad.SetLogy()
            dt.SetMaximum(100*dt.GetMaximum())
        dt.GetXaxis().SetTitleSize(0.045)
        dt.GetYaxis().SetTitleSize(0.045)
        dt.GetXaxis().SetTitleOffset(1.35)
        dt.GetYaxis().SetTitleOffset(1.6)
        dt.Draw('E HIST')
        # Unfolded data with total error
        hut=copy.deepcopy(histUnfoldTotal)
        for ibin in range(1, hut.GetNbinsX()+1):
            print('bin %d has content %f and width %f for a final content of %f. Bin error is %f' %(ibin, hut.GetBinContent(ibin), hut.GetBinWidth(ibin), hut.GetBinContent(ibin)/hut.GetBinWidth(ibin), hut.GetBinError(ibin)))
            hut.SetBinContent(ibin,hut.GetBinContent(ibin)/hut.GetBinWidth(ibin))
            hut.SetBinError(ibin,hut.GetBinError(ibin)/hut.GetBinWidth(ibin))
            print('after: bin content %f, bin error %f' % (hut.GetBinContent(ibin), hut.GetBinError(ibin)))
        print('hut integral before: %f' % hut.Integral())
        hut.Scale(1/hut.Integral())
        print('hut integral after: %f' % hut.Integral())
        theunf=copy.deepcopy(hut)
        # Outer error: total error
        hut.SetFillStyle(2001)
        hut.SetFillColor(29)
        hut.SetLineWidth(0)
        hut.Draw('E2 SAME')
        # Middle error: stat+bgr
        hmu=copy.deepcopy(histMunfold)
        for ibin in range(1, hmu.GetNbinsX()+1):
            hmu.SetBinContent(ibin,hmu.GetBinContent(ibin)/hmu.GetBinWidth(ibin))
            hmu.SetBinError(ibin,hmu.GetBinError(ibin)/hmu.GetBinWidth(ibin))
        hmu.Scale(1/hmu.Integral())
        hmu.SetFillStyle(2001)
        hmu.SetFillColor(ROOT.kAzure-9)
        hmu.SetLineWidth(0)
        hmu.Draw('SAME E2')
        # Inner error: stat only
        hus=copy.deepcopy(histUnfoldStat)
        for ibin in range(1, hus.GetNbinsX()+1):
            hus.SetBinContent(ibin,hus.GetBinContent(ibin)/hus.GetBinWidth(ibin))
            hus.SetBinError(ibin,hus.GetBinError(ibin)/hus.GetBinWidth(ibin))
        hus.Scale(1/hus.Integral())
        #hus.SetFillStyle(2001)
        #hus.SetFillColor(ROOT.kAzure-4)
        hus.SetLineColor(ROOT.kBlack)
        hus.SetMarkerColor(ROOT.kBlack)
        hus.SetLineWidth(2)
        hus.SetMarkerSize(3)
        #hus.SetLineWidth(0)
        # Rewrite points in order to not have them partially covered
        dt.Draw('SAME E HIST')
        dt_alt.SetLineWidth(2)
        dt_alt.SetLineColor(ROOT.kBlue)
        dt_alt.Draw('SAME E HIST')
        dt_inc.SetLineWidth(2)
        dt_inc.SetLineColor(ROOT.kMagenta)
        ###dt_inc.Draw('SAME E HIST')
        # Add theoretical uncertainties on the nominal prediction
        # HERE HERE HERE
        dterr=ROOT.TGraphAsymmErrors(dt)
        for ipoint in range(0, dterr.GetN()+1):
            print(dt.GetBinCenter(ipoint), dt.GetBinLowEdge(ipoint), dt.GetBinLowEdge(ipoint+1))
            dterr.SetPoint(ipoint, dt.GetBinCenter(ipoint), dt.GetBinContent(ipoint)) 
            dterr.SetPointEYhigh(ipoint, dt_nom_up.GetBinContent(ipoint)-dt.GetBinContent(ipoint))
            dterr.SetPointEYlow (ipoint, dt.GetBinContent(ipoint)-dt_nom_dn.GetBinContent(ipoint))
            dterr.SetPointEXhigh(ipoint, dt.GetBinLowEdge(ipoint+1)-dt.GetBinCenter(ipoint))
            dterr.SetPointEXlow(ipoint,  dt.GetBinCenter(ipoint)-dt.GetBinLowEdge(ipoint))
            #dterr.SetPointEYhigh(ipoint, 1.06*dt.GetBinContent(ipoint))
            #dterr.SetPointEYlow (ipoint, 0.94*dt.GetBinContent(ipoint))
            #print(dt.GetBinContent(ipoint), 0.94*dt.GetBinContent(ipoint), 1.06*dt.GetBinContent(ipoint))
            print(dt.GetBinContent(ipoint), dt_nom_up.GetBinContent(ipoint), dt_nom_dn.GetBinContent(ipoint))

        for ipoint in range(0, dterr.GetN()):
            print(ipoint, dt.GetBinContent(ipoint), dterr.GetY()[ipoint], dterr.GetErrorYlow(ipoint), dterr.GetErrorYhigh(ipoint))

        dterr.SetLineColor(dt.GetLineColor())
        dterr.SetFillColor(dt.GetLineColor())
        dterr.SetFillStyle(3001)
        hus.Draw('SAME PE')
        dterr.Draw('2 SAME')
        #theunf.Draw('SAME PE')
        ###histDensityGenData.SetLineColor(kRed)
        ##histDensityGenData.Draw("SAME")
        ##histDensityGenMC.Draw("SAME HIST")
        leg_money = ROOT.TLegend(0.4,0.6,0.9,0.9)
        leg_money.SetTextSize(0.025)
        leg_money.SetBorderSize(0)
        leg_money.SetEntrySeparation(0.25)
        leg_money.AddEntry(hus, 'Unfolded data (stat.unc.)', 'pel')
        leg_money.AddEntry(dt, 'POWHEG prediction: #chi^{2}/NDOF=%0.3f'% dt.Chi2Test(hus, 'CHI2/NDF WW'), 'la')
        leg_money.AddEntry(dt_alt, 'aMC@NLO prediction: #chi^{2}/NDOF=%0.3f'% dt_alt.Chi2Test(hus, 'CHI2/NDF WW'), 'la')
        ###leg_money.AddEntry(dt_inc, 'PYTHIA #chi^{2}/NDOF=%0.3f'% dt_inc.Chi2Test(hus, 'CHI2/NDF WW'), 'la')
        #leg_money.AddEntry(hus, 'Stat. unc.', 'f')
        leg_money.AddEntry(hmu, 'Stat.+bgr. unc.', 'f')
        leg_money.AddEntry(hut, 'Total unc.', 'f')
        leg_money.AddEntry(dterr, 'Theory unc. on POWHEG prediction', 'f')
        #leg_money.AddEntry(histUnfoldTotal, '#frac{#chi^{2}}{NDOF}=%0.3f' % histUnfoldTotal.Chi2Test(self.dataTruth_nom, 'CHI2/NDF WW'), '')
        leg_money.Draw()
        tdr.setTDRStyle()
        CMS_lumi.CMS_lumi(moneyplot, 4, 0, aLittleExtra=0.08)
        moneyplot.SaveAs(os.path.join(self.outputDir, '3_differentialXsec_%s_%s_%s.pdf' % (label, key, self.var)))
        #moneyplot.SaveAs(os.path.join(self.outputDir, '3_differentialXsec_%s_%s_%s.png' % (label, key, self.var)))
        moneyplot.SaveAs(os.path.join(self.outputDir, '3_differentialXsec_%s_%s_%s.C' % (label, key, self.var)))
        # Dump to txt
        with open(os.path.join(self.outputDir, '3_differentialXsec_%s_%s_%s.txt' % (label, key, self.var)), 'w') as text_dumper:
            for ibin in range(0, hut.GetNbinsX()+1):
                statdown=hus.GetBinErrorLow(ibin)
                statup=hus.GetBinErrorUp(ibin)
                bgrdown=ROOT.TMath.Sqrt(hmu.GetBinErrorLow(ibin)*hmu.GetBinErrorLow(ibin) - statdown*statdown)
                bgrup=ROOT.TMath.Sqrt(hmu.GetBinErrorUp(ibin)*hmu.GetBinErrorUp(ibin)     - statup*statup    )
                systdown=ROOT.TMath.Sqrt(hut.GetBinErrorLow(ibin)*hut.GetBinErrorLow(ibin) - bgrdown*bgrdown - statdown*statdown)
                systup=ROOT.TMath.Sqrt(hut.GetBinErrorUp(ibin)*hut.GetBinErrorUp(ibin) - bgrup*bgrup - statup*statup    )
                text_dumper.write('$[%0.3f, %0.3f]$ & %0.3f $\\pm$ %0.3f (stat) $\\pm$ %0.3f (bgr) $\\pm$ %0.3f (other syst) (total: $\\pm$ %0.3f)\\\\ \n ' % (hut.GetBinLowEdge(ibin), hut.GetBinLowEdge(ibin+1 if ibin is not hut.GetNbinsX()+1 else ibin), hut.GetBinContent(ibin), statdown, bgrdown, systdown, hut.GetBinErrorUp(ibin)))

        # # Individual saving.
        # self.print_histo(histMunfold, key, label)
        # self.print_histo(histMdetFold, key, label)
        # self.print_histo(histEmatStat, key, label, 'colz')
        # self.print_histo(histEmatTotal, key, label, 'colz')
        # self.print_histo(histUnfoldTotal, key, label)

    def sub_bkg_by_hand(self):
        subdata=copy.deepcopy(ROOT.TH1D(self.data))
        for i in range(1,len(self.bkg)):
            subdata.Add(self.bkg[i], -1)
        return subdata



### End class Unfolder
def main(args): 
    tdr.setTDRStyle()
    print('start')
    print('Creating output dir %s/...' % args.outputDir)
    os.system('mkdir -p %s ' % args.outputDir)
    print('Cleaning output dir %s/...' % args.outputDir)
    os.system('rm %s/*png' % args.outputDir)
    os.system('rm %s/*pdf' % args.outputDir)
    print('...done!')

    # Should move it to be specifiable from command line, probably
    vardict = {
        'Zpt'       : ['p_{T}^{Z} [GeV]'          , 'p_{T}^{Z}'          ],
        'LeadJetPt' : ['Leading jet p_{T} [GeV]', 'p_{T}^{jet}'        ],
        'MWZ'       : ['M(WZ) [GeV]'             , 'M_{WZ}'             ],
        'Wpt'       : ['p_{T}^{W} [GeV]'          , 'p_{T}^{W}'          ] 
        }
    
    for var, fancy in vardict.items():
        fancyvar=fancy[0]
        diffvar=fancy[1]
        u = Unfolder(args,var,fancyvar, diffvar)
        u.print_responses()
        u.study_responses()
        u.do_unfolding('nom')
        u.do_unfolding('alt')
        u.do_unfolding('inc')

### End main

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputDir',       help='Input directory', default=None)
    parser.add_argument('-o', '--outputDir',      help='Output directory', default='./')
    parser.add_argument('-c', '--combineInput',   help='Data and postfit from combine output', default=None)
    parser.add_argument('--closure',              help='Use MC as data, for closure test', action='store_true')
    parser.add_argument('-d', '--data',           help='File containing data histogram', default=None)
    parser.add_argument('-m', '--mc',             help='File containing mc reco histogram', default=None)
    parser.add_argument('-g', '--gen',            help='File containing gen info for matrix', default=None)
    parser.add_argument('-l', '--lepCat',         help='Lepton multiplicity (1 or 2)', default=1, type=int)
    parser.add_argument('-e', '--epochs',         help='Number of epochs', default=100, type=int)
    parser.add_argument('-s', '--splitMode',      help='Split mode (input or random)', default='input')
    parser.add_argument('-v', '--verbose',        help='Verbose printing of the L-curve scan', action='store_true')
    parser.add_argument('-r', '--responseAsPdf',  help='Print response matrix as pdf', action='store_true') 
    parser.add_argument('-f', '--finalState',     help='Final state', default=None)
    parser.add_argument('--charge',               help='Charge of the W', default='')
    parser.add_argument('-b', '--bias',           help='Scale bias (0 deactivates bias vector)', default=None, type=float)
    parser.add_argument('-a', '--areaConstraint', help='Area constraint', action='store_true')
    args = parser.parse_args()
    # execute only if run as a script
    ROOT.gROOT.SetBatch()
    main(args)
