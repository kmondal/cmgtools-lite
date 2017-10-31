#include <cmath>
#include <map>

int SR_ewk_ss2l(int nj, float mtw1, float mtw2, float ptdil, float met, int charge){
   
  float mtw  = std::min(mtw1,mtw2);
  int   cha  = charge;
  
  if      (nj==0 && ptdil<50 && mtw<100 && met<100)                         return 1;   // 0jet, ptdil<50 -- VR         
  else if (nj==0 && ptdil<50 && mtw<100 && met>100 && met<150 && cha == 1) return 2; // 0jet, ptdil<50 MET>100, ++    
  else if (nj==0 && ptdil<50 && mtw<100 && met>100 && met<150 && cha == -1) return 3;// 0jet, ptdil<50 MET>100, --   
  else if (nj==0 && ptdil<50 && mtw<100 && met>150 && met < 200)            return 4;// 0jet, ptdil<50 MET>150       
  else if (nj==0 && ptdil<50 && mtw<100 && met > 200)                return 5;// 0jet, ptdil<50 MET>200       
  else if (nj==0 && ptdil>50 && mtw<100 && met<100)                         return 6;   // 0jet, ptdil>50     VR         
  else if (nj==0 && ptdil>50 && mtw<100 && met>100 && met<150 && cha == 1) return 7;// 0jet, ptdil>50 MET>100, ++     
  else if (nj==0 && ptdil>50 && mtw<100 && met>100 && met<150 && cha == -1) return 8;// 0jet, ptdil>50 MET>100, --   
  else if (nj==0 && ptdil>50 && mtw<100 && met>150 && met < 200)            return 9;// 0jet, ptdil>50 MET>150       
  else if (nj==0 && ptdil>50 && mtw<100 && met>200)    return 10;// 0jet, ptdil>50 MET>200       
  else if (nj==0 && mtw>100 && met<100)                                     return 11;  // 0jet, MT>100                 
  else if (nj==0 && mtw>100 && met>100 && met<150 && cha == 1)             return 12;// 0jet, MT>100, MET>100,++     
  else if (nj==0 && mtw>100 && met>100 && met<150 && cha == -1)             return 13;// 0jet, MT>100, MET>100, --    
  else if (nj==0 && mtw>100 && met>150 && met<200)                          return 14;// 0jet, MT>100, MET>150        
  else if (nj==0 && mtw>100 && met>200)                            return 15;// 0jet, MT>100, MET>200        
  else if (nj==1 && ptdil<50 && mtw<100 && met<100 )                        return 16;  // 1jet, ptdil<50 -- VR
  else if (nj==1 && ptdil<50 && mtw<100 && met>100 && met<150 && cha == 1) return 17;  // 1jet, ptdil<50 MET>100, ++ 
  else if (nj==1 && ptdil<50 && mtw<100 && met>100 && met<150 && cha == -1) return 18;  // 1jet, ptdil<50 MET>100, --
  else if (nj==1 && ptdil<50 && mtw<100 && met>150 && met<200)              return 19;  // 1jet, ptdil<50 MET>150
  else if (nj==1 && ptdil<50 && mtw<100 && met>200)             return 20;  // 1jet, ptdil<50 MET>200
  else if (nj==1 && ptdil>50 && mtw<100 && met<100)                         return 21;  // 1jet, ptdil>50 -- VR
  else if (nj==1 && ptdil>50 && mtw<100 && met>100 && met<150 && cha == 1) return 22;  // 1jet, ptdil>50 MET>100, ++
  else if (nj==1 && ptdil>50 && mtw<100 && met>100 && met<150 && cha == -1) return 23;// 1jet, ptdil>50 MET>100, -- 
  else if (nj==1 && ptdil>50 && mtw<100 && met>150 && met < 200)            return 24;// 1jet, ptdil>50 MET>150     
  else if (nj==1 && ptdil>50 && mtw<100 && met>200)     return 25;  // 1jet, ptdil>50 MET>200     
  else if (nj==1 && mtw>100 && met<100)                                     return 26;  // 1jet, MT>100  
  else if (nj==1 && mtw>100 && met>100 && met<150 && cha == 1)             return 27;  // 1jet, MT>100, MET>100, ++
  else if (nj==1 && mtw>100 && met>100 && met<150 && cha == -1)             return 28;  // 1jet, MT>100, MET>100, --
  else if (nj==1 && mtw>100 && met>150 && met<200)                          return 29;  // 1jet, MT>100, MET>150
  else if (nj==1 && mtw>100 && met>200)                       return 30;  // 1jet, MT>100, MET>200        
  
  return -99;   
  
}
