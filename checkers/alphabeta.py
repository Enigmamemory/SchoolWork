from node import Node
import checkers as ck
import random
import datetime
from datetime import timedelta

def fillNode(newnode, alldata): #given a new node and the data gathered
    newnode.setBoard(alldata[0])
    newnode.setPlayer(alldata[1])
    newnode.setTime(alldata[2])
    newnode.setPieces1(alldata[3][0])
    newnode.setPieces2(alldata[3][1])
    newnode.setPieces3(alldata[3][2])
    newnode.setPieces4(alldata[3][3])
    newnode.setTurnJumps(alldata[4][0])
    newnode.setTurnEnemy(alldata[4][1])
    newnode.setTurnMoves(alldata[4][2])

def centerValue(pieces1, pieces2, pieces3, pieces4):
    v = 0
    n1 = 0
    n2 = 0
    for p1 in pieces1:
        c1 = ck.findCoord(p1)
        if (c1[0] >= 2 and c1[0] <= 3) and (c1[1] >= 2 and c1[1] <= 5):
            if n1 > 2:
                v -= 30
            else:
                v += 30
    for p2 in pieces2:
        c2 = ck.findCoord(p2)
        if (c2[0] >= 4 and c2[0] <= 5) and (c2[1] >= 2 and c2[1] <= 5):
            n2 += 1
            if n2 > 2:
                v += 30
            else:
                v -= 30
    for p3 in pieces3:
        c3 = ck.findCoord(p3)
        if (c3[0] >= 2 and c3[0] <= 5) and (c3[1] >= 2 and c3[1] <= 5):
            n1 += 1
            if n1 > 2:
                v -= 30
            else:
                v += 30
    for p4 in pieces4:
        c4 = ck.findCoord(p4)
        if (c4[0] >= 2 and c4[0] <= 5) and (c4[1] >= 2 and c4[1] <= 5):
            n2 += 1
            if n2 > 2:
                v += 30
            else:
                v -= 30
    return v
                                            
def endgameValue(pieces1, pieces2, pieces3, pieces4, AIturn):

    '''
    coords1 = ck.translateJumps(pieces1)
    coords2 = ck.translateJumps(pieces2)
    coords3 = ck.translateJumps(pieces3)
    coords4 = ck.translateJumps(pieces4)
    '''

    v = 0
    
    if AIturn % 2 == 0: #if AI is player 2

        tpieces = pieces1 + pieces3
        
        for p1 in tpieces:
            final = 0
            c1 = ck.findCoord(p1)
            found1 = 0
            for p2 in pieces2:
                c2 = ck.findCoord(p2)
                if ((c2[1] == c1[1] or abs(c2[1] - c1[1]) == 2) and c2[0] - c1[0] == 2):
                    found1 += 1
                    if found1 > 1:
                        final = 0
                        break
                else:
                    if (c2[1] == c1[1]) and c2[0] - c1[0] > 0:
                        final -= 10 * (c2[0] - c1[0])
                    elif c2[0] - c1[0] > 0:
                        final -= 5 * (c2[0] - c1[0]) + 5 * abs(c2[1] - c1[1])
            if found1 != True:
                for p4 in pieces4:
                    c4 = ck.findCoord(p4)
                    if ((c4[1] == c1[1] or abs(c4[1] - c1[1]) == 2) and abs(c4[0] - c1[0]) == 2):
                        found1 += 1
                        if found1 > 1:
                            final = 0
                            break
                    else:
                        if (c4[1] == c1[1]) > 0:
                            final -= 10 * abs(c4[0] - c1[0])
                        else:
                            final -= 5 * abs(c4[0] - c1[0]) + 5 * abs(c4[1] - c1[1])

            v += final

        if len(pieces1) + len(pieces3)*2 > len(pieces2) + len(pieces4)*2:
            v = v * -1

    else:

        tpieces = pieces2 + pieces4
        
        for p2 in tpieces:
            final = 0
            c2 = ck.findCoord(p2)
            found2 = 0
            for p1 in pieces1:
                c1 = ck.findCoord(p1)
                if ((c2[1] == c1[1] or abs(c2[1] - c1[1]) == 2) and c2[0] - c1[0] == 2):
                    v += 40
                    found2 += 1
                    if found2 > 1:
                        final = 0
                        break
                else:
                    if (c2[1] == c1[1]) and c2[0] - c1[0] > 0:
                        final -= 20 * (c2[0] - c1[0])
                    elif c2[0] - c1[0] > 0:
                        final -= 10 * (c2[0] - c1[0]) + 10 * abs(c2[1] - c1[1])
            if found2 != True:
                for p3 in pieces3:
                    c3 = ck.findCoord(p3)
                    if ((c3[1] == c2[1] or abs(c3[1] - c2[1]) == 2) and abs(c3[0] - c2[0]) == 2):
                        v += 40
                        found2 += 1
                        if found2 > 1:
                            final = 0
                            break

                    else:
                        if (c3[1] == c2[1]):
                            final -= 20 * abs(c3[0] - c2[0])
                        else:
                            final -= 10 * abs(c3[0] - c2[0]) + 10 * abs(c3[1] - c2[1])

            v += final
            
        if len(pieces1) + len(pieces3)*2 < len(pieces2) + len(pieces4)*2:
            v = v * -1

    return v


