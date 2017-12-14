import os
import argparse

import utils

class AcceptanceComputer:

    def __init__(self, inputFiles):
        print('Initialization')
        print('Input files are: %s' % inputFiles)

### End class AcceptanceCounter

class Unfolder:
    tunfolder=None
    data=None
    mc=None
    matrix=None

    def __init__(self, args):
        print('Initialization')
        data, mc, mcResp = load_data(args.inputDir, args.data, args.mc, args.gen, treeName=['tree'])


    def load_data(folder, dataFName, mcFName, genFName, treeName=['tree']):
        # To be extended with the damn friend trees
        # Alternatively, take some minitrees as input (with only the few variables we are interested in. This is a better option, actually.
        data=None
        mc=None
        dataFile = get_file_from_glob(os.path.join(folder, dataFName) if folder else dataFName)
        mcFile   = get_file_from_glob(os.path.join(folder, mcFName)   if folder else mcFName)
        genFile  = get_file_from_glob(os.path.join(folder, genFName)  if folder else genFName)
        #data_handle = TFile.Open(dataFile)
        #mc_handle   = TFile.Open(mcFile)
        # Pass histograms, not trees?
        data = TChain("data")
        data.Add(dataFile+'/'+treeName)
        mc = TChain("mc")
        mc.Add(mcFile+'/'+treeName)
        
        # Add reading gen file to build response matrix

        # Pass through numpy arrays?

        return data, mc
        
    def buildMatrix(self):
        print('Here we build the matrix')

    def init(self):
        print('Initialize the tunfolder')

### End class Unfolder
def main(args): 
    u = Unfolder(args, data, mc)
    u.buildMatrix()
    u.init()
### End main
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputDir',   help='Input directory', default=None)
    parser.add_argument('-d', '--data',       help='File containing data histogram', default=None)
    parser.add_argument('-m', '--mc',         help='File containing mc reco histogram', default=None)
    parser.add_argument('-g', '--gen',   help='File containing gen info for matrix', default=None)
    parser.add_argument('-l', '--lepCat',     help='Lepton multiplicity (1 or 2)', default=1, type=int)
    parser.add_argument('-m', '--multiclass', help='Multiclass (ttbar-LF and ttbar-HF are in different classes)', action='store_true')
    parser.add_argument('-e', '--epochs',     help='Number of epochs', default=100, type=int)
    parser.add_argument('-s', '--splitMode',  help='Split mode (input or random)', default='input')
    

#parser.add_argument('-n', '--nevts',      help='Number of events to be loaded from tree', default=-1, type=int)
    args = parser.parse_args()
    # execute only if run as a script
    main(args)
