from tauUtils import command as command
from tauUtils import clean
from tauUtils import os
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
parser.add_option('-p', '--pretend',        dest='pretend',        help='only print commands out', action='store_true')

(opt, args) = parser.parse_args()

inputDir  = opt.inputDir
outputDir = opt.outputDir
action    = opt.action
subaction = opt.subaction
pretend   = opt.pretend
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
        cmd = "python mcPlots.py {mca} {cuts} {plots} -P {inputDir} --Fs {inputDir}/leptonBuilderEWK --Fs {inputDir}/leptonJetReCleanerSusyEWK2L --pdir {outputDir} {pgroup} -j {jei} -l {lumi} --s2v --tree treeProducerSusyMultilepton --mcc {mcc} --mcc {mccother} --mcc {trigdef} -f {daweights} --plotgroup fakes_appldata+=promptsub  --legendWidth 0.20 --legendFontSize 0.035 --showMCError -f {toplot} --showRatio --perBin --legendHeader \'{header}\' --maxRatioRange 0.5 1.5 --fixRatioRange --ratioOffset 0.03 {functions} {enablecuts} ".format(mca=mca,cuts=cuts,plots=plots,inputDir=inputDir,outputDir=out,pgroup=pgroup,jei=jei,lumi=lumi,mcc=mcc,mccother=mccother,trigdef=trigdef,daweights=daweights,toplot=toplot,functions=functions,enablecuts=enablecuts,header=header)
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

if(action=='generalplots'):
        cmd = 'print susy-interface/plotmaker.py 3l 3lA {inputDir} {outputDir} -l 12.9 --make data --plots br -o SR {blind} --pretend'.format(inputDir=inputDir,outputDir=outputDir,blind=blind)
        command(cmd, pretend)

elif(action=='tauopt'):
        mca='susy-ewkino/crtau/mca_taus.txt'
        for region in regions:
                if subaction and (region != subaction):
                        continue
                cmd = 'python susy-interface/plotmaker.py 3l {region} {inputDir} {outputDir} --mca {mca} -l 12.9 --make data --plots br -o {sr} {blind} -q batch '.format(region=regions[region][0],inputDir=inputDir,outputDir=outputDir,mca=mca,blind=blind,sr=regions[region][1])
                command(cmd,pretend)

elif(action=='crtauNotWorkingBecauseOfPeopleSBadCommitPolicies'):
        print 'Now plotting CRs for estimating tau fakes'
        mca='susy-ewkino/crtau/mca_taus.txt'
        #mca='susy-ewkino/3l/mca_ewkino.txt'
        cuts='susy-ewkino/crtau/cuts_qcd.txt'
        config='taustudies'
        config='taus'
        region='CRTAUH'
        batch=' -q batch '
        batch=''
        direct=' --pretend '
        direct=' '
        out=outputDir+'qcd/'
        cmd = 'python susy-interface/plotmaker.py {config} {region} {inputDir} {outputDir} --mca {mca} --cuts {cuts} -l 12.9 --make data -o {sr} {blind} {batch} {pretend}'.format(config=config,region=regions[region][0],inputDir=inputDir,outputDir=out,mca=mca,cuts=cuts,blind=blind,sr=regions[region][1],batch=batch,pretend=direct)
        print cmd
        command(cmd, pretend)
        
        cuts='susy-ewkino/crtau/cuts_ttbar.txt'
        out=outputDir+'ttbar/'
        cmd = 'python susy-interface/plotmaker.py {config} {region} {inputDir} {outputDir} --mca {mca} --cuts {cuts} -l 12.9 --make data  -o {sr} {blind} {batch} {pretend}'.format(config=config,region=regions[region][0],inputDir=inputDir,outputDir=out,mca=mca,cuts=cuts,blind=blind,sr=regions[region][1],batch=batch,pretend=direct)
        print cmd
        command(cmd, pretend)

        cuts='susy-ewkino/crtau/cuts_wjet.txt'
        out=outputDir+'wjet/'
        cmd = 'python susy-interface/plotmaker.py {config} {region} {inputDir} {outputDir} --mca {mca} --cuts {cuts} -l 12.9 --make data  -o {sr} {blind} {batch} {pretend}'.format(config=config,region=regions[region][0],inputDir=inputDir,outputDir=out,mca=mca,cuts=cuts,blind=blind,sr=regions[region][1],batch=batch,pretend=direct)
        print cmd
        command(cmd, pretend)

