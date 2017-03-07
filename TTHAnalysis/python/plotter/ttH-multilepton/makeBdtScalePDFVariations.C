Double_t fitRatio(TH1* h1, TH1*h2)
{
  TH1* h = (TH1*) h1->Clone("forRatio");
  TF1*  fun = new TF1("retta","[0]+[1]*x",-1.,1.);
  h->Divide(h2);
  h->Fit(fun,"Q");
  Double_t r = fun->GetParameter(1);
  delete h;
  delete fun;
  return r;
}

void makeBdtScalePDFVariations(TString dir, TString region, bool savePdfReplicas=false, bool doScaleStudy=false){

  TFile* f = TFile::Open(Form("%s/%s/2lss_3l_plots.root",dir.Data(),region.Data()), "READ");
  
  cout << "File: " << f->GetName() << endl;
  vector<TString> variable;
  if(region.Contains("2lss"))
    {
      variable.push_back("kinMVA_2lss_ttbar_withBDTv8");
      variable.push_back("kinMVA_2lss_ttV_withHj");
    }
  else if(region.Contains("3l"))
    {
      variable.push_back("kinMVA_3l_ttbar");
      variable.push_back( region.Contains("prescale") ? "kinMVA_3l_ttV_withMEM" : "kinMVA_3l_ttV");
    }
  
  vector<TString> proc;
  proc.push_back("ttH");
  proc.push_back("TTW");
  proc.push_back("TTZ");

  for(int iVariable=0;iVariable<2; ++iVariable)
    {
      cout << "BDT: " << variable[iVariable] << endl;
      TFile* outPdf = NULL;
      TFile* outScale = NULL;
      if(savePdfReplicas)
        {
          outPdf = TFile::Open(Form("%s_pdfVars.root",f->GetName()), "RECREATE");
          cout << "Distribution of replicas will be saved in: " << outPdf->GetName() << endl;
        }
      if(doScaleStudy)
        {
          outScale = TFile::Open(Form("%s_scaleVars.root",f->GetName()), "RECREATE");
          cout << "Plot for scale variation studies will be saved in: " << outScale->GetName() << endl;
        }
      
      for(int iproc=0; iproc<3; ++iproc)
        {
          cout << "=== PROC " << proc[iproc] << " ====" << endl;
          // PDF
          TH1* nominal = (TH1*) f->Get(Form("%s_%s",variable[iVariable].Data(),proc[iproc].Data()));
          
          cout << "=========== PDF: ";
          TH1D* h = new TH1D(Form("%s_%s",variable[iVariable].Data(),proc[iproc].Data()), Form("%s_%s",variable[iVariable].Data(),proc[iproc].Data()), 400, -1.,1.);
          for(int ivar=1; ivar<101; ++ivar)
            {
              TH1* var = (TH1*) f->Get(Form("%s_%s_pdf%d",variable[iVariable].Data(),proc[iproc].Data(),ivar));
              double r(fitRatio(var, nominal));
              h->Fill(r);
              //kinMVA_2lss_ttbar_withBDTv8_TTZ_pdf1
              
            }
          cout << h->GetRMS() << endl;
          if(savePdfReplicas)
            {
              outPdf->cd();
              h->Write();
            }
          delete h;

          // SCALE
          cout << "=========== SCALE: " << endl;
          TGraph* gr = new TGraph(8);
          gr->SetName(Form("%s_%s",variable[iVariable].Data(),proc[iproc].Data()));
          double max(0.);
          for(int ivar=1; ivar<9; ++ivar)
            {
              TH1* var = (TH1*) f->Get(Form("%s_%s_scale%d",variable[iVariable].Data(),proc[iproc].Data(),ivar));
              double r(fitRatio(var, nominal));
              //cout << r << endl;
              if(r>max) max=r;
              gr->SetPoint(ivar-1,ivar,r);
            }
          cout << max << endl;
          if(doScaleStudy)
            {
              outScale->cd();
              gr->Write();
            }

        }
      
      if(outPdf)   outPdf  ->Close();
      if(outScale) outScale->Close();

    }
  gApplication->Terminate();
}
