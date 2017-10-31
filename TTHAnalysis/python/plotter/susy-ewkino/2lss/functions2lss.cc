#include <cmath>
#include <map>
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"
#include "Math/GenVector/PxPyPzM4D.h"
#include "Math/GenVector/Boost.h"
#include "TLorentzVector.h"
#include "TH2Poly.h"
#include "TGraphAsymmErrors.h"
#include "TH1F.h"
#include "TFile.h"
#include "PhysicsTools/Heppy/interface/Davismt2.h"
#include "TSystem.h"

TString CMSSW_BASE_2lss = gSystem->ExpandPathName("${CMSSW_BASE}");

float mt_2_2lss(float pt1, float phi1, float pt2, float phi2) {
    return std::sqrt(2*pt1*pt2*(1-std::cos(phi1-phi2)));
}

float pt_2_2lss(float pt1, float phi1, float pt2, float phi2) {
    phi2 -= phi1;
    return hypot(pt1 + pt2 * std::cos(phi2), pt2*std::sin(phi2));
}

int SSR_2lss(int nj, float ptl1, float phil1, float ptl2, float phil2, float met, float metphi, int charge){
  float mtw1 = mt_2_2lss(ptl1,phil1, met, metphi);
  float mtw2 = mt_2_2lss(ptl2,phil2, met, metphi);
  float mtw  = std::min(mtw1,mtw2);
  float ptdil = pt_2_2lss(ptl1,phil1,ptl2,phil2);
  int   cha  = charge;

  if      (nj == 0 && mtw > 100 && met > 140) return 1;
  else if (nj == 1 && mtw < 100 && met > 200) return 2;
  else return -1;
}


int SR_ewk_ss2l(int nj, float ptl1, float phil1, float ptl2, float phil2, float met, float metphi, int charge){
  
  float mtw1 = mt_2_2lss(ptl1,phil1, met, metphi);
  float mtw2 = mt_2_2lss(ptl2,phil2, met, metphi);
  float mtw  = std::min(mtw1,mtw2);
  float ptdil = pt_2_2lss(ptl1,phil1,ptl2,phil2);
  int   cha  = charge;

  if      (nj==0 && ptdil<75 && mtw<100 && met<100)            return 1;  //VR

  else if (nj==0 && ptdil<75 && mtw<100 && met>100 && met<150 && cha == +1) return 2;
  else if (nj==0 && ptdil<75 && mtw<100 && met>100 && met<150 && cha == -1) return 3;


  else if (nj==0 && ptdil<75 && mtw<100 && met>150 && met < 200)            return 4;
  else if (nj==0 && ptdil<75 && mtw<100 && met > 200)            			    return 5;

  else if (nj==0 && ptdil>75 && mtw<100 && met<100)            return 6; //VR


  else if (nj==0 && ptdil>75 && mtw<100 && met>100 && met<150 && cha == +1) return 7;
  else if (nj==0 && ptdil>75 && mtw<100 && met>100 && met<150 && cha == -1) return 8;

  else if (nj==0 && ptdil>75 && mtw<100 && met>150 && met < 200)            return 9;
  else if (nj==0 && ptdil>75 && mtw<100 && met>200)				             return 10;

  else if (nj==0 && mtw>100 && met<100)                        return 11;  //VR


  else if (nj==0 && mtw>100 && met>100 && met<150 && cha == +1)             return 12;
  else if (nj==0 && mtw>100 && met>100 && met<150 && cha == -1)             return 13;

  else if (nj==0 && mtw>100 && met>150 && met<200)                          return 14;
  else if (nj==0 && mtw>100 && met>200)                        			    return 15;

  else if (nj==1 && ptdil<75 && mtw<100 && met<100 )            return 16;  //VR

  else if (nj==1 && ptdil<75 && mtw<100 && met>100 && met<150 && cha == +1) return 17;
  else if (nj==1 && ptdil<75 && mtw<100 && met>100 && met<150 && cha == -1) return 18;

  else if (nj==1 && ptdil<75 && mtw<100 && met>150 && met<200)              return 19;
  else if (nj==1 && ptdil<75 && mtw<100 && met>200)         		          return 20;

  else if (nj==1 && ptdil>75 && mtw<100 && met<100)            return 21; //VR


  else if (nj==1 && ptdil>75 && mtw<100 && met>100 && met<150 && cha == +1) return 22;
  else if (nj==1 && ptdil>75 && mtw<100 && met>100 && met<150 && cha == -1) return 23;

  else if (nj==1 && ptdil>75 && mtw<100 && met>150 && met < 200)            return 24;
  else if (nj==1 && ptdil>75 && mtw<100 && met>200) 					          return 25;

  else if (nj==1 && mtw>100 && met<100)                        return 26;  //VR

  else if (nj==1 && mtw>100 && met>100 && met<150 && cha == +1)             return 27;
  else if (nj==1 && mtw>100 && met>100 && met<150 && cha == -1)             return 28;

  else if (nj==1 && mtw>100 && met>150 && met<200)                          return 29;
  else if (nj==1 && mtw>100 && met>200)                   				       return 30;

  return -99;   
  
}

