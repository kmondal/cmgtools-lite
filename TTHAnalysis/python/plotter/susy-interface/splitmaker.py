import datetime, sys, os
from optparse import OptionParser
from lib import maker
from lib import functions as func

parser = OptionParser(usage="%prog cfg regions treedir outdir [options]")
parser = maker.addMakerOptions(parser)
parser.add_option("--exclude", dest="exclude", type="string", action="append", default=[], help="Sample names to exclude")
parser.add_option("--accept" , dest="accept" , type="string", action="append", default=[], help="Sample names to accept")
parser.add_option("--tmpdir" , dest="tmpdir" , type="string", default=None, help="Temporary output directory") 
parser.add_option("--gen"    , dest="gen"    , action="store_true", default=False, help="Use GenPart collection for splitting")
parser.add_option("--pdgId1" , dest="pdgId1" , type="int", default=None, help="PdgId of particle 1 when using --gen")
parser.add_option("--pdgId2" , dest="pdgId2" , type="int", default=None, help="PdgId of particle 2 when using --gen")
parser.add_option("--minmass", dest="minmass", type="int", default=100 , help="Minimum mass of particle 1 (for parallel splitting)")
parser.add_option("--maxmass", dest="maxmass", type="int", default=1200, help="Maximum mass of particle 1 (for parallel splitting)")
parser.add_option("--step"   , dest="step"   , type="int", default=None, help="Mass step of particle 1 (for parallel splitting)")
parser.add_option("--dm"     , dest="deltam" , type="int", default=None, help="Mass difference between particle 1 and 2 (for parallel splitting)") 

base = "python splitSMSTrees.py {O} {T} {GEN} {TMP} --tree {TREENAME} {MASS} {LSP} {FLAGS}"
(options, args) = parser.parse_args()
options = maker.splitLists(options)
mm      = maker.Maker("splitmaker", base, args, options, parser.defaults)

tmp = "--tmpdir "+options.tmpdir if options.tmpdir else ""
gen = "--gen" if options.gen else ""
if options.gen:
	gen += " --pdgId1 %d"%options.pdgId1 if options.pdgId1 else ""
	gen += " --pdgId2 %d"%options.pdgId2 if options.pdgId2 else ""

flags   = " ".join(mm.options.flags) ## we do not want to have all flags, only the additional ones given here


## loop over all directories in the input dir
for d in os.listdir(mm.treedir):


	## only consider real samples
	if not os.path.isdir(mm.treedir +"/"+ d): continue
	if not os.path.exists(mm.treedir +"/"+ d +"/"+mm.getVariable("treename","treeProducerSusyMultilepton")+"/tree.root") and \
       not os.path.exists(mm.treedir +"/"+ d +"/"+mm.getVariable("treename","treeProducerSusyMultilepton")+"/tree.root.url"): continue

	if options.accept  != [] and all([d.find(a) == -1 for a in options.accept ]): continue
	if options.exclude != [] and any([d.find(e) >  -1 for e in options.exclude]): continue

	dset = mm.treedir +"/"+ d

	## split tree per mass (parallel splitting)
	if options.minmass and options.maxmass and options.step:
	
		masses = [options.minmass + i*options.step for i in range((options.maxmass - options.minmass)/options.step+1)]
		for mass in masses:
			lsp = "--lsp "+str(mass-options.deltam) if options.deltam else ""
			mm.submit([mm.outdir, dset, gen, tmp, mm.getVariable("treename","treeProducerSusyMultilepton"), "--mass "+str(mass), lsp, flags],str(mass)+"_"+d,False)
		mm.runJobs()
		mm.clearJobs()
	
	## only one splitting job
	else:
		mm.submit([mm.outdir, dset, gen, tmp, mm.getVariable("treename","treeProducerSusyMultilepton"), "", "", flags], d)


