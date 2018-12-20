class Node:
    def __init__(self, prevnode = None, prevmove = None):
        self.board = [0] * 64
        self.player = 0
        self.time = 0
        self.pieces1 = [] #need to make func for pieces1, pieces2, pieces3, pieces4
        self.pieces2 = [] 
        self.pieces3 = []
        self.pieces4 = []
        self.turnjumps = []
        self.turnmoves = []
        self.turnenemy = []
        self.prevnode = prevnode
        self.prevmove = prevmove
        self.istype = 0
        self.alpha = None
        self.beta = None
        self.value = None

    def returnBoard(self):
        return self.board

    def returnPlayer(self):
        return self.player

    def returnTime(self):
        return self.time

    def returnPieces1(self):
        return self.pieces1

    def returnPieces2(self):
        return self.pieces2

    def returnPieces3(self):
        return self.pieces3

    def returnPieces4(self):
        return self.pieces4
    
    def returnTurnJumps(self):
        return self.turnjumps

    def returnTurnMoves(self):
        return self.turnmoves

    def returnTurnEnemy(self):
        return self.turnenemy

    def returnPrevNode(self):
        return self.prevnode

    def returnPrevMove(self):
        return self.prevmove

    def returnIsType(self):
        return self.istype

    def returnAlpha(self):
        return self.alpha

    def returnBeta(self):
        return self.beta

    def returnValue(self):
        return self.value

    def setBoard(self,board):
        self.board = board

    def setPlayer(self, player):
        self.player = player

    def setTime(self,time):
        self.time = time

    def setPieces1(self,pieces1):
        self.pieces1 = pieces1

    def setPieces2(self,pieces2):
        self.pieces2 = pieces2

    def setPieces3(self,pieces3):
        self.pieces3 = pieces3

    def setPieces4(self,pieces4):
        self.pieces4 = pieces4
        
    def setTurnJumps(self,turnjumps):
        self.turnjumps = turnjumps

    def setTurnMoves(self, turnmoves):
        self.turnmoves = turnmoves

    def setTurnEnemy(self, turnenemy):
        self.turnenemy = turnenemy

    def setPrevNode(self, prevnode):
        self.prevnode = prevnode

    def setPrevMove(self, prevmove):
        self.prevmove = prevmove

    def setIsType(self,istype):
        self.istype = istype

    def setAlpha(self,alpha):
        self.alpha = alpha

    def setBeta(self,beta):
        self.beta = beta

    def setValue(self,value):
        self.value = value

    def createChild(self, prevmove = None):
        copy = Node()
        copy.board = self.board
        copy.player = self.player
        copy.time = self.time
        copy.pieces1 = self.pieces1
        copy.pieces2 = self.pieces2
        copy.pieces3 = self.pieces3
        copy.pieces4 = self.pieces4
        copy.prevnode = self
        copy.prevmove = prevmove

        return copy
