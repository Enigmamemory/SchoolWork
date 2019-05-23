from node import Node
import math

#first going to create structure for running neural net
#going from input to output

def ParseFile(fname):
    info = []
    with open(fname) as f:
        for line in f:
            row = line.split()
            frow = [float(i) for i in row]
            #print(frow)
            info.append(frow)

    return info

def CreateSet(info): 

    inputs = []
    outputs = []

    size = int(info[0][0])
    inum = int(info[0][1])
    onum = int(info[0][2])

    snum = 1

    
    #print("CreateSet info")
    #print(inum)
    #print(len(info))
    #print(len(info[1]))
    #print(size)
    
    while snum < size+1:

        ilist = info[snum][:inum]
        olist = info[snum][inum:]

        inputs.append(ilist)
        outputs.append(olist)
        
        snum += 1

    #print(outputs)
        
    return [inputs, outputs]

def CreateNodes(info):

    innode = []
    hidden = []
    outnode = []
    
    num = 0
    
    while num < int(info[0][0]):
        stuff = Node()
        innode.append(stuff)
        num += 1
        
    num = 0
        
    while num < int(info[0][1]):
        stuff = Node()
        stuff.inWeights(info[1 + num])
        
        hidden.append(stuff)
        num += 1
    
    num = 0

    while num < int(info[0][2]):
        stuff = Node()
        stuff.inWeights(info[1 + int(info[0][1]) + num])
        
        outnode.append(stuff)
        num += 1

    '''
    print("Create Nodes Info")
    print(len(innode))
    print(len(hidden))
    print(len(outnode))
    print(info[0])
    '''

    return [innode, hidden, outnode]

def FillInputs(inputs, innode):
    inum = 0

    while inum < len(inputs):
        innode[inum].inActive(inputs[inum])

        inum += 1

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def Activation1(innode, onode):
    num = 0
    v = 0
    oweight = onode.retWeights()
    while num < len(innode):
        iactive = innode[num].retActive()
        #print("Checking innode[num]'s active parameter in Activation1()")
        #print(iactive)
        ow = oweight[num+1]
        v += iactive * ow
        num += 1
    v += -1 * oweight[0]
    onode.inPact(v)
    act = sigmoid(v)
    onode.inActive(act)

    return act

def Rounding(results):
    num = 0
    while num < len(results):
        if results[num] >= 0.5:
            results[num] = 1
        else:
            results[num] = 0
        num += 1

    return results

def RunOnce(innode, hidden, outnode):

    #print("starting run once")
    
    checkout = []

    hnum = 0

    while hnum < len(hidden):
        hnode = hidden[hnum]

        test = Activation1(innode, hnode)
        
        hnum += 1
        
    onum = 0

    while onum < len(outnode):
        onode = outnode[onum]

        test = Activation1(hidden, onode)

        checkout.append(test)

        onum += 1

    return checkout
    
