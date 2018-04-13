void compareDressedUndressed()
{
  gStyle->SetOptStat(0);

  TFile* fdressed = TFile::Open("/nfs/fanae/user/vischia/workarea/cmssw/wz/fts_unskimmed_dressed/lepgenVarsWZSM/evVarFriend_WZTo3LNu.root", "READ");
  TFile* fundressed = TFile::Open("/pool/ciencias/HeppyTrees/RA7/wz/wzUnskimmed/lepgenVarsWZSM/evVarFriend_WZTo3LNu.root", "READ");
  
  TTree* tdressed = (TTree*) fdressed->Get("sf/t");
  TTree* tundressed = (TTree*) fundressed->Get("sf/t");

  vector<TString> vars;
  vars.push_back("genLepZ1_pt");
  vars.push_back("genLepZ2_pt");
  vars.push_back("genLepW_pt");

  for(auto& var : vars)
    {
      tdressed->Draw(var+TString(">>dressed"));
      tundressed->Draw(var+TString(">>undressed"));
      
      TH1F* dressed   = (TH1F*)gDirectory->Get("dressed");
      TH1F* undressed = (TH1F*)gDirectory->Get("undressed");
      
      cout << dressed->GetEntries()<<endl;
      cout << undressed->GetEntries()<< endl;
      dressed->SetTitle(var);
      undressed->SetTitle(var);

      dressed->Scale(1./dressed->Integral());
      undressed->Scale(1./undressed->Integral());
      
      dressed->SetLineColor(kRed);
      undressed->SetFillColor(kBlue);
      //undressed->SetFillStyle(1);
      
      TLegend* l = new TLegend(0.8,0.8,0.99,0.99);
      l->AddEntry(dressed, TString(" Dressed"), "l");
      l->AddEntry(undressed, TString(" Undressed"), "f");
      
      TCanvas* c = new TCanvas("c", "c", 1600, 800);
      c->Divide(2,1);
      c->cd(1);
      gPad->SetLogy();
      undressed->DrawCopy("");
      dressed->DrawCopy("same");
      l->Draw();
      c->cd(2);
      dressed->Add(undressed, -1);
      dressed->Draw();
      c->Print("dressedCheck_"+var+".png");
    }
}

void compareRochesterNonrochester()
{
  gStyle->SetOptStat(0);

  TFile* froch   = TFile::Open("/nfs/fanae/user/vischia/workarea/cmssw/wz/fts_rochester/leptonBuilderWZSM/evVarFriend_WZTo3LNu.root", "READ");
  TFile* fnoroch = TFile::Open("/pool/ciencias/HeppyTrees/RA7/estructura/wzSkimmed/leptonBuilderWZSM/evVarFriend_WZTo3LNu.root", "READ");
  
  TTree* troch   = (TTree*) froch  ->Get("sf/t");
  TTree* tnoroch = (TTree*) fnoroch->Get("sf/t");

  vector<TString> vars;
  vars.push_back("LepZ1_pt");
  vars.push_back("LepZ2_pt");
  vars.push_back("LepW_pt");

  vector<TString> cuts;
  cuts.push_back("abs(LepZ1_pdgId)==13");
  cuts.push_back("abs(LepZ2_pdgId)==13");
  cuts.push_back("abs(LepW_pdgId)==13");

  int k=0;
  for(auto& var : vars)
    {
      troch  ->Draw(var+TString(">>rochester")  , cuts[k]);
      tnoroch->Draw(var+TString(">>norochester"), cuts[k]);
  
      TH1F* roch   = (TH1F*)gDirectory->Get("rochester");
      TH1F* noroch = (TH1F*)gDirectory->Get("norochester");
      
      cout << roch->GetEntries()<<endl;
      cout << noroch->GetEntries()<< endl;
      roch->SetTitle(var);
      noroch->SetTitle(var);

      roch->Scale(1./roch->Integral());
      noroch->Scale(1./noroch->Integral());
      
      roch->SetLineColor(kRed);
      noroch->SetFillColor(kBlue);
     
      TLegend* l = new TLegend(0.8,0.8,0.99,0.99);
      l->AddEntry(roch  , TString(" Rochester"), "l");
      l->AddEntry(noroch, TString(" No Rochester"), "f");
      
      TCanvas* c = new TCanvas("c", "c", 1600, 800);
      c->Divide(2,1);
      c->cd(1);
      gPad->SetLogy();
      noroch->DrawCopy("");
      roch->DrawCopy("same");
      l->Draw();
      c->cd(2);
      roch->Add(noroch, -1);
      roch->Draw();
      c->Print("rochesterCheck_muOnly_"+var+".png");
      k++;
    }
}

void compareDistributions(TString what="rochester")
{
  if(what.Contains("rochester"))
    compareRochesterNonrochester();
  if(what.Contains("dressed"))
    compareDressedUndressed();

}
