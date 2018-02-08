from utils import command as command
from utils import clean
from utils import os
import string

"""
"""
        # Regions:
    # 
    # C:         3lC         SR-42            OSSF + 1tau
    # D:         3lD         SR-56            e mu tau
    # E:         3lE         SR-70            SS + 1 tau
    # F:         3lF         SR-80            A: OSSF, F: e/mu + 1tau
    # I:         3lI         SR-96            3l + 1tau

regions = {
    'C':      ['3lC', 'SR-42', 'OSSF + 1tau'              ], 
    'D':      ['3lD', 'SR-56', 'e mu tau'                 ],
    'E':      ['3lE', 'SR-70', 'SS + 1 tau'               ],
    'F':      ['3lF', 'SR-80', 'A: OSSF, F: e/mu + 1tau'  ],
    'I':      ['4lI', 'SR-96', '3l + 1tau'                ],
    'CRTAUH': ['CRTAUH', 'CRTAUH', 'Control regions tauh' ],
    }

"""
"""

import optparse
# Command line options
usage = 'usage: %prog [--newData]'
parser = optparse.OptionParser(usage)
parser.add_option('-i', '--input',          dest='inputDir',       help='input directory',        default='/pool/ciencias/HeppyTrees/RA7/estructura/trees_8011_July5_allscans/',           type='string')
parser.add_option('-o', '--output',         dest='outputDir',      help='output directory',       default='~/www/susyRA7/',           type='string')
parser.add_option('-a', '--action',         dest='action',         help='which action to perform', default='crtau', type='string')
parser.add_option('-s', '--subaction',      dest='subaction',      help='which subAction to perform', default='', type='string')
parser.add_option('-w', '--workingpoint',   dest='workingpoint',   help='which working point to apply', default='', type='string')
parser.add_option('-p', '--pretend',        dest='pretend',        help='only print commands out', action='store_true')
parser.add_option('-m', '--mconly',         dest='mconly', action='store_true', help='use mc-only mca file')
parser.add_option('-u', '--user',           dest='user', help='in which user\'s dir put the plots by default', default = 'vischia', type='string')
parser.add_option('--pog',            dest='pog',    action='store_true', help='use POG IDs instead of leptonMVA ones')
 
(opt, args) = parser.parse_args()

inputDir     = opt.inputDir
outputDir    = opt.outputDir
action       = opt.action
subaction    = opt.subaction
workingpoint = opt.workingpoint
pretend      = opt.pretend
mconly       = opt.mconly
pog          = opt.pog

if 'mc' in action:
        mconly=True
        action=action.replace('mc','')

blind = '--flags "-X blinding"'

index="/nfs/fanae/user/%s/www/index.php"%opt.user

def runPlots(cuts, mca, out, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, toplot, weights, functions, enablecuts, header):

        clean(out)
        os.system('mkdir -p {out}'.format(out=out))
        os.system('cp {index} {outputDir}'.format(index=index,outputDir=out))
        # --Fs {inputDir}/leptonJetReCleanerSusyEWK3L --Fs {inputDir}/leptonBuilderEWK 
        daweights=''
        if weights != '':
                daweights=" -W '{weights}' ".format(weights=weights)
        cmd = "python mcPlots.py {mca} {cuts} {plots} -P {inputDir} --Fs {inputDir}/leptonJetReCleanerWZSM --Fs {inputDir}/leptonBuilderWZSM --FMCs {inputDir}/bTagEventWeightFullSimWZ30 --pdir {outputDir}  -j {jei} -l {lumi} --s2v --tree treeProducerSusyMultilepton --mcc {mcc} {mccother} --mcc {trigdef} -f {daweights} {pgroup} --legendWidth 0.18 --legendFontSize 0.026 --showMCError -f {toplot} --showRatio --perBin --legendHeader \'{header}\' --maxRatioRange 0.5 5.0 --fixRatioRange --print root,C,pdf,png,txt --ratioOffset 0.03 {functions} {enablecuts} --env oviedo ".format(mca=mca,cuts=cuts,plots=plots,inputDir=inputDir,outputDir=out,pgroup=pgroup,jei=jei,lumi=lumi,mcc=mcc,mccother=mccother,trigdef=trigdef,daweights=daweights,toplot=toplot,functions=functions,enablecuts=enablecuts,header=header)
        command(cmd, pretend)
        os.system('cp {index} {outputDir}'.format(index=index,outputDir=out))


