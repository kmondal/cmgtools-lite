#include "TMath.h"
#include <assert.h>
#include <iostream>
#include "TH2F.h"
#include "TH1F.h"
#include "TFile.h"
#include "TSystem.h"
#include "TGraphAsymmErrors.h"

int allTight(int nLep, int l1isTight, int l2isTight, int l3isTight, int l4isTight = 0){
    if(nLep == 3) return ((l1isTight+l2isTight+l3isTight)==3);
    return ((l1isTight+l2isTight+l3isTight+l4isTight)==4);
}

int isGoodFake(float pt, int isTight) {
    if(pt == 0) return 0;
    if(isTight) return 0;
    return 1;
}

int isFake(int nLep, int lep1mcUCSX, int lep2mcUCSX, int lep3mcUCSX, int lep4mcUCSX = 0) {
    if(nLep == 3) return ((lep1mcUCSX==2 || lep1mcUCSX==3) || (lep2mcUCSX==2 || lep2mcUCSX==3) || (lep3mcUCSX==2 || lep3mcUCSX==3));
    return ((lep1mcUCSX==2 || lep1mcUCSX==3) || (lep2mcUCSX==2 || lep2mcUCSX==3) || (lep3mcUCSX==2 || lep3mcUCSX==3) || (lep4mcUCSX==2 || lep4mcUCSX==3));
}



float mTcalc(float mT_3l, float mT_4l, float mT_fo_3l, float mT_fo_4l, int nLepTight, int nLepSel, int UCSX1, int UCSX2, int UCSX3){
  float mTW = 0.;
  if (nLepTight<3 || UCSX1>1 || UCSX2>1 || UCSX3>1){
      if (nLepSel==3) mTW = mT_fo_3l;
      else if (nLepSel==4) mTW = mT_fo_4l;
  } else {
      if (nLepTight==3) mTW = mT_3l;
      else if (nLepTight==4) mTW = mT_4l;
  }
  return mTW;
}


int SR1b2b(int SRorig, float mT) {
    // Start from M17 SRs
    int SR = SRorig;
    
    // Push SRs to make room for the new bins
    if (SRorig>12) SR+=4;  // (offZ 8)
    if (SRorig>16) SR+=4; // (offZ 12)
    if (SRorig>35) SR+=4;  // (onZ 5)
    if (SRorig>39) SR+=4;  // (onZ 6)


    // Now split interesting SRs according to mT
    if ((SRorig>=9 && SRorig<=16) || (SRorig>=32 && SRorig<=39)) {
      if (mT > 120.) SR+=4;
    }

    return SR;
}

////////////////////////
// Lepton SF material //
////////////////////////

float getLeptonSF_mu_Unc(float pt, int var) {
  if (pt<20) 
    return var*TMath::Sqrt(0.03*0.03+0.01*0.01+0.01*0.01);
  else 
    return var*0.03; //TMath::Sqrt(0.02*0.02+0.01*0.01);  
}




float getSF(TH2F* hist, float pt, float eta){
    int xbin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
    int ybin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(eta)));
    return hist->GetBinContent(xbin,ybin);
}

float getUnc(TH2F* hist, float pt, float eta){
    int xbin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
    int ybin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(eta)));
    return hist->GetBinError(xbin,ybin);
}



TFile *_file_reco_leptonSF_mu = NULL;
TFile *_file_recoToMedium_leptonSF_mu = NULL;
TFile *_file_MediumToMultiIso_leptonSF_mu = NULL;
TFile *_file_recoToTight_leptonSF_el = NULL;
TFile *_file_reco_leptonSF_el = NULL;

TGraphAsymmErrors *_histo_reco_leptonSF_mu = NULL;
TH2F *_histo_recoToMedium_leptonSF_mu = NULL;
TH2F *_histo_MediumToMultiIso_leptonSF_mu = NULL;

TH2F *_histo_reco_leptonSF_el = NULL;
TH2F *_histo_recoToTight_leptonSF_el = NULL;
TH2F *_histo_TightToMultiIso_leptonSF_el = NULL;
TH2F *_histo_TightToHitsConv_leptonSF_el = NULL;



