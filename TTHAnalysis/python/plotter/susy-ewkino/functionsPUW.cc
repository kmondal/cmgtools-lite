#include <assert.h>
#include <iostream>
#include "TH2F.h"
#include "TH1F.h"
#include "TFile.h"
#include "TSystem.h"

TString CMSSW_BASE_PUW = gSystem->ExpandPathName("${CMSSW_BASE}");
TString DATA_PUW = CMSSW_BASE_PUW+"/src/CMGTools/TTHAnalysis/data";

TFile* f_puw_nInt_ICHEP    = new TFile(DATA_PUW+"/pileup/puWeights_12fb_63mb.root"     , "read");;
TFile* f_puw_nInt_ICHEP_Up = new TFile(DATA_PUW+"/pileup/puWeights_12fb_63mb_Up.root"  , "read");
TFile* f_puw_nInt_ICHEP_Dn = new TFile(DATA_PUW+"/pileup/puWeights_12fb_63mb_Down.root", "read");
TH1F* h_puw_nInt_ICHEP    = (TH1F*) (f_puw_nInt_ICHEP   ->Get("puw"));
TH1F* h_puw_nInt_ICHEP_Up = (TH1F*) (f_puw_nInt_ICHEP_Up->Get("puw"));
TH1F* h_puw_nInt_ICHEP_Dn = (TH1F*) (f_puw_nInt_ICHEP_Dn->Get("puw"));

float puw_nInt_ICHEP(float nInt, int var=0) { 

  float puw = h_puw_nInt_ICHEP->GetBinContent(h_puw_nInt_ICHEP->FindBin(nInt)); 
  if(var== 0) return puw;
  if(var== 1) return h_puw_nInt_ICHEP_Up->GetBinContent(h_puw_nInt_ICHEP_Up->FindBin(nInt)) / puw;
  if(var==-1) return h_puw_nInt_ICHEP_Dn->GetBinContent(h_puw_nInt_ICHEP_Dn->FindBin(nInt)) / puw;
  cout <<"[WARNING!!!]  don't know what to do with PUweight, please check!! ";
  return 0;
}

TFile* f_puw_nInt_Moriond    = new TFile(DATA_PUW+"/pileup/puw_nTrueInt_Moriond2017_36p5fb_Summer16_69mb_central.root", "read");
TFile* f_puw_nInt_Moriond_Up = new TFile(DATA_PUW+"/pileup/puw_nTrueInt_Moriond2017_36p5fb_Summer16_69mb_up.root"     , "read");
TFile* f_puw_nInt_Moriond_Dn = new TFile(DATA_PUW+"/pileup/puw_nTrueInt_Moriond2017_36p5fb_Summer16_69mb_down.root"   , "read");
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

// debugging
//TFile* f_puw_63    = new TFile("pileup_63.root", "read");
//TFile* f_puw_66    = new TFile("pileup_66.root", "read");
//TFile* f_puw_69    = new TFile("pileup_69.root", "read");
//TH1F* h_puw_63    = (TH1F*) (f_puw_63   ->Get("puw"));
//TH1F* h_puw_66    = (TH1F*) (f_puw_66   ->Get("puw"));
//TH1F* h_puw_69    = (TH1F*) (f_puw_69   ->Get("puw"));
//float puw63(float nInt) { 
//  return  h_puw_63->GetBinContent(h_puw_63->FindBin(nInt)); 
//}
//float puw66(float nInt) { 
//  return  h_puw_66->GetBinContent(h_puw_66->FindBin(nInt)); 
//}
//float puw69(float nInt) { 
//  return  h_puw_69->GetBinContent(h_puw_69->FindBin(nInt)); 
//}