def runCards(variable, binning, cuts, mca, out, plots, systs, inputDir, processes, signals, pgroup, outputDir, jei, lumi, mcc, mccother, trigdef, weights, functions, enablecuts):
        # example var: SSR4bins
        # example binning: '4,0.5,4.5'
        os.system('mkdir -p {out}'.format(out=out))
        daweights=''
        if weights != '':
                daweights=" -W '{weights}' ".format(weights=weights)
        daprocesses=''
        if processes != '':
                daprocesses=" -p data,{processes} ".format(processes=processes)

        cmd = "python makeShapeCardsSusy.py {mca} {cuts} {variable} '{binning}' {systs} -P {inputDir} --Fs {inputDir}/leptonBuilderEWK --Fs {inputDir}/leptonJetReCleanerSusyEWK2L -j {jei} -l {lumi} --s2v --tree treeProducerSusyMultilepton --mcc {mcc} --mcc {mccother} --mcc {trigdef} -f  {daweights} {functions} {daprocesses} {signals} {pgroup} --od {outputDir} --ms -o {variable} {enablecuts} ".format(mca=mca,cuts=cuts,variable=variable,binning=binning,systs=systs,inputDir=inputDir,daprocesses=daprocesses,signals=signals,pgroup=pgroup,jei=jei,lumi=lumi,mcc=mcc,mccother=mccother,trigdef=trigdef,daweights=daweights,functions=functions,outputDir=out,enablecuts=enablecuts)
        command(cmd, pretend)
        os.system('cp {index} {outputDir}'.format(index=index,outputDir=out))
        
######################################################################################

if(action=='srwz'):
        print 'Now plotting generic WZ SR plots'
        plots='wzsm/plots_wzsm.txt'
        mcc='wzsm/mcc_varsub_wzsm.txt'
        mccother=''
        trigdef='wzsm/mcc_triggerdefs.txt'
        wp='1'
        enablecuts=' '
        if(workingpoint=='VT'):
                wp='1'
        elif(workingpoint=='M'):
                wp='0'
        else:
                print("Defaulting to wp=1 (VTight)")
        if(wp=='1'):
                #os.system('rm wzsm/fakeRate-2lss-frdata.txt')
                #os.system('cp wzsm/fakeRate-2lss-frdata-wpVT.txt wzsm/fakeRate-2lss-frdata.txt')
                enablecuts=' -E SR ' 
                if pog: enablecuts=' -X MVAVT -E cutPOGT '
        else:
                #os.system('rm wzsm/fakeRate-2lss-frdata.txt')
                #os.system('cp wzsm/fakeRate-2lss-frdata-wpM.txt wzsm/fakeRate-2lss-frdata.txt')
                enablecuts=' -E SR ' if not pog else ' -X MVAVT -E cutPOGM -E SR '

        # 0 = medium, 1 = vtight
        # The first parameter, which getLepSF calls "isTight", is a way of deactivating the SF (it returns 1 if it is false). It is hence wrong to pass "isTight" as this parameter, because this implies that the SF is set to 1 for any non-VTight lepton. And by the way the default value of wp is zero, which means that passing only 1 as isTight implies applying the Medium SFs to the VTight WP. LoL
        weights=' puw_nInt_Moriond(nTrueInt)*bTagWeight ' if (mconly or pog) else ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,{wp})*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,{wp})*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,{wp})*bTagWeight '.format(wp=wp)
        #weights=' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,{wp})*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,{wp})*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,{wp})*bTagWeight '.format(wp=wp) if not mconly else ' puw_nInt_Moriond(nTrueInt)*bTagWeight ' 
        functions=' --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc --load-macro wzsm/functionsWZ.cc '
        toplot='--sP m3l,m3lmet,m3l_l,m3lmet_l,flavor,nBJet30,ptZ1,ptZ2,ptW,METflavour_logblind,MET_logblind,MET_logblind_20,lepJetDR_Z1,lepJetDR_Z2,lepJetDR_W,wzBalance_pt,wzBalance_conePt,wzBalance_pt2,wzBalance_conePt2,deltaR_wz,deltaR_wz_log ' 
        if(subaction!=''):
                toplot='--sP \'{toplot}\''.format(toplot=subaction)
        if(subaction=='all'):
                toplot=''
        batch=' -q batch '
        batch=''
        direct=' --pretend '
        direct=' '
        jei='6'
        jei='60'
        # https://hypernews.cern.ch/HyperNews/CMS/get/physics-announcements/4495.html
        lumi='35.867'
        pgroup=' --pgroup internal:=ttZ,Gstar,ZGi --pgroup external:=TTG,WG,ZG,TG,Gstare --pgroup incl_fakes_appldata+=incl_promptsub '
        pgroup=' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata --plotgroup fakes_appldata+=promptsub --neglist promptsub '
        pgroup=' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata --plotgroup fakes_appldata+=promptsub --neglist promptsub ' if not mconly else " -p data -p prompt_.* -p fakes_tt.* -p fakes_dy.* -p rares.*"
        #
        header='All'
        cuts='wzsm/cuts_wzsm.txt'
        mca= 'wzsm/mca_includes.txt' if not mconly else 'wzsm/mca_MC_includes.txt'
        out=''
        if(wp=='1'):
                out=outputDir+'wz{mc}{pog}/lepmvaVT/srwz/'.format(mc='' if not mconly else 'MC', pog='' if not pog else 'pog')
        elif(wp=='0'):
                out=outputDir+'wz{mc}{pog}/lepmvaM/srwz/'.format(mc='' if not mconly else 'MC', pog='' if not pog else 'pog' )
        else:
                out=outputDir+'wz{mc}{pog}/lepmvaVT/srwz/'.format(mc='' if not mconly else 'MC', pog='' if not pog else 'pog')
        runPlots(cuts, mca, out, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, toplot, weights, functions,enablecuts, header)