TString CMSSW_BASE_RA7 = gSystem->ExpandPathName("${CMSSW_BASE}");
TString DATA_RA7 = CMSSW_BASE_RA7+"/src/CMGTools/TTHAnalysis/data";

//// LEPTON SF FULLSIM
/*
float leptonSF_ra7(int pdgid, float pt, float eta, int var=0){
  
  if (!_histo_reco_leptonSF_mu) {
     _file_reco_leptonSF_mu = new TFile(DATA_RA7+"/leptonSF/muonSF_trk_EWKino_fullsim_M17_36p5fb.root", "data");
     _file_recoToMedium_leptonSF_mu = new TFile(DATA_RA7+"/leptonSF/ra7_lepsf_fullsim/muons/TnP_NUM_MediumID_DENOM_generalTracks_VAR_map_pt_eta.root", "read");
     _file_MediumToMultiIso_leptonSF_mu = new TFile(DATA_RA7+"/leptonSF/ra7_lepsf_fullsim/muons/TnP_NUM_MultiIsoLoose_DENOM_MediumID_VAR_map_pt_eta.root", "read");
     _histo_reco_leptonSF_mu = (TGraphAsymmErrors*)(_file_reco_leptonSF_mu->Get("ratio_eff_eta3_dr030e030_corr"));
     _histo_recoToMedium_leptonSF_mu = (TH2F*)(_file_recoToMedium_leptonSF_mu->Get("SF"));
     _histo_MediumToMultiIso_leptonSF_mu = (TH2F*)(_file_MediumToMultiIso_leptonSF_mu->Get("SF"));
   }
   if (!_histo_recoToTight_leptonSF_el) {
     _file_recoToTight_leptonSF_el = new TFile(DATA_RA7+"/leptonSF/ra7_lepsf_fullsim/electrons/scaleFactors.root", "read");
     _histo_recoToTight_leptonSF_el = (TH2F*)(_file_recoToTight_leptonSF_el->Get("GsfElectronToMVATightIDEmuTightIP2DSIP3D4"));
     _histo_TightToMultiIso_leptonSF_el = (TH2F*)(_file_recoToTight_leptonSF_el->Get("MVATightElectronToMultiIsoM"));
     _histo_TightToHitsConv_leptonSF_el = (TH2F*)(_file_recoToTight_leptonSF_el->Get("MVATightElectronToConvVetoIHit0"));
     
     _file_reco_leptonSF_el = new TFile(DATA_RA7+"/leptonSF/ra7_lepsf_fullsim/electrons/egammaEffi.txt_EGM2D.root", "read");
     _histo_reco_leptonSF_el = (TH2F*) (_file_reco_leptonSF_el->Get("EGamma_SF2D"));
   }
   float out = 0.;
   if (abs(pdgid)==13){
     out = _histo_reco_leptonSF_mu->Eval(eta);
     TH2F *hist = _histo_recoToMedium_leptonSF_mu;
     int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
     int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
     out *= hist->GetBinContent(ptbin,etabin);
     hist = _histo_MediumToMultiIso_leptonSF_mu;
     ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
     etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
     out *= hist->GetBinContent(ptbin,etabin);
     return out + out*getLeptonSF_mu_Unc(pt,var);
   }
   float err = 0.;
   if (abs(pdgid)==11){
     TH2F *hist = _histo_recoToTight_leptonSF_el;
     int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
     int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
     out = hist->GetBinContent(ptbin,etabin);
     err = hist->GetBinError(ptbin,etabin)*hist->GetBinError(ptbin,etabin);
     hist = _histo_TightToHitsConv_leptonSF_el;
     ptbin  = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt)));
     etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(eta)));
     out *= hist->GetBinContent(etabin,ptbin);
     err += hist->GetBinError(etabin,ptbin)*hist->GetBinError(etabin,ptbin);
     hist = _histo_TightToMultiIso_leptonSF_el;
     ptbin  = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt)));
     etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(eta)));
     out *= hist->GetBinContent(etabin,ptbin);
     err += hist->GetBinError(etabin,ptbin)*hist->GetBinError(etabin,ptbin);
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
*/


// LEPTON SCALE FACTORS FULLSIM
// -------------------------------------------------------------


