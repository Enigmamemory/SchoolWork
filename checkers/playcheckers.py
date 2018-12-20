from node import Node
import checkers as ck
import alphabeta as ab
import random
import datetime
from datetime import timedelta

AI1 = False
AI2 = False
Custboard = False

p1 = input("Should Player 1 be AI controlled? Type 'y' for yes, or 'n' for no: ")
if p1 == 'y':
    AI1 = True

p2 = input("Should Player 2 be AI controlled? Type 'y' for yes, or 'n' for no: ")
if p2 == 'y':
    AI2 = True

ctime= int(input("How many seconds would you like the AI to take? Please enter a positive integer: "))
    
wboard = input("Would you like to load a custom board? This may overwrite the time parameter. Type 'y' for yes, or 'n' for no: ")

testdata = ck.boardSetup(ctime)

if wboard == 'y':
    cboard = input("Please enter the name of the file here: ")
    testdata = ck.boardSetup(ctime,cboard)

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

    #print(player)
    
    if player % 2 == 1:
        #print("It is indeed player 1's turn")
        #print(AI1)
        if AI1 == True:

            #Will not program iterative deepening atm, first check alpha beta
            movelist = []
            itercount = 1

            curtime = datetime.datetime.now()
            #print(curtime)

            endgame = ck.checkEndgame(testpieces[0], testpieces[1], testpieces[2], testpieces[3])
            if endgame:
                print("endgame established")
            
            while True:
                '''
                if itercount > 3:
                    print("Breaking early for bugfixing")
                    break
                '''
                
                #Create root node, fill with info
                rootnode = Node()
                ab.fillNode(rootnode, alldata)

                #print("Starting search number: ")
                #print(itercount)
                checkup = ab.AIsearch(rootnode, itercount, player, curtime, endgame)
                
                if checkup == None:
                    print("Deepest Iteration: " + str(itercount - 1))
                    break
                else:
                    movelist = checkup
                    #print("finished an iteration: ")
                    #print(itercount)
                    #print(ck.translateJumps(movelist))
                itercount += 1

            #print(len(movelist))
            if len(movelist) != 1:
                rng = random.randint(0, len(movelist) - 1)
                bestmove = movelist[rng]
            else:
                bestmove = movelist[0]

            print(ck.translateJumps([bestmove]))
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

        else:
            changes = ck.chooseMove(testboard, turnjumps, turnenemy, turnmoves, player)
            testboard = changes[0]
            player = changes[1]
            testdata = [testboard, player, time]


    else:
        if AI2 == True:

            movelist = []
            itercount = 1

            curtime = datetime.datetime.now()
            #print(curtime)

            endgame = ck.checkEndgame(testpieces[0], testpieces[1], testpieces[2], testpieces[3])
            if endgame:
                print("Endgame established")
            
            while True:
                '''
                if itercount > 3:
                    print("Breaking early for bugfixing")
                    break
                '''
                
                #Create root node, fill with info
                rootnode = Node()
                ab.fillNode(rootnode, alldata)

                #print("Starting search number: ")
                #print(itercount)
                checkup = ab.AIsearch(rootnode, itercount, player, curtime, endgame)
                
                if checkup == None:
                    print("Deepest Iteration: " + str(itercount - 1))
                    break
                else:
                    movelist = checkup
                    #print("finished an iteration: ")
                    #print(itercount)
                    #print(ck.translateJumps(movelist))
                itercount += 1

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
            
        else:
            changes = ck.chooseMove(testboard, turnjumps, turnenemy, turnmoves, player)
            testboard = changes[0]
            player = changes[1]
            testdata = [testboard, player, time]

    