def BackProp(innode, hidden, outnode, learn, expected):

    #list for storing the jdeltas for output node and idelta for hidden nodes
    jdelta = []
    idelta = []
    
    onum = 0

    #acquiring delta j for use to find delta i
    while onum < len(outnode):
        
        oact = outnode[onum].retActive()
        #print("output node's activation in j delta")
        #print(oact)
        j = (oact * (1 - oact)) * (expected[onum] - oact)
        jdelta.append(j)
            
        onum += 1

    hnum = 0

    #print("Checking jdelta:")
    #print(jdelta)
    
    #acquiring delta i
    while hnum < len(hidden):
        jnum = 0
        wsum = 0

        while jnum < len(jdelta):
            oweights = outnode[jnum].retWeights()
            w = oweights[hnum + 1]
            wsum += jdelta[jnum] * w

            #print("In delta i for loop")
            #print(w)
            #print(jdelta[jnum])
            #print(wsum)

            jnum += 1
            
        hact = hidden[hnum].retActive()
        #print("hidden node's activation in i delta")
        #print(hact)
        i = (hact * (1-hact)) * wsum
        idelta.append(i)

        hnum += 1

    onum = 0

    #print("Checking idelta:")
    #print(idelta)
    
    while onum < len(outnode):

        hnum = 0
        
        oweights = outnode[onum].retWeights()
        j = jdelta[onum]

        while hnum < len(hidden):
            
            w = oweights[hnum + 1]
            #print("checking oweights[hnum + 1] before changes")
            #print(oweights[hnum + 1])
            hact = hidden[hnum].retActive()
            w += learn*hact*j
            oweights[hnum + 1] = w
            #print("checking oweights[hnum + 1] after changes")
            #print(oweights[hnum + 1])
            hnum += 1

        bias = oweights[0]
        #print("checking oweights[0] before changes")
        #print(oweights[0])
        bias += learn * -1 * j
        oweights[0] = bias
        #print("checking oweights[0] after changes")
        #print(oweights[0])

        outnode[onum].inWeights(oweights)

        onum += 1
    
    hnum = 0


    while hnum < len(hidden):

        inum = 0
        
        hweights = hidden[hnum].retWeights()
        i = idelta[hnum]

        while inum < len(innode):

            w = hweights[inum + 1]
            #print("checking hweights[inum + 1] before changes")
            #print(hweights[inum + 1])
            iact = innode[inum].retActive()
            w += learn*iact*i
            hweights[inum + 1] = w
            #print("checking hweights[inum + 1] after changes")
            #print(hweights[inum + 1])
            
            inum += 1

        bias = hweights[0]
        #print("checking hweights[0] before changes")
        #print(hweights[0])
        bias += learn * -1 * i
        hweights[0] = bias
        #print("checking hweights[0] after changes")
        #print(hweights[0])
        
        hidden[hnum].inWeights(hweights)
            
        hnum += 1
    

def RetNet(innode, hidden, outnode, ofile):

    f = open(ofile, "w")
    
    nlen = len(innode)
    hlen = len(hidden)
    olen = len(outnode)

    line1 = str(nlen) + " " + str(hlen) + " " + str(olen)
    f.write(line1)
    f.write("\n")
    
    for hnode in hidden:
        hweights = hnode.retWeights()
        size = len(hweights)
        hnum = 0
        while hnum < size:

            hweights[hnum] = format(round(hweights[hnum],3),'.3f')
            
            hnum += 1
            
        wlist = " ".join(str(i) for i in hweights)
        f.write(wlist)
        f.write("\n")

    for onode in outnode:
        oweights = onode.retWeights()
        size = len(oweights)
        onum = 0
        while onum < size:

            oweights[onum] = format(round(oweights[onum],3),'.3f')
            
            onum += 1
        
        wlist = " ".join(str(i) for i in oweights)
        f.write(wlist)
        f.write("\n")

def RetResults(data, ofile):

    f = open(ofile, "w")

    for line in data:
        lsize = len(line)
        if lsize == 8:
            lnum = 4
        else:
            lnum = 0
        while lnum < lsize:

            line[lnum] = format(round(line[lnum],3),'.3f')
            
            lnum += 1
        
        wlist = " ".join(str(i) for i in line)
        f.write(wlist)
        f.write('\n')
    
def PrepResults(expected):

    size = len(expected)

    num = 0

    output = []
    
    while num < size:
        base = [0, 0, 0, 0, 0, 0, 0, 0]
        output.append(base)
        num += 1

    return output

def CalculateParts(data):
    asum = 0
    bsum = 0
    csum = 0
    dsum = 0
    acsum = 0
    prsum = 0
    resum = 0
    f1sum = 0

    num = len(data)
    
    for line in data:
        line[4] = (line[0] + line[3]) / (line[0] + line[1] + line[2] + line[3])
        line[5] = line[0] / (line[0] + line[1])
        line[6] = line[0] / (line[0] + line[2])
        line[7] = (line[5] * line[6] * 2) / (line[5] + line[6])

        asum += line[0]
        bsum += line[1]
        csum += line[2]
        dsum += line[3]
        acsum += line[4]
        prsum += line[5]
        resum += line[6]
        f1sum += line[7]

    micro = [((asum + dsum) / (asum + bsum + csum + dsum)), (asum / (asum + bsum)), (asum / (asum + csum)), ((2 * (asum / (asum + bsum)) * (asum / (asum + csum))) / ((asum / (asum + bsum)) + (asum / (asum + csum))))]

    macro = [(acsum / num), (prsum / num), (resum / num), ((2 * (prsum / num) * (resum / num)) / ((prsum/num) + (resum / num)))]

    data.append(micro)
    data.append(macro)

    return data

