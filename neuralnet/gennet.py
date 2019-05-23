import random

def GenNet(inputs, hidden, outputs):
    hnum = 0
    data = [[inputs, hidden, outputs]]
    while hnum < hidden:
        hweights = []
        inum = 0
        while inum < inputs + 1:
        
            value = format(round(random.random(),3),'.3f')
            hweights.append(value)

            inum += 1

        data.append(hweights)
        hnum += 1

    onum = 0
    while onum < outputs:
        hnum = 0
        oweights = []
        while hnum < hidden + 1:

            value = format(round(random.random(),3),'.3f')
            oweights.append(value)

            hnum += 1

        data.append(oweights)
        onum += 1

    return data

def RetNet(data, ofile):

    f = open(ofile, "w")
    
    nlen = data[0][0]
    hlen = data[0][1]
    olen = data[0][2]

    line1 = str(nlen) + " " + str(hlen) + " " + str(olen)
    f.write(line1)
    f.write("\n")

    hnum = 0

    while hnum < hlen:
        hweights = data[hnum + 1]
        line = " ".join(str(i) for i in hweights)
        f.write(line)
        f.write("\n")

        hnum += 1

    onum = 0

    while onum < olen:
        oweights = data[onum + hlen + 1]
        line = " ".join(str(i) for i in oweights)
        f.write(line)
        f.write("\n")

        onum += 1
   
data = GenNet(25, 10, 1)
RetNet(data, "pokeinit")