elif(action=='crtau'):
        print 'Now plotting CRs for estimating tau fakes'
        mca='susy-ewkino/crtau/mca_taus.txt'
        #mca='susy-ewkino/crwz/mca_crwz_forScan_12p9.txt'
        plots='susy-ewkino/crtau/plots_taus.txt'
        mcc='susy-ewkino/3l/mcc_ewkino.txt'
        #mcc='susy-ewkino/crwz/lepchoice-crwz-FO.txt'
        trigdef='susy-ewkino/mcc_triggerdefs.txt'
        functions='susy-ewkino/3l/functionsEWK.cc'
        toplot='--sP \'MET\''
        if(subaction!=''):
                toplot='--sP \'{toplot}\''.format(toplot=subaction)
        if(subaction=='all'):
                toplot=''
        config='taustudies'
        config='taus'
        region='CRTAUH'
        batch=' -q batch '
        batch=''
        direct=' --pretend '
        direct=' '
        jei='8'
        lumi='1.0'

        cuts='susy-ewkino/crtau/cuts_qcd.txt'
        #cuts='susy-ewkino/crwz/cuts_crwz.txt'
        out=outputDir+'qcd/'
        clean(out)
        # When I will plot signal region, reimplement the {blind} part
        cmd = "python mcPlots.py {mca} {cuts} {plots} -P {inputDir} --Fs {inputDir}/leptonJetReCleanerSusyEWK2L --Fs {inputDir}/leptonBuilderEWK --pdir {outputDir} -j {jei} -l {lumi} --s2v --tree treeProducerSusyMultilepton --mcc {mcc} --mcc {trigdef} -f  --plotgroup fakes_appldata+=promptsub  --legendWidth 0.20 --legendFontSize 0.035 --showMCError -f {toplot} --showRatio --perBin --legendHeader \'EWK #tau_{{h}} CR\' --maxRatioRange 0.5 1.5 --fixRatioRange --ratioOffset 0.03  --load-macro {functions}".format(mca=mca,cuts=cuts,plots=plots,inputDir=inputDir,outputDir=out,jei=jei,lumi=lumi,mcc=mcc,trigdef=trigdef,toplot=toplot,functions=functions)
        #print cmd
        command(cmd, pretend)
        os.system('cp {index} {outputDir}'.format(index=index,outputDir=out))

        cuts='susy-ewkino/crtau/cuts_ttbar.txt'
        out=outputDir+'ttbar/'
        clean(out)
        # When I will plot signal region, reimplement the {blind} part
        cmd = "python mcPlots.py {mca} {cuts} {plots} -P {inputDir} --Fs {inputDir}/leptonJetReCleanerSusyEWK2L --Fs {inputDir}/leptonBuilderEWK --pdir {outputDir} -j {jei} -l {lumi} --s2v --tree treeProducerSusyMultilepton --mcc {mcc} --mcc {trigdef} -f  --plotgroup fakes_appldata+=promptsub  --legendWidth 0.20 --legendFontSize 0.035 --showMCError -f {toplot} --showRatio --perBin --legendHeader \'EWK #tau_{{h}} CR\' --maxRatioRange 0.5 1.5 --fixRatioRange --ratioOffset 0.03  --load-macro {functions}".format(mca=mca,cuts=cuts,plots=plots,inputDir=inputDir,outputDir=out,jei=jei,lumi=lumi,mcc=mcc,trigdef=trigdef,toplot=toplot,functions=functions)
        #print cmd
        command(cmd, pretend)
        #os.system('cp {index} {outputDir}'.format(index=index,outputDir=out))

        cuts='susy-ewkino/crtau/cuts_wjet.txt'
        out=outputDir+'wjet/'
        clean(out)
        # When I will plot signal region, reimplement the {blind} part
        cmd = "python mcPlots.py {mca} {cuts} {plots} -P {inputDir} --Fs {inputDir}/leptonJetReCleanerSusyEWK2L --Fs {inputDir}/leptonBuilderEWK --pdir {outputDir} -j {jei} -l {lumi} --s2v --tree treeProducerSusyMultilepton --mcc {mcc} --mcc {trigdef} -f  --plotgroup fakes_appldata+=promptsub  --legendWidth 0.20 --legendFontSize 0.035 --showMCError -f {toplot} --showRatio --perBin --legendHeader \'EWK #tau_{{h}} CR\' --maxRatioRange 0.5 1.5 --fixRatioRange --ratioOffset 0.03  --load-macro {functions}".format(mca=mca,cuts=cuts,plots=plots,inputDir=inputDir,outputDir=out,jei=jei,lumi=lumi,mcc=mcc,trigdef=trigdef,toplot=toplot,functions=functions)
        #print cmd
        command(cmd, pretend)
        os.system('cp {index} {outputDir}'.format(index=index,outputDir=out))

