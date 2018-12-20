def boardSetup(ctime, x = None): 
    board = [0]*64
    player = 0
    time = ctime
    
    if x != None:
        inboard = open(x,"r")
        lcount = 0
        bcount = 0
        for line in inboard:
            #parselist = []
            count = 0
            #print(line)
            if lcount > 7 or bcount > 63:
                if lcount == 8:
                    player = int(line)
                elif lcount == 9:
                    time = int(line)
                else:
                    break
            else:
    
                for letter in line:
                    if count % 2 == 0:
                        #parselist.append(letter)
                        if letter == ' ':
                            board[bcount] = 0
                        else:
                            board[bcount] = int(letter)
                        bcount += 1
                    count += 1
                if count != 16:
                    board[bcount] = 0
                    bcount += 1
                #parselist.append(' ')
                #print(bcount)

            #print(lcount)
            lcount += 1

    else: #Sets up board for beginning game state
        player = 1
        lcount = 0
        while lcount < 8:
            wcount = 0
            while wcount < 8:
                if (lcount*8 + wcount) % 2 == (lcount + 1) % 2:
                    if lcount < 3:
                        board[lcount*8 + wcount] = 1
                    elif lcount > 4:
                        board[lcount*8 + wcount] = 2
                wcount += 1
            lcount += 1

    return [board, player, time]

def printBoard(board):
    lcount = 0

    while lcount < 8:
        wcount = 0
        row = []
        while wcount < 8:
            row.append(board[lcount*8 + wcount])
            wcount += 1
        print(row)
        lcount += 1

def printGUI(board):
    print("   0   1   2   3   4   5   6   7 ")
    rows = 0
    while rows < 8:

        print(" ---------------------------------")
        print(" |   |   |   |   |   |   |   |   |")
        onerow = str(rows) + "|"
        cnum = 0
        while cnum < 8:

            sq = "   "
            if board[rows*8 + cnum] != 0:
                if board[rows*8 + cnum] == 1:
                    sq = "\x1b[0;32;40m"+" v "+"\x1b[0m"
                elif board[rows*8 + cnum] == 2:
                    sq = "\x1b[1;31;40m"+" ^ "+"\x1b[0m"
                elif board[rows*8 + cnum] == 3:
                    sq = "\x1b[0;32;40m"+" W "+"\x1b[0m"
                elif board[rows*8 + cnum] == 4:
                    sq = "\x1b[1;31;40m"+" M "+"\x1b[0m"
            onerow += sq + "|"
            cnum += 1

        print(onerow)
        rows += 1
        print(" |   |   |   |   |   |   |   |   |")
    print(" ---------------------------------")

def findPieces(board):
    pieces1 = []
    pieces2 = []
    pieces3 = []
    pieces4 = []
    count = 0
    for square in board:
        if square == 1:
            pieces1.append(count)
        elif square == 2:
            pieces2.append(count)
        elif square == 3:
            pieces3.append(count)
        elif square == 4:
            pieces4.append(count)
        count += 1

    return [pieces1,pieces2,pieces3,pieces4]

def combinePieces(piecelist):
    joinlist = []
    for pieces in piecelist:
        joinlist += pieces
    return joinlist

def isEnemy(myp,thatp):
    return myp % 2 != thatp % 2

def findCoord(square):
    return [int(square/8),square % 8]

def translateJumps(jumplist):
    newjumps = []
    for jumps in jumplist:
        translist = []
        for jump in jumps:
            coords = findCoord(jump)
            translist.append(coords)
        newjumps.append(translist)
    return newjumps

def isthereJump(jumplist):
    return len(jumplist) > 1

def isthereEnemy(enemylist):
    return len(enemylist) > 0

def gatherJumps(jumprec, posjumps, enemy = False):
    for jumplist in jumprec:
        if isthereJump(jumplist) or (enemy == True and isthereEnemy(jumplist)):
            posjumps.append(jumplist)

    return posjumps

def printJumps(posjumps):
    counter = 0
    for jumplist in posjumps:
        print(str(counter) + ":")
        print(jumplist)
        counter += 1

def gatherSimple(simpledata):
    origsq = simpledata[0]
    posmoves = []
    simplecheck = simpledata[2]
    for sqcheck in simplecheck:
        if sqcheck >= 0:
            posmoves.append([origsq, sqcheck])
    return posmoves
        