elif(action=='response'):
        print 'Now producing nominal response matrices for WZ production'
        print 'Starting from %s ' % inputDir
        plots='wzsm/plots_wzsm.txt'
        mcc='wzsm/mcc_varsub_wzsm.txt'
        mccother=''
        trigdef='wzsm/mcc_triggerdefs.txt'
        wp='1'
        enablecuts=' '
        if(workingpoint=='VT'):
                wp='1'
        elif(workingpoint=='M'):
                wp='0'
        else:
                print("Defaulting to wp=1 (VTight)")
        if(wp=='1'):
                #os.system('rm wzsm/fakeRate-2lss-frdata.txt')
                #os.system('cp wzsm/fakeRate-2lss-frdata-wpVT.txt wzsm/fakeRate-2lss-frdata.txt')
                enablecuts=' -E SR ' 
                if pog: enablecuts=' -X MVAVT -E cutPOGT '
        else:
                #os.system('rm wzsm/fakeRate-2lss-frdata.txt')
                #os.system('cp wzsm/fakeRate-2lss-frdata-wpM.txt wzsm/fakeRate-2lss-frdata.txt')
                enablecuts=' -E SR ' if not pog else ' -X MVAVT -E cutPOGM -E SR '

        # 0 = medium, 1 = vtight
        # The first parameter, which getLepSF calls "isTight", is a way of deactivating the SF (it returns 1 if it is false). It is hence wrong to pass "isTight" as this parameter, because this implies that the SF is set to 1 for any non-VTight lepton. And by the way the default value of wp is zero, which means that passing only 1 as isTight implies applying the Medium SFs to the VTight WP. LoL
        weights=' puw_nInt_Moriond(nTrueInt)*bTagWeight ' if (mconly or pog) else ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,{wp})*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,{wp})*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,{wp})*bTagWeight '.format(wp=wp)
        #weights=' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,{wp})*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,{wp})*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,{wp})*bTagWeight '.format(wp=wp) if not mconly else ' puw_nInt_Moriond(nTrueInt)*bTagWeight ' 
        functions=' --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc --load-macro wzsm/functionsWZ.cc '
        toplot='--sP nJet30_response,Z1pt_response,Z1conePt_response ' 
        # This is not up to the generic user
        #if(subaction!=''):
        #        toplot='--sP \'{toplot}\''.format(toplot=subaction)
        #if(subaction=='all'):
        #        toplot=''
        batch=' -q batch '
        batch=''
        direct=' --pretend '
        direct=' '
        jei='6'
        jei='60'
        # https://hypernews.cern.ch/HyperNews/CMS/get/physics-announcements/4495.html
        lumi='35.867'
        pgroup=' '
        #pgroup=' --pgroup internal:=ttZ,Gstar,ZGi --pgroup external:=TTG,WG,ZG,TG,Gstare --pgroup incl_fakes_appldata+=incl_promptsub '
        #pgroup=' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata --plotgroup fakes_appldata+=promptsub --neglist promptsub '
        #pgroup=' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata --plotgroup fakes_appldata+=promptsub --neglist promptsub ' if not mconly else " -p data -p prompt_.* -p fakes_tt.* -p fakes_dy.* -p rares.*"
        #
        header='All'
        cuts='wzsm/cuts_wzsm.txt'
        mca= 'wzsm/mca_unfolding.txt'
        out=''
        if(wp=='1'):
                out=outputDir+'wz{mc}{pog}/lepmvaVT/response/'.format(mc='' if not mconly else 'MC', pog='' if not pog else 'pog')
        elif(wp=='0'):
                out=outputDir+'wz{mc}{pog}/lepmvaM/response/'.format(mc='' if not mconly else 'MC', pog='' if not pog else 'pog' )
        else:
                out=outputDir+'wz{mc}{pog}/lepmvaVT/response/'.format(mc='' if not mconly else 'MC', pog='' if not pog else 'pog')
        runPlots(cuts, mca, out, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, toplot, weights, functions,enablecuts, header)