// electrons
TFile* f_elSF_id   = new TFile(DATA_RA7+"/leptonSF/electronSF_id_EWKino_fullsim_M17_36p5fb.root"    , "read");
TFile* f_elSF_eff  = new TFile(DATA_RA7+"/leptonSF/electronSF_trkEff_EWKino_fullsim_M17_36p5fb.root", "read");
TH2F* h_elSF_cvhit = (TH2F*) f_elSF_id ->Get("MVATightElectronToConvVetoIHit0");
TH2F* h_elSF_mIso  = (TH2F*) f_elSF_id ->Get("MVATightElectronToMultiIsoM");
TH2F* h_elSF_mva   = (TH2F*) f_elSF_id ->Get("GsfElectronToMVATightIDEmuTightIP2DSIP3D4");
TH2F* h_elSF_trk   = (TH2F*) f_elSF_eff->Get("EGamma_SF2D");

// muons
TFile* f_muSF_mIso  = new TFile(DATA_RA7+"/leptonSF/ra7_lepsf_fullsim/muons/TnP_NUM_MultiIsoLoose_DENOM_MediumID_VAR_map_pt_eta.root" , "read");
TFile* f_muSF_id    = new TFile(DATA_RA7+"/leptonSF/ra7_lepsf_fullsim/muons/TnP_NUM_MediumID_DENOM_generalTracks_VAR_map_pt_eta.root"   , "read");
TFile* f_muSF_trk   = new TFile(DATA_RA7+"/leptonSF/muonSF_trk_EWKino_fullsim_M17_36p5fb.root"  , "read"); 
TH2F* h_muSF_mIso  = (TH2F*) f_muSF_mIso ->Get("SF" );
TH2F* h_muSF_id    = (TH2F*) f_muSF_id   ->Get("SF" );
TGraphAsymmErrors* h_muSF_trk = (TGraphAsymmErrors*) f_muSF_trk->Get("ratio_eff_eta3_dr030e030_corr");

float getElectronSF(float pt, float eta){
    return getSF(h_elSF_cvhit, pt, abs(eta))*getSF(h_elSF_mIso, pt, abs(eta))*getSF(h_elSF_mva, pt, abs(eta))*getSF(h_elSF_trk, eta, pt);
}

float getElectronUnc(float pt, float eta, int var = 0){
    float error1 = getUnc(h_elSF_cvhit, pt , abs(eta));
    float error2 = getUnc(h_elSF_mIso , pt , abs(eta));
    float error3 = getUnc(h_elSF_mva  , pt , abs(eta));
    float error4 = getUnc(h_elSF_trk  , eta, pt);
    return var*TMath::Sqrt(error1*error1 + error2*error2 + error3*error3 + error4*error4);
}

float getMuonSF(float pt, float eta){
    return h_muSF_trk->Eval(eta)*getSF(h_muSF_mIso, pt, abs(eta))*getSF(h_muSF_id, pt, abs(eta)); 
}

float getMuonUnc(float pt, int var = 0) {
    if (pt<20)  //FIXME: check uncertainty on tracking efficiency once it is available
         return var*TMath::Sqrt(0.03*0.03+0.01*0.01+0.01*0.01);
    return var*TMath::Sqrt(0.02*0.02+0.01*0.01);  
}

float getLepSF(float pt, float eta, int pdgId, int isTight, int wp = 0, int var = 0){
    if(!isTight) return 1.0;
    float sf  = 1.0; 
    float err = 0.0;
    if(abs(pdgId) == 11) { sf = getElectronSF(pt, eta); err = getElectronUnc(pt, eta, var); }
    if(abs(pdgId) == 13) { sf = getMuonSF    (pt, eta); err = sf*getMuonUnc (pt, var);          } // only relative error
    if(abs(pdgId) == 15) { sf = 0.95                      ; err = 0.05;                             }
    return (var==0)?sf:(sf+var*err)/sf;
}

float leptonSF(float lepSF1, float lepSF2, float lepSF3 = 1, float lepSF4 = 1){
    return lepSF1*lepSF2*lepSF3*lepSF4;
}