def AIsearch(innode, itermax, AIturn, curtime, endgame, itercur = 0): #practically, itermax starts at 2

    '''
    if curtime == None:
        curtime = datetime.datetime.now()
    '''

    thistime = datetime.datetime.now()

    diff = thistime - curtime
        
    tmax = timedelta(seconds = innode.returnTime())

    if diff > tmax:
        print("beginning time: ")
        print(curtime)
        print("current time: ")
        print(thistime)
        print("time limit: ")
        print(tmax)
        print("time difference: ")
        print(diff)
        return None
    
    bestmove = []
    turnmoves = innode.returnTurnJumps()
    turnenemy = []
    isJump = False

    #print("checking jumps at start")
    #print(turnmoves)
    #print("checking moves at start")
    #print(innode.returnTurnMoves())
    
    if len(turnmoves) != 0:
        isJump = True
        turnenemy = innode.returnTurnEnemy()
    else:
        turnmoves = innode.returnTurnMoves()

    #print("checking jumps after if/else statement")
    #print(turnmoves)

    if len(turnmoves) == 0: #it is possible that the game reaches a winning state before a terminal node. This is shown by the turn player having no moves left. Signify that it's a winning/losing state with a very large number

        #also need to adjust for AI as Player 1 or 2 eventually

        #actually assuming perspective of program, this line should be fine
        
        if itercur % 2 == 1:
            #print("sensed winning position")
            return [100000 - itercur, None, None]
        else:
            #print("sensed losing position")
            return [-100000 + itercur, None, None]
        #ck.printGUI(innode.returnBoard())
        


    #Before changing the board any further, check if it's a terminal node:

    #print('itercur at the start of function')
    #print(itercur)
    
    if itercur == itermax:
        #need heuristic evlauation to get v
        #return as [v, None, None]

        #New heuristics: 
        
        player = innode.returnPlayer()
        #board = innode.returnBoard()
        #ck.printGUI(board)
        
        p1 = innode.returnPieces1()
        p2 = innode.returnPieces2()
        p3 = innode.returnPieces3()
        p4 = innode.returnPieces4()
        
        if AIturn % 2 == 0: #if AI is player 2
            
            v = 0
            v += len(p2) * 100
            v += len(p4) * 200
            v += len(p1) * -100
            v += len(p3) * -200

            if endgame == False:
                v += -1 * centerValue(p1,p2,p3,p4)

        else: #if AI is player 1

            v = 0
            v += len(p2) * -100
            v += len(p4) * -200
            v += len(p1) * 100
            v += len(p3) * 200

            if endgame == False:
                v += centerValue(p1,p2,p3,p4)
            
        if endgame:
            v += endgameValue(p1,p2,p3,p4,AIturn)
        
        #print(v)
        return [v, None, None]

    #Otherwise, proceed
    
    #itercur += 1

    #if it's not, then need to explore all branches eventually with while loop

    pos = 0

    #need to randomize which moves are examined first BEFORE anything happens. Otherwise - WILL HAVE BUGS :(

    #will randomize by randomizing an array with len = len(turnmoves). Then, append elements from turnmoves into a new randmoves list

    randsel = list(range(len(turnmoves)))
    random.shuffle(randsel)

    randmoves = []
    randenemy = []
    
    for num in randsel:
        
        randmoves.append(turnmoves[num])
        if isJump == True:
            randenemy.append(turnenemy[num])
        
    
    
    while pos < len(turnmoves): #need to use numerical position to find correct move and enemy, if necessary
        
        #Performing the move in question on phantom board copy
        curboard = innode.returnBoard().copy()
        curmoves = []
        curenemy = []
        
        if isJump == True:
            curmoves = randmoves[pos]
            curenemy = randenemy[pos]
            curboard = ck.changeBoard(curboard,curmoves,curenemy)
        else:
            curmoves = randmoves[pos]
            curboard = ck.changeBoard(curboard,curmoves)

        #Get new info of the phantom board

        indata = [curboard, innode.returnPlayer() + 1, innode.returnTime()]
        alldata = ck.gatherInfo(indata)

        #print("start of while loop, itercur check")
        #print(itercur)
        #print("what move checking?")
        #print(ck.translateJumps([curmoves]))

        #If not, search deeper by calling another AI search function
        #After that, wait for a response from child node and do alpha beta eval

        newnode = Node()

        #need to fill in the info into newnode
        fillNode(newnode, alldata)

        #remember to store innode as newnode's prevNode
        newnode.setPrevNode(innode)

        #REMEMBER TO STORE THE ALPHA BETA VALUES OF INNODE INTO NEWNODE

        #may need to copy node values, probably not though
        pv = innode.returnValue()
        palpha = innode.returnAlpha()
        pbeta = innode.returnBeta()

        newnode.setBeta(pbeta)
        newnode.setAlpha(palpha)


        #call AISearch on the "child node" and wait for its response
        #print("before recurse call, itercur check")
        #print(itercur)
        results = AIsearch(newnode, itermax, AIturn, curtime, endgame, itercur + 1)
        #print("recurse left a layer, checking itercur")
        #print(itercur)

        #print("checking results")
        #print(results)
        #Perform alpha beta evaluation by comparing innode values to results values

        if results == None:
            return None
        
        c = results[0] #comparing this value to innode's value, alpha, beta
        #print("checking c, pv after c is set to results[0]")
        #print(c)
        #print(pv)

        #Note that if v is updated, that means that node found a new best value. What this means is that if v is changed while innode's prevnode is None, aka innode represents the root node which will not set a prevnode, then the move responsible for changing the value of v need to be noted.
        
        if itercur % 2 == 0: #all instances here should be max nodes
            #print("entering max node check")
            #print(c)
            #print(pv)
            #print(palpha)
            #print(pbeta)
            vrep = False

            if pv == None:
                #print("should've set value")
                innode.setValue(c)
                vrep = True
            elif c > pv:
                innode.setValue(c)
                vrep = True

            if innode.returnPrevNode() == None:
                if vrep == True: #if new highest value found, need to keep track of a new list of best moves
                    bestmove = [curmoves]
                #elif c == pv: #here only add moves with same highest value to existing list, will randomize collection at end after return
                    #bestmove.append(curmoves)


            if pbeta != None:
                if c >= pbeta:
                    #print("pruning branches from max node")
                    break

            if palpha == None:
                innode.setAlpha(c)
            elif c > palpha:
                innode.setAlpha(c)


        else: #therefore all instances here should be min nodes
            #print("entering min node check")
            #print(c)
            #print(pv)
            #print(palpha)
            #print(pbeta)
            if pv == None:
                #print("should've set value")
                innode.setValue(c)
            elif c < pv:
                innode.setValue(c)

            if palpha != None:
                if c <= palpha:
                    #print("pruning branches from min node")
                    break

            if pbeta == None:
                innode.setBeta(c)
            elif c < pbeta:
                innode.setBeta(c)
                

            #Here, might decide to prune, therefore do not check other moves in loop. This means break out of this loop

        pos += 1 #needed to advance loop to next move

    #Once exit loop, needs to check if current AISearch func uses the root innode or one of the child innodes. The root innode, upon exiting loop, has a bestmove result. The child innodes only care about passing the [v, alpha, beta] values to their parent nodes.
        
    if innode.returnPrevNode() == None:
        #print("should be returning a best move")
        #print(bestmove)
        return bestmove
    else:
        return [innode.returnValue(), innode.returnAlpha(), innode.returnBeta()]

