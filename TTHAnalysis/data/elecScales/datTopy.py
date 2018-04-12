datFile = open(args[0],"r")
pyFile  = open(args[1],"w")

if "Data" in datFile:
  isData = True
else:
  isData = False

def getCat(aeta, pt, r9):
  #Inline categorization with nested ifs
  r9Cat  = 0 + 1*(r9 >= 0.94) 
  etaCat = 1 + 1*(eta > 1) + 1*(eta > 1.4442) + 1*(eta > 1.566) + 1*(eta > 2.)       
  ptCat  = 0 if etaCat >= 3 else ( 1 + (pt > 20) + (pt > 33) + (pt > 39) + (pt > 45) + (pt > 50) + (pt > 58) + (pt > 100) if r9Cat == 0 else ( 1 + (pt > 20) + (pt > 35) + (pt > 43) + (pt > 50) + (pt > 55) + (pt > 100) if (r9Cat == 1 and etaCat == 1) else ( 1 + (pt > 20) + (pt > 40) + (pt > 50) + (pt > 100)))
  totalCat = 100*etaCat + 10*ptCat + r9Cat
  return totalCat

catCentralUnc = {}

for line in datFile.readlines():
  words = line.split(" ")
  items = []
  for it in words:
    if len(it) >= 0:
      items.append(it)
  if not(len(items) == 9):
    print "Entry with no 9 items!!"
    break
  