// For WZ sync exercise
/////////////////////////////////////////////////////////////////////
float leptonSF_ra5(int pdgid, float pt, float eta, int var=0){
  
  if (!_histo_reco_leptonSF_mu) {
     _file_reco_leptonSF_mu = new TFile(DATA_RA7+"/leptonSF/ra7_lepsf_fullsim/muons/sf_mu_trk_susy_ICHEP.root", "data");
     _file_recoToMedium_leptonSF_mu = new TFile(DATA_RA7+"/leptonSF/ra7_lepsf_fullsim/muons/TnP_NUM_MediumID_DENOM_generalTracks_VAR_map_pt_eta.root", "read");
     _file_MediumToMultiIso_leptonSF_mu = new TFile(DATA_RA7+"/leptonSF/ra7_lepsf_fullsim/muons/TnP_NUM_MultiIsoMedium_DENOM_MediumID_VAR_map_pt_eta.root", "read");
     _histo_reco_leptonSF_mu = (TGraphAsymmErrors*)(_file_reco_leptonSF_mu->Get("ratio_eta"));
     _histo_recoToMedium_leptonSF_mu = (TH2F*)(_file_recoToMedium_leptonSF_mu->Get("SF"));
     _histo_MediumToMultiIso_leptonSF_mu = (TH2F*)(_file_MediumToMultiIso_leptonSF_mu->Get("SF"));
   }
   if (!_histo_recoToTight_leptonSF_el) {
     _file_recoToTight_leptonSF_el = new TFile(DATA_RA7+"/leptonSF/ra7_lepsf_fullsim/electrons/scaleFactors.root", "read");
     _histo_recoToTight_leptonSF_el = (TH2F*)(_file_recoToTight_leptonSF_el->Get("GsfElectronToMVATightIDEmuTightIP2DSIP3D4"));
     _histo_TightToMultiIso_leptonSF_el = (TH2F*)(_file_recoToTight_leptonSF_el->Get("MVATightElectronToMultiIsoTISOEmu"));
     
     _file_reco_leptonSF_el = new TFile(DATA_RA7+"/leptonSF/ra7_lepsf_fullsim/electrons/egammaEffi.txt_EGM2D.root", "read");
     _histo_reco_leptonSF_el = (TH2F*) (_file_reco_leptonSF_el->Get("EGamma_SF2D"));
   }
   float out = 0.;
   if (abs(pdgid)==13){
     out = _histo_reco_leptonSF_mu->Eval(eta);
     TH2F *hist = _histo_recoToMedium_leptonSF_mu;
     int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
     int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
     out *= hist->GetBinContent(ptbin,etabin);
     hist = _histo_MediumToMultiIso_leptonSF_mu;
     ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
     etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
     out *= hist->GetBinContent(ptbin,etabin);
     return out + out*getLeptonSF_mu_Unc(pt,var);
   }
   float err = 0.;
   if (abs(pdgid)==11){
     TH2F *hist = _histo_recoToTight_leptonSF_el;
     int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
     int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
     out = hist->GetBinContent(ptbin,etabin);
     err = hist->GetBinError(ptbin,etabin)*hist->GetBinError(ptbin,etabin);
     hist = _histo_TightToMultiIso_leptonSF_el;
     ptbin  = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt)));
     etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(eta)));
     out *= hist->GetBinContent(etabin,ptbin);
     err += hist->GetBinError(etabin,ptbin)*hist->GetBinError(etabin,ptbin);
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
 