'''
#Test Code#

testdata = ck.boardSetup()

testboard = testdata[0]
player = testdata[1]
time = testdata[2]

while True:

    alldata = ck.gatherInfo(testdata)

    testboard = alldata[0]
    player = alldata[1]
    time = alldata[2]
    testpieces = alldata[3]
    testchange = alldata[4]

    if player % 2 == 1:
        print("It is Player 1's turn")
    else:
        print("It is Player 2's turn")

    ck.printGUI(testboard)

    turnjumps = testchange[0]
    turnenemy = testchange[1]
    turnmoves = testchange[2]

    if ck.gameOver(turnjumps, turnmoves, player):
        break

    if player % 2 == 1: #hard code p1 to be human atm
    
        changes = ck.chooseMove(testboard, turnjumps, turnenemy, turnmoves, player)
        testboard = changes[0]
        player = changes[1]
        testdata = [testboard, player, time]

    else:

        #Create root node, fill with info
        rootnode = Node()
        fillNode(rootnode, alldata)

        #Will not program iterative deepening atm, first check alpha beta
        movelist = AIsearch(rootnode, 6, player)

        if len(movelist) != 1:
            rng = random.randint(0, len(movelist) - 1)
            bestmove = movelist[rng]
        else:
            bestmove = movelist[0]

        #print(bestmove)
        #print(turnjumps)
        #print(turnmoves)
        bestenemy = None
            
        if len(turnjumps) != 0:
            bestenemy = turnenemy[turnjumps.index(bestmove)]

 
        #print(bestenemy)
        changes = ck.thisMove(testboard,bestmove,player,bestenemy)
        
        testboard = changes[0]
        player = changes[1]
        testdata = [testboard, player, time]

'''
