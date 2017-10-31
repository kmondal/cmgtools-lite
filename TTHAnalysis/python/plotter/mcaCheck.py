import os, sys
from optparse import OptionParser

parser = OptionParser(usage="%prog mca.txt treeDir [options]")
parser.add_option("--tree", dest="treename", default="treeProducerSusyMultilepton", help="Name of the tree producer");
(options, args) = parser.parse_args()

if len(args)<2:
	print "Format: python mcaCheck.py <mca file> <tree directory> [--treename <nameOfTree>]"
	sys.exit()

def findDatasets(sample, mcaSamples):
	return [e[1] for e in mcaSamples if e[0] == sample]

def compareLists(list1, list2, mcaSamples):
	result = []
	for entry in list1:
		if not entry in list2:
			result.append((entry, findDatasets(entry, mcaSamples)))
	return result

def getDoubleCounts(set, mcaSamples):
	result = []
	list   = [e[0] for e in mcaSamples]
	for entry in set:
		if list.count(entry)>1: 
			result.append((entry, findDatasets(entry, mcaSamples)))
	return result

mcapath = args[0]
treedir = args[1].rstrip("/")+"/"
print "Collecting list of samples..."

## reading samples from MCA
mcasamples = []
for line in [l.rstrip("\n").strip() for l in open(mcapath, "r").readlines()]:
	if len(line)==0 or line[0:1]=="#": continue
	if line.count(";") < 1: continue
	sl = line.split(";")
	if sl[0].count(":") < 1: continue
	ssl = sl[0].split(":")
	for sname in ssl[1].split("+"):
		mcasamples.append((sname.strip(), ssl[0].strip()))

## reading samples from input directory
dirsamples = []
for d in os.listdir(treedir):
	path = treedir+d
	if not os.path.isdir(path): continue
	if not os.path.isdir(path+"/"+options.treename): continue
	if not os.path.exists(path+"/"+options.treename+"/tree.root") and \
	   not os.path.exists(path+"/"+options.treename+"/tree.root.url"): continue
	dirsamples.append(d)

## getting list of samples in MCA but not in input directory
mcaset    = list(set([e[0] for e in mcasamples]))
inMcaOnly = sorted(compareLists   (mcaset    , dirsamples, mcasamples))
inDirOnly = sorted(compareLists   (dirsamples, mcaset    , mcasamples))
doubles   = sorted(getDoubleCounts(mcaset    , mcasamples))

if len(inMcaOnly)>0:
	print ""
	print "Following samples are only in the MCA but not in the tree directory:"
	print "\n".join([e[0]+" ("+", ".join(e[1])+")" for e in inMcaOnly])
if len(inDirOnly)>0:
	print ""
	print "Following samples are only in the tree directory but not in the MCA:"
	print "\n".join([e[0]+" ("+", ".join(e[1])+")" for e in inDirOnly])
if len(doubles)>0:
	print ""
	print "Following samples are present more than once in the MCA:"
	print "\n".join([e[0]+" ("+", ".join(e[1])+")" for e in doubles])
if len(inMcaOnly)==0 and len(inDirOnly)==0 and len(doubles)==0:
	print ""
	print "MCA is OK"