elif(action=='ttcr'):
        print 'Now plotting WZ CR plots'
        plots='wzsm/plots_wzsm.txt'
        mcc='wzsm/mcc_varsub_wzsm.txt'
        #mccother='--mcc wzsm/lepchoice-crwz-FO.txt'
        mccother=' '
        enablecuts=' -E TTCR '
        if(workingpoint=='VT'):
                wp='1'
        elif(workingpoint=='M'):
                wp='0'
        else:
                print("Defaulting to wp=1 (VTight)")
        if(wp=='1'):
                #os.system('rm wzsm/fakeRate-2lss-frdata.txt')
                #os.system('cp wzsm/fakeRate-2lss-frdata-wpVT.txt wzsm/fakeRate-2lss-frdata.txt')
                enablecuts=' -E TTCR ' # it is already enabled by default
                if pog: enablecuts=' -E TTCR -X MVAVT -E cutPOGT '
        else:
                #os.system('cp wzsm/fakeRate-2lss-frdata-wpM.txt wzsm/fakeRate-2lss-frdata.txt')
                enablecuts=' -E TTCR -E MVAM -X MVAVT ' if not pog else ' -E TTCR -X MVAVT -E cutPOGM '

        trigdef='wzsm/mcc_triggerdefs.txt'
        weights=' puw_nInt_Moriond(nTrueInt)*bTagWeight ' if (mconly or pog) else ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,{wp})*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,{wp})*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,{wp})*bTagWeight '.format(wp=wp)
        #weights=' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1)*bTagWeight ' if not mconly else ' puw_nInt_Moriond(nTrueInt)*bTagWeight ' 
        functions=' --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc --load-macro wzsm/functionsWZ.cc '
        toplot='--sP mll_3l, mll, m3l,m3lmet,m3l_l,m3lmet_l,flavor,nBJet30,ptZ1,ptZ2,ptW,METflavour_logblind,MET_logblind,MET_logblind_20,lepJetDR_Z1,lepJetDR_Z2,lepJetDR_W,wzBalance_pt,wzBalance_conePt,wzBalance_pt2,wzBalance_conePt2,deltaR_wz,deltaR_wz_log '
        if(subaction!=''):
                toplot='--sP \'{toplot}\''.format(toplot=subaction)
        if(subaction=='all'):
                toplot=''
        batch=' -q batch '
        batch=''
        direct=' --pretend '
        direct=' '
        jei='6'
        jei='60'
        # https://hypernews.cern.ch/HyperNews/CMS/get/physics-announcements/4495.html
        lumi='35.867'
        pgroup=' --pgroup internal:=ttZ,Gstar,ZGi --pgroup external:=TTG,WG,ZG,TG,Gstare --pgroup incl_fakes_appldata+=incl_promptsub '
        pgroup=' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata --plotgroup fakes_appldata+=promptsub --neglist promptsub '
        pgroup=' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata --plotgroup fakes_appldata+=promptsub --neglist promptsub ' if not mconly else " -p data -p prompt_.* -p fakes_tt.* -p fakes_dy.* -p rares.*"
        #
        header='All'
        #cuts='wzsm/cuts_crwz.txt'
        cuts='wzsm/cuts_wzsm.txt'
        mca= 'wzsm/mca_includes.txt' if not mconly else 'wzsm/mca_MC_includes.txt'
        out=''
        if(wp=='1'):
                out=outputDir+'wz{mc}{pog}/lepmvaVT/ttcr/'.format(mc='' if not mconly else 'MC', pog='' if not pog else 'pog')
        elif(wp=='0'):
                out=outputDir+'wz{mc}{pog}/lepmvaM/ttcr/'.format(mc='' if not mconly else 'MC', pog='' if not pog else 'pog')
        else:
                out=outputDir+'wz{mc}{pog}/lepmvaVT/ttcr/'.format(mc='' if not mconly else 'MC', pog='' if not pog else 'pog')
        runPlots(cuts, mca, out, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, toplot, weights, functions,enablecuts, header)

