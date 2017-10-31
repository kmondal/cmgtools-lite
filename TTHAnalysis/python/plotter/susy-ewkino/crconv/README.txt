# Once produced cards, go to a combine release (7_4_7 at the moment), and convert the cards using the physics model uploaded to the HiggsAnalysis/CombinedLimit git repository (SusyConversions.py)

Command lines (preliminary tests):


#Convert to workspace
text2workspace.py -P HiggsAnalysis.CombinedLimit.SusyConversions:susyConversions --PO verbose --PO modes=internal,external m3l.card.txt

# Run (yet to be compared with algo=singles, etc). Convergence issues, must fit across all CRs simultaneously.
combine -M MultiDimFit m3l.card.root  --algo=cross --cl=0.68 
