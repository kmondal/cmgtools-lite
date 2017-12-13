import os
import argparse

class AcceptanceComputer:

    def __init__(self, inputFiles):
        print('Initialization')
        print('Input files are: %s' % inputFiles)

### End class AcceptanceCounter

class Unfolder:
    tunfolder=None
    matrix=None
    
    def __init__(self, args):
        print('Initialization')

    def buildMatrix(self):
        print('Here we build the matrix')

    def init(self):
        print('Initialize the tunfolder')

### End class Unfolder

def main(args):
    u = Unfolder(args)
    u.buildMatrix()
    u.init()
### End main


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--lepCat',     help='Lepton multiplicity (1 or 2)', default=1, type=int)
    parser.add_argument('-m', '--multiclass', help='Multiclass (ttbar-LF and ttbar-HF are in different classes)', action='store_true')
    parser.add_argument('-e', '--epochs',     help='Number of epochs', default=100, type=int)
    parser.add_argument('-s', '--splitMode',  help='Split mode (input or random)', default='input')
#parser.add_argument('-n', '--nevts',      help='Number of events to be loaded from tree', default=-1, type=int)
    args = parser.parse_args()
    lepCat=args.lepCat
    # execute only if run as a script
    main(args)