// For WZ sync exercise
/////////////////////////////////////////////////////////////////////
float OLDleptonSF_ra7(int pdgid, float pt, float eta, int var=0){
  
  if (!_histo_reco_leptonSF_mu) {
     _file_reco_leptonSF_mu = new TFile("/nfs/fanae/user/nachos/leptonSF/sf_mu_trk_susy_ICHEP.root", "data");
     _file_recoToMedium_leptonSF_mu = new TFile("/nfs/fanae/user/nachos/leptonSF/TnP_MuonID_NUM_MediumID_DENOM_generalTracks_VAR_map_pt_eta.root", "read");
     _file_MediumToMultiIso_leptonSF_mu = new TFile("/nfs/fanae/user/nachos/leptonSF/TnP_MuonID_NUM_MultiIsoLoose_DENOM_MediumID_VAR_map_pt_eta.root", "read");
     _histo_reco_leptonSF_mu = (TGraphAsymmErrors*)(_file_reco_leptonSF_mu->Get("ratio_eta"));
     _histo_recoToMedium_leptonSF_mu = (TH2F*)(_file_recoToMedium_leptonSF_mu->Get("pt_abseta_PLOT_pair_probeMultiplicity_bin0"));
     _histo_MediumToMultiIso_leptonSF_mu = (TH2F*)(_file_MediumToMultiIso_leptonSF_mu->Get("pt_abseta_PLOT_pair_probeMultiplicity_bin0_&_Medium2016_pass"));
   }
   if (!_histo_recoToTight_leptonSF_el) {
     _file_recoToTight_leptonSF_el = new TFile("/nfs/fanae/user/nachos/leptonSF/sf_el_susy_ICHEP.root", "read");
     _histo_recoToTight_leptonSF_el = (TH2F*)(_file_recoToTight_leptonSF_el->Get("GsfElectronToTightID2D3D"));
     _histo_TightToMultiIso_leptonSF_el = (TH2F*)(_file_recoToTight_leptonSF_el->Get("MVATightElectronToMultiIsoM"));
     
     _file_reco_leptonSF_el = new TFile("/nfs/fanae/user/nachos/leptonSF/sf_el_trk_susy_ICHEP.root", "read");
     _histo_reco_leptonSF_el = (TH2F*) (_file_reco_leptonSF_el->Get("EGamma_SF2D"));
   }
   float out = 0.;
   if (abs(pdgid)==13){
     out = _histo_reco_leptonSF_mu->Eval(eta);
     TH2F *hist = _histo_recoToMedium_leptonSF_mu;
     int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
     int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
     /*out *= hist->GetBinContent(ptbin,etabin);
     hist = _histo_MediumToMultiIso_leptonSF_mu;
     ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
     etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
     out *= hist->GetBinContent(ptbin,etabin);*/
     return out + out*getLeptonSF_mu_Unc(pt,var);
   }
   float err = 0.;
   if (abs(pdgid)==11){
     TH2F *hist = _histo_recoToTight_leptonSF_el;
     int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt)));
     int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(fabs(eta))));
     out = hist->GetBinContent(ptbin,etabin);
     err = hist->GetBinError(ptbin,etabin)*hist->GetBinError(ptbin,etabin);
     hist = _histo_TightToMultiIso_leptonSF_el;
     ptbin  = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt)));
     etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(eta)));
     out *= hist->GetBinContent(etabin,ptbin);
     err += hist->GetBinError(etabin,ptbin)*hist->GetBinError(etabin,ptbin);
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




// LEPTON SCALE FACTORS FASTSIM
// -------------------------------------------------------------

// electrons
TFile* f_elSF_FS_MIM = new TFile(DATA_RA7+"/leptonSF/ra7_lepsf_fastsim/electrons/sf_el_multiMedium.root", "read");
TFile* f_elSF_FS_Tid = new TFile(DATA_RA7+"/leptonSF/ra7_lepsf_fastsim/electrons/sf_el_tightMVA_IDISOEmu_mutliT_tight2DIP_tight3DIP_vtxC_hitseq0_charge.root"   , "read");
TH2F* h_elSF_FS_MIM  = (TH2F*) f_elSF_FS_MIM->Get("histo2D");
TH2F* h_elSF_FS_Tid  = (TH2F*) f_elSF_FS_Tid->Get("histo2D");

// muons
TFile* f_muSF_FS_MIL = new TFile(DATA_RA7+"/leptonSF/ra7_lepsf_fastsim/muons/sf_mu_mediumID_multiL.root", "read");
TFile* f_muSF_FS_Mid = new TFile(DATA_RA7+"/leptonSF/ra7_lepsf_fastsim/muons/sf_mu_medium.root"   , "read");
TH2F* h_muSF_FS_MIL  = (TH2F*) f_muSF_FS_MIL->Get("histo2D");
TH2F* h_muSF_FS_Mid  = (TH2F*) f_muSF_FS_Mid->Get("histo2D");


