import os
import copy
#from ROOT import heppy

import ROOT
from ROOT import gSystem, TLorentzVector
# You would need to run 
'''
 cmsenv
 g++ -c -o RochCorStandalone_cpp.so -L${ROOTSYS}/lib RochCorStandalone.cpp `root-config --cflags` `root-config --libs`
'''
# But it does not work, so you need to run
'''
ROOT.gROOT.ProcessLine('.L RochCorStandalone.cpp+') 
'''
# and then you can use it at your leisure. Teimado linker.
gSystem.Load(os.path.join(os.path.dirname(__file__), 'RochCorStandalone_cpp.so'))
from ROOT import RochCorStandalone, RochCorStandalone2012

from PhysicsTools.Heppy.utils.cmsswRelease import isNewerThan

is2012 = isNewerThan('CMSSW_5_2_0')

class RochesterCorrections(object):
    
    def __init__(self):
        self.cor = RochCorStandalone()
        self.cor2012 = RochCorStandalone2012()

    def corrected_p4( self, particle, run ):
        '''Returns the corrected p4 for a particle.

        The particle remains unchanged. 
        '''
        ptc = particle
        p4 = ptc.p4()
        tlp4 = TLorentzVector( p4.Px(), p4.Py(), p4.Pz(), p4.Energy() )
        cortlp4 = copy.copy(tlp4)
        if run<100:
            if is2012:
                self.cor2012.momcor_mc( cortlp4, ptc.charge, 0.0, 0 )
            else:
                self.cor.momcor_mc( cortlp4, ptc.charge, 0.0, 0 )
        else: # data
            if is2012:
                self.cor2012.momcor_data( cortlp4, ptc.charge, 0.0, 0 )
            else:
                self.cor.momcor_data( cortlp4, ptc.charge, 0.0, int(run>173692) )
        corp4 = p4.__class__( cortlp4.Px(), cortlp4.Py(), cortlp4.Pz(), cortlp4.Energy() )
        return corp4

        
    def correct( self, particle, run ):
        '''Correct a particles.  '''
        corp4 = self.corrected_p4(particle, run) 
        particle.pt  =corp4.Pt()
        particle.eta =corp4.Eta()
        particle.phi =corp4.Phi()
        particle.mass=corp4.M()

    def correct_all( self, particles, run ):
        '''Correct a list of particles.

        The p4 of each particle will change '''
        for ptc in particles: 
            corp4 = self.corrected_p4(ptc, run) 
            ptc.setP4( corp4 )




rochcor = RochesterCorrections() 
        