elif(action=='crconv'):
        print 'Now plotting CRs for estimating fakes from conversions'
        plots='susy-ewkino/crconv/plots_convs.txt'
        mcc='susy-ewkino/crconv/mcc_convs.txt'
        mccother='susy-ewkino/2lss/lepchoice-2lss-FO.txt'
        trigdef='susy-ewkino/mcc_triggerdefs.txt'
        print "WARNING: Please re-add eventBTagSF to applied weights, when new recipe is out"
        #weights3l='puw_nInt_Moriond(nTrueInt)*triggerSF(0,LepGood1_conePt,LepGood1_pdgId,LepGood2_conePt,LepGood2_pdgId,LepGood3_conePt,LepGood3_pdgId)*leptonSF_2lss_ewk(LepGood1_pdgId,LepGood1_conePt,LepGood1_eta)*leptonSF_2lss_ewk(LepGood2_pdgId,LepGood2_conePt,LepGood2_eta)*eventBTagSF'
        #wp='0'
        wp='1'
        weights3l='puw_nInt_Moriond(nTrueInt)*getLepSF(LepGood1_conePt,LepGood1_eta,LepGood1_pdgId,{wp},0)*getLepSF(LepGood2_conePt,LepGood2_eta,LepGood2_pdgId,{wp},0)*getLepSF(LepGood3_conePt,LepGood3_eta,LepGood3_pdgId,{wp},0)'.format(wp=wp)
        #weights2l='puw_nInt_Moriond(nTrueInt)*triggerSF(-1,LepGood1_conePt,LepGood1_pdgId,LepGood2_conePt,LepGood2_pdgId,0,0)*leptonSF_2lss_ewk(LepGood1_pdgId,LepGood1_conePt,LepGood1_eta)*leptonSF_2lss_ewk(LepGood2_pdgId,LepGood2_conePt,LepGood2_eta)*eventBTagSF'
        wp='1'
        weights2l='puw_nInt_Moriond(nTrueInt)*getLepSF(LepGood1_conePt,LepGood1_eta,LepGood1_pdgId,{wp},0)*getLepSF(LepGood2_conePt,LepGood2_eta,LepGood2_pdgId,{wp},0)'.format(wp=wp)
        #functions='--load-macro susy-ewkino/3l/functionsEWK.cc --load-macro susy-ewkino/functionsPUW.cc --load-macro susy-ewkino/functionsSF.cc --load-macro functions.cc '
        functions=' --load-macro susy-ewkino/functionsPUW.cc --load-macro susy-ewkino/functionsSF.cc --load-macro functions.cc '
        toplot='--sP \'m3l\''
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
        #
        header=''

        cuts='susy-ewkino/crconv/cuts_convs_3l.txt'
        mca='susy-ewkino/crconv/mca-3l-mc-conv.txt'
        out=outputDir+'3l_mc_conv/'
        #runPlots(cuts, mca, out, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, toplot, weights3l, functions,enablecuts)
        
        cuts='susy-ewkino/crconv/cuts_convs_3l.txt'
        mca='susy-ewkino/crconv/mca-3l-mcdata-conv.txt'
        
        # Inclusive
        out=outputDir+'3l_mcdata_conv/'
        header='Inclusive'
        #toplot=' --sP \'m3l\' --sP \'flavor3l\' --sP \'lep1_istight\' --sP \'lep1_pt\' --sP \'lep2_istight\' --sP \'lep2_pt\' --sP \'lep3_istight\' --sP \'lep3_pt\' --sP \'lep4_istight\' --sP \'lep4_pt\' '
        toplot=' --sP \'m3l\' --sP \'flavor3l\' --sP \'el_matchStuff\' --sP \'mu_matchStuff\' '
        # 
        if(subaction=='all'):
                toplot=''
        runPlots(cuts, mca, out, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, toplot, weights3l, functions, enablecuts, header)
        toplot='--sP \'m3l\''
        if(subaction=='all'):
                toplot=' '
        # eee
        out=outputDir+'3l_mcdata_conv/eee/'
        enablecuts=' --enable-cut=eee '
        header='#it{eee}'
        runPlots(cuts, mca, out, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, toplot, weights3l, functions, enablecuts, header)
        
        # mmm
        out=outputDir+'3l_mcdata_conv/mmm/'
        enablecuts=' --enable-cut=mmm '
        header='#mu#mu#mu'
        runPlots(cuts, mca, out, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, toplot, weights3l, functions, enablecuts, header)
        
        # eem
        out=outputDir+'3l_mcdata_conv/eem/'
        enablecuts=' --enable-cut=eem '
        header='#it{e}#it{e}#mu'
        runPlots(cuts, mca, out, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, toplot, weights3l, functions, enablecuts, header)
        
        # mme
        out=outputDir+'3l_mcdata_conv/mme/'
        enablecuts=' --enable-cut=mme '
        header='#mu#mu#it{e}'
        runPlots(cuts, mca, out, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, toplot, weights3l, functions, enablecuts, header)


        #enablecuts=' '
        #twoltoplot='{toplot} --sP m3l '.format(toplot=toplot)
        #
        #cuts='susy-ewkino/crconv/cuts_convs_2lgamma.txt'
        #mca='susy-ewkino/crconv/mca-ss2l-mcdata-conv.txt'
        #out=outputDir+'ss2lgamma_mcdata_conv/'
        #header='2l#gamma'
        #runPlots(cuts, mca, out, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, twoltoplot, weights2l, functions, enablecuts, header)
        #
        #cuts='susy-ewkino/crconv/cuts_convs_ss2l.txt'
        #mca='susy-ewkino/crconv/mca-ss2l-mcdata-conv.txt'
        #out=outputDir+'ss2l_mcdata_conv/'
        #header='ss2l'
        #runPlots(cuts, mca, out, plots, inputDir, outputDir, pgroup, jei, lumi, mcc, mccother, trigdef, twoltoplot, weights2l, functions, enablecuts, header)