float getElectronSFFS(float pt, float eta){
    return getSF(h_elSF_FS_MIM, pt, abs(eta))*getSF(h_elSF_FS_Tid, pt, abs(eta));
}

float getElectronUncFS(int var = 0){
	return var*0.02;
}

float getMuonSFFS(float pt, float eta){
    return getSF(h_muSF_FS_MIL, pt, abs(eta))*getSF(h_muSF_FS_Mid, pt, abs(eta)); 
}

float getMuonUncFS(float pt, int var = 0) {
	return var*0.02;
}



float getLepSFFS(float pt, float eta, int pdgId, int isTight, int wp = 0, int var = 0){
    if(!isTight) return 1.0;
    if(abs(pdgId) == 13) return (var==0)?getMuonSFFS    (pt, eta):(1+getMuonUncFS(var));
    if(abs(pdgId) == 11) return (var==0)?getElectronSFFS(pt, eta):(1+getElectronUncFS(var));
    return 1.0;
}

float leptonSFFS(float lepSF1, float lepSF2, float lepSF3 = 1.0, float lepSF4 = 1.0){
    return lepSF1*lepSF2*lepSF3*lepSF4;
}







TFile* f_trigSF       = new TFile(DATA_RA7+"/triggerSF/triggerSF_EWKino_fullsim_ICHEP2016_9p2fb.root"       , "read");
TFile* f_trigSF_ele27 = new TFile(DATA_RA7+"/triggerSF/triggerSF_Ele27_EWKino_fullsim_ICHEP2016_12p9fb.root", "read");

TH2F* h_trigSF_3l_mu = (TH2F*) f_trigSF      ->Get("eff_3l_mu" );
TH2F* h_trigSF_3l_el = (TH2F*) f_trigSF      ->Get("eff_3l_ele");
TH2F* h_trigSF_2l_mu = (TH2F*) f_trigSF      ->Get("eff_2l_mu" );
TH2F* h_trigSF_2l_el = (TH2F*) f_trigSF      ->Get("eff_2l_ele");
TH2F* h_trigSF_ele27 = (TH2F*) f_trigSF_ele27->Get("hist2dnum_Ele27_WPLoose_Gsf__HLT_Ele27_WPLoose_Gsf");

float triggerSF(int BR, float pt1, int pdg1, 
                        float pt2, int pdg2, 
                        float pt3 = 0, int pdg3 = 0, 
                        float pt4 = 0, int pdg4 = 0){
    // Lesya's mail:
    // - split for trailing ele or trailing mu
    // - 3l: subleading vs trailing lepton pt (1l + 2l triggers)
    // - 2l: leading light lepton vs subleading light lepton ==> good for both 2l+tau and 2lSS cases (1l + 2l triggers)
    // - l+tautau: use flat 86% everywhere; pt_e > 35 GeV; pt_mu > 25 GeV (1l + l/tau triggers)

    // 3l: 2tau (flat 86% in dedicated function)
    if(BR == 6) return 1.0;

    // 3l: 3light
    if(BR <= 2) {
        TH2F* hist = (abs(pdg3) == 13)?h_trigSF_3l_mu:h_trigSF_3l_el;
        int xbin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt2)));
        int ybin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt3)));
        return hist->GetBinContent(xbin,ybin);
    } 

    // 3l: 2light + 1tau
    if(BR >= 3 && BR <= 5){
        vector<int> pdgs; vector<float> pts;
        if(abs(pdg1)!=15) { pdgs.push_back(abs(pdg1)); pts.push_back(pt1); }
        if(abs(pdg2)!=15) { pdgs.push_back(abs(pdg2)); pts.push_back(pt2); }
        if(abs(pdg3)!=15) { pdgs.push_back(abs(pdg3)); pts.push_back(pt3); }
        TH2F* hist = (pdgs[1] == 13)?h_trigSF_2l_mu:h_trigSF_2l_el;
        int xbin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pts[0])));
        int ybin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pts[1])));
        return hist->GetBinContent(xbin,ybin);
    }

    // 2lss 
    if(BR == -1){
        TH2F* hist = (pdg2 == 13)?h_trigSF_2l_mu:h_trigSF_2l_el;
        int xbin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(pt1)));
        int ybin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(pt2)));
        return hist->GetBinContent(xbin,ybin);
    }

    // others: (4l, crwz) 
    return 1;
}



