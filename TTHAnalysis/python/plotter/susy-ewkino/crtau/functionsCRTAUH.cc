int CRTAUH(int nTau, float mT2L, float mT2T, float mll, float mT, float met, int offset = 0) {

  if(nTau==0) return offset + 1;
  if(nTau==1) return offset + 2;
  
  return 0;
}

int SR(int nLep, int nTau, int nOSSF, int nOSLF, float mT2L, float mT2T, float mll, float mT, float met) {
  
  if(nLep==2)
    return CRTAUH(nTau, mT2L, mT2T, mll, mT, met, 140);
  if(nLep==1)
    return CRTAUH(nTau, mT2L, mT2T, mll, mT, met, 143);
  if(nLep==0)
    return CRTAUH(nTau, mT2L, mT2T, mll, mT, met, 146);
  if(nLep>0 && nLep <3)
    return CRTAUH(nTau, mT2L, mT2T, mll, mT, met, 149);
  return 0;
}

void functionsCRTAUH() {}
