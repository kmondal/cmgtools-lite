#include "TMath.h"
#include <assert.h>
#include <iostream>
#include "TH2F.h"
#include "TH1F.h"
#include "TFile.h"
#include "TSystem.h"
#include "TLorentzVector.h"
#include "TGraphAsymmErrors.h"

int nJB(int nJ, float nBJ) {
    int bin = 0;
    
    // Push SRs to make room for the new bins
    if (nJ==1) bin =  1+nBJ;
    if (nJ==2) bin =  3+nBJ;
    if (nJ==3) bin =  6+nBJ;
    if (nJ>=4) bin = 10+nBJ;
    
    return bin;
}

Float_t WZdeltaPhi(Float_t phi1, Float_t phi2)
{
  Float_t res(phi1 - phi2);
  while(res >   M_PI) res -= Float_t(2*M_PI);
  while(res <= -M_PI) res += Float_t(2*M_PI);
  return res;
}

Float_t baseDeltaR(Float_t eta1, Float_t phi1, Float_t eta2, Float_t phi2)
{
  Float_t res;
  Float_t dEta(std::abs(eta1-eta2));
  Float_t dPhi(WZdeltaPhi(phi1, phi2));
  res= std::sqrt(dEta*dEta + dPhi*dPhi);
  return res;
}

// Shitty heppy, lots of helpers just because functions called in plots.txt cannot return complex types
Float_t sump4(Int_t component, Float_t v1pt, Float_t v1eta, Float_t v1phi, Float_t v1m, Float_t v2pt, Float_t v2eta, Float_t v2phi, Float_t v2m)
{
  TLorentzVector v1; v1.SetPtEtaPhiM(v1pt, v1eta, v1phi, v1m);
  TLorentzVector v2; v2.SetPtEtaPhiM(v2pt, v2eta, v2phi, v2m);
  TLorentzVector v; v = v1 + v2;
  Float_t ret;
  
  switch(component)
    {
    case 0:
      ret = v.Pt();
      break;
    case 1: 
      ret = v.Eta();
      break;
    case 2:
      ret = v.Phi();
      break;
    case 3:
      ret = v.M();
      break;
    default:
      ret = -99999.;
    }
  return ret;
}


//                balance = self.bestOSPair.l1.p4()
//                balance += self.bestOSPair.l2.p4()
//                self.ret["deltaR_WZ"] = deltaR(balance.Eta(), balance.Phi(), self.lepSelFO[i].p4().Eta(), self.lepSelFO[i].p4().Phi())
//                balance -= self.lepSelFO[i].p4()
//                metmom = ROOT.TLorentzVector()
//                metmom.SetPtEtaPhiM(self.met[0],0,self.metphi[0],0)
//                balance -= metmom
//                # Later do it with standalone function like makeMassMET
//                self.ret["wzBalance_pt"] = balance.Pt()
//                balance = self.bestOSPair.l1.p4(self.bestOSPair.l1.conePt)
//                balance += self.bestOSPair.l2.p4(self.bestOSPair.l2.conePt)
//                balance -= self.lepSelFO[i].p4(self.lepSelFO[i].conePt)
//                balance -= metmom
//                self.ret["wzBalance_conePt"] = balance.Pt()
//


// TBD: implement the same but with conePt
Float_t WZbalance(Float_t zpt, Float_t zeta, Float_t zphi, Float_t zm, Float_t wpt, Float_t weta, Float_t wphi, Float_t wm)
{
  TLorentzVector z; z.SetPtEtaPhiM(zpt, zeta, zphi, zm);
  TLorentzVector w; w.SetPtEtaPhiM(wpt, weta, wphi, wm);
  TLorentzVector balance = z + w;
  return balance.Pt();
}

Float_t WZdeltaR(Float_t zeta, Float_t zphi, Float_t weta, Float_t wphi)
{
  ///// save time //TLorentzVector  w; w.SetPtEtaPhiM(wpt ,  weta,  wphi,  wm);
  //
  //Float_t res(baseDeltaR(z.Eta(), z.Phi(), weta, wphi));
  Float_t res(baseDeltaR(zeta, zphi, weta, wphi));
  //std::cout << baseDeltaR(z.Eta(), z.Phi(), weta, wphi) << std::endl;
  // save time //return deltaR(z.Eta(), z.Phi(), w.Eta(), w.Phi());
  return res;
}

Int_t getWZRegion(Float_t met, Float_t mZ1, Int_t nBJets, Int_t nFOLep, Int_t l4_tight, Float_t l4_pt){
  //Region index in the WZ analysis: SR->0; CRDY->1; CRTT->2; CRZZ->3;
  if (met > 30 && TMath::Abs(91.1876-mZ1) < 15 && nBJets == 0 && nFOLep == 3)                        return 0;
  else if (met <= 30 && TMath::Abs(91.1876-mZ1) < 15 && nBJets == 0 && nFOLep == 3)                  return 1;
  else if (met > 30 && TMath::Abs(91.1876-mZ1) > 5 && nBJets > 0 && nFOLep == 3)                     return 2;
  else if (met > 30 && TMath::Abs(91.1876-mZ1) < 15 && nBJets == 0 && nFOLep == 4 && l4_pt > 10)     return 3;
  else return -1;
}

void functionsWZ() {}
