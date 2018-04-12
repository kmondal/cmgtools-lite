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
