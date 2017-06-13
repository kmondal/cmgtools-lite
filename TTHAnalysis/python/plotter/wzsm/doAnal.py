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

(opt, args) = parser.parse_args()

inputDir     = opt.inputDir
outputDir    = opt.outputDir
action       = opt.action
subaction    = opt.subaction
workingpoint = opt.workingpoint
pretend      = opt.pretend
blind = '--flags "-X blinding"'

index="/nfs/fanae/user/vischia/www/index.php"

def runPlots(cuts, mca, out, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, toplot, weights, functions, enablecuts, header):

        clean(out)
        os.system('mkdir -p {out}'.format(out=out))
        os.system('cp {index} {outputDir}'.format(index=index,outputDir=out))
        # --Fs {inputDir}/leptonJetReCleanerSusyEWK3L --Fs {inputDir}/leptonBuilderEWK 
        daweights=''
        if weights != '':
                daweights=" -W '{weights}' ".format(weights=weights)
        cmd = "python mcPlots.py {mca} {cuts} {plots} -P {inputDir} --Fs {inputDir}/leptonJetReCleanerWZSM --Fs {inputDir}/leptonBuilderWZSM --FMCs {inputDir}/bTagEventWeightFullSimWZ30 --pdir {outputDir}  -j {jei} -l {lumi} --s2v --tree treeProducerSusyMultilepton --mcc {mcc} {mccother} --mcc {trigdef} -f {daweights} {pgroup} --plotgroup fakes_appldata+=promptsub  --legendWidth 0.18 --legendFontSize 0.026 --showMCError -f {toplot} --showRatio --perBin --legendHeader \'{header}\' --maxRatioRange 0.5 2.0 --fixRatioRange --print C,pdf,png,txt --ratioOffset 0.03 {functions} {enablecuts} --env oviedo ".format(mca=mca,cuts=cuts,plots=plots,inputDir=inputDir,outputDir=out,pgroup=pgroup,jei=jei,lumi=lumi,mcc=mcc,mccother=mccother,trigdef=trigdef,daweights=daweights,toplot=toplot,functions=functions,enablecuts=enablecuts,header=header)
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
                os.system('rm wzsm/fakeRate-2lss-frdata.txt')
                os.system('cp wzsm/fakeRate-2lss-frdata-wpVT.txt wzsm/fakeRate-2lss-frdata.txt')
                # enablecuts=' -E MVAVT ' # it is already enabled by default
        else:
                os.system('rm wzsm/fakeRate-2lss-frdata.txt')
                os.system('cp wzsm/fakeRate-2lss-frdata-wpM.txt wzsm/fakeRate-2lss-frdata.txt')
                enablecuts=' -E MVAM -X MVAVT '

        # 0 = medium, 1 = vtight
        # The first parameter, which getLepSF calls "isTight", is a way of deactivating the SF (it returns 1 if it is false). It is hence wrong to pass "isTight" as this parameter, because this implies that the SF is set to 1 for any non-VTight lepton. And by the way the default value of wp is zero, which means that passing only 1 as isTight implies applying the Medium SFs to the VTight WP. LoL
        weights=' puw_nInt_Moriond(nTrueInt)*getLepSF(LepSel1_conePt,LepSel1_eta,LepSel1_pdgId,1,{wp})*getLepSF(LepSel2_conePt,LepSel2_eta,LepSel2_pdgId,1,{wp})*getLepSF(LepSel3_conePt,LepSel3_eta,LepSel3_pdgId,1,{wp})*bTagWeight '.format(wp=wp)
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
        jei='40'
        # https://hypernews.cern.ch/HyperNews/CMS/get/physics-announcements/4495.html
        lumi='35.867'
        pgroup=' --pgroup internal:=ttZ,Gstar,ZGi --pgroup external:=TTG,WG,ZG,TG,Gstare --pgroup incl_fakes_appldata+=incl_promptsub '
        pgroup=' -p data -p prompt.* -p rares.* -p fakes_appldata --plotgroup fakes_appldata+=promptsub --neglist promptsub '
        #
        header='All'
        cuts='wzsm/cuts_wzsm.txt'
        mca='wzsm/mca_includes.txt'
        out=''
        if(wp=='1'):
                out=outputDir+'wz/lepmvaVT/srwz/'
        elif(wp=='0'):
                out=outputDir+'wz/lepmvaM/srwz/'
        else:
                out=outputDir+'wz/lepmvaVT/srwz/'
        runPlots(cuts, mca, out, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, toplot, weights, functions,enablecuts, header)

elif(action=='crwz'):
        print 'Now plotting WZ CR plots'
        plots='wzsm/plots_wzsm.txt'
        mcc='wzsm/mcc_varsub_wzsm.txt'
        #mccother='--mcc wzsm/lepchoice-crwz-FO.txt'
        mccother=' '
        enablecuts=' -E TTCR -X bveto'
        if(workingpoint=='VT'):
                wp='1'
        elif(workingpoint=='M'):
                wp='0'
        else:
                print("Defaulting to wp=1 (VTight)")
        if(wp=='1'):
                os.system('rm wzsm/fakeRate-2lss-frdata.txt')
                os.system('cp wzsm/fakeRate-2lss-frdata-wpVT.txt wzsm/fakeRate-2lss-frdata.txt')
                # enablecuts=' -E TTCR -X bveto -E MVAVT ' # it is already enabled by default
        else:
                os.system('rm wzsm/fakeRate-2lss-frdata.txt')
                os.system('cp wzsm/fakeRate-2lss-frdata-wpM.txt wzsm/fakeRate-2lss-frdata.txt')
                enablecuts=' -E TTCR -X bveto -E MVAM -X MVAVT '

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
        jei='40'
        # https://hypernews.cern.ch/HyperNews/CMS/get/physics-announcements/4495.html
        lumi='35.867'
        pgroup=' --pgroup internal:=ttZ,Gstar,ZGi --pgroup external:=TTG,WG,ZG,TG,Gstare --pgroup incl_fakes_appldata+=incl_promptsub '
        pgroup=' -p data -p prompt.* -p rares.* -p fakes_appldata --plotgroup fakes_appldata+=promptsub --neglist promptsub '
        #
        header='All'
        #cuts='wzsm/cuts_crwz.txt'
        cuts='wzsm/cuts_wzsm.txt'
        mca='wzsm/mca_includes.txt'
        out=''
        if(wp=='1'):
                out=outputDir+'wz/lepmvaVT/crwz/'
        elif(wp=='0'):
                out=outputDir+'wz/lepmvaM/crwz/'
        else:
                out=outputDir+'wz/lepmvaVT/crwz/'
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
        jei='40'
        # https://hypernews.cern.ch/HyperNews/CMS/get/physics-announcements/4495.html
        lumi='35.867'
        enablecuts=' '
        pgroup=' --pgroup internal:=ttZ,Gstar,ZGi --pgroup external:=TTG,WG,ZG,TG,Gstare --pgroup incl_fakes_appldata+=incl_promptsub '
        pgroup=' -p data -p prompt.* -p rares.* -p fakes_appldata --plotgroup fakes_appldata+=promptsub --neglist promptsub '
        #
        header='All'
        cuts='wzsm/cuts_wwwsm.txt'
        mca='wzsm/mca_includes.txt'
        out=outputDir+'www/'
        runPlots(cuts, mca, out, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, toplot, weights, functions,enablecuts, header)
        

print 'Everything is done now'