#include "TGraphAsymmErrors.h"
TFile *_file_reco_leptonSF_mu = NULL;
TFile *_file_recoToMedium_leptonSF_mu = NULL;
TFile *_file_MediumToMVA_leptonSF_mu = NULL;
TFile *_file_recoToMVA_leptonSF_el = NULL;
TFile *_file_reco_leptonSF_el = NULL;

TGraphAsymmErrors *_histo_reco_leptonSF_mu = NULL;
TH2F *_histo_recoToMedium_leptonSF_mu = NULL;
TH2F *_histo_MediumToMVA_leptonSF_mu = NULL;
TH2F *_histo_recoToMVA_leptonSF_el = NULL;
TH2F *_histo_reco_leptonSF_el = NULL;

float getLeptonSF_mu_Unc(float pt, int var) {
  if (pt<20) 
    return var*TMath::Sqrt(0.03*0.03+0.01*0.01+0.01*0.01);
  else 
    return var*TMath::Sqrt(0.02*0.02+0.01*0.01);  
}

float leptonSF_2lss_ewk(int pdgid, float pt, float eta, int var=0){
  
  if (!_histo_reco_leptonSF_mu) {
     _file_reco_leptonSF_mu = new TFile(CMSSW_BASE_2lss+"/src/CMGTools/TTHAnalysis/data/leptonSF/SF2016_muon_trackingEff.root", "data");
     _file_recoToMedium_leptonSF_mu = new TFile(CMSSW_BASE_2lss+"/src/CMGTools/TTHAnalysis/data/leptonSF/SF2016_muon_mediumId.root", "read");
     _file_MediumToMVA_leptonSF_mu = new TFile(CMSSW_BASE_2lss+"/src/CMGTools/TTHAnalysis/data/leptonSF/SF2016_muon_lepMVAveryTight.root", "read");
     _histo_reco_leptonSF_mu = (TGraphAsymmErrors*)(_file_reco_leptonSF_mu->Get("ratio_eta"));
     _histo_recoToMedium_leptonSF_mu = (TH2F*)(_file_recoToMedium_leptonSF_mu->Get("pt_abseta_PLOT_pair_probeMultiplicity_bin0"));
     _histo_MediumToMVA_leptonSF_mu = (TH2F*)(_file_MediumToMVA_leptonSF_mu->Get("pt_abseta_PLOT_pair_probeMultiplicity_bin0_&_tag_combRelIsoPF04dBeta_bin0_&_tag_pt_bin0_&_mvaPreSel_pass"));
   }
   if (!_histo_recoToMVA_leptonSF_el) {
     _file_recoToMVA_leptonSF_el = new TFile(CMSSW_BASE_2lss+"/src/CMGTools/TTHAnalysis/data/leptonSF/SF2016_electron_full.root", "read");
     _histo_recoToMVA_leptonSF_el = (TH2F*)(_file_recoToMVA_leptonSF_el->Get("GsfElectronToLeptonMvaVTIDEmuTightIP2DSIP3D8miniIso04"));
     
     _file_reco_leptonSF_el = new TFile(CMSSW_BASE_2lss+"/src/CMGTools/TTHAnalysis/data/leptonSF/SF2016_electron_trackingEff.root", "read");
     _histo_reco_leptonSF_el = (TH2F*) (_file_reco_leptonSF_el->Get("EGamma_SF2D"));
   }
   float out = 0.;
   if (abs(pdgid)==13){
     out = _histo_reco_leptonSF_mu->Eval(eta);
     TH2F *hist = _histo_recoToMedium_leptonSF_mu;
     int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
     int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
     out *= hist->GetBinContent(ptbin,etabin);
     hist = _histo_MediumToMVA_leptonSF_mu;
     ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
     etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
     out *=hist->GetBinContent(ptbin,etabin);
     return out + out*getLeptonSF_mu_Unc(pt,var);
   }
   float err = 0.;
   if (abs(pdgid)==11){
     TH2F *hist = _histo_recoToMVA_leptonSF_el;
     int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
     int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
     out = hist->GetBinContent(ptbin,etabin);
     err = hist->GetBinError(ptbin,etabin)*hist->GetBinError(ptbin,etabin);
     hist = _histo_reco_leptonSF_el;
     ptbin  = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt)));
     etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(eta)));
     out *= hist->GetBinContent(etabin,ptbin);
     err += hist->GetBinError(etabin,ptbin)*hist->GetBinError(etabin,ptbin);
     err = TMath::Sqrt(err);
     return out + out*err*var;
   }
   //cout << "[ERROR]!!!! SF UnKNOWN!!! PLEASE CHECK" << endl;
   return 1.;
 }

void functions2lss() {}