elif(action=='crconvcards'):
        print 'Now trying to build datacards'
        plots='susy-ewkino/crconv/plots_convs.txt'
        mcc='susy-ewkino/crconv/mcc_convs.txt'
        mccother='susy-ewkino/2lss/lepchoice-2lss-FO.txt'
        trigdef='susy-ewkino/mcc_triggerdefs.txt'
        print "WARNING: Please re-add eventBTagSF to applied weights, when new recipe is out"
        #wp='0'
        wp='1'
        weights3l='puw_nInt_Moriond(nTrueInt)*getLepSF(LepGood1_conePt,LepGood1_eta,LepGood1_pdgId,{wp},0)*getLepSF(LepGood2_conePt,LepGood2_eta,LepGood2_pdgId,{wp},0)*getLepSF(LepGood3_conePt,LepGood3_eta,LepGood3_pdgId,{wp},0)'.format(wp=wp)
        #weights2l='puw_nInt_Moriond(nTrueInt)*triggerSF(-1,LepGood1_conePt,LepGood1_pdgId,LepGood2_conePt,LepGood2_pdgId,0,0)*leptonSF_2lss_ewk(LepGood1_pdgId,LepGood1_conePt,LepGood1_eta)*leptonSF_2lss_ewk(LepGood2_pdgId,LepGood2_conePt,LepGood2_eta)*eventBTagSF'
        wp='1'
        weights2l='puw_nInt_Moriond(nTrueInt)*getLepSF(LepGood1_conePt,LepGood1_eta,LepGood1_pdgId,{wp},0)*getLepSF(LepGood2_conePt,LepGood2_eta,LepGood2_pdgId,{wp},0)'.format(wp=wp)
        functions=' --load-macro susy-ewkino/functionsPUW.cc --load-macro susy-ewkino/functionsSF.cc --load-macro functions.cc '
        systs='susy-ewkino/crconv/systs_conv.txt'
        variable='met'
        binning='10,50,300'
        if(subaction!=''):
                variable='{toplot}'.format(toplot=subaction)
        if(subaction=='all'):
                variable=''
        batch=' -q batch '
        batch=''
        direct=' --pretend '
        direct=' '
        jei='6'
        jei='60'
        # https://hypernews.cern.ch/HyperNews/CMS/get/physics-announcements/4495.html
        lumi='35.867'
        pgroup=' --pgroup internal:=ttZ,Gstar,ZGi --pgroup external:=TTG,WG,ZG,TG,Gstare --pgroup incl_fakes_appldata+=incl_promptsub '
        signals=' --sp internal --sp external '
        enablecuts=' '

        # Overwrite var, for now
        variable='m3l'
        binning='40,0,200'

        cuts='susy-ewkino/crconv/cuts_convs_3l.txt'
        mca='susy-ewkino/crconv/mca-3l-mcdata-conv.txt'
        out=outputDir+'datacards/3l_mcdata_conv/inclusive/'
        processes='WZ,Fakes,Rares,ttZ,Gstar,TTG,WG,ZG'
        processes=''
        
        # Inclusive
        enablecuts=''
        runCards(variable, binning, cuts, mca, out, plots, systs, inputDir, processes, signals, pgroup, outputDir, jei, lumi, mcc, mccother, trigdef, weights3l, functions, enablecuts)

        # eee
        out=outputDir+'datacards/3l_mcdata_conv/eee/'
        enablecuts=' --enable-cut=eee '
        runCards(variable, binning, cuts, mca, out, plots, systs, inputDir, processes, signals, pgroup, outputDir, jei, lumi, mcc, mccother, trigdef, weights3l, functions, enablecuts)

        # mmm
        out=outputDir+'datacards/3l_mcdata_conv/mmm/'
        enablecuts=' --enable-cut=mmm '
        runCards(variable, binning, cuts, mca, out, plots, systs, inputDir, processes, signals, pgroup, outputDir, jei, lumi, mcc, mccother, trigdef, weights3l, functions, enablecuts)

        # eem
        out=outputDir+'datacards/3l_mcdata_conv/eem/'
        enablecuts=' --enable-cut=eem '
        runCards(variable, binning, cuts, mca, out, plots, systs, inputDir, processes, signals, pgroup, outputDir, jei, lumi, mcc, mccother, trigdef, weights3l, functions, enablecuts)

        # mme
        out=outputDir+'datacards/3l_mcdata_conv/mme/'
        enablecuts=' --enable-cut=mme '
        runCards(variable, binning, cuts, mca, out, plots, systs, inputDir, processes, signals, pgroup, outputDir, jei, lumi, mcc, mccother, trigdef, weights3l, functions, enablecuts)

        
        enablecuts=''
        variable='mll'
        binning='40,0,400'        
        cuts='susy-ewkino/crconv/cuts_convs_2lgamma.txt'
        mca='susy-ewkino/crconv/mca-ss2l-mcdata-conv.txt'
        out=outputDir+'datacards/ss2lgamma_mcdata_conv/'
        processes='Gstar,TG,TTG,ttZ,WG,ZG,WZ,Fakes,Rares,Flips'
        processes=''
        #runCards(variable, binning, cuts, mca, out, plots, systs, inputDir, processes, signals, pgroup, outputDir, jei, lumi, mcc, mccother, trigdef, weights2l, functions, enablecuts)

        cuts='susy-ewkino/crconv/cuts_convs_ss2l.txt'
        mca='susy-ewkino/crconv/mca-ss2l-mcdata-conv.txt'
        out=outputDir+'datacards/ss2l_mcdata_conv/'
        processes='Gstar,TG,TTG,ttZ,WG,ZG,WZ,Fakes,Rares,Flips,TTG'
        processes=''
        #runCards(variable, binning, cuts, mca, out, plots, systs, inputDir, processes, signals, pgroup, outputDir, jei, lumi, mcc, mccother, trigdef, weights2l, functions, enablecuts)

print 'Everything is done now'
