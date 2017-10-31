import os, datetime, subprocess

T="/mnt/t3nfs01/data01/shome/cheidegg/o/2017-02-25_ewkskims80X_M17_3l_bkg;/mnt/t3nfs01/data01/shome/cheidegg/o/2017-02-23_ewkskims80X_M17_3l_data"
O="/afs/cern.ch/user/c/cheidegg/www/heppy/2017-02-26_ewk80X_reminiAODNewMCSSR" # Do NOT give a trailing /
L=35.9

## below is the most crucial part: the base command for plotting
## give the usual command by which you would plot a, say, SR plot with mcPlots
## even better: give the susy-interface command that you would use
## the command you use needs to contain
## - {OUTDIR} replacing the path of the output directory
## - {PLOTS} replacing the path of the plots file
## - select the plot 'SSR' (i.e. '--sP SSR' or via susy-interface: --selPlots SSR)
## - {FLAGS} a placeholder where to insert a flag if necessary
base = "python susy-interface/plotmaker.py 3l 3lA '"+T+"' {OUTDIR} --plot {PLOTS} -l "+str(L)+" --make data --selPlots SSR -o SSR --flags '--perBin -X blinding --perBin --ratioOffset 0.03 --print C,png,pdf,txt --plotgroup rares_ttX+=rares_ttW --plotgroup rares_ttX+=rares_ttZ --plotgroup fakes_appldata+=promptsub {FLAGS} --neglist promptsub --showMCError' --noFlags"

## give bins expression (min, max) for what is to be used IN THE FINAL PLOT!
bins  = [1,8]

## give expressions to draw, or file paths to access
exprs = [
         "plots_2lss.root",
         "plots_2lss.root", 
         "SuperSig3L1(countTaus(3, LepSel_pdgId[0], LepSel_pdgId[1], LepSel_pdgId[2]), srMt, met_pt)",
         "SuperSig3L2(countTaus(3, LepSel_pdgId[0], LepSel_pdgId[1], LepSel_pdgId[2]), met_pt)",
         "SuperSig3L3(countTaus(3, LepSel_pdgId[0], LepSel_pdgId[1], LepSel_pdgId[2]), mT2L_3l, met_pt)",
         "SuperSig3L4(countTaus(3, LepSel_pdgId[0], LepSel_pdgId[1], LepSel_pdgId[2]), mT2T_3l, met_pt)",
         "SuperSig3L5(countTaus(3, LepSel_pdgId[0], LepSel_pdgId[1], LepSel_pdgId[2]), met_pt)",
         "SuperSig4L1(met_pt)"
         ]


### below is the lists giving the expressions to plot and the bins by which to vary them
### syntax: exprs = [firstExpr, secondExpr, ...]
###         varys = [[startFirstExpr, endFirstExpr], [startSecondExpr, endSecondExpr], ...]
#exprs = ["SuperSig(3,countTaus(3, LepSel_pdgId[0], LepSel_pdgId[1], LepSel_pdgId[2]                 ), nOSSF_3l, nOSLF_3l, mT2L_3l, mT2T_3l, srMll(3, mll_3l, mllL_3l, mllT_3l), srMt(3, mT_3l, mTL_3l, mTT_3l), met_pt)", 
#        "SuperSig(4,countTaus(4, LepSel_pdgId[0], LepSel_pdgId[1], LepSel_pdgId[2], LepSel_pdgId[3]), nOSSF_4l, nOSLF_4l, mT2L_4l, mT2T_4l, srMll(4, mll_4l, mllL_4l, mllT_4l), srMt(4, mT_4l, mTL_4l, mTT_4l), met_pt)"] 
#varys = [[1,5], [6,6]]


## ---------------- do variation stuff below ------------------

## define functions

def bash(cmd):
	pipe = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	back = pipe.stdout.read().rstrip("\n").strip()
	return back

def mkdir(path, clean=False):
	path = path.rstrip("/")
	if os.path.isdir(path): 
		os.system("rm -rf "+path+"/*")
		return
	os.system("mkdir -p "+path)

def unwrap(exprs, varys):
	unwrapped = []
	for v, vary in enumerate(varys):
		bins = unwrapBins(vary)
		for b in bins:
			unwrapped.append((b, exprs[v]))
	return unwrapped
	
def unwrapBins(bins):
	full = []
	for i in range(bins[0], bins[1]+1):
		full.append(i)
	return full


## prepare plots file
timestamp = datetime.datetime.now().strftime("%y%m%d%H%M%S%f")
mkdir("tmp",True)
remember = []

## run the plots
for i,expr in enumerate(exprs):

	bin = i+1
	mkdir("tmp/draw",True)

	if os.path.exists(expr):
		if not expr in remember: remember.append(expr)
		continue

	plotsfile = "tmp/"+timestamp+"_"+str(i)+".txt"
	outfile   = "tmp/"+timestamp+"_"+str(i)+".root"

	fp = open(plotsfile, "w")
	fp.write("SSR : if3("+expr+","+str(bin)+",0) : "+str(bins[1]-bins[0]+1)+","+str(bins[0])+","+str(bins[1]+1)+" ; YTitle='Events', XTitle='Super Signal Region', Legend='TL', IncludeOverflows=False, LegendCutoff=1e-5, RMin=0, RMax=3, Logy, YMin=0.1, YMax=5000\n")
	#fp.write("SSR : if3("+expr+","+str(bin)+",0) : "+str(bins[1]-bins[0]+1)+","+str(bins[0]-0.5)+","+str(bins[1]+0.5)+" ; YTitle='Events', XTitle='Super Signal Region', Legend='TL', IncludeOverflows=False, LegendCutoff=1e-5, RMin=0, RMax=3, Logy, YMin=0.1, YMax=5000\n")
	fp.close()

	flags = " ".join(["--add-histos "+f for f in remember])
	if len(remember)>0: remember = [] # only load them once
	if i > 0: 
		flags += " --add-histos tmp/"+timestamp+"_"+str(i-1)+".root"
	theCmd = base.format(OUTDIR="tmp/draw", PLOTS=plotsfile, FLAGS=flags)
	os.system(theCmd)

	if i+1 == len(exprs):
		mkdir(O)
		os.system("mv tmp/draw/* "+O)
		os.system("cp /afs/cern.ch/user/g/gpetrucc/php/index.php "+O)
	else:
		theFile = bash("find tmp/draw -print | grep -i '.*[.]root'")
		print "mv "+theFile+" "+outfile
		os.system("mv "+theFile+" "+outfile)



## deprecated


#fullExprs = unwrap(exprs, varys)
#for i,(bin,expr) in enumerate(fullExprs):
