import sys, os
import ROOT

# this script can be used to count how many entries in a list of tree or friend tree files satisfy a certain requirement
# (useful to look for event numbers)

for dd in os.listdir(sys.argv[2]):
	d = sys.argv[2].rstrip("/")+"/"+dd
	if not os.path.isdir(d): continue
	if not os.path.isdir(d + "/treeProducerSusyMultilepton"): continue
	path = None
	if os.path.exists(d + "/treeProducerSusyMultilepton/tree.root"):
		path = d + "/treeProducerSusyMultilepton/tree.root"
	elif os.path.exists(d + "/treeProducerSusyMultilepton/tree.root.url"):
		path = open(d + "/treeProducerSusyMultilepton/tree.root.url").readlines()[0].rstrip("\n")
	else:
		continue
	f = ROOT.TFile.Open(path)
	t = f.Get("tree")
	if not t: t = f.Get("sf/t")
	if not t: continue
	n = t.GetEntries(sys.argv[1])
	if n>0: print n,'entries in',dd
	f.Close()