elif(action=='test'):
        print 'Now plotting generic DY plots'
        plots='wzsm/plots_wzsm.txt'
        mcc='wzsm/mcc_varsub_wzsm.txt'
        mccother=''
        trigdef='wzsm/mcc_triggerdefs.txt'
        wp='1'
        enablecuts=' '
        if(workingpoint=='VT'):
                wp='1'
        elif(workingpoint=='M'):
                wp='0'
        else:
                print("Defaulting to wp=1 (VTight)")
        if(wp=='1'):
                #os.system('rm wzsm/fakeRate-2lss-frdata.txt')
                #os.system('cp wzsm/fakeRate-2lss-frdata-wpVT.txt wzsm/fakeRate-2lss-frdata.txt')
                enablecuts=' -E test -X MVAVT -X ptWZ -X lowMll -X hasOSSF -X threelightlep'
                enablecuts=' '
        else:
                #os.system('rm wzsm/fakeRate-2lss-frdata.txt')
                #os.system('cp wzsm/fakeRate-2lss-frdata-wpM.txt wzsm/fakeRate-2lss-frdata.txt')
                enablecuts=' -E test -X MVAVT -X ptWZ -X lowMll -X hasOSSF '
                enablecuts=' '

        # 0 = medium, 1 = vtight
        # The first parameter, which getLepSF calls "isTight", is a way of deactivating the SF (it returns 1 if it is false). It is hence wrong to pass "isTight" as this parameter, because this implies that the SF is set to 1 for any non-VTight lepton. And by the way the default value of wp is zero, which means that passing only 1 as isTight implies applying the Medium SFs to the VTight WP. LoL
        weights=' puw_nInt_Moriond(nTrueInt)*bTagWeight ' if (mconly or pog) else ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,{wp})*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,{wp})*bTagWeight '.format(wp=wp)
        #weights=' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,{wp})*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,{wp})*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,{wp})*bTagWeight '.format(wp=wp) if not mconly else ' puw_nInt_Moriond(nTrueInt)*bTagWeight ' 
        functions=' --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc --load-macro wzsm/functionsWZ.cc '
        toplot='--sP m3l,m3lmet,m3l_l,m3lmet_l,flavor,nBJet30,ptZ1,ptZ2,ptW,METflavour_logblind,MET_logblind,MET_logblind_20,lepJetDR_Z1,lepJetDR_Z2,lepJetDR_W,wzBalance_pt,wzBalance_conePt,wzBalance_pt2,wzBalance_conePt2,deltaR_wz,deltaR_wz_log ' 
        if(subaction!=''):
                toplot='--sP \'{toplot}\''.format(toplot=subaction)
        if(subaction=='all'):
                toplot=''
        toplot='--sP \'MET_logblind\''
        batch=' -q batch '
        batch=''
        direct=' --pretend '
        direct=' '
        jei='6'
        jei='40'
        # https://hypernews.cern.ch/HyperNews/CMS/get/physics-announcements/4495.html
        lumi='35.867'
        pgroup=' --pgroup internal:=ttZ,Gstar,ZGi --pgroup external:=TTG,WG,ZG,TG,Gstare --pgroup incl_fakes_appldata+=incl_promptsub '
        pgroup=' -p data -p prompt.* -p convs.* -p rares.* -p fakes_appldata --plotgroup fakes_appldata+=promptsub --neglist promptsub '
        pgroup=' -p data -p prompt.* -p convs.* -p rares.* -p fakes_appldata --plotgroup fakes_appldata+=promptsub --neglist promptsub ' if not mconly else " -p data -p prompt.* -p fakes_tt.* -p fakes_dy.* -p rares.*"
        #
        header='All'
        cuts='wzsm/cuts_test.txt'
        mca= 'wzsm/mca_test.txt' if not mconly else 'wzsm/mca_MC_includes.txt'
        out=''
        if(wp=='1'):
                out=outputDir+'wz{mc}{pog}/lepmvaVT/srwz/'.format(mc='' if not mconly else 'MC', pog='' if not pog else 'pog')
        elif(wp=='0'):
                out=outputDir+'wz{mc}{pog}/lepmvaM/srwz/'.format(mc='' if not mconly else 'MC', pog='' if not pog else 'pog' )
        else:
                out=outputDir+'wz{mc}{pog}/lepmvaVT/srwz/'.format(mc='' if not mconly else 'MC', pog='' if not pog else 'pog')
        runPlots(cuts, mca, out, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, toplot, weights, functions,enablecuts, header)


elif(action=='dycr'):
        print 'Now plotting DY CR plots'
        plots='wzsm/plots_wzsm.txt'
        mcc='wzsm/mcc_varsub_wzsm.txt'
        mccother='--mcc wzsm/lepchoice-crwz-FO.txt'
        #mccother=' '
        enablecuts=' -E DYCR '
        if(workingpoint=='VT'):
                wp='1'
        elif(workingpoint=='M'):
                wp='0'
        else:
                print("Defaulting to wp=1 (VTight)")
        if(wp=='1'):
                #os.system('rm wzsm/fakeRate-2lss-frdata.txt')
                #os.system('cp wzsm/fakeRate-2lss-frdata-wpVT.txt wzsm/fakeRate-2lss-frdata.txt')
                enablecuts=' -E DYCR -X met30 ' # it is already enabled by default
                if pog: enablecuts=' -E DYCR -X met30 -X MVAVT -E cutPOGT '
        else:
                #os.system('rm wzsm/fakeRate-2lss-frdata.txt')
                #os.system('cp wzsm/fakeRate-2lss-frdata-wpM.txt wzsm/fakeRate-2lss-frdata.txt')
                enablecuts=' -E DYCRM -E MVAM -X MVAVT ' if not pog else ' -E DYCR -X MVAVT -E cutPOGM '

        trigdef='wzsm/mcc_triggerdefs.txt'
        weights=' puw_nInt_Moriond(nTrueInt)*bTagWeight ' if (mconly or pog) else ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,{wp})*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,{wp})*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,{wp})*bTagWeight '.format(wp=wp)
        #weights=' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1)*bTagWeight ' if not mconly else ' puw_nInt_Moriond(nTrueInt)*bTagWeight ' 
        #weights=' puw_nInt_Moriond(nTrueInt)*bTagWeight '
        functions=' --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc --load-macro wzsm/functionsWZ.cc '
        toplot='--sP m3l,m3lmet,m3l_l,m3lmet_l,flavor,nBJet30,ptZ1,ptZ2,ptW,METflavour_logblind,MET_logblind,MET_logblind_20,lepJetDR_Z1,lepJetDR_Z2,lepJetDR_W,wzBalance_pt,wzBalance_conePt,wzBalance_pt2,wzBalance_conePt2,deltaR_wz,deltaR_wz_log '
        if(subaction!=''):
                toplot='--sP \'{toplot}\''.format(toplot=subaction)
        if(subaction=='all'):
                toplot=''
        batch=' -q batch '
        batch=''
        direct=' --pretend '
        direct=' '
        jei='6'
        jei='60'
        # https://hypernews.cern.ch/HyperNews/CMS/get/physics-announcements/4495.html
        lumi='35.867'
        #pgroup=' --pgroup internal:=ttZ,Gstar,ZGi --pgroup external:=TTG,WG,ZG,TG,Gstare --pgroup incl_fakes_appldata+=incl_promptsub '
        pgroup=' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata --plotgroup fakes_appldata+=promptsub --neglist promptsub ' if not mconly else " -p data -p prompt_.* -p fakes_tt.* -p fakes_dy.* -p rares.*"
        #pgroup=' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata --plotgroup fakes_appldata+=promptsub --neglist promptsub ' if not mconly else " "
        #
        header='All'
        #cuts='wzsm/cuts_crwz.txt'
        cuts='wzsm/cuts_wzsm.txt'
        mca= 'wzsm/mca_includes.txt' if not mconly else 'wzsm/mca_MC_includes.txt'
        out=''
        if(wp=='1'):
                out=outputDir+'wz{mc}{pog}/lepmvaVT/dycr/'.format(mc='' if not mconly else 'MC', pog='' if not pog else 'pog')
        elif(wp=='0'):
                out=outputDir+'wz{mc}{pog}/lepmvaM/dycr/'.format(mc='' if not mconly else 'MC', pog='' if not pog else 'pog')
        else:
                out=outputDir+'wz{mc}{pog}/lepmvaVT/dycr/'.format(mc='' if not mconly else 'MC', pog='' if not pog else 'pog')
        runPlots(cuts, mca, out, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, toplot, weights, functions,enablecuts, header)