def simpleMove(board,square, ptype = None): #looks for simple move for one piece
    origintdiv = int(square/8)
    enemypiece = []
    posdraft = [square - 7, square - 9, square + 7, square + 9]

    if ptype == None:
        ptype = board[square]
    
    if ptype < 3:
        if ptype % 2 == 1:
            posdraft[0] = -1
            posdraft[1] = -1
        else:
            posdraft[2] = -1
            posdraft[3] = -1

    for pnum in range(len(posdraft)):

        pos = posdraft[pnum]
        #print(pos)
        #print("before if statement")
        if pos > 63 or pos < 0:
            posdraft[pnum] = -1
            #print("statement 1")
        elif abs(origintdiv - int(pos/8)) != 1:
            posdraft[pnum] = -1
            #print("statement 2")
        elif board[pos] != 0:
            if isEnemy(ptype, board[pos]):
                enemypiece.append(pos)
            posdraft[pnum] = -1
            #print("statement 3")
        #print(posdraft[pnum])
                
    return [square,ptype,posdraft,enemypiece]

def findJumps(board, simpledata, jumplist, takelist, jumprec, takerec):
    #board is the board state
    #simpledata is the return statement from simpleMove
    #jumplist should start with the original square at first call, will add jumps
    #takelist should be empty at first call, will add pieces taken
    #jumprec should be an empty record list, keeps track of complete pos jumps
    #takerec should be an empty record list, keeps track of pieces taken with jumps
    origsq = simpledata[0]
    ptype = simpledata[1] #original piece type, needed for simpleMove call
    movelist = simpledata[2]
    enemylist = simpledata[3]
    isjumps = False
    returnlist = [jumprec, takerec]
    #print("simpledata")
    #print(simpledata)
    
    if len(enemylist) > 0: #if enemy piece near piece at original square
        for enemy in enemylist: #check jump for each piece
            #print("what is enemylist")
            #print(enemylist)
            #print("what is enemy")
            #print(enemy)
            #print("what is jumplist at beginning of for loop")
            #print(jumplist)
            #print("what is takelist at beginning of for loop")
            #print(takelist)
            jumplist2 = jumplist.copy() #want these two lists to reset for every enemy check
            takelist2 = takelist.copy()
            jumpdir = enemy - origsq
            dest = enemy + jumpdir #jumps must go in same direction
            if abs(int(dest/8) - int(enemy/8)) == 1 and dest >= 0 and dest <= 63:
                
                #make sure jump doesn't go off the board
                #print("made it past first check")
                
                if (board[dest] == 0 or (jumplist.count(dest) != 0 and dest != origsq)) and takelist.count(enemy) == 0:
                    #print("made it past second check")
                    #print("what is dest")
                    #print(dest)
                    #print("what is enemy")
                    #print(enemy)
                    
                    #check if location is free
                    #and if the piece we wanted to take wasn't already taken
                    jumplist2.append(dest)
                    takelist2.append(enemy)

                    #print(jumplist2)
                    #print(takelist2)
                    
                    isjumps = True #if there are no jumps, never reach this part

                    #check for a second jump
                    simpledata2 = simpleMove(board, dest, ptype)
                    
                    #run the findJump function again

                    #print("recursing +1")
                    #print("what is jumplist2")
                    #print(jumplist2)
                    #print("what is takelist2")
                    #print(takelist2)
                    returnlist = findJumps(board, simpledata2, jumplist2, takelist2, jumprec, takerec)

    #if you exit the loop without running findJumps
    #or if you don't even make it into the if statement (aka no enemy pieces)
    #that means there are no further jumps
    #should be marked by isjumps still being False
    #if True, loop exited in a function that performed future jumps
    #so do not add the jump order to the record

    #print("Made it out of if statement")
    if isjumps == False:
        #print ("isjump is false")
        #print ("what is jumplist recorded")
        #print (jumplist)
        #print ("what is takelist recorded")
        #print (takelist)
        jumprec.append(jumplist)
        takerec.append(takelist)

    #print(returnlist)
    return returnlist

def translateCoord(coordlist):
    #print(coordlist)
    newjumps = []
    for coords in coordlist:
        jump = coords[0] * 8 + coords[1]
        newjumps.append(jump)
    return newjumps

def changeBoard(board,chosen,enemy = None):
    
    #nchosen = translateCoord(chosen)
    first = chosen[0]
    last = chosen[-1]

    ptype = board[first] #maybe pointer issues again, check to make sure
    board[last] = ptype
    if first != last:
        board[first] = 0
    
    if enemy != None:
        #nenemy = translateCoord(enemy)
        for piece in enemy:
            #print(piece)
            board[piece] = 0

    counter = 0
    while counter < 8:
        if board[counter] == 2:
            board[counter] = 4
        counter += 1

    counter = 56
    while counter < 64:
        if board[counter] == 1:
            board[counter] = 3
        counter += 1
    
    return board

def gameOver(turnjumps,turnmoves, player):
    if len(turnjumps) == 0 and len(turnmoves) == 0:
        if player % 2 == 1:
            print("Player 1 loses - no moves remaining")
        else:
            print("Player 2 loses - no moves remaining")
        return True
    else:
        return False

