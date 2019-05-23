from random import shuffle

def TurnOnType(tarray, tstr):
    if tstr == "Normal":
        tarray[0] = 1
    elif tstr == "Fighting":
        tarray[1] = 1
    elif tstr == "Flying":
        tarray[2] = 1
    elif tstr == "Poison":
        tarray[3] = 1
    elif tstr == "Ground":
        tarray[4] = 1
    elif tstr == "Rock":
        tarray[5] = 1
    elif tstr == "Bug":
        tarray[6] = 1
    elif tstr == "Ghost":
        tarray[7] = 1
    elif tstr == "Steel":
        tarray[8] = 1
    elif tstr == "Fire":
        tarray[9] = 1
    elif tstr == "Water":
        tarray[10] = 1
    elif tstr == "Grass":
        tarray[11] = 1
    elif tstr == "Electric":
        tarray[12] = 1
    elif tstr == "Psychic":
        tarray[13] = 1
    elif tstr == "Ice":
        tarray[14] = 1
    elif tstr == "Dragon":
        tarray[15] = 1
    elif tstr == "Dark":
        tarray[16] = 1
    elif tstr == "Fairy":
        tarray[17] = 1

    return tarray

def StandardizeStats(stats):
    total = stats[0]
    hp = stats[1]
    atk = stats[2]
    dfs = stats[3]
    spa = stats[4]
    spd = stats[5]
    spe = stats[6]

    return [format(round(total/780,3),'.3f'),
            format(round(hp/255,3),'.3f'),
            format(round(atk/255,3),'.3f'),
            format(round(dfs/255,3),'.3f'),
            format(round(spa/255,3),'.3f'),
            format(round(spd/255,3),'.3f'),
            format(round(spe/255,3),'.3f')]

f = open("DexRaw","r")

bigdict = {}

for line in f:
    tarray = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    test = line.split()
    #print(test)
    name = test[0]
    darray = []
    if len(test) == 9:
        tstr = test[1]
        stats = [int(test[2]), int(test[3]), int(test[4]), int(test[5]), int(test[6]), int(test[7]), int(test[8])]
        da1 = TurnOnType(tarray, tstr)
        da2 = StandardizeStats(stats)
        darray = da1 + da2
        
    else:
        tstr1 = test[1]
        tstr2 = test[2]
        stats = [int(test[3]), int(test[4]), int(test[5]), int(test[6]), int(test[7]), int(test[8]), int(test[9])]
        da1 = TurnOnType(tarray, tstr1)
        da1 = TurnOnType(da1, tstr2)
        da2 = StandardizeStats(stats)
        darray = da1 + da2

    bigdict[name] = darray

goodpoke = []
badpoke = []

f1 = open("GoodPoke","r")

for line in f1:
    test = line.split()
    #print(test[0])
    parray = bigdict[test[0]]
    #print(parray)
    parray.append(1)
    goodpoke.append(parray)

f2 = open("BadPoke","r")

for line in f2:
    test = line.split()
    #print(test[0])
    parray = bigdict[test[0]]
    #print(parray)
    parray.append(0)
    badpoke.append(parray)

f3 = open("TrainPoke","w")
f4 = open("TestPoke","w")

shuffle(goodpoke)
shuffle(badpoke)

goodtrain = goodpoke[:130]
badtrain = badpoke[:130]

goodtest = goodpoke[130:]
badtest = badpoke[130:]

print(len(goodtrain))
print(len(badtrain))
print(len(goodtest))
print(len(badtest))

trainspec = "260 25 1"
testspec = "226 25 1"

trainlist = goodtrain + badtrain
shuffle(trainlist)

testlist = goodtest + badtest
shuffle(testlist)

f3.write(trainspec)
f3.write("\n")
f4.write(testspec)
f4.write("\n")

for stuff in trainlist:
    test = " ".join(str(i) for i in stuff)
    f3.write(test)
    f3.write("\n")

for stuff in testlist:
    test = " ".join(str(i) for i in stuff)
    f4.write(test)
    f4.write("\n")