elif(action=='zzcr'):
        print 'Now plotting ZZ CR plots'
        plots='wzsm/plots_wzsm.txt'
        mcc='wzsm/mcc_varsub_wzsm.txt'
        mccother='--mcc wzsm/lepchoice-crwz-FO.txt'
        #mccother=' '
        enablecuts=' -E ZZCR '
        if(workingpoint=='VT'):
                wp='1'
        elif(workingpoint=='M'):
                wp='0'
        else:
                print("Defaulting to wp=1 (VTight)")
        if(wp=='1'):
                #os.system('rm wzsm/fakeRate-2lss-frdata.txt')
                #os.system('cp wzsm/fakeRate-2lss-frdata-wpVT.txt wzsm/fakeRate-2lss-frdata.txt')
                enablecuts=' -E ZZCR ' # it is already enabled by default
                if pog: enablecuts=' -E ZZCR -X MVAVT -E cutPOGT '
        else:
                #os.system('rm wzsm/fakeRate-2lss-frdata.txt')
                #os.system('cp wzsm/fakeRate-2lss-frdata-wpM.txt wzsm/fakeRate-2lss-frdata.txt')
                enablecuts=' -E ZZCR -E MVAM -X MVAVT ' if not pog else ' -E ZZCR -X MVAVT -E cutPOGM '

        trigdef='wzsm/mcc_triggerdefs.txt'
        weights=' puw_nInt_Moriond(nTrueInt)*bTagWeight ' if (mconly or pog) else ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,{wp})*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,{wp})*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,{wp})*getLepSF(LepSel4_conePt,LepSel4_eta,LepSel4_pdgId,1,{wp})*bTagWeight '.format(wp=wp)
        #weights=' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1)*bTagWeight ' if not mconly else ' puw_nInt_Moriond(nTrueInt)*bTagWeight ' 
        #weights=' puw_nInt_Moriond(nTrueInt)*bTagWeight '
        functions=' --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc --load-macro wzsm/functionsWZ.cc '
        toplot='--sP m3l,m3lmet,m3l_l,m3lmet_l,flavor,nBJet30,ptZ1,ptZ2,ptW,METflavour_logblind,MET_logblind,MET_logblind_20,lepJetDR_Z1,lepJetDR_Z2,lepJetDR_W,wzBalance_pt,wzBalance_conePt,wzBalance_pt2,wzBalance_conePt2,deltaR_wz,deltaR_wz_log '
        if(subaction!=''):
                toplot='--sP \'{toplot}\''.format(toplot=subaction)
        if(subaction=='all'):
                toplot=''
        batch=' -q batch '
        batch=''
        direct=' --pretend '
        direct=' '
        jei='6'
        jei='60'
        # https://hypernews.cern.ch/HyperNews/CMS/get/physics-announcements/4495.html
        lumi='35.867'
        #pgroup=' --pgroup internal:=ttZ,Gstar,ZGi --pgroup external:=TTG,WG,ZG,TG,Gstare --pgroup incl_fakes_appldata+=incl_promptsub '
        pgroup=' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata --plotgroup fakes_appldata+=promptsub --neglist promptsub ' if not mconly else " -p data -p prompt_.* -p fakes_tt.* -p fakes_dy.* -p rares.*"
        #pgroup=' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata --plotgroup fakes_appldata+=promptsub --neglist promptsub ' if not mconly else " "
        #
        header='All'
        #cuts='wzsm/cuts_crwz.txt'
        cuts='wzsm/cuts_wzsm.txt'
        mca= 'wzsm/mca_includes.txt' if not mconly else 'wzsm/mca_MC_includes.txt'
        out=''
        if(wp=='1'):
                out=outputDir+'wz{mc}{pog}/lepmvaVT/zzcr/'.format(mc='' if not mconly else 'MC', pog='' if not pog else 'pog')
        elif(wp=='0'):
                out=outputDir+'wz{mc}{pog}/lepmvaM/zzcr/'.format(mc='' if not mconly else 'MC', pog='' if not pog else 'pog')
        else:
                out=outputDir+'wz{mc}{pog}/lepmvaVT/zzcr/'.format(mc='' if not mconly else 'MC', pog='' if not pog else 'pog')
        runPlots(cuts, mca, out, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, toplot, weights, functions,enablecuts, header)