def chooseMove(testboard, turnjumps, turnenemy, turnmoves, player):

    isJump = True
    
    if len(turnjumps) == 0:
        isJump = False
        transmoves = translateJumps(turnmoves)
        printJumps(transmoves) 

    transjumps = translateJumps(turnjumps)
    printJumps(transjumps)
    #transenemy = translateJumps(turnenemy)
    #printJumps(transenemy)

    movprompt = input("Choose your move by entering the corrosponding integer\n")

    print("")
    print("###################")
    print("")
    
    #print(turnjumps)
    #print(turnenemy)

    try:
        movchoose = int(movprompt)
        if isJump:
            #print (turnjumps[movchoose])
            #print (turnenemy[movchoose])
            testboard = changeBoard(testboard, turnjumps[movchoose], turnenemy[movchoose])
        else:
            testboard = changeBoard(testboard, turnmoves[movchoose])
    except:
        print("Looks like that wasn't valid, defaulting to option 0")
        if isJump:
            #print (turnjumps[movchoose])
            #print (turnenemy[movchoose])
            testboard = changeBoard(testboard, turnjumps[0], turnenemy[0])
        else:
            testboard = changeBoard(testboard, turnmoves[0])

    player += 1
    #print(testjumps)

    #print(board)

    return [testboard,player]

def thisMove(testboard, amove, player, aenemy = None):
    if aenemy == None:
        testboard = changeBoard(testboard, amove)
    else:
        testboard = changeBoard(testboard, amove, aenemy)
    player += 1

    print("")
    print("###################")
    print("")
    return [testboard,player]

def gatherTurns(testboard, testpieces, turnjumps, turnenemy, turnmoves, player):
    for pieces in testpieces:
        if testboard[pieces] % 2 == player % 2:
            #posjumps = []
            testmoves = simpleMove(testboard,pieces)
            testjumps = findJumps(testboard, testmoves, [pieces], [], [], [])
            #print(testmoves)
            #print(testjumps)
            #coordjumps = translateJumps(testjumps[0])
            #coordenemy = translateJumps(testjumps[1])
            #print(coordjumps)
            #print(coordenemy)
            #newposj = gatherJumps(coordjumps,posjumps)
            #turnjumps = gatherJumps(coordjumps,turnjumps)
            #turnenemy = gatherJumps(coordenemy,turnenemy, True)
            #print(testjumps[0])
            
            turnjumps = gatherJumps(testjumps[0],turnjumps)
            turnenemy = gatherJumps(testjumps[1],turnenemy, True)
            #coordjumps = translateJumps(turnjumps)
            if len(turnjumps) == 0:
                testsimple = gatherSimple(testmoves)
                #coordsimple = translateJumps(testsimple)
                #turnmoves += coordsimple
                turnmoves += testsimple


            '''
            if len(newposj) > 0:
                printJumps(newposj)
            else:

                printJumps(coordmoves)
            '''
            #print(coordjumps)
            
    return [turnjumps, turnenemy, turnmoves]

def gatherInfo(testdata):
    testboard = testdata[0]
    player = testdata[1]
    time = testdata[2]

    testpieces2 = findPieces(testboard)
    testpieces = combinePieces(testpieces2)

    testchange = gatherTurns(testboard, testpieces, [], [], [], player)

    return [testboard, player, time, testpieces2, testchange]
    
def checkEndgame(pieces1, pieces2, pieces3, pieces4):
    if (len(pieces1) + len(pieces3) <= 3) or (len(pieces2) + len(pieces4) <= 3):
        return True
    elif (len(pieces1) + len(pieces2) + len(pieces3) + len(pieces4) <= 8):
        return True
    return False

#testdata = boardSetup("sampleCheckers4.txt")
#testdata = boardSetup()

'''
testboard = testdata[0]
player = testdata[1]
time = testdata[2]
'''

#print(player)
#print(time)
#printGUI(testboard)
          
#printBoard(testboard)
#print(testboard)

'''
while True:

    alldata = gatherInfo(testdata)

    testboard = alldata[0]
    player = alldata[1]
    time = alldata[2]
    testpieces = alldata[3]
    testchange = alldata[4]

    if player % 2 == 1:
        print("It is Player 1's turn")
    else:
        print("It is Player 2's turn")

    printGUI(testboard)

    turnjumps = testchange[0]
    turnenemy = testchange[1]
    turnmoves = testchange[2]

    if gameOver(turnjumps, turnmoves, player):
        break
    
    changes = chooseMove(testboard, turnjumps, turnenemy, turnmoves, player)
    testboard = changes[0]
    player = changes[1]
    testdata = [testboard, player, time]
'''
