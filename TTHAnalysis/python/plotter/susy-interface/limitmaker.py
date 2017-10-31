import os
from optparse import OptionParser
from lib import maker
from lib import functions as func

parser = OptionParser(usage="%prog cfg regions treedir outdir [options]")
parser = maker.addMakerOptions(parser)
parser.add_option("--perBin"  ,  dest="perBin"  , action="store_true", default=False, help="Run every value of the bin separately.")
parser.add_option("--finalize",  dest="finalize", action="store_true", default=False, help="After running, tidy up output directory like scanmaker")

base = "python makeShapeCardsSusy.py {MCA} {CUTS} \"{EXPR}\" \"{BINS}\" {SYS} -o SR {T} --tree {TREENAME} {MCCS} {MACROS} --neg --s2v -f -l {LUMI} --od {O} {FRIENDS} {PROCS} {FLAGS}"
(options, args) = parser.parse_args()
options = maker.splitLists(options)
mm      = maker.Maker("limitmaker", base, args, options, parser.defaults)

friends = mm.collectFriends()	
sl      = mm.getVariable("lumi","12.9").replace(".","p")
outDirs = []

for r in range(len(mm.regions)):
	mm.iterateRegion()

	mccs     = mm.collectMCCs  ()
	macros   = mm.collectMacros()	
	flags    = mm.collectFlags (["flagsLimits"])
	scenario = mm.getScenario(True)

	procs    = " ".join(["-p "+b for b in mm.getProcs()])
	binnings = [mm.getVariable("bins","")] if not options.perBin else func.getAllBins(mm.getVariable("bins",""))
	
	for ib,b in enumerate(binnings):
	
		if options.perBin: 
			scenario += "_"+b.replace(".","p")
			mm.useVar("bins", b)
	
		output = mm.outdir +"/limit/"+ scenario +"/"+ sl +"fb"
		func.mkdir(output)
		outDirs.append(output)
	
		flags += " "+mm.getExprCut()
		
		mm.submit([mm.getVariable("mcafile",""), mm.getVariable("cutfile",""), mm.getVariable("expr",""), mm.getVariable("bins",""), mm.getVariable("sysfile",""), mm.treedirs, mm.getVariable("treename","treeProducerSusyMultilepton"), mccs, macros, mm.getVariable("lumi","12.9"), output, friends, procs, flags], mm.region.name, False)

mm.runJobs()
mm.clearJobs()

if options.finalize:
	for output in outDirs:
		for d in os.listdir(output):
			path = output +"/"+d
			if d in ["index.php", "common"]: continue
			if not os.path.exists(path+"/SR.card.txt"): continue
			hasSig = d[0:4]=="sig_"
			new    = d if not hasSig else d.lstrip("sig_")
			model  = "_".join(d.split("_")[:-2]).lstrip("sig_")
			mp     = "_".join(d.split("_")[-2:])
			if not os.path.isdir(output+"/"+model): os.system("mkdir -p "+output+"/"+model+"/mps")
			os.system("mkdir -p "+output+"/"+model+"/mps/"+mp+"/common")
			os.system("mv "+path+" "+output+"/"+model+"/mps/"+mp+"/sig_"+new)
			os.system("cp "+output+"/common/SR.input.root "+output+"/"+model+"/mps/"+mp+"/common")
	