elif(action=='convcr'):
        print 'Now plotting conv CR plots'
        plots='wzsm/plots_wzsm.txt'
        mcc='wzsm/mcc_varsub_wzsm.txt'
        mccother='--mcc wzsm/lepchoice-crwz-FO.txt'
        #mccother=' '
        enablecuts=' -E convCR '
        if(workingpoint=='VT'):
                wp='1'
        elif(workingpoint=='M'):
                wp='0'
        else:
                print("Defaulting to wp=1 (VTight)")
        if(wp=='1'):
                #os.system('rm wzsm/fakeRate-2lss-frdata.txt')
                #os.system('cp wzsm/fakeRate-2lss-frdata-wpVT.txt wzsm/fakeRate-2lss-frdata.txt')
                enablecuts=' -E convCR ' # it is already enabled by default
                if pog: enablecuts=' -E convCR -X MVAVT -E cutPOGT '
        else:
                #os.system('rm wzsm/fakeRate-2lss-frdata.txt')
                #os.system('cp wzsm/fakeRate-2lss-frdata-wpM.txt wzsm/fakeRate-2lss-frdata.txt')
                enablecuts=' -E convCR -E MVAM -X MVAVT ' if not pog else ' -E convCR -X MVAVT -E cutPOGM '

        trigdef='wzsm/mcc_triggerdefs.txt'
        weights=' puw_nInt_Moriond(nTrueInt)*bTagWeight ' if (mconly or pog) else ' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,{wp})*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,{wp})*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,{wp})*bTagWeight '.format(wp=wp)
        #weights=' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1)*bTagWeight ' if not mconly else ' puw_nInt_Moriond(nTrueInt)*bTagWeight ' 
        #weights=' puw_nInt_Moriond(nTrueInt)*bTagWeight '
        functions=' --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc --load-macro wzsm/functionsWZ.cc '
        toplot='--sP m3l,m3lmet,m3l_l,m3lmet_l,flavor,nBJet30,ptZ1,ptZ2,ptW,METflavour_logblind,MET_logblind,MET_logblind_20,lepJetDR_Z1,lepJetDR_Z2,lepJetDR_W,wzBalance_pt,wzBalance_conePt,wzBalance_pt2,wzBalance_conePt2,deltaR_wz,deltaR_wz_log '
        if(subaction!=''):
                toplot='--sP \'{toplot}\''.format(toplot=subaction)
        if(subaction=='all'):
                toplot=''
        batch=' -q batch '
        batch=''
        direct=' --pretend '
        direct=' '
        jei='6'
        jei='60'
        # https://hypernews.cern.ch/HyperNews/CMS/get/physics-announcements/4495.html
        lumi='35.867'
        #pgroup=' --pgroup internal:=ttZ,Gstar,ZGi --pgroup external:=TTG,WG,ZG,TG,Gstare --pgroup incl_fakes_appldata+=incl_promptsub '
        pgroup=' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata --plotgroup fakes_appldata+=promptsub --neglist promptsub ' if not mconly else " -p data -p prompt_.* -p fakes_tt.* -p fakes_dy.* -p rares.*"
        #pgroup=' -p data -p prompt_.* -p convs.* -p rares.* -p fakes_appldata --plotgroup fakes_appldata+=promptsub --neglist promptsub ' if not mconly else " "
        #
        header='All'
        #cuts='wzsm/cuts_crwz.txt'
        cuts='wzsm/cuts_wzsm.txt'
        mca= 'wzsm/mca_includes.txt' if not mconly else 'wzsm/mca_MC_includes.txt'
        out=''
        if(wp=='1'):
                out=outputDir+'wz{mc}{pog}/lepmvaVT/convcr/'.format(mc='' if not mconly else 'MC', pog='' if not pog else 'pog')
        elif(wp=='0'):
                out=outputDir+'wz{mc}{pog}/lepmvaM/convcr/'.format(mc='' if not mconly else 'MC', pog='' if not pog else 'pog')
        else:
                out=outputDir+'wz{mc}{pog}/lepmvaVT/convcr/'.format(mc='' if not mconly else 'MC', pog='' if not pog else 'pog')
        runPlots(cuts, mca, out, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, toplot, weights, functions,enablecuts, header)