//////////////////
// PUW material //
//////////////////



TFile* f_puw_nInt_ICHEP    = new TFile(DATA_RA7+"/pileup/puWeights_12fb_63mb.root"     , "read");;
TFile* f_puw_nInt_ICHEP_Up = new TFile(DATA_RA7+"/pileup/puWeights_12fb_63mb_Up.root"  , "read");
TFile* f_puw_nInt_ICHEP_Dn = new TFile(DATA_RA7+"/pileup/puWeights_12fb_63mb_Down.root", "read");
TH1F* h_puw_nInt_ICHEP    = (TH1F*) (f_puw_nInt_ICHEP   ->Get("puw"));
TH1F* h_puw_nInt_ICHEP_Up = (TH1F*) (f_puw_nInt_ICHEP_Up->Get("puw"));
TH1F* h_puw_nInt_ICHEP_Dn = (TH1F*) (f_puw_nInt_ICHEP_Dn->Get("puw"));

float puw_nInt_ICHEP(float nInt, int var=0) { 

  float puw = h_puw_nInt_ICHEP->GetBinContent(h_puw_nInt_ICHEP->FindBin(nInt)); 
  if(var== 0) return puw;
  if(var== 1) return h_puw_nInt_ICHEP_Up->GetBinContent(h_puw_nInt_ICHEP_Up->FindBin(nInt)) / puw;
  if(var==-1) return h_puw_nInt_ICHEP_Dn->GetBinContent(h_puw_nInt_ICHEP_Dn->FindBin(nInt)) / puw;
  cout <<"[WARNING!!!]  don't know what to do with PUweight, please check!! ";
  return -9999.;
}

TFile* f_puw_nInt_Moriond    = new TFile(DATA_RA7+"/pileup/puw_nTrueInt_Moriond2017_36p5fb_Summer16_69mb_central.root", "read");
TFile* f_puw_nInt_Moriond_Up = new TFile(DATA_RA7+"/pileup/puw_nTrueInt_Moriond2017_36p5fb_Summer16_69mb_up.root"     , "read");
TFile* f_puw_nInt_Moriond_Dn = new TFile(DATA_RA7+"/pileup/puw_nTrueInt_Moriond2017_36p5fb_Summer16_69mb_down.root"   , "read");
TH1F* h_puw_nInt_Moriond    = (TH1F*) (f_puw_nInt_Moriond   ->Get("puw"));
TH1F* h_puw_nInt_Moriond_Up = (TH1F*) (f_puw_nInt_Moriond_Up->Get("puw"));
TH1F* h_puw_nInt_Moriond_Dn = (TH1F*) (f_puw_nInt_Moriond_Dn->Get("puw"));

float puw_nInt_Moriond(float nInt, int var=0, int evt = 0) { 

  float puw = h_puw_nInt_Moriond->GetBinContent(h_puw_nInt_Moriond->FindBin(nInt)); 
  if(var== 0) return puw;
  if(puw== 0) return 0;
  if(var== 1) return float(h_puw_nInt_Moriond_Up->GetBinContent(h_puw_nInt_Moriond_Up->FindBin(nInt))) / puw;
  if(var==-1) return float(h_puw_nInt_Moriond_Dn->GetBinContent(h_puw_nInt_Moriond_Dn->FindBin(nInt))) / puw;
  cout <<"[WARNING!!!]  don't know what to do with PUweight, please check!! ";
  return 0;
}

//Old material for WZ exercise
float OLDpuw_nInt_Moriond(float nInt, int var = 0) { 
    TFile* puw36p4fb   = new TFile("/nfs/fanae/user/nachos/ForECO/puw_nTrueInt_Moriond2017_36p4fb.root", "read");
    TH1F* hist    = (TH1F*) puw36p4fb  ->Get("puw");
    return hist -> GetBinContent(hist -> FindBin(nInt));
}



void functionsRA7() {}