def TrainNet(nfile, tfile, ofile, epoch, learn):
    ninfo = ParseFile(nfile)
    tinfo = ParseFile(tfile)

    sinfo = CreateSet(tinfo)
    nodes = CreateNodes(ninfo)

    inputs = sinfo[0]
    outputs = sinfo[1]

    innode = nodes[0]
    hidden = nodes[1]
    outnode = nodes[2]

    enum = 0

    while enum < epoch:
        
        snum = 0
        
        while snum < len(inputs):
            FillInputs(inputs[snum], innode)
            
            checkout = RunOnce(innode, hidden, outnode)

            expected = outputs[snum]

            BackProp(innode, hidden, outnode, learn, expected)

            snum += 1
        
        enum += 1

    RetNet(innode, hidden, outnode, ofile)

def TestNet(nfile, tfile, ofile):
    ninfo = ParseFile(nfile)
    tinfo = ParseFile(tfile)

    sinfo = CreateSet(tinfo)
    nodes = CreateNodes(ninfo)

    inputs = sinfo[0]
    outputs = sinfo[1]

    innode = nodes[0]
    hidden = nodes[1]
    outnode = nodes[2]

    data = PrepResults(outputs[0])

    #print(data)
    
    snum = 0
    
    while snum < len(inputs):
        FillInputs(inputs[snum], innode)
            
        checkout = RunOnce(innode, hidden, outnode)

        rounded = Rounding(checkout)
        expected = outputs[snum]

        #print("What's length of expected outputs?")
        #print(len(outputs))
        #print("what's lenght of recieved outputs?")
        #print(len(rounded))
        
        #print("output vs expected")

        #print(rounded)
        #print(expected)
        
        cnum = 0

        #print("outside cnum for loop")
        
        while cnum < len(rounded):
            
            param = data[cnum]
            #print("data and param before setting anything")
            #print(data)
            #print(param)

            #print("rounded[cnum] and expected[cnum] before setting anything")
            #print(rounded[cnum])
            #print(expected[cnum])

            if rounded[cnum] == 1 and expected[cnum] == 1:
                param[0] += 1

            elif rounded[cnum] == 1 and expected[cnum] == 0:
                param[1] += 1

            elif rounded[cnum] == 0 and expected[cnum] == 1:
                param[2] += 1

            else:
                param[3] += 1

            data[cnum] = param

            #print("After setting params and putting them into data")
            #print(data)
            
            cnum += 1
        
        snum += 1

    newdata = CalculateParts(data)

    RetResults(newdata, ofile)


mode = input("Would you like to test or train? Press 1 for test, and 2 for train: ")

if mode == "1":
    print("Set to test mode")
elif mode == "2":
    print("Set to train mode")
else:
    print("Unsure what was typed, defaulting to test mode")
    mode = "1"

nfile = input("Please enter your neural net file name here: ")
tfile = input("Please enter your set data here: ")
ofile = input("Please enter the name of your output file here: ")
    
if mode == "1":
    TestNet(nfile, tfile, ofile)
else:
    lstr = input("Please enter a learning rate (float): ")
    learn = float(lstr)
    estr = input("Please enter the epoch size (int): ")
    epoch = int(estr)
    TrainNet(nfile, tfile, ofile, epoch, learn)

print("Finished operations, closing program. Please check your output file: " + ofile)

#info = ParseFile("sample.NNWDBC.init")

#print(info[0])