elif(action=='www'):
        print 'Now plotting generic plots'
        plots='wzsm/plots_wzsm.txt'
        mcc='wzsm/mcc_varsub_wzsm.txt'
        mccother=''
        trigdef='wzsm/mcc_triggerdefs.txt'
        weights=' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1)*bTagWeight '
        functions=' --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc --load-macro wzsm/functionsWZ.cc '
        toplot='--sP m3l,m3lmet,m3l_l,m3lmet_l '
        if(subaction!=''):
                toplot='--sP \'{toplot}\''.format(toplot=subaction)
        if(subaction=='all'):
                toplot=''
        batch=' -q batch '
        batch=''
        direct=' --pretend '
        direct=' '
        jei='6'
        jei='60'
        # https://hypernews.cern.ch/HyperNews/CMS/get/physics-announcements/4495.html
        lumi='35.867'
        enablecuts=' '
        pgroup=' --pgroup internal:=ttZ,Gstar,ZGi --pgroup external:=TTG,WG,ZG,TG,Gstare --pgroup incl_fakes_appldata+=incl_promptsub '
        pgroup=' -p data -p prompt_.* -p rares.* -p fakes_appldata --plotgroup fakes_appldata+=promptsub --neglist promptsub '
        #
        header='All'
        cuts='wzsm/cuts_wwwsm.txt'
        mca= 'wzsm/mca_includes.txt' if not mconly else 'wzsm/mca_MC_includes.txt'
        out=outputDir+'www/'
        runPlots(cuts, mca, out, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, toplot, weights, functions,enablecuts, header)
        

elif(action=="trigTests"):
        print "Now getting 2D histograms for the trigger efficiency tests... Please be patient"
        if subaction=='':
          doWhat = ["1El", "1Mu", "MuMu", "ElEl", "ElMu"]
        else:
          doWhat = [subaction]
        
        plots = 'wzsm/plots_eff.txt'
        mca = 'wzsm/includes/mca_trigTestData.txt' #Run over prompt DY leptons + JetHT + MET datasets
        cuts = 'wzsm/cuts_triggerStudies.txt'
        pgroup = ' -p data -p dy '
        out = outputDir+'wz{mc}{pog}/triggers/'
        mcc='wzsm/mcc_varsub_wzsm.txt'
        mccother=''
        trigdef='wzsm/mcc_triggerdefs.txt'
        toplot = ''
        weights=' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1) '
        functions=' --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc --load-macro wzsm/functionsWZ.cc '       
        jei='64'

        lumi='35.867'
        for channel in doWhat:
          tmpout = out + channel
          enablecuts = ' '
          if "1" in channel:
            enablecuts += "-E oneTight "
            if "El" in channel:
              enablecuts += "-E firstEl "
            elif "Mu" in channeL:
              enablecuts += "-E firstMu "

          else:
            enablecuts += "-E twoTight "
            if "El" in channel and "Mu" in channel:
              enablecuts += "-E ElMu "
            elif "El" in channel:
              enablecuts += "-E firstEl -E secondEl "
            elif "Mu" in channeL:
              enablecuts += "-E firstMu -E secondMu "
          print "Channel: " + channel
          runPlots(cuts, mca, tmpout, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, toplot, weights, functions,enablecuts, '')

elif(action=="AC"):
        print "Now getting 1D histograms for the anomalous couplings tests... Please be patient"
        
        plots = 'wzsm/plots_wzsm.txt'
        mca = 'wzsm/includes/includes/mca_AC.txt' #Run over prompt DY leptons + JetHT + MET datasets
        cuts = 'wzsm/cuts_wzsm.txt'
        pgroup = ' '
        out = outputDir+'wz{mc}{pog}/AC/'
        mcc='wzsm/mcc_varsub_wzsm.txt'
        mccother=''
        trigdef='wzsm/mcc_triggerdefs.txt'
        toplot = ''
        weights=' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1)*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1)*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1) '
        functions=' --load-macro wzsm/functionsPUW.cc --load-macro wzsm/functionsSF.cc --load-macro wzsm/functionsWZ.cc '       
        jei='64'

        lumi='35.867'
        #SR
        enablecuts = " -E SR "
        runPlots(cuts, mca, tmpout, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, toplot, weights, functions,enablecuts, '')
        #theEnablers = [" -E TTCR ", " -E DYCR ", " -E ttXCR ",  " -E ZZCR ",  " -E convCR "]
        #for E in theEnablers:
        #         runPlots(cuts, mca, tmpout, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, toplot, weights, functions,E, '')

print 'Everything is done now'
