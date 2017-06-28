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

TLorentzVector Zp4(Float_t z1pt, Float_t z1eta, Float_t z1phi, Float_t z1m, Float_t z2pt, Float_t z2eta, Float_t z2phi, Float_t z2m)
{
  TLorentzVector z1; z1.SetPtEtaPhiM(z1pt, z1eta, z1phi, z1m);
  TLorentzVector z2; z2.SetPtEtaPhiM(z2pt, z2eta, z2phi, z2m);
  TLorentzVector z; z = z1 + z2;
  return z;
}

// Shitty heppy, lots of helpers just because functions called in plots.txt cannot return complex types
Float_t Zeta(Float_t z1pt, Float_t z1eta, Float_t z1phi, Float_t z1m, Float_t z2pt, Float_t z2eta, Float_t z2phi, Float_t z2m)
{
  TLorentzVector z = Zp4(z1pt, z1eta, z1phi, z1m, z2pt, z2eta, z2phi, z2m);
  return z.Eta();
}

Float_t Zphi(Float_t z1pt, Float_t z1eta, Float_t z1phi, Float_t z1m, Float_t z2pt, Float_t z2eta, Float_t z2phi, Float_t z2m)
{
  TLorentzVector z = Zp4(z1pt, z1eta, z1phi, z1m, z2pt, z2eta, z2phi, z2m);
  return z.Phi();
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



void functionsWZ() {}
